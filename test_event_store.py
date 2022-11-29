import pytest
import json
from datetime import datetime
from event_store import DatetimeEventStore


def get_json():
    with open("data_test.json", 'r') as json_read:
        return json.load(json_read)


class TestDatetimeEventStore:
    event_store = DatetimeEventStore()

    def initialize(self):
        self.event_store.events = []
        self.event_store.events = get_json()
        self.event_store.format_data()

    def test_store_event_success(self):
        self.initialize()
        assert self.event_store.store_event(datetime(2018, 8, 23), "test event") == \
               {"id": 5, "date": datetime(2018, 8, 23), "event": "test event"}
        assert self.event_store.events[-1]['date'] == datetime(2018, 8, 23)
        assert self.event_store.events[-1]['event'] == "test event"
        assert self.event_store.events[-2]['id'] + 1 == self.event_store.events[-1]['id']

    def test_store_event_error(self):
        self.initialize()
        with pytest.raises(TypeError):
            assert self.event_store.store_event(at=datetime(2018, 8, 20))
            assert self.event_store.store_event(event="test event")

    def test_get_event(self):
        self.initialize()
        res = self.event_store.get_events(start=datetime(2018, 8, 18), end=datetime(2018, 8, 22))
        assert len(res) == 5
        res = self.event_store.get_events(start=datetime(2018, 8, 19), end=datetime(2018, 8, 21))
        assert res == [{"id": 1, "date": datetime(2018, 8, 19), "event": "Processing 1"},
                       {"id": 2, "date": datetime(2018, 8, 20), "event": "Processing 2"},
                       {"id": 3, "date": datetime(2018, 8, 21), "event": "Processing 3"}]

    def test_get_no_event(self):
        self.initialize()
        res = self.event_store.get_events(start=datetime(2019, 8, 17), end=datetime(2019, 8, 21))
        assert res == []

    def test_update_event(self):
        self.initialize()
        self.event_store.update_event(1, {"date": datetime(2022, 10, 15), "event": "Updating"})
        assert self.event_store.events[1] == {"id": 1, "date": datetime(2022, 10, 15), "event": "Updating"}

    def test_delete_by_id_success(self):
        self.initialize()
        self.event_store.delete_event_by_id(2)
        assert self.event_store.events == [{"id": 0, "date": datetime(2018, 8, 18), "event": "Start process"},
                                           {"id": 1, "date": datetime(2018, 8, 19), "event": "Processing 1"},
                                           {"id": 3, "date": datetime(2018, 8, 21), "event": "Processing 3"},
                                           {"id": 4, "date": datetime(2018, 8, 22), "event": "End process"}]

    def test_delete_event_success(self):
        self.initialize()
        self.event_store.delete_event([{"id": 1, "date": datetime(2018, 8, 19), "event": "Processing 1"},
                                       {"id": 2, "date": datetime(2018, 8, 20), "event": "Processing 2"}])
        assert self.event_store.events == [{"id": 0, "date": datetime(2018, 8, 18), "event": "Start process"},
                                           {"id": 3, "date": datetime(2018, 8, 21), "event": "Processing 3"},
                                           {"id": 4, "date": datetime(2018, 8, 22), "event": "End process"}]
        self.event_store.delete_event(self.event_store.get_events("2018-01-01", "2018-12-31"))
        assert self.event_store.events == []

    def test_delete_event_wrong_entry(self):
        self.initialize()
        self.event_store.delete_event([{"date": datetime(2018, 8, 19), "event": "Processing 2"}])
        assert len(self.event_store.events) == 5
        self.event_store.delete_event([])
        assert len(self.event_store.events) == 5
        with pytest.raises(TypeError):
            self.event_store.delete_event(15)
            assert len(self.event_store.events) == 5

    def test_validate_success(self):
        self.initialize()
        assert self.event_store.validate("2018-08-18") == datetime(2018, 8, 18)
        assert self.event_store.validate("2018-08-18 00:00:00") == datetime(2018, 8, 18)

    def test_validate_error(self):
        self.initialize()
        with pytest.raises(ValueError):
            self.event_store.validate("2018/08/10")

