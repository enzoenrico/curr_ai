from csv import excel
import os
from pydoc import cli
from typing import List
import chromadb
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate

from langchain_community.document_loaders import TwitterTweetLoader

from dotenv import load_dotenv
from numpy import number
from regex import W
import tweepy

from utils import TweetLoader

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

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50, length_function=len
        )

        self.chat = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")
        self.embeddings = OpenAIEmbeddings()

        # find a way to insert both chat history and external context into the outside_context variable
        self.prompt = PromptTemplate(
            template=raw_prompt, input_variables=["outside_context", "user_prompt"]
        )

        self._initChroma()

        # remove hardcoded values
        self.x_document_list = self._initXLoader(["elonmusk"])

        # chromadb.from_documents(split_documents(Document()))
        #                           ^class document, no matter from what loader
        # self.store = #chromadb
        # use chromadb.as_retriever to find similar

    def _initXLoader(self, users: List[str]):
        "loads tweets from users into a List[Document] and returns it"

        # replace that bitch, keep the functionality tho
        # ./utils/TweetLoader.py

        try:
            print("[+] creating twitter loader")
            x_loader = TwitterTweetLoader.from_bearer_token(
                oauth2_bearer_token=os.environ["X_BEARER_TOKEN"],
                twitter_users=users,  # change this.
                number_tweets=2,
            )
        except Exception as err:
            print(f"[-]{err}")
            return

        x_documents = x_loader.load()
        split_x_docs = self.text_splitter.split_documents(documents=x_documents)
        self.chroma.add_documents(split_x_docs)

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

        # prompt question with context

        prompt_with_user_question = self.prompt.format(
            outside_context=context_from_chroma, user_prompt=question
        )
        response = self.chat.invoke(prompt_with_user_question)
        return str(response.content)


# panga = RAG()
# panga.query("what is elon's musk latest tweet about?")
tl = TweetLoader.TweetLoader()
#running into 429 - too many requests
tl.searchUser('')

