import pytest
import podcast.description.review_services as revss
from podcast.adapters.service.memory_repository import MemoryRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.domainmodel.model import Podcast, Episode, Category, Author, Playlist, User, Review


@pytest.fixture
def csv_reader():
    return CSVDataReader('podcast/adapters/data/podcasts-mini.csv', 'podcast/adapters/data/episodes-mini.csv')


@pytest.fixture
def my_repository():
    return MemoryRepository()


@pytest.fixture
def temp_author():
    return Author(7, 'MarijuanaChurch')


@pytest.fixture
def temp_podcast(temp_author):
    return Podcast(140, temp_author, 'MarijuanaChurch', 'http://is5.mzstatic.com/image/thumb/Music118/v4/75/9c/c6/759cc6f9-43ae-06b1-d264-0373ef8ced1c/source/600x600bb.jpg', 'Podcast by MarijuanaChurch', 'http://soundcloud.com/user-519367239', 1326044305, 'English')


@pytest.fixture
def temp_user():
    return User(1, "Amazing User", "superpassword")


@pytest.fixture
def temp_review(temp_user, temp_podcast):
    return Review(0, 5, "this is a comment", temp_user, temp_podcast)


def test_add_review(my_repository, csv_reader, temp_user, temp_review):  # tests add_review() function from review_services.py
    my_repository.load_data(csv_reader)
    with pytest.raises(revss.NonExistentPodcastException) as exc_info:
        revss.add_review(-37, "username", "comment text", 5, my_repository)
    assert str(exc_info.value) == ""

    with pytest.raises(revss.UnknownUserException) as exc_info:
        revss.add_review(140, "username", "comment text", 5, my_repository)
    assert str(exc_info.value) == ""

    my_repository.users = [temp_user]
    revss.add_review(140, "Amazing User", "this is a comment", 5, my_repository)
    assert my_repository.reviews == [temp_review]
