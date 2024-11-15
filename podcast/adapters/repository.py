from abc import ABC, abstractmethod
from typing import List
from podcast.domainmodel.model import Category, Author, Podcast, Episode, User, Playlist, Review

repo_instance = None

class AbstractRepository(ABC):

    @abstractmethod
    def __init__(self, db_session):
        self._db_session = db_session

    @abstractmethod
    def get_podcast(self, podcast_id: int) -> Podcast:
        pass

    @abstractmethod
    def get_authors(self) -> List[Author]:
        pass

    @abstractmethod
    def get_categories(self) -> List[Category]:
        pass

    @abstractmethod
    def get_episodes(self) -> List[Episode]:
        pass

    @abstractmethod
    def get_episode(self, episode_id: int) -> Episode:
        pass

    # @abstractmethod
    # def add_episode(self, episode: Episode):
    #     pass

    @abstractmethod
    def get_episodes_by_podcast_id(self, podcast_id: int) -> List[Episode]:
        pass

    @abstractmethod
    def search_podcasts_by_query(self, query: str) -> List[Podcast]:
        pass

    @abstractmethod
    def search_podcast_by_category_id(self, category_id: str) -> List[Podcast]:
        pass

    @abstractmethod
    def create_playlist(self, user: User):
        pass

    @abstractmethod
    def get_playlist(self, user: User):
        pass

    @abstractmethod
    def add_episode_to_playlist(self, new_episode: Episode, user: User):
        pass

    @abstractmethod
    def add_podcast_to_playlist(self, new_podcast: Podcast, user: User):
        pass

    @abstractmethod
    def delete_episode_from_playlist(self, del_episode: Episode, user: User):
        pass

    @abstractmethod
    def delete_podcast_from_playlist(self, del_podcast: Podcast, user: User):
        pass

    @abstractmethod
    def recently_added_episode_to_playlist(self, episode_id):
        pass

    @abstractmethod
    def get_recently_added_episode(self):
        pass

    @abstractmethod
    def recently_added_podcast_to_playlist(self, podcast_id):
        pass

    @abstractmethod
    def get_recently_added_podcast(self):
        pass

    @abstractmethod
    def add_review(self, review):
        pass

    @abstractmethod
    def get_all_reviews(self) -> List[Review]:
        pass

    @abstractmethod
    def get_reviews_by_podcast(self, podcast_id: int) -> List[Review]:
        pass

    @abstractmethod
    def get_user_reviews(self, username):
        pass

    @abstractmethod
    def get_average_rating(self, podcast_id: int) -> float:
        pass

    @abstractmethod
    def load_data(self, csv_reader):
        pass

    @abstractmethod
    def get_podcasts(self):
        pass
