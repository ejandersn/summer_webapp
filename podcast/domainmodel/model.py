from __future__ import annotations


def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("ID must be a non-negative integer.")


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


class Author:
    def __init__(self, author_id: int, name: str):
        validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return f"<Author {self._id}: {self._name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.id)


class Podcast:
    def __init__(self, podcast_id: int, author: Author, title: str = "Untitled", image: str = None,
                 description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
        validate_non_negative_int(podcast_id)
        self._id = podcast_id
        self._author = author
        validate_non_empty_string(title, "Podcast title")
        self._title = title.strip()
        self._image = image
        self._description = description
        self._language = language
        self._website = website
        self._itunes_id = itunes_id
        self.categories = []
        self.episodes = []
        self.__reviews = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def author(self) -> Author:
        return self._author

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    @property
    def reviews(self) -> list:
        return self.__reviews

    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category: Category):
        if category in self.categories:
            self.categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self.episodes:
            self.episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self.episodes:
            self.episodes.remove(episode)

    def add_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance.")
        self.__reviews.append(review)

    def __repr__(self):
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.title < other.title

    def __hash__(self):
        return hash(self.id)


class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def __repr__(self) -> str:
        return f"<Category {self._id}: {self._name}>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._name < other.name

    def __hash__(self):
        return hash(self._id)


class User:
    def __init__(self, user_id: (int, None), username: str, password: str):
        # validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._id = user_id
        self._username = username.lower().strip()
        self._password = password
        self._subscription_list = []
        self.__reviews = []
        self._playlists = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def subscription_list(self):
        return self._subscription_list

    @property
    def reviews(self):
        return self.__reviews

    @property
    def playlists(self):
        return self._playlists

    @id.setter
    def id(self, new_id: int):
        if not isinstance(new_id, int):
            raise TypeError("Expected an integer ID.")
        self._id = new_id

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    def add_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance.")
        self.__reviews.append(review)

    # def remove_review(self, review: Review):
    #     if review in self.reviews:
    #         self.__reviews.remove(review)

    def add_playlist(self, playlist: Playlist):
        if not isinstance(playlist, Playlist):
            raise TypeError("Expected a Playlist instance.")
        if playlist not in self.playlists:
            self._playlists.append(playlist)

    def remove_playlist(self, playlist: Playlist):
        if playlist in self.playlists:
            self._playlists.remove(playlist)

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))


class Episode:
    def __init__(self, episode_id: int, podcast: Podcast, title: str, audio_length: int, publication_date: str,
                 description: str, audio_link: str):
        self._id = episode_id
        self._podcast = podcast
        self._title = title
        self._audio_length = audio_length
        self._publication_date = publication_date[0:10]
        self._description = description
        self._audio_link = audio_link

    def __repr__(self):
        return f"<Episode {self.id}: {self.title}>"
        # return f"<{self.podcast.title}: Episode {self.id}: {self.title}>"

    def __hash__(self):
        return hash((self.id, self.title))

    def __eq__(self, other):
        if not isinstance(other, Episode):
            return False
        return self.id == other.id and self.title == other.title

    def __lt__(self, other):
        if not isinstance(other, Episode):
            return False
        return self.id < other.id

    @property
    def id(self):
        return self._id

    @property
    def podcast(self):
        return self._podcast

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title: str):
        if not isinstance(new_title, str):
            raise TypeError("Title must be a string.")
        self._title = new_title

    @property
    def audio_length(self):
        return self._audio_length

    @property
    def publication_date(self):
        return self._publication_date

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        if not isinstance(new_description, str):
            raise TypeError("Description must be a string.")
        self._description = new_description

    @property
    def audio_link(self):
        return self._audio_link


