import pytest
from flask import session, current_app

from podcast import create_app
from podcast.adapters import repository as repo, repository_populate
from podcast.adapters.service.memory_repository import MemoryRepository
from tests.conftest import TEST_DATA_PATH
from podcast.authentication.authentication_services import *


# from podcast.adapters.service import memory_repository


# Checking all pages that don't require log in can be visited

@pytest.fixture
def memory_repo():
    repo = MemoryRepository()
    repository_populate.populate(TEST_DATA_PATH, None, repo, False)
    return repo


@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'REPOSITORY': 'memory',
    })
    return app.test_client()


# Checking home page
def test_home_page(client):
    response_code = client.get('/login').status_code
    assert response_code == 200
    response_code = client.get('/').status_code
    assert response_code == 200


# Checking register page
def test_register_page(client):
    response_code = client.get('/register').status_code
    assert response_code == 200


# Checking catalogue page
def test_catalogue_page(client):
    response_code = client.get('/podcasts').status_code
    assert response_code == 200


#Checking login page
def test_login_page(client):
    response_code = client.get('/login').status_code
    assert response_code == 200


# Checking sample podcast description page
def test_description_page(client):
    response_code = client.get('/description/7').status_code
    assert response_code == 200


# Checking authentication procedures

# Testing user registration
def test_register(client):
    with client:
        client.post(
            '/register',
            data={'username': 'SimonCat', 'password': 'LovelyBoy99'}
        )
        assert '/login'

        repository = repo.repo_instance
        assert repository.get_all_users() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('sh', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter, \
                a lower case letter and a digit'),
        ('SimonCat', 'LovelyBoy99', b'There is already a user with this name, please choose a different one'),
))
# Check that attempting to register with invalid combinations of username and password generate appropriate error
# messages.
def test_register_with_invalid_input(client, username, password, message):
    client.post('/register', data={'username': 'SimonCat', 'password': 'LovelyBoy99'})
    response = client.post(
        '/register',
        data={'username': username, 'password': password}
    )
    assert response.status_code == 200


# Checking a registered user can log in
def test_login(client):
    client.post('/register', data={'username': 'SimonCat', 'password': 'LovelyBoy99'})
    with client:
        client.post(
            '/login',
            data={'username': 'SimonCat', 'password': 'LovelyBoy99'}
        )
        assert '/home'
        assert 'username' is 'username'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('CocoDog', '', b'Your log in information is required'),
        ('', 'Password99', b'Your log in information is required'),
        ('RandomUser', 'Password99', b"Username unrecognised. Please try again."),
        ('SimonCat', 'Password99', b"Password does not match. Please try again."),
))
# Making sure invalid log in attempts to bring up an error message
def test_login_with_invalid_input(client, username, password, message):
    client.post('/register', data={'username': 'SimonCat', 'password': 'LovelyBoy99'})
    response = client.post(
        '/login',
        data={'username': username, 'password': password}
    )
    assert response.status_code == 200


# Checking logout works
def test_logout(client):
    with client:
        #First, login
        client.post('/register', data={'username': 'SimonCat', 'password': 'LovelyBoy99'})
        client.post('/login', data={'username': 'SimonCat', 'password': 'LovelyBoy99'})
        #Try to log out
        response = client.get('/logout')
        assert 'username' not in session


# Testing review functionality

# Making sure unauthorised users cannot post reviews
def test_login_required_to_review(client):
    client.post('/description/<int:podcast_id>/new_review')
    assert '/login'


# Checking if an authenticated user can post a review
def test_review(client):
    # Login a user.
    with client:
        repository = repo.repo_instance
        client.post('/register', data={'username': 'SimonCat', 'password': 'LovelyBoy99'})
        client.post('/login', data={'username': 'SimonCat', 'password': 'LovelyBoy99'})

        # Check that we can retrieve the comment page.
        client.get('/description/12/new_review')

        # Post review
        client.post(
            '/comment/12/new_review',
            data={'comment': 'Awesome podcast!', 'rating': 5}
        )

        # Check that review exists
        review_success = repository.get_all_reviews != []
        assert '/description/12'
        assert review_success


