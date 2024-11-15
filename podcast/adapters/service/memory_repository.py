from abc import ABC

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Category, Author, Podcast, Episode, Playlist, User, Review


class MemoryRepository(AbstractRepository, ABC):
    def __init__(self):
        self.csv_reader = None
        self.podcasts = []
        self.episodes = []
        self.users = list()
        self.reviews = list()
        self.authors = {}
        self.categories = {}
        self.all_playlists = []
        self.recently_added_episode = -1
        self.recently_added_podcast = -1

    def load_data(self, csv_reader):
        self.csv_reader = csv_reader
        self.load_categories()
        self.load_authors()
        self.load_podcasts()
        self.load_episodes()

    def load_podcasts(self):
        podcasts_data = self.csv_reader.get_podcasts()
        self.podcasts = [self._create_podcast(row) for row in podcasts_data]

    def load_episodes(self):
        episodes_data = self.csv_reader.get_episodes()
        self.episodes = [self._create_episode(row) for row in episodes_data]
        self._assign_episodes_to_podcasts()

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

    def _create_podcast(self, data):
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
            category = self._create_category(name)
            podcast.add_category(category)

        return podcast

    def _create_episode(self, data):
        episode = Episode(
            episode_id=int(data.get('id', 0)),
            podcast=self._get_podcast(int(data.get('podcast_id', 0))),
            title=data.get('title', "Unknown"),
            audio_length=int(data.get('audio_length', 0)),
            publication_date=data.get('pub_date', 'Unknown'),
            description=data.get('description', 'Unknown'),
            audio_link=data.get('audio_link', 'Unknown')
        )
        return episode

    def _create_category(self, category_name):
        normalized_name = category_name.strip().lower()
        if normalized_name not in self.categories:
            category_id = len(self.categories) + 1
            category = Category(
                category_id=category_id,
                name=normalized_name.capitalize()
            )
            self.categories[normalized_name] = category
        return self.categories[normalized_name]

    def _add_category_to_podcast(self, data):
        category_names = data.get('categories', "").split('|')
        categories = []
        for name in category_names:
            category = self._create_category(name)
            categories.append(category)
        return categories

    def _get_podcast(self, podcast_id):
        for podcast in self.podcasts:
            if podcast.id == int(podcast_id):
                return podcast
        return None

    def _get_episode(self, episode_id):
        for episode in self.episodes:
            if episode.id == int(episode_id):
                return episode
        return None

    def get_podcast(self, podcast_id):
        return self._get_podcast(podcast_id)

    def get_podcasts(self):
        return self.podcasts

    def get_categories(self):
        return sorted(self.categories.values(), key=lambda c: c.name)

    def search_podcast_by_category_id(self, category_id):
        category = next((c for c in self.categories.values() if c.id == int(category_id)), None)
        if category is None:
            return []
        podcasts_in_category = [podcast for podcast in self.podcasts if category in podcast.categories]
        return podcasts_in_category

    def get_authors(self):
        return list(self.authors.values())


    def search_podcast_by_author_id(self, author_id):
        return [podcast for podcast in self.podcasts if podcast.author.id == int(author_id)]


    def _assign_episodes_to_podcasts(self):
        for episode in self.episodes:
            podcast = episode.podcast
            if podcast:
                podcast.episodes.append(episode)

    def search_podcasts_by_query(self, query):
        matching_podcasts = []

        for podcast in self.podcasts:
            if query.lower() in podcast.title.lower() or \
                    query.lower() in podcast.author.name.lower() or \
                    any(query.lower() in category.name.lower() for category in podcast.categories):
                matching_podcasts.append(podcast)

        return matching_podcasts

    def add_user(self, user: User):
        user.id = len(self.users)
        self.users.append(user)

    def _get_user(self, username):
        for user in self.users:
            if user.username.lower() == username.lower():
                return user
        return None

    def get_user(self, username):
        return self._get_user(username)

    def get_all_users(self):
        return self.users

    def get_user_reviews(self, username):
        reviewlist = []
        user = self._get_user(username)
        for review in self.reviews:
            if review.user.username.lower() == username.lower():
                reviewlist.append(review)
        return reviewlist

    def add_review(self, review: Review):
        self.reviews.append(review)

    def _get_review(self, rev_id):
        for review in self.reviews:
            if review.id == rev_id:
                return review
        return None

    def get_review(self, rev_id):
        return self._get_review(rev_id)

    def get_all_reviews(self):
        return self.reviews

    def get_reviews_by_podcast(self, podcast_id):
        review_list = []
        for review in self.reviews:
            if self.get_podcast(podcast_id) == review.podcast:
                review_list.append(review)
        return review_list

    def create_playlist(self, user: User):
        user_found = False
        for playlist in self.all_playlists:
            if playlist.user == user:
                user_found = True
        if not user_found:
            new_playlist = Playlist(len(self.all_playlists), user, user.username + "'s Playlist",
                                    "Save episodes and whole playlists to watch later!", [], [])
            self.all_playlists.append(new_playlist)
            user.add_playlist(new_playlist)

    def get_playlist(self, user: User):
        for playlist in self.all_playlists:
            if playlist.user == user:
                return playlist
        raise ValueError("User does not have playlist.")

    def add_episode_to_playlist(self, new_episode: Episode, user: User):
        playlist = self.get_playlist(user)
        playlist.add_episode(new_episode)

    def add_podcast_to_playlist(self, new_podcast: Podcast, user: User):
        playlist = self.get_playlist(user)
        playlist.add_podcast(new_podcast)

    def delete_episode_from_playlist(self, del_episode: Episode, user: User):
        playlist = self.get_playlist(user)
        playlist.delete_episode(del_episode)

    def delete_podcast_from_playlist(self, del_podcast: Podcast, user: User):
        playlist = self.get_playlist(user)
        playlist.delete_podcast(del_podcast)

    def get_episode(self, episode_id):
        return self._get_episode(episode_id)

    def recently_added_episode_to_playlist(self, episode_id):
        self.recently_added_episode = episode_id

    def get_recently_added_episode(self):
        return self.recently_added_episode

    def recently_added_podcast_to_playlist(self, podcast_id):
        self.recently_added_podcast = podcast_id

    def get_recently_added_podcast(self):
        return self.recently_added_podcast

    def get_average_rating(self, podcast_id: int):
        review_list = self.get_reviews_by_podcast(podcast_id)
        if len(review_list) == 0:
            return 'No ratings yet!'
        total_sum = 0
        for review in review_list:
            total_sum += review.rating
        return '{0:.1f}'.format(total_sum / len(review_list))


    def add_episode(self, episode: Episode):
        pass


    def get_episodes(self) -> list[Episode]:
        pass

    def get_episodes_by_podcast_id(self, podcast_id: int) -> list[Episode]:
        podcast = self.get_podcast(podcast_id)
        return podcast.episodes