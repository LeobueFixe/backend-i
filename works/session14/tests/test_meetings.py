import json
import sys
from pathlib import Path

# Add src directory to path so imports work without PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from fastapi.testclient import TestClient
from api.main import api
from api.services import data as data_service

client = TestClient(api)


@pytest.fixture(autouse=True)
def clean_database(tmp_path, monkeypatch):
    db_file = tmp_path / "database.json"
    meetings_dir = tmp_path / "meetings"

    monkeypatch.setattr(data_service, "DB_PATH", db_file)
    monkeypatch.setattr(data_service, "FOLDER_PATH", meetings_dir)

    # Ensure a clean DB for every test
    db_file.parent.mkdir(parents=True, exist_ok=True)
    db_file.write_text(json.dumps({"meetings": []}, indent=4), encoding="utf-8")

    yield


@pytest.fixture
def meeting_with_action_items():
    payload = {
        "title": "Planning",
        "date": "2026-03-10T10:00:00",
        "owner": "Jorge",
        "participants": ["Alex"],
    }
    resp = client.post("/meetings", json=payload)
    meeting = resp.json()
    meeting_id = meeting["id"]

    for i in range(2):
        action = {
            "description": f"Task {i+1}",
            "owner": "Jorge" if i == 0 else "Alex",
            "due_date": "2026-03-20",
        }
        client.post(f"/meetings/{meeting_id}/action-items", json=action)

    return meeting


def test_create_meeting_ok():
    payload = {
        "title": "Planning",
        "date": "2026-03-10T10:00:00",
        "owner": "Jorge",
        "participants": ["Alex"],
    }
    r = client.post("/meetings", json=payload)
    assert r.status_code == 201

    data = r.json()
    assert data["title"] == payload["title"]
    assert data["owner"] == payload["owner"]
    assert data["participants"] == payload["participants"]


def test_create_meeting_title_too_short_error():
    payload = {
        "title": "Hi",
        "date": "2026-03-10T10:00:00",
        "owner": "Jorge",
        "participants": ["Alex"],
    }
    r = client.post("/meetings", json=payload)
    assert r.status_code == 422


def test_create_meeting_owner_too_short_error():
    payload = {
        "title": "Planning",
        "date": "2026-03-10T10:00:00",
        "owner": "J",
        "participants": ["Alex"],
    }
    r = client.post("/meetings", json=payload)
    assert r.status_code == 422


def test_list_action_items_with_fixture(meeting_with_action_items):
    meeting_id = meeting_with_action_items["id"]
    r = client.get(f"/meetings/{meeting_id}/action-items?owner=Jorge&limit=10&offset=0")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["owner"] == "Jorge"


def test_dashboard_summary_empty():
    r = client.get("/dashboard/summary")
    assert r.status_code == 200
    body = r.json()
    assert body["total_meetings"] == 0
    assert body["total_action_items"] == 0
    assert body["unique_owners"] == 0
    assert body["owners"] == []


def test_dashboard_summary_with_data(meeting_with_action_items):
    r = client.get("/dashboard/summary")
    assert r.status_code == 200
    body = r.json()
    assert body["total_meetings"] == 1
    assert body["total_action_items"] == 2
    assert body["unique_owners"] >= 2
    assert "Jorge" in body["owners"]

