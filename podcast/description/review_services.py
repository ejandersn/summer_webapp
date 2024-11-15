from typing import List, Iterable

from flask import redirect, url_for

from podcast.authentication.authentication import login_required
from podcast.domainmodel.model import Review


class NonExistentPodcastException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(podcast_id: int, username: str, comment_text: str, rating: int, repository):

    podcast = repository.get_podcast(podcast_id)
    if podcast is None:
        raise NonExistentPodcastException

    review_author = repository.get_user(username)

    if review_author is None:
        raise UnknownUserException

    rev_id = len(repository.get_all_reviews())

    review = Review(rev_id, rating, comment_text, review_author, podcast)

    repository.add_review(review)
