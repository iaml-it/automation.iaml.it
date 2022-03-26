import time

from yaml import safe_load

from src.eventbrite import Eventbrite
from src.storage import Storage

config = safe_load(open('../db_config.yaml', 'r'))
DB_HOST = config['host']
DB_USERNAME = config['username']
DB_PASSWORD = config['password']
DB_NAME = config['db_name']
organizers = [
    7297766259  # fevr.eventbrite.it
]


def save_to_storage(storage: Storage):
    evb = Eventbrite()
    events = []

    evb_events = storage.cache.read_cache('*')
    for evb_event in evb_events:
        event = evb.to_model_event(evb_event)
        events.append(event.__dict__)
    storage.add_events(events)


def cache_all_events(storage: Storage):
    ts = int(time.time() * 100)
    history = True
    evb = Eventbrite()
    for organizer_id in organizers:
        events = evb.organizer_events(organizer_id, history=history)
        cache_name = 'evb-events-{}-{}.json'.format(organizer_id, ts)
        storage.cache.write_cache(cache_name, events)


def main():
    storage = Storage(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)

    # storage.cache.clearCache()

    cache_all_events(storage)
    save_to_storage(storage)


if __name__ == '__main__':
    main()
