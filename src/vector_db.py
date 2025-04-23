import torch
from transformers import AutoModel, AutoTokenizer
import faiss
import numpy as np
import json
from uuid import uuid4
        
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document
from langchain_core.embeddings import FakeEmbeddings

class VectorDB:
    def __init__(self, urls):
        # Load a pre-trained model and tokenizer
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"  # Example model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        
        #for Fauss initialization
        self.fake_embeddings_size = 4096

        # save url separately for the output to user
        self.urls=urls
        # initialize the list documents in the string type and "summary(topic1, topic2)" format
        self.list_texts=[]

    # Generate embeddings
    def generate_embeddings(self, texts):
        # generating embeddings
        inputs = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state[:, 0, :]
        return embeddings

    def prepare_data(self, texts):
        # put the documents in the list as the strings with "summary(topic1, topic2)" format
        dict_texts = json.loads(texts)
        delimiter = ", "
        joined_str = str(dict_texts["summary"]) + "(" + delimiter.join(dict_texts["topics"]) + ")"
        self.list_texts.append(joined_str)

    def createFaissIndex(self):
        # prepare indices based on L2 distance metric
        self.embeddings = self.generate_embeddings(self.list_texts)

        # Convert embeddings to numpy array
        embeddings_np = self.embeddings.numpy()  # Assuming embeddings are in PyTorch tensor
        
        # Create a Faiss index
        dimension = embeddings_np.shape[1]  # Dimensionality of the vectors
        self.index = faiss.IndexFlatL2(dimension)  # Using L2 distance metric
        self.index.add(embeddings_np)  # Add embeddings to the index

        print(f"Total vectors in index: {self.index.ntotal}")

    def createVectorStore(self):
        # prepare FAISS vectore store with indices based on L2 distance metric
        docs=[]
        for text in self.list_texts:
            page = Document(page_content=text, metadata = {"source": "website"})
            docs.append(page)

        print(docs)
        uuids = [str(uuid4()) for _ in range(len(self.list_texts))]

        # initialization of the vectore store with Fake embeddings
        fake_embeddings = FakeEmbeddings(size=self.fake_embeddings_size)
        fake_index = faiss.IndexFlatL2(len(fake_embeddings.embed_query("hello world")))  # Using L2 distance metric

        # Wrap FAISS index in LangChain's FAISS VectorStore
        self.vector_store = FAISS(
            embedding_function=fake_embeddings,
            index=fake_index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )
        self.vector_store.add_documents(documents=docs, ids=uuids)

    def search_in_db(self, query):
        print("Search in db")
        # generate embeddings for the user query
        query_vector = self.generate_embeddings(query).numpy()
        k = 1  # Number of nearest neighbors
        #compare query embeddings with embeddings of articles based on faiss index
        distances, indices = self.index.search(query_vector, k)
        
        # take the most appropriate result with the closest distance
        result = self.list_texts[indices[0][0]]
        distance = distances[0][0]
        url = self.urls[indices[0][0]]
        print(f"[{distance:3.4f}]The closest result is: [{result}], url: [{url}]")
        
        return distance, url

    def simularity_search(self, query):
        print("Simularity search")
        # compare query with documents from FAISS vectore store
        results = self.vector_store.similarity_search_with_score(
            query, k=1, filter={"source": "website"}
        )
        output_score = []
        # show the most appropriate results with the highest score
        for res, score in results:
            print(f"* [SIM={score:3.4f}] [{res.page_content}]")
            output_score.append(score)

        return output_score
