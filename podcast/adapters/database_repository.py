from abc import ABC
from typing import List
from sqlalchemy.orm import scoped_session, joinedload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import select

from podcast.adapters.orm import podcast_table, authors_table, categories_table, podcast_categories_table
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Author, Category, Episode, Playlist, User, Review


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        print("Committing session.")
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)
        self.csv_reader = None
        self.podcasts = []
        self.episodes = {}
        self.authors = {}
        self.categories = {}
        self.categories_list = []

        self.recently_added_episode = -1
        self.recently_added_podcast = -1

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def load_data(self, csvreader):
        self.csv_reader = csvreader
        episodes_dict = self.csv_reader.get_episodes()
        self.load_categories()
        with self._session_cm as scm:
            scm.session.add_all(self.categories_list)
            scm.commit()
        categories = self.get_categories()
        self.load_authors()
        self.load_podcasts(categories)
        for podcast in self.podcasts:
            self.hydrate_podcast(episodes_dict, podcast)
        with self._session_cm as scm:
            scm.session.add_all(self.podcasts)
            scm.commit()

    def hydrate_podcast(self, episodes_dict, podcast):
        for item in episodes_dict:
            if int(item["podcast_id"]) == podcast.id:
                episode = self._create_episode(item, podcast)
                podcast.episodes.append(episode)

    def load_podcasts(self, categories):
        podcasts_data = self.csv_reader.get_podcasts()
        for row in podcasts_data:
            podcast = self._create_podcast(row, categories)
            self.podcasts.append(podcast)

    def load_categories(self):
        podcasts_data = self.csv_reader.get_podcasts()
        unique_categories = {}
        for row in podcasts_data:
            category_names = row.get('categories', "").split('|')
            for name in category_names:
                normalized_name = name.strip().lower()
                if normalized_name not in unique_categories:
                    unique_categories[normalized_name] = Category(
                        category_id=len(unique_categories) + 1,
                        name=normalized_name.capitalize()
                    )
                    self.categories_list.append(unique_categories[normalized_name])
        self.categories = unique_categories

    def load_authors(self):
        podcasts_data = self.csv_reader.get_podcasts()
        unique_authors = {}
        for row in podcasts_data:
            author_name = row.get('author', "").strip()
            if author_name and author_name not in unique_authors:
                author_id = len(unique_authors) + 1
                unique_authors[author_name] = Author(
                    author_id=author_id,
                    name=author_name
                )
        self.authors = unique_authors

    def _create_podcast(self, data, categories):
        author_name = data.get('author', "").strip()
        author = self.authors.get(author_name)

        if not author:
            author = Author(author_id=len(self.authors) + 1, name=author_name)
            self.authors[author_name] = author

        podcast = Podcast(
            podcast_id=int(data.get('id', 0)),
            title=data.get('title', "Untitled"),
            image=data.get('image', None),
            author=author,
            description=data.get('description', ""),
            language=data.get('language', "Unspecified"),
            website=data.get('website', ""),
            itunes_id=data.get('itunes_id', None)
        )

        author.add_podcast(podcast)

        category_names = data.get('categories', "").split('|')
        for name in category_names:
            name = name.strip()
            for category in categories:
                if name.lower() == category.name.lower():
                    podcast.add_category(category)

        return podcast

    def _create_episode(self, data, podcast=None):
        episode = Episode(
            episode_id=int(data.get('id', 0)),
            podcast=podcast,
            title=data.get('title', "Unknown"),
            audio_length=int(data.get('audio_length', 0)),
            publication_date=data.get('pub_date', 'Unknown'),
            description=data.get('description', 'Unknown'),
            audio_link=data.get('audio', 'Unknown')
        )
        return episode

    def get_podcasts(self, sorting: bool = False) -> List[Podcast]:
        podcasts = self._session_cm.session.query(Podcast).all()
        sorted_podcasts = sorted(podcasts, key=lambda podcast: podcast.title)
        return sorted_podcasts

    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            query = self._session_cm.session.query(Podcast).filter(
                Podcast._id == podcast_id)
            podcast = query.one()
        except NoResultFound:
            print(f'Podcast {podcast_id} was not found')

        return podcast


    def get_episodes_by_podcast_id(self, podcast_id: int) -> List[Episode]:
        with self._session_cm as scm:
            query = scm.session.query(Episode).filter(Episode.podcast_id == podcast_id).all()
            return query

    def add_user(self, user):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_all_users(self, sorting: bool = False) -> list[type[User]]:
        users = self._session_cm.session.query(User).all()
        return users

    def get_user(self, username: str) -> User:
        user = None
        try:
            query = self._session_cm.session.query(User).filter(
                User._username == username.lower())
            user = query.one()
        except NoResultFound:
            print(f'User {username} was not found')

        return user

    def add_review(self, review):
        with self._session_cm as scm:
            scm.session.merge(review)
            scm.commit()

    def get_all_reviews(self, sorting: bool = False) -> list[type[Review]]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def get_user_reviews(self, username):
        reviewlist = []
        all_reviews = self.get_all_reviews()
        for review in all_reviews:
            if review.user.username.lower() == username.lower():
                reviewlist.append(review)
        return reviewlist


    def get_authors(self) -> List[Author]:
        authors = self._session_cm.session.query(Author).all()
        return authors

    def get_categories(self) -> list[type[Category]]:
        categories = self._session_cm.session.query(Category).all()
        return categories

    def get_episodes(self, sorting: bool = False) -> list[type[Episode]]:
        episodes = self._session_cm.session.query(Episode).all()
        return episodes

    def get_episode(self, episode_id: int) -> Episode:
        episode = None
        try:
            query = self._session_cm.session.query(Episode).filter(
                Episode._id == episode_id)
            episode = query.one()
        except NoResultFound:
            print(f'Podcast {episode_id} was not found')

        return episode

    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.merge(episode)
            scm.commit()

    def search_podcast_by_title(self, title_string: str) -> List[Podcast]:
        title_string = title_string.strip().lower()
        stmt = select(podcast_table).where(podcast_table.c.title.ilike(f"%{title_string}%"))
        result = self._session_cm.session.execute(stmt).scalars().all()
        filtered = []
        for id in result:
            podcast = self.get_podcast(id)
            if podcast is not None:
                filtered.append(podcast)
        return filtered if filtered else []

    def search_podcast_by_author(self, author_name: str) -> List[Podcast]:
        filtered = []
        author_name = author_name.strip().lower()
        stmt = select(authors_table).where(authors_table.c.name.ilike(f"%{author_name}%"))
        author_ids = self._session_cm.session.execute(stmt).scalars().all()
        for author_id in author_ids:
            stmt = select(podcast_table).where(podcast_table.c.author_id == author_id)
            results = self._session_cm.session.execute(stmt).scalars().all()
            for podcast_id in results:
                podcast = self.get_podcast(podcast_id)
                if podcast is not None:
                    filtered.append(podcast)

        return filtered if filtered else []

    def search_podcast_by_author_id(self, author_id: str) -> List[Podcast]:
        filtered = []
        author_id = author_id.strip().lower()
        stmt = select(podcast_table).where(podcast_table.c.author_id == author_id)
        podcast_ids = self._session_cm.session.execute(stmt).scalars().all()
        for podcast_id in podcast_ids:
            podcast = self.get_podcast(podcast_id)
            if podcast is not None:
                filtered.append(podcast)
        return filtered if filtered else []

    def search_podcast_by_category(self, category_string: str) -> List[Podcast]:
        category_string = category_string.strip().lower()
        stmt = select(categories_table).where(categories_table.c.category_name.ilike(f"%{category_string}%"))
        results = self._session_cm.session.execute(stmt).scalars().all()
        filtered = []
        for category_id in results:
            stmt = select(podcast_categories_table.c.podcast_id).where(podcast_categories_table.c.category_id == category_id)
            results = self._session_cm.session.execute(stmt).scalars().all()
            for podcast_id in results:
                podcast = self.get_podcast(podcast_id)
                if podcast is not None:
                    filtered.append(podcast)

        return filtered

    def search_podcast_by_category_id(self, category_id: str) -> List[Podcast]:
        category_id = category_id.strip().lower()
        filtered = []
        stmt = select(podcast_categories_table.c.podcast_id).where(podcast_categories_table.c.category_id == category_id)
        results = self._session_cm.session.execute(stmt).scalars().all()
        for podcast_id in results:
            podcast = self.get_podcast(podcast_id)
            if podcast is not None:
                filtered.append(podcast)

        return filtered

    def search_podcasts_by_query(self, query: str) -> List[Podcast]:
        filtered = []
        titles = self.search_podcast_by_title(query)
        for podcast in titles:
            filtered.append(podcast)
        authors = self.search_podcast_by_author(query)
        for podcast in authors:
            if podcast not in filtered:
                filtered.append(podcast)
        authors = self.search_podcast_by_category(query)
        for podcast in authors:
            if podcast not in filtered:
                filtered.append(podcast)
        return filtered

    def search_podcast_by_language(self, language_string: str) -> List[Podcast]:
        pass

    def create_playlist(self, user: User):
        user_found = False
        all_playlists = self.get_all_playlists()
        for playlist in all_playlists:
            if playlist.user == user:
                user_found = True
        if not user_found:
            new_playlist = Playlist(None, user, user.username + "'s Playlist",
                                    "Save episodes and whole playlists to watch later!", [], [])
            with self._session_cm as scm:
                scm.session.merge(new_playlist)
                scm.commit()

    def get_all_playlists(self) -> List[Playlist]:
        all_playlists = self._session_cm.session.query(Playlist).all()
        return all_playlists

    def get_playlist(self, user: User):
        all_playlists = self.get_all_playlists()
        for playlist in all_playlists:
            if playlist.user == user:
                return playlist
        raise ValueError("User does not have playlist.")

    def add_episode_to_playlist(self, new_episode: Episode, user: User):
        playlist = self.get_playlist(user)
        playlist.add_episode(new_episode)
        with self._session_cm as scm:
            scm.session.merge(playlist)
            scm.commit()

    def add_podcast_to_playlist(self, new_podcast: Podcast, user: User):
        playlist = self.get_playlist(user)
        playlist.add_podcast(new_podcast)
        with self._session_cm as scm:
            scm.session.merge(playlist)
            scm.commit()

    def delete_episode_from_playlist(self, del_episode: Episode, user: User):
        playlist = self.get_playlist(user)
        playlist.delete_episode(del_episode)
        with self._session_cm as scm:
            scm.session.merge(playlist)
            scm.commit()

    def delete_podcast_from_playlist(self, del_podcast: Podcast, user: User):
        playlist = self.get_playlist(user)
        playlist.delete_podcast(del_podcast)
        with self._session_cm as scm:
            scm.session.merge(playlist)
            scm.commit()

    def recently_added_episode_to_playlist(self, episode_id):
        self.recently_added_episode = episode_id

    def get_recently_added_episode(self):
        return self.recently_added_episode

    def recently_added_podcast_to_playlist(self, podcast_id):
        self.recently_added_podcast = podcast_id

    def get_recently_added_podcast(self):
        return self.recently_added_podcast

    def get_reviews_by_podcast(self, podcast_id: int):
        podcast = self.get_podcast(podcast_id)
        return podcast.reviews

    def get_average_rating(self, podcast_id: int):
        review_list = self.get_reviews_by_podcast(podcast_id)
        if len(review_list) == 0:
            return 'No ratings yet!'
        total_sum = 0
        for review in review_list:
            total_sum += review.rating
        return '{0:.1f}'.format(total_sum / len(review_list))