import pytest

from podcast import create_app
from pathlib import Path

from podcast.adapters import repository_populate
from podcast.adapters.service import memory_repository
from podcast.adapters.service.memory_repository import MemoryRepository


# the csv files in the test folder are different from the csv files in the covid/adapters/data folder!
# tests are written against the csv files in tests, this data path is used to override default path for testing
TEST_DATA_PATH = Path(__file__).parent / "data"

@pytest.fixture
def in_memory_repo():
    repo = memory_repository.MemoryRepository()
    database_mode = False
    repository_populate.populate(TEST_DATA_PATH, None, repo, database_mode)
    return repo


# @pytest.fixture
# def client():
#     my_app = create_app({
#         'TESTING': True,                                # Set to True during testing.
#         'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
#         'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
#     })
#     return my_app.test_client()

#
# class AuthenticationManager:
#     def __init__(self, client):
#         self.__client = client
#
#     def login(self, user_name='thorke', password='cLQ^C#oFXloS'):
#         return self.__client.post(
#             'authentication/login',
#             data={'user_name': user_name, 'password': password}
#         )
#
#     def logout(self):
#         return self.__client.get('/auth/logout')
#
#     @pytest.fixture
#     def auth(client):
#         return AuthenticationManager(client)
