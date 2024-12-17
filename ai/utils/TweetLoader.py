from http import client
import os
from re import M
import tweepy
import tweepy.client


class TweetLoader:
    def __init__(self):
        self.__api_key = os.environ["X_API_KEY"]
        self.__api_secret = os.environ["X_API_SECRET"]

        self.__access_token = os.environ["X_ACCESS_TOKEN"]
        self.__access_token_secret = os.environ["X_ACCESS_TOKEN_SECRET"]

        try:
            self.__setClient()
            # self.api = tweepy.API(self.auth)
            print("[+] Tweepy API connector created successfully")
        except:
            print("[ERROR] Error creating auth")
            return

    def __setClient(self):
        """
        Sets up the Twitter API client using authentication credentials from environment variables.
        DEPRECATED: This class is deprecated. Please use TweetLoader.TweetLoader() instead.
        The method retrieves the following credentials from environment variables:
        - X_BEARER_TOKEN
        - X_API_KEY
        - X_API_SECRET
        - X_ACCESS_TOKEN
        - X_ACCESS_TOKEN_SECRET
        These credentials are used to create an authenticated tweepy.Client instance
        which is then stored in the instance variable 'client'.
        Returns:
            None
        """
        print("[WARNING] This class is deprecated. Please use TweetLoader.TweetLoader() instead.")
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
        )
        # Attempt to get user information
        # user_me = client.get_me()
        # print(user_me)
        # print("[+] Successfully authenticated with Twitter API")
        self.client = client

    def searchUser(self, user: str):
        # user_info = self.api.search_users(q=user)
        response = self.client.get_me()

        #running into 429 - too many requests
        # cache the users
        if response.data:
            user_info = response.data.id
            tweets = self.client.get_tweets(ids=[user_info])
            return tweets
        print("no proper response")
        return None