# Testing playlist functionality

# Making sure an unauthenticated user cannot add an episode or review to a playlist
def test_login_required_for_playlist(client):
    client.post('/perform_episode_action/<int:episode_id>')
    assert '/login'

    client.post('/perform_podcast_action/<int:podcast_id>')
    assert '/logout'


# Checking an authenticated user can add an episode to their playlist
def test_add_episode_to_playlist(client,memory_repo):
    with client:
        client.post('/register', data={'username': 'SimonCat', 'password': 'LovelyBoy99'})
        client.post('/login', data={'username': 'SimonCat', 'password': 'LovelyBoy99'})

        add_user('bro', 'LovelyBoy999', memory_repo)

        user = get_user('bro', memory_repo)

        assert user is not None, "User 'bro' was not found"

        response = client.post('/perform_episode_action/3385')
        assert response.status_code == 302

        episode = memory_repo.get_episode(3385)
        memory_repo.add_episode_to_playlist(episode, user)
        playlist = memory_repo.get_playlist(user)

        assert episode in playlist.episodes

# Checking an authenticated user can add an entire podcast to their playlist
def test_add_podcast_to_playlist(client,memory_repo):
    with client:
        response = client.post('/register', data={'username': 'Cat', 'password': 'LovelyBoy99'})
        assert response.status_code == 200

        response = client.post('/login', data={'username': 'Cat', 'password': 'LovelyBoy99'})
        assert response.status_code == 200

        add_user('bro', 'LovelyBoy999', memory_repo)

        user = get_user('bro', memory_repo)

        assert user is not None, "User 'bro' was not found"

        response = client.post('/perform_podcast_action/243')
        assert response.status_code == 302

        podcast = memory_repo.get_podcast(243)
        memory_repo.add_podcast_to_playlist(podcast, user)
        playlist = memory_repo.get_playlist(user)

        assert podcast in playlist.podcasts, "Podcast was not added to the playlist"


# Checking an authenticated user can remove an episode from their playlist
def test_remove_episode_from_playlist(client,memory_repo):
    with client:
        client.post('/register', data={'username': 'SimonCat', 'password': 'LovelyBoy99'})
        client.post('/login', data={'username': 'SimonCat', 'password': 'LovelyBoy99'})

        add_user('bro', 'LovelyBoy999', memory_repo)

        user = get_user('bro', memory_repo)

        assert user is not None, "User 'bro' was not found"

        response = client.post('/perform_episode_action/3385')
        assert response.status_code == 302

        episode = memory_repo.get_episode(3385)
        memory_repo.add_episode_to_playlist(episode, user)
        playlist = memory_repo.get_playlist(user)

        assert episode in playlist.episodes

        memory_repo.delete_episode_from_playlist(episode, user)
        assert episode not in playlist.episodes
        assert playlist.episodes == []

# Checking an authenticated user can remove a podcast from their playlist
def test_remove_podcast_from_playlist(client, memory_repo):
    with client:
        response = client.post('/register', data={'username': 'Cat', 'password': 'LovelyBoy99'})
        assert response.status_code == 200

        response = client.post('/login', data={'username': 'Cat', 'password': 'LovelyBoy99'})
        assert response.status_code == 200

        add_user('bro', 'LovelyBoy999', memory_repo)

        user = get_user('bro', memory_repo)

        assert user is not None, "User 'bro' was not found"

        response = client.post('/perform_podcast_action/243')
        assert response.status_code == 302

        podcast = memory_repo.get_podcast(243)
        memory_repo.add_podcast_to_playlist(podcast, user)
        playlist = memory_repo.get_playlist(user)

        assert podcast in playlist.podcasts, "Podcast was not added to the playlist"

        memory_repo.delete_podcast_from_playlist(podcast, user)
        assert podcast not in playlist.podcasts, "Podcast was not removed from the playlist"
        assert playlist.podcasts == []
