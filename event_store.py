from datetime import datetime, date


class DatetimeEventStore:
    def __init__(self, events=[]):
        self.events = events

    def store_event(self, at, event):
        self.events.append({"date": self.validate(at), 'event': event})
        return self.events[-1]

    def get_events(self, start, end):
        events_to_get = []
        for event in self.events:
            if self.validate(start) <= self.validate(event["date"]) <= self.validate(end):
                events_to_get.append(event)
        return events_to_get

    def update_event(self, id, data):
        self.events[id] = {"date": self.validate(data['date']), "event": data['event']}

    def delete_event(self, events_to_remove):
        for event in events_to_remove:
            try:
                self.events.remove(event)
            except ValueError:
                pass

    @staticmethod
    def validate(date_to_validate):
        if not isinstance(date_to_validate, date):
            try:
                date_to_validate = datetime.strptime(date_to_validate, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    date_to_validate = datetime.strptime(date_to_validate, '%Y-%m-%d')
                except ValueError:
                    raise ValueError("Incorrect data format, should be YYYY-MM-DD or YYYY-MM-DD HH-MM-SS")
        return date_to_validate