class Review:
    def __init__(self, rev_id: int, rating: int, comment: str, user: User, podcast: Podcast):
        validate_non_negative_int(rev_id)
        try:
            validate_non_empty_string(comment)
        except ValueError:
            comment = 'No comment.'
        try:
            validate_non_negative_int(rating)
        except ValueError:
            rating = abs(rating)
            rating = int(-1 * rating // 1 * -1)
            if rating == 0:
                rating = 1
        if not isinstance(user, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self.__id = rev_id
        self.__user = user
        self.__podcast = podcast
        self.__rating = rating
        self.__comment = comment
        podcast.add_review(self)
        user.add_review(self)

    def __repr__(self):
        return f"<Review {self.id}: Written by {self.user.username}>"

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self.id == other.id and self.user == other.user and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, Review):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.user, self.podcast))

    @property
    def id(self) -> int:
        return self.__id

    @property
    def user(self):
        return self.__user

    @property
    def podcast(self):
        return self.__podcast

    @property
    def rating(self):
        return self.__rating

    @property
    def comment(self):
        return self.__comment

    def delete_review(self):
        self.podcast.reviews.remove(self)
        self.user.reviews.remove(self)


class Playlist:
    def __init__(self, playlist_id: int, user: User, title: str, description: str, episodes: list[Episode], podcasts: list[Podcast]):
        self._id = playlist_id
        self._user = user
        self._title = title
        self._description = description
        self._episodes = episodes
        self._podcasts = podcasts
        # self._recently_added_episode = -1
        # self._recently_added_podcast = -1

    def __repr__(self):
        return f"<Playlist {self._id}: {self._title}, creator: {self._user.username}>"

    def __hash__(self):
        return hash((self._id, self.user, self.title, self.description))

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.id == other.id and self.user == other.user and self.title == other.title

    def __lt__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.id < other.id

    @property
    def id(self):
        return self._id

    @property
    def user(self):
        return self._user

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def episodes(self):
        return self._episodes

    @property
    def podcasts(self):
        return self._podcasts

    # @property
    # def recently_added_episode(self):
    #     return self._recently_added_episode
    #
    # @property
    # def recently_added_podcast(self):
    #     return self._recently_added_podcast

    @title.setter
    def title(self, new_title: str):
        if not isinstance(new_title, str):
            raise TypeError("Title must be a string.")
        self._title = new_title

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            raise TypeError("Description must be a string.")
        self._description = new_description

    def add_episode(self, new_episode: Episode):
        if not isinstance(new_episode, Episode):
            raise TypeError("Episode must be a Episode object.")
        self._episodes.append(new_episode)

    def add_podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcasts.append(new_podcast)

    def merge_playlist(self, other_playlist: Playlist):
        if not isinstance(other_playlist, Playlist):
            raise TypeError("Playlist must be a Playlist object.")
        self.episodes.extend(other_playlist.episodes)
        self.podcasts.extend(other_playlist.podcasts)

    def delete_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Episode must be a Episode object.")
        try:
            self.episodes.remove(episode)
        except ValueError:
            raise ValueError("Episode not in Playlist.")

    def delete_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        try:
            self.podcasts.remove(podcast)
        except ValueError:
            raise ValueError("Podcast not in Playlist.")

    def reassign_user(self, new_user: User):
        if not isinstance(new_user, User):
            raise TypeError("User must be a User object.")
        self._user = new_user


class Chart:
    def __init__(self, chart_id: int, title: str, podcasts: list[Podcast]):
        self._id = chart_id
        self._title = title
        self._podcasts = podcasts

    def __repr__(self):
        return f"<Chart {self.id}: {self.title}. Contains {len(self.podcasts)} podcasts.>"

    def __eq__(self, other):
        if not isinstance(other, Chart):
            return False
        return self.id == other.id and self.title == other.title and self.podcasts == other.podcasts

    def __lt__(self, other):
        if not isinstance(other, Chart):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.title))

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def podcasts(self):
        return self._podcasts

    @podcasts.setter
    def podcasts(self, new_podcasts):
        new_list = []
        for podcast in new_podcasts:
            if not isinstance(podcast, Podcast):
                raise TypeError("Podcasts item must be a Podcast object.")
            else:
                new_list.append(podcast)
        self._podcasts = new_list