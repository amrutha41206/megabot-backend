from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from groq import Groq
import os
import shutil
import time
import threading
import gc


class RAGEngine:

    def __init__(self, session_id=None):

        # Lazy loading (saves RAM at startup)
        self.model = None

        self.documents = {}
        self.document_upload_order = []
        self.current_document = None

        self.client = None

        self.relevance_threshold = 0.5

        self.session_id = session_id or "default"
        self.session_folder = f"uploaded_documents/{self.session_id}"

        os.makedirs(self.session_folder, exist_ok=True)

        self.max_documents_per_session = 3

        self.upload_lock = threading.Lock()

    # --------------------------------------------------

    def get_embedding_model(self):
        """
        Load SentenceTransformer only when required.
        Saves hundreds of MB during application startup.
        """

        if self.model is None:
            print("Loading embedding model...")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

        return self.model

    # --------------------------------------------------

    def get_groq_client(self):

        if self.client is None:
            self.client = Groq(
                api_key=os.getenv("GROQ_API_KEY")
            )

        return self.client

    # --------------------------------------------------

    def cleanup_old_documents(self):

        while len(self.documents) > self.max_documents_per_session:

            oldest_doc = self.document_upload_order.pop(0)

            if oldest_doc in self.documents:

                file_path = self.documents[oldest_doc].get("file_path")

                if file_path and os.path.exists(file_path):
                    os.remove(file_path)

                del self.documents[oldest_doc]

                gc.collect()

                if self.current_document == oldest_doc:

                    if self.documents:

                        self.current_document = (
                            self.document_upload_order[-1]
                            if self.document_upload_order
                            else list(self.documents.keys())[0]
                        )

                    else:
                        self.current_document = None
    # --------------------------------------------------

    def load_pdf(self, file_path, doc_name="document"):

        from document_processor import extract_text, split_into_chunks

        with self.upload_lock:

            print(f"Loading document: {doc_name}")

            text = extract_text(file_path)

            # Smaller chunks = lower RAM usage
            chunks = split_into_chunks(
                text,
                chunk_size=200,
                overlap=20
            )

            model = self.get_embedding_model()

            embeddings = model.encode(
                chunks,
                show_progress_bar=False,
                convert_to_numpy=True
            ).astype("float32")

            index = faiss.IndexFlatL2(
                embeddings.shape[1]
            )

            index.add(embeddings)

            # IMPORTANT:
            # Do NOT store embeddings in memory.
            self.documents[doc_name] = {
                "index": index,
                "chunks": chunks,
                "file_path": file_path,
                "upload_timestamp": time.time()
            }

            if doc_name in self.document_upload_order:
                self.document_upload_order.remove(doc_name)

            self.document_upload_order.append(doc_name)

            self.cleanup_old_documents()

            self.current_document = doc_name

            # Free memory immediately
            del embeddings
            gc.collect()

            print(
                f"✓ [Session {self.session_id}] "
                f"{doc_name} loaded with {len(chunks)} chunks"
            )

    # --------------------------------------------------

    def get_documents_list(self):

        doc_list = []

        for doc_name in self.document_upload_order:

            if doc_name in self.documents:

                doc_list.append(
                    {
                        "name": doc_name,
                        "chunks": len(
                            self.documents[doc_name]["chunks"]
                        ),
                        "is_current":
                            doc_name == self.current_document,
                    }
                )

        return doc_list

    # --------------------------------------------------

    def set_current_document(self, doc_name):

        if doc_name not in self.documents:
            return False

        self.current_document = doc_name
        return True
    # --------------------------------------------------

    def delete_document(self, doc_name):

        if doc_name not in self.documents:
            return False

        file_path = self.documents[doc_name].get("file_path")

        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        del self.documents[doc_name]

        if doc_name in self.document_upload_order:
            self.document_upload_order.remove(doc_name)

        if self.current_document == doc_name:

            if self.documents:

                self.current_document = (
                    self.document_upload_order[-1]
                    if self.document_upload_order
                    else list(self.documents.keys())[0]
                )

            else:
                self.current_document = None

        gc.collect()

        return True

    # --------------------------------------------------

    def clear_session(self):

        for doc_name in list(self.documents.keys()):

            file_path = self.documents[doc_name].get("file_path")

            if file_path and os.path.exists(file_path):
                os.remove(file_path)

        self.documents.clear()
        self.document_upload_order.clear()
        self.current_document = None

        if os.path.exists(self.session_folder):
            shutil.rmtree(self.session_folder)
            os.makedirs(self.session_folder, exist_ok=True)

        gc.collect()

    # --------------------------------------------------

    def search(self, query, top_k=2):

        if self.current_document is None:
            return [], []

        if self.current_document not in self.documents:
            return [], []

        doc = self.documents[self.current_document]

        index = doc["index"]
        chunks = doc["chunks"]

        actual_top_k = min(top_k, len(chunks))

        model = self.get_embedding_model()

        query_embedding = model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        distances, indices = index.search(
            query_embedding,
            actual_top_k
        )

        similarities = 1 / (1 + distances[0][:actual_top_k])

        results = []
        scores = []

        for idx, score in zip(
            indices[0][:actual_top_k],
            similarities
        ):
            results.append(chunks[idx])
            scores.append(float(score))

        del query_embedding

        return results, scores

    # --------------------------------------------------

    def is_relevant(self, scores):

        if not scores:
            return False

        max_score = max(scores)

        print(
            f"Relevance Score: {max_score:.3f}"
        )

        return max_score >= self.relevance_threshold
