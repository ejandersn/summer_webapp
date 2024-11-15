# contains get and add user etc
from flask import current_app
from podcast.domainmodel.model import User
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(username, password, repository):
    if repository.get_user(username) is not None:
        raise NameNotUniqueException()

    user_id = None
    user = User(user_id, username, generate_password_hash(password))
    repository.add_user(user)
    repository.create_playlist(user)
    repository.recently_added_podcast_to_playlist(-1)
    repository.recently_added_episode_to_playlist(-1)


def get_user(username, repository):
    user = repository.get_user(username)
    if user is None:
        raise UnknownUserException()
    return user


def authenticate_user(username: str, password: str, repository):
    authenticated = False

    user = repository.get_user(username)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException
