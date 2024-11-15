from pathlib import Path

import pytest
from flask import session, app, current_app

from podcast import create_app
from podcast.adapters import repository_populate
from podcast.adapters.service.memory_repository import MemoryRepository
from tests.conftest import TEST_DATA_PATH


# from podcast import create_app


@pytest.fixture
def memory_repo():
    """Create an in-memory repository with test data."""
    # TEST_DATA_PATH = Path(__file__).parent / "data"
    repo = MemoryRepository()
    repository_populate.populate(TEST_DATA_PATH, None, repo, False)
    return repo

@pytest.fixture
def client(memory_repo):
    """Create a test client with the in-memory repository."""
    app = create_app({
        'TESTING': True,
        'REPOSITORY': 'memory',  # Use a string instead
    })
    return app.test_client()

def test_podcasts(client):  # testing podcast page response
    with client:
        response_code = client.get('/podcasts').status_code
        assert response_code == 200


def test_search_podcasts_title(client):  # Simulate a search for a specific podcast title
    response = client.get('/podcasts?search=Test%20Podcast')
    assert response.status_code == 200
    assert b'Jesmond Parish Church' in response.data


def test_search_podcasts_category(client):  # simulate searching for category keyword
    response = client.get('/podcasts?search_title=education')
    assert response.status_code == 200
    assert b'6 Minute Grammar' in response.data


def test_search_podcasts_author(client):  # simulate searching for author
    response = client.get('/podcasts?page=1&search_title=robert&title=')
    assert response.status_code == 200
    assert b'Happiness Podcast' in response.data


def test_filter_podcasts_by_category(client):  # Simulate filtering podcasts by category
    response = client.get('/podcasts?category=4')
    assert response.status_code == 200
    assert b'8bit Saga' in response.data


def test_filter_podcasts_by_author(client):  # Simulate filter podcast by author
    response = client.get('/podcasts?author=4')
    assert response.status_code == 200
    assert b'1869, the Cornell University Press Podcast' in response.data


def test_filter_podcasts_by_title(client):  # simulate filter by title
    response = client.get('/podcasts?title=191')
    assert response.status_code == 200
    assert b'The Butt Show' in response.data


def test_no_results_for_invalid_search(client):  # Simulate a search for a non-existent podcast
    response = client.get('/podcasts?search_title=Nonexistent%20Podcast')
    assert response.status_code == 200
    assert b'No podcasts available matching your search criteria.' in response.data
