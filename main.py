import requests
import json
from pymongo import MongoClient
import glob
import time
import os


organizers = [
  7297766259 # fevr.eventbrite.it
]

db_url = 'localhost:27017'
db_name = 'iaml_automation'

def main():
  storage = Storage(db_url,db_name)

  # storage.cache.clearCache()

  cacheAllEvents(storage)
  saveToStorage(storage)

def saveToStorage(storage: 'Storage'):
  evb = Eventbrite()
  events = []

  evb_events = storage.cache.readCache('*')
  for evb_event in evb_events:
    event = evb.toModelEvent(evb_event)
    events.append(event.__dict__)
  storage.addEvents(events)


def cacheAllEvents(storage: 'Storage'):
  ts = int(time.time() * 100 )
  history = True
  evb = Eventbrite()
  for organizer_id in organizers:
    events = evb.organizer_events(organizer_id, history=history)
    cache_name = 'evb-events-{}-{}.json'.format(organizer_id,ts)
    storage.cache.writeCache(cache_name, events)


class Cache():
  def __init__(self):
    self.basepath = './cache/'

  def clearCache(self):
    files = glob.glob(self.basepath+'*.json')
    for file in files:
      os.remove(file) 

  def existCache(self,name):
    filenames = glob.glob('{}{}.json'.format(self.basepath,name))
    return len(filenames) > 0

  def readCache(self,name):
    filenames = glob.glob('{}{}.json'.format(self.basepath,name))
    data = []
    for filename in filenames:
      with open(filename,'r') as file: data.extend( json.load(file) ) 
    return data

  def writeCache(self, name, data):
    filename = './cache/{}.json'.format(name)
    with open(filename,'w') as file: json.dump(data, file, indent=2)


class Storage():
  def __init__(self, url, db_name):
    self.cache = Cache()
    self.client = MongoClient(url)
    self.db = self.client.get_database(db_name)


    

  def addEvents(self, events):
    result = self.db.events.insert_many(events)
    return result
    

  def addEvent(self, event):
    result = self.db.events.insert_one(event)
    return result


class Model():
  def __init__(self):
    super(self)
    self.id

class ModelOrganizer(Model):
  def __init__(self):
    super(self)
    self.name = None

class ModelEvent(Model):
  def __init__(self): 
    self.data_src = None
    self.event_id = None
    self.event_url = None

    self.organizer_id = None

    self.img_url = None 

    self.title = None
    self.description = None
    self.tags = None
    self.speaker = None
    self.event_format = 'talk'

    self.venue = None

    self.date_start = None
    self.date_end = None
    self.recurrent = False

    self.price = 0
    self.currency = "EUR"


class Eventbrite():
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

  def toModelEvent(self, event_data):
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
    
    data.date_start = event_data['start']['local']   # use 'utc' + timestamp ? 
    data.date_end = event_data['end']['local']
    return data



  def organizer_events(self, organizer_id, page_num = -1, page_size=30, history = False):
    """
      example URL :
      https://www.eventbrite.it/org/7297766259/showmore/?page_size=30&type=past&page=1
    """
    path = "org/{}/showmore/?page={}&page_size={}&type={}"
    event_type = "past" if history else "future"
    if page_size <= 0 or page_size >=30: page_size=30

    allpages = False
    if page_num <= 0:
      allpages = True
      page_num = 1
    
    events = []
    while True:
      fullpath = path.format(organizer_id, page_num, page_size, event_type )
      success, response = self.request(fullpath)
      if not success:
         print("errors :(")
         break
      #print(response)
      events.extend(response['events'])

      if not allpages or not response['has_next_page']:
        break
      else:
        print("one more page: {} {}".format(page_num, response['has_next_page']))
        page_num += 1

    return events
        
    




if __name__ == '__main__':
  main()











"""

  
    
    "ticket_availability": {
      "quantity_sold_add_on": 0,
      "minimum_ticket_price_rounded": {
        "currency": "EUR",
        "display": "0 EUR",
        "value": 0
      },
      "maximum_ticket_price": {
        "currency": "EUR",
        "major_value": "0.00",
        "value": 0,
        "display": "0.00 EUR"
      },
      "num_ticket_classes": 2,
      "has_available_hidden_tickets": false,
      "end_sales_date": {
        "timezone": "Europe/Rome",
        "local": "2022-02-17T19:00:00",
        "utc": "2022-02-17T18:00:00Z"
      },
      "minimum_ticket_price": {
        "currency": "EUR",
        "major_value": "0.00",
        "value": 0,
        "display": "0.00 EUR"
      },
      "is_free": false,
      "maximum_ticket_price_rounded": {
        "currency": "EUR",
        "display": "0 EUR",
        "value": 0
      },
      "is_hold_unavailable": false,
      "waitlist_enabled": false,
      "has_available_tickets": false,
      "common_sales_end_date": null,
      "is_sold_out": true,
      "waitlist_available": false
    },
    "category": {
      "subcategories": [],
      "short_name_localized": "Scienze e tecnologia",
      "name": "Science & Technology",
      "short_name": "Science & Tech",
      "name_localized": "Scienze e tecnologia",
      "id": "102"
    },
    "user_id": "114965312043",
    "source": "coyote",
    "show_seatmap_thumbnail": false,
    "inventory_type": "limited",
    "show_colors_in_seatmap_thumbnail": false,
    "logo_id": "220005079",
    "start": {
      "utc": "2022-02-17T18:00:00Z",
      "date_header": "Oggi",
      "timezone": "Europe/Rome",
      "local": "2022-02-17T19:00:00",
      "formatted_time": "19:00"
    },
    "listed": true,
    "is_series": false,
    "hide_end_date": false,
    "status": "completed",
    "_type": "event",
    "description": {
      "text": "EVENTO LIVE SU https://www.facebook.com/groups/frontendersverona",
      "html": "EVENTO LIVE SU https://www.facebook.com/groups/frontendersverona"
    },
    "format": {
      "short_name_localized": "Seminario",
      "name": "Seminar or Talk",
      "short_name": "Seminar",
      "name_localized": "Seminario o conferenza",
      "schema_url": "https://schema.org/EducationEvent",
      "id": "2"
    },
    "show_pick_a_seat": false,
    "is_free": false,
    "organization_id": "114965312043",
    "is_externally_ticketed": false,
    "is_protected_event": false,
    "is_series_parent": false,
    "end": {
      "timezone": "Europe/Rome",
      "local": "2022-02-17T20:30:00",
      "utc": "2022-02-17T19:30:00Z"
    },
    "format_id": "2",
    "tld": ".it",
    "price_range": "",
    "name": {
      "text": "No Code e AI"
    },
    "language": "it-it",
    "url": "https://www.eventbrite.it/e/biglietti-no-code-e-ai-257900305757",
    "venue": null,
    "summary": "EVENTO LIVE SU https://www.facebook.com/groups/frontendersverona",
    "is_locked": false,
    "shareable": true,
    "style_id": "165018769",
    "online_event": true,
    "organizer_id": "7297766259",
    "category_id": "102",
    "survey_type": "attendee",
    "published": "2022-01-28T14:18:41Z"
  },


"""