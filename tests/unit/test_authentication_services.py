import pytest
from podcast.adapters.service.memory_repository import MemoryRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader
import podcast.authentication.authentication_services as authss
from podcast.domainmodel.model import User


@pytest.fixture
def csv_reader():
    return CSVDataReader('podcast/adapters/data/podcasts-mini.csv', 'podcast/adapters/data/episodes-mini.csv')


@pytest.fixture
def my_repository():
    return MemoryRepository()


@pytest.fixture
def temp_user():
    return User(0, "Amazing User", "superpassword")


def test_add_user(my_repository, temp_user):  # tests add_user() function from authentication_services.py
    authss.add_user("Amazing User", 'superpassword', my_repository)
    assert my_repository.get_all_users() == [temp_user]
    with pytest.raises(authss.NameNotUniqueException) as exc_info:
        authss.add_user("Amazing User", 'password1234', my_repository)
    assert str(exc_info.value) == ""


def test_get_user(my_repository, temp_user):  # tests get_user() function from authentication_services.py
    authss.add_user("Amazing User", 'superpassword', my_repository)
    assert authss.get_user("Amazing User", my_repository) == temp_user
    with pytest.raises(authss.UnknownUserException) as exc_info:
        authss.get_user("Loser User", my_repository)
    assert str(exc_info.value) == ""


def test_authenticate_user(my_repository, temp_user):  # tests authenticate_user() function from authentication_services.py
    authss.add_user("Amazing User", 'superpassword', my_repository)
    with pytest.raises(authss.AuthenticationException) as exc_info:
        authss.authenticate_user('Amazing User', 'not-the-right-password', my_repository)
    assert str(exc_info.value) == ""
    try:
        authss.authenticate_user('Amazing User', 'superpassword', my_repository)
    except authss.AuthenticationException as exc:
        assert False
