import pytest
from datetime import datetime
from event_store import DatetimeEventStore

data_test = [
    {
        "date": datetime(2018, 8, 18),
        "event": "Start process"
    },
    {
        "date": datetime(2018, 8, 19),
        "event": "Processing 1"
    },
    {
        "date": datetime(2018, 8, 20),
        "event": "Processing 2"
    },
    {
        "date": datetime(2018, 8, 21),
        "event": "Processing 3"
    },
    {
        "date": datetime(2018, 8, 22),
        "event": "End process"
    },
]


class TestDatetimeEventStore:
    event_store = DatetimeEventStore()

    def initialize(self):
        self.event_store.events = []
        self.event_store.events = data_test.copy()

    def test_store_event_success(self):
        self.initialize()
        assert self.event_store.store_event(datetime(2018, 8, 23), "test event") == \
               {"date": datetime(2018, 8, 23), "event": "test event"}
        assert self.event_store.events[-1]['date'] == datetime(2018, 8, 23)
        assert self.event_store.events[-1]['event'] == "test event"

    def test_store_event_error(self):
        self.initialize()
        with pytest.raises(TypeError):
            assert self.event_store.store_event(at=datetime(2018, 8, 20))
            assert self.event_store.store_event(event="test event")

    def test_get_event(self):
        self.initialize()
        res = self.event_store.get_events(start=datetime(2018, 8, 18), end=datetime(2018, 8, 22))
        print(data_test)
        assert res == data_test
        res = self.event_store.get_events(start=datetime(2018, 8, 19), end=datetime(2018, 8, 21))
        assert res == [{"date": datetime(2018, 8, 19), "event": "Processing 1"},
                       {"date": datetime(2018, 8, 20), "event": "Processing 2"},
                       {"date": datetime(2018, 8, 21), "event": "Processing 3"},]

    def test_get_no_event(self):
        res = self.event_store.get_events(start=datetime(2019, 8, 17), end=datetime(2019, 8, 21))
        assert res == []

    def test_validate_success(self):
        self.initialize()
        assert self.event_store.validate("2018-08-18") == datetime(2018, 8, 18)
        assert self.event_store.validate("2018-08-18 00:00:00") == datetime(2018, 8, 18)

    def test_validate_error(self):
        self.initialize()
        with pytest.raises(ValueError):
            self.event_store.validate("2018/08/10")

