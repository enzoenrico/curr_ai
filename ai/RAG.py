from csv import excel
import os
from typing import List
from xml.dom.minidom import Document
import chromadb
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv

from utils.TweetLoader import TweetLoader


load_dotenv()


class RAG:
    def __init__(self):
        raw_prompt = """
        The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
        Your objective is to assit the user based on the provided context, composed by previous interactions and external data:
        Context:
            {outside_context}
        Awnser the user's following prompt:
            {user_prompt}
        """

        self.chroma_path = "./chroma/langchain_chromadb"

        self.text_splitter: RecursiveCharacterTextSplitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=500, chunk_overlap=50, length_function=len
            )
        )

        self.chat = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")
        self.embeddings = OpenAIEmbeddings()

        # find a way to insert both chat history and external context into the outside_context variable
        self.prompt = PromptTemplate(
            template=raw_prompt, input_variables=["outside_context", "user_prompt"]
        )

        self._initChroma()
        self._initXLoader()

        docs = self.loader.load()
        self._splitAndSave(docs)

    def _splitAndSave(self, documents):
        split_docs = self.text_splitter.split_documents(documents)
        try:
            self.chroma.add_documents(split_docs)
            print("[+]Successfully added documents to chromadb")
        except Exception as err:
            print(f"[-]Something went wrong adding documents to chromadb: \n {err}")

    def _initXLoader(self):
        "loads tweets from users into a List[Document] and returns it"
        try:
            print("[+] creating twitter loader")
            # should return document list for later splitting
            x_loader = TweetLoader(users=["elonmusk"], n_tweets=50)
            self.loader = x_loader
        except Exception as err:
            print(f"[-]{err}")
            return

    def _initChroma(self):
        print("[+]Initializing ChromaDB client")
        persistent_client = chromadb.PersistentClient()
        # collection name
        self.collection = persistent_client.get_or_create_collection("langchain_chroma")
        self.chroma = Chroma(
            client=persistent_client,
            # text empeddings ada 2
            embedding_function=self.embeddings,
            persist_directory=self.chroma_path,
        )
        self.retriever = self.chroma.as_retriever(kwargs={"k": 3})
        print("[+]Chorma initialized successfully")

    def query(self, question: str) -> str:
        context_from_chroma = self.retriever.invoke(question)
        print(f"Gathered Context: \n {context_from_chroma}")

        # prompt question with context
        prompt_with_user_question = self.prompt.format(
            outside_context=context_from_chroma, user_prompt=question
        )
        response = self.chat.invoke(prompt_with_user_question)
        return str(response.content)


panga = RAG()
# query_answ = panga.query("what is elon's musk latest tweet about?")
# print(f"Query Answer:\n\r{query_answ}")
# running into 429 - too many requests

while True:
    question = input("question here \n")

    query_answ = panga.query(question=question)
    print(f"Query Answer:\n\r{query_answ}")
