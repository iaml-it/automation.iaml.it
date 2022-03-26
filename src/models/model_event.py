from src.models.model import Model


class ModelEvent(Model):
    def __init__(self):
        super().__init__()
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
