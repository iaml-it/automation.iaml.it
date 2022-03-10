*Hosting*
- Heroku offers a free tier-0 for JavaScript and MongoDB, we could host the app for free, forever.
- Firebase is also free to use for the tier-0.

## v0

### Module: URL Receiver
receives event URL from EventBrite Web Hook and pushes it to a Storage

### Module: Event Gatherer
given an organization eventbrite page saves to a Storage all pubblicly available events

### Module: Eventbrite Reader
Eventbrite is public and free. Is the only event website which integrates with Facebook events.

Reads urls from a storage and requires event data from eventbrite API pushing data to some sort of database.

- define a "standard" data structure for all events
- for a given organizer (ex: https://www.eventbrite.it/o/fevr-7297766259 ).
- scan for the list of events (first time: import past).
- for each event collect as much metadata as possible, especially:
  - event details ( when, where, who, what, why, whateva )
  - speaker
  - event category
  - event tags
  - event keywords
  - event hashtags
  - event cover image (?)

### Module: Writer Firebase/mongodb
Push the list of standard event datastructures to firebase or monrgodb (free on heroku)

### Module: Push GitHub
Push the list of standard event to github as json-serialized data. 
- Goal: backup event history data on github. 
- Goal: update the website. 
- The json-data will be parsed by jekill at the next website update.

