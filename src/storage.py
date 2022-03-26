from pymongo import MongoClient
from src.utils.cache import Cache


class Storage:
    def __init__(self, username, password, host, db_name):
        self.cache = Cache()
        self.client = MongoClient(f"mongodb+srv://{username}:{password}@{host}/{db_name}?retryWrites=true&w=majority")
        self.db = self.client.iaml_automation
        self.collection = self.db.eventlist

    def add_events(self, events):
        try:
            result = self.collection.insert_many(events)
            return result
        except Exception as e:
            print("An exception occurred ::", e)
            return None

    def add_event(self, event):
        try:
            result = self.collection.insert_one(event)
            return result
        except Exception as e:
            print("An exception occurred ::", e)
            return None
