import datetime
import os
import pprint
from typing import Any, Dict, Iterable, List
from xml.dom.minidom import Document
from sympy import true, use
import tweepy
import tweepy.client

from langchain_core.documents import Document


class TweetLoader:
    def __init__(self, n_tweets: int, users: List[str]):
        self.n_tweets = n_tweets
        self.users = users

        try:
            self.__setClient()
            # self.api = tweepy.API(self.auth)
            print("[+] Tweepy API connector created successfully")
        except:
            print("[ERROR] Error creating auth")
            return

        # twitter_response = self.searchUsers()
        # self.load_documents(twitter_response)

    def __setClient(self):
        bearer_token = os.environ.get("X_BEARER_TOKEN")
        api_key = os.environ.get("X_API_KEY")
        api_secret = os.environ.get("X_API_SECRET")
        access_token = os.environ.get("X_ACCESS_TOKEN")
        access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

        # Create authenticated client

        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=true,
        )
        self.client = client

    def load(self) -> List[Document]:

        results: List[Document] = []

        for username in self.users:
            user = self.client.get_user(username=username)
            print("USER !!")
            print(user)
            print()
            if user.data:
                user_id = user.data.id
                print(f"UserID: {user_id}")

            # rate limit happens here (╬▔皿▔)╯
            users_tweets = self.client.get_users_tweets(id=user_id)

            docs = self._format_tweets(users_tweets, user)
            results.extend(docs)
        return results

    def _format_tweets(self, tweets_response, user_response) -> List[Document]:
        # TODO: add related tweets to metadata or document context
        # add:
        #   - referenced tweets
        #   - created_at
        documents = []

        if not tweets_response.data:
            return documents

        print("Tweets_response: \n")
        pprint.pprint(tweets_response)
        print()

        for tweet in tweets_response.data:
            metadata = {
                "id": tweet.id,
                # change to not be just id, get whole user context
                "author_id": user_response.data.id,
                "author_username": user_response.data.username,
                "created_at": tweet.created_at,
            }

            if hasattr(tweet, "referenced_tweets"):
                print(f'Referenced_tweets: \n {tweet.referenced_tweets}')
                metadata["referenced_tweets"] = tweet.referenced_tweets

            clean_meta = self._clean_metadata(metadata=metadata)
            print(f"[+]Clean metdata -> \n {clean_meta}")

            doc = Document(page_content=tweet.text, metadata=clean_meta)
            print("Generated document: \n")
            print(doc)
            print()
            documents.append(doc)

        return documents

    def _clean_metadata(self, metadata: Dict[str, Any]):
        clean_meta = {}

        for key, value in metadata.items():
            # if isinstance(value, datetime):
            #     clean_meta[key] = value.isoformat()
            if hasattr(value, "__dict__"):
                clean_meta[key] = str(value)

            elif isinstance(value, (str, int, float, bool)):
                clean_meta[key] = value

            elif value is None:
                clean_meta[key] = ""
        return clean_meta
