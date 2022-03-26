import json

import requests as requests

from src.models.model_event import ModelEvent


class Eventbrite:
    BASEURL = "https://www.eventbrite.it/"

    def request(self, path):
        url = self.BASEURL + path
        print(url)
        content = requests.get(url).content
        data = json.loads(content)
        if data['success']:
            return True, data['data']
        else:
            return False, []

    @staticmethod
    def to_model_event(event_data):
        data = ModelEvent()
        data.data_src = 'eventbrite'

        data.event_id = event_data['id']
        data.event_url = event_data['url']

        data.organizer_id = event_data['organizer']['id']
        data.organizer_name = event_data['organizer']['name']
        data.organizer_url = event_data['organizer']['url']

        data.img_url = event_data['logo']['url']

        data.title = event_data['name']['text']
        data.description = event_data['description']['text']
        data.tags = []
        data.speaker = ""
        data.event_format = 'talk'

        data.venue = event_data['venue']

        data.date_start = event_data['start']['local']  # use 'utc' + timestamp ?
        data.date_end = event_data['end']['local']
        return data

    def organizer_events(self, organizer_id, page_num=-1, page_size=30, history=False):
        """
          example URL :
          https://www.eventbrite.it/org/7297766259/showmore/?page_size=30&type=past&page=1
        """
        path = "org/{}/showmore/?page={}&page_size={}&type={}"
        event_type = "past" if history else "future"
        if page_size <= 0 or page_size >= 30:
            page_size = 30

        all_pages = False
        if page_num <= 0:
            all_pages = True
            page_num = 1

        events = []
        while True:
            fullpath = path.format(organizer_id, page_num, page_size, event_type)
            success, response = self.request(fullpath)
            if not success:
                print("errors :(")
                break
            # print(response)
            events.extend(response['events'])

            if not all_pages or not response['has_next_page']:
                break
            else:
                print("one more page: {} {}".format(page_num, response['has_next_page']))
                page_num += 1

        return events
