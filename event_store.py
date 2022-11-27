from datetime import datetime


class DatetimeEventStore:
    def __init__(self, events=[]):
        self.events = events

    def store_event(self, at, event):
        pass

    def get_events(self, start, end):
        pass
