import pytest
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist, Chart
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")

@pytest.fixture
def my_podcast_2(my_author):
    return Podcast(101, my_author, "Another podcast")

@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


@pytest.fixture
def my_episode(my_podcast):
    return Episode(1, my_podcast, "episode 1", 34.5, "4/09/34", "description", "link")


@pytest.fixture
def my_episode_2(my_podcast):
    return Episode(2, my_podcast, "episode 2", 34.5, "4/09/34", "description", "link")


@pytest.fixture
def my_review(my_podcast, my_user):
    return Review(1, 5, "comment", my_user, my_podcast)


@pytest.fixture
def my_playlist_empty(my_user, my_episode):
    return Playlist(1, my_user, "my_playlist", "some description", [], [])


@pytest.fixture
def my_playlist_nonempty_1(my_user, my_episode, my_podcast):
    return Playlist(2, my_user, "my_playlist", "some description", [my_episode], [my_podcast])


@pytest.fixture
def my_playlist_nonempty_2(my_user, my_episode_2, my_podcast_2):
    return Playlist(3, my_user, "my_playlist", "some description", [my_episode_2], [my_podcast_2])


def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""
    assert podcast1.reviews == []

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, "Todd Clayton")

    podcast4 = Podcast(123, " ")
    assert podcast4.title is 'Untitled'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_add_review(my_podcast, my_user):  # tests add_review() method of Podcast class
    assert my_podcast.reviews == []
    new_review = Review(3, 3, "comment", my_user, my_podcast)
    # my_podcast.add_review(new_review)
    print(my_podcast.reviews[0])
    if len(my_podcast.reviews) > 1:
        assert [my_podcast.reviews[0]] == [new_review]
    else:
        assert my_podcast.reviews == [new_review]
    with pytest.raises(TypeError) as exc:
        my_podcast.add_review("I'm a string not a Review object")
    assert str(exc.value) == "Expected a Review instance."


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert repr(user1) == "<User 1: shyamli>"
    assert repr(user2) == "<User 2: asma>"
    assert repr(user3) == "<User 3: jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user1, user2, user3]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 < user3
    assert user3 > user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_user_add_review(my_user, my_review, my_podcast):  # tests the add_review() method of User class
    if len(my_user.reviews) > 0:
        assert [my_user.reviews[0]] == [my_review]
    new_review = Review(7, 5, "comment", my_user, my_podcast)
    if len(my_user.reviews) > 0:
        assert [my_user.reviews[0]] == [my_review]
    else:
        assert my_user.reviews == [my_review, new_review]
    with pytest.raises(TypeError) as exc_info:
        my_user.add_review("definitely a review and not a string in disguise")
    assert str(exc_info.value) == "Expected a Review instance."


def test_user_add_playlist(my_user):  # tests the add_playlist() method of User class
    assert my_user.playlists == []
    new_playlist = Playlist(0, my_user, "title", "description", [], [])
    my_user.add_playlist(new_playlist)
    assert my_user.playlists == [new_playlist]
    with pytest.raises(TypeError) as exc_info:
        my_user.add_playlist("not a Playlist lmao you've been pranked")
    assert str(exc_info.value) == "Expected a Playlist instance."


def test_user_remove_playlist(my_user):  # tests the remove_playlist() method of User class
    new_playlist = Playlist(0, my_user, "title", "description", [], [])
    my_user.add_playlist(new_playlist)
    assert my_user.playlists == [new_playlist]
    my_user.remove_playlist(new_playlist)
    assert my_user.playlists == []


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "<User 1: shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"

    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User(2, "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1

# TODO : Write Unit Tests for CSVDataReader, Episode, Review, Playlist classes


# Episode Unit Tests:
def test_episode_initialization(my_podcast):  # Tests if an episode can be initialized
    episode1 = Episode(1, my_podcast, "episode 1", 34.5,"4/09/34", "description", "link")
    episode2 = Episode(2, my_podcast, "episode 2", 29.1,"14/09/34", "description2", "link")
    episode3 = Episode(3, my_podcast, "episode 3", 44.9,"30/09/34", "description3", "link")
    assert episode1.id == 1
    assert episode2.id == 2
    assert episode3.id == 3
    assert episode1.podcast == my_podcast
    assert episode2.podcast == my_podcast
    assert episode3.podcast == my_podcast
    assert episode1.title == "episode 1"
    assert episode2.title == "episode 2"
    assert episode3.title == "episode 3"
    assert repr(episode1) == '<Episode 1: episode 1>'


def test_episode_title_setter(my_episode):  # Tests the episode title setter
    my_episode.title = "title"
    assert my_episode.title == "title"
    with pytest.raises(TypeError) as exc_info:
        my_episode.title = 123
    assert str(exc_info.value) == "Title must be a string."


def test_episode_description_setter(my_episode):  # Tests the episode description setter
    my_episode.description = "description"
    assert my_episode.description == "description"
    with pytest.raises(TypeError) as exc_info:
        my_episode.description = 123
    assert str(exc_info.value) == "Description must be a string."


def test_episode_hash(my_episode, my_episode_2, my_podcast):  # tests the episode hash
    episode_same = Episode(1, my_podcast, "episode 1", 34.5, "4/09/34", "description", "link")
    assert hash(my_episode) == hash(episode_same)
    assert hash(my_episode) != hash(my_episode_2)


def test_episode_repr(my_episode):  # tests the episode repr
    assert repr(my_episode) == "<Episode 1: episode 1>"


def test_episode_lt(my_episode, my_episode_2):  # tests the episode lt
    assert my_episode < my_episode_2
    assert not my_episode_2 < my_episode
    assert not my_episode < my_episode


def test_episode_eq(my_episode, my_episode_2, my_podcast):  # tests episode "equal to"
    assert my_episode != my_episode_2
    assert my_episode == my_episode
    new_episode = Episode(1, my_podcast, "episode 2", 34.5, "4/09/34", "description", "link")
    assert my_episode != new_episode


# Review Unit Tests

def test_review_initialization(my_podcast, my_user):  # Tests if a review can be initialized
    review1 = Review(1,5,"comment",my_user,my_podcast)
    review2 = Review(2,5," 3",my_user,my_podcast)
    review3 = Review(3,5,"coment",my_user,my_podcast)
    assert review1.id == 1
    assert review2.id == 2
    assert review3.id == 3
    assert review1.podcast == my_podcast
    assert review2.podcast == my_podcast
    assert review3.podcast == my_podcast
    assert review1.comment == "comment"
    assert review2.comment == " 3"
    assert review3.comment == "coment"
    assert review1.user == my_user
    # with pytest.raises(ValueError):
    #     Review(2,-5,"    ",my_user,my_podcast)
    with pytest.raises(ValueError):
        Review(-2, 5, " w3   ", my_user, my_podcast)
    assert repr(review1) == "<Review 1: Written by shyamli>"
    assert repr(review2) == "<Review 2: Written by shyamli>"
    assert repr(review3) == "<Review 3: Written by shyamli>"


def test_review_hash_setter(my_review, my_user, my_podcast):  # Tests the review hash
    review_same = Review(1, 5, "comment", my_user, my_podcast)
    review_different = Review(2, 4, "different comment", my_user, my_podcast)
    assert hash(my_review) == hash(review_same)
    assert hash(my_review) != hash(review_different)


def test_review_repr(my_review):  # tests review repr
    assert repr(my_review) == "<Review 1: Written by shyamli>"


def test_review_lt(my_review, my_user, my_podcast):  # tests review "less than"
    new_review = Review(2, 5, "comment", my_user, my_podcast)
    assert my_review < new_review


def test_review_eq(my_review, my_user, my_podcast):  # tests review "equal to"
    assert my_review == my_review
    new_review = Review(2, 5, "comment", my_user, my_podcast)
    assert my_review != new_review

def test_playlist_initialization(my_user, my_episode, my_episode_2, my_podcast, my_podcast_2):  # Tests if a playlist can be initialized
    playlist1 = Playlist(1, my_user, "title", "description", [], [])
    playlist2 = Playlist(2, my_user, "TITLE", "DESCRIPTION", [my_episode], [my_podcast])
    playlist3 = Playlist(3, my_user, " title " + "3", "this is a \n description", [my_episode, my_episode_2], [my_podcast, my_podcast_2])
    assert playlist1.id == 1
    assert playlist2.id == 2
    assert playlist3.id == 3
    assert playlist1.user == my_user
    assert playlist2.user == my_user
    assert playlist3.user == my_user
    assert playlist1.title == "title"
    assert playlist2.title == "TITLE"
    assert playlist3.title == " title 3"
    assert playlist1.description == "description"
    assert playlist2.description == "DESCRIPTION"
    assert playlist3.description == "this is a \n description"
    assert playlist1.episodes == []
    assert playlist2.episodes == [my_episode]
    assert playlist3.episodes == [my_episode, my_episode_2]
    assert playlist1.podcasts == []
    assert playlist2.podcasts == [my_podcast]
    assert playlist3.podcasts == [my_podcast, my_podcast_2]
    assert repr(playlist1) == "<Playlist 1: title, creator: shyamli>"


def test_playlist_title_setter(my_playlist_empty):  # Tests the playlist title setter
    my_playlist_empty.title = "title"
    assert my_playlist_empty.title == "title"
    with pytest.raises(TypeError) as exc_info:
        my_playlist_empty.title = 123
    assert str(exc_info.value) == "Title must be a string."


def test_playlist_description_setter(my_playlist_empty):  # Tests the playlist description setter
    my_playlist_empty.description = "description"
    assert my_playlist_empty.description == "description"
    with pytest.raises(TypeError) as exc_info:
        my_playlist_empty.description = 123
    assert str(exc_info.value) == "Description must be a string."


def test_playlist_add_episode(my_playlist_empty, my_episode):  # Tests the playlist add_episode method
    my_playlist_empty.add_episode(my_episode)
    assert my_playlist_empty.episodes[0] == my_episode
    with pytest.raises(TypeError) as exc_info:
        my_playlist_empty.add_episode("this is a string not an episode")
    assert str(exc_info.value) == "Episode must be a Episode object."


def test_playlist_add_podcast(my_playlist_empty, my_podcast):  # Tests the playlist add_podcast method
    my_playlist_empty.add_podcast(my_podcast)
    assert my_playlist_empty.podcasts[0] == my_podcast
    with pytest.raises(TypeError) as exc_info:
        my_playlist_empty.add_podcast("this is a string not a podcast")
    assert str(exc_info.value) == "Podcast must be a Podcast object."


def test_playlist_merge_playlist(my_playlist_nonempty_1, my_playlist_nonempty_2):  # Tests the playlist merge_playlist method
    goal_list_ep = my_playlist_nonempty_1.episodes + my_playlist_nonempty_2.episodes
    goal_list_pod = my_playlist_nonempty_1.podcasts + my_playlist_nonempty_2.podcasts
    my_playlist_nonempty_1.merge_playlist(my_playlist_nonempty_2)
    assert my_playlist_nonempty_1.episodes == goal_list_ep
    assert my_playlist_nonempty_1.podcasts == goal_list_pod
    with pytest.raises(TypeError) as exc_info:
        my_playlist_nonempty_2.merge_playlist("not a account")
    assert str(exc_info.value) == "Playlist must be a Playlist object."


def test_playlist_delete_episode(my_playlist_nonempty_1, my_episode):  # Tests the playlist delete_episode method
    my_playlist_nonempty_1.delete_episode(my_episode)
    assert len(my_playlist_nonempty_1.episodes) == 0
    with pytest.raises(ValueError) as exc_info:
        my_playlist_nonempty_1.delete_episode(my_episode)
    assert str(exc_info.value) == "Episode not in Playlist."
    with pytest.raises(TypeError) as exc_info:
        my_playlist_nonempty_1.delete_episode("this is a string")
    assert str(exc_info.value) == "Episode must be a Episode object."


def test_playlist_delete_podcast(my_playlist_nonempty_1, my_podcast):  # Tests the playlist delete_episode method
    my_playlist_nonempty_1.delete_podcast(my_podcast)
    assert len(my_playlist_nonempty_1.podcasts) == 0
    with pytest.raises(ValueError) as exc_info:
        my_playlist_nonempty_1.delete_podcast(my_podcast)
    assert str(exc_info.value) == "Podcast not in Playlist."
    with pytest.raises(TypeError) as exc_info:
        my_playlist_nonempty_1.delete_podcast("this is a string")
    assert str(exc_info.value) == "Podcast must be a Podcast object."


def test_playlist_reassign_user(my_playlist_empty, my_user):  # Tests the playlist reassign_user method
    assert my_playlist_empty.user == my_user
    new_user = User(1, "user", "Abcd1234")
    my_playlist_empty.reassign_user(new_user)
    assert my_playlist_empty.user == new_user


def test_playlist_hash(my_playlist_empty, my_playlist_nonempty_1, my_user):  # Tests the playlist hash
    playlist_same = Playlist(1, my_user, "my_playlist", "some description", [], [])
    assert hash(my_playlist_empty) == hash(playlist_same)
    assert hash(my_playlist_empty) != hash(my_playlist_nonempty_1)


def test_playlist_repr(my_playlist_empty, my_playlist_nonempty_1):  # Tests the playlist repr
    assert repr(my_playlist_empty) == "<Playlist 1: my_playlist, creator: shyamli>"
    assert repr(my_playlist_nonempty_1) == "<Playlist 2: my_playlist, creator: shyamli>"


def test_playlist_lt(my_playlist_empty, my_playlist_nonempty_2):  # Tests the playlist "less than"
    assert my_playlist_empty < my_playlist_nonempty_2
    assert not my_playlist_nonempty_2 < my_playlist_empty


def test_playlist_eq(my_playlist_empty, my_playlist_nonempty_2):  # Tests the playlist "equal to"
    assert my_playlist_empty == my_playlist_empty
    assert my_playlist_nonempty_2 == my_playlist_nonempty_2
    assert my_playlist_empty != my_playlist_nonempty_2


# Chart unit tests

def test_chart_initialization():  # Tests if a chart can be initialised
    reader = CSVDataReader('podcast/adapters/data/podcasts-mini.csv', 'podcast/adapters/data/episodes-mini.csv')
    podcasts = reader.get_podcasts()
    chart1 = Chart(1,"Chart 1",podcasts)
    chart2 = Chart(2,"Chart 2",podcasts)
    assert chart1.id == 1
    assert chart2.id == 2
    assert chart1.title == "Chart 1"
    assert chart2.title == "Chart 2"
    assert chart1.podcasts == podcasts
    assert chart2.podcasts == podcasts


def test_chart_repr():  # tests the chart repr
    reader = CSVDataReader('podcast/adapters/data/podcasts-mini.csv', 'podcast/adapters/data/episodes-mini.csv')
    podcasts = reader.get_podcasts()
    chart = Chart(1, "Chart 1", podcasts)
    assert repr(chart) == "<Chart 1: Chart 1. Contains 7 podcasts.>"


def test_chart_hash():  # tests the chart hash
    reader = CSVDataReader('podcast/adapters/data/podcasts-mini.csv', 'podcast/adapters/data/episodes-mini.csv')
    podcasts = reader.get_podcasts()
    chart1 = Chart(1, "Chart 1", podcasts)
    chart2 = Chart(2, "Chart 2", podcasts)
    assert hash(chart1) == hash(chart1)
    assert hash(chart1) != hash(chart2)


def test_chart_lt(my_podcast):  # tests the Chart "less than"
    reader = CSVDataReader('podcast/adapters/data/podcasts-mini.csv', 'podcast/adapters/data/episodes-mini.csv')
    podcasts = reader.get_podcasts()
    chart1 = Chart(1, "Chart 1", podcasts)
    chart2 = Chart(2, "Chart 2", podcasts)
    assert chart1 < chart2
    assert not chart2 < chart1


def test_chart_eq():  # tests the Chart "equal to"
    reader = CSVDataReader('podcast/adapters/data/podcasts-mini.csv', 'podcast/adapters/data/episodes-mini.csv')
    podcasts = reader.get_podcasts()
    chart1 = Chart(1, "Chart 1", podcasts)
    chart2 = Chart(1, "Chart 1", podcasts)
    chart3 = Chart(3, "Chart 1", podcasts)
    chart4 = Chart(1, "Chart 4", podcasts)
    assert chart1 == chart1
    assert chart1 == chart2
    assert chart1 != chart3
    assert chart1 != chart4


def test_chart_podcasts_setter(my_podcast, my_episode):  # tests the podcast setter for the Chart class
    reader = CSVDataReader('podcast/adapters/data/podcasts-mini.csv', 'podcast/adapters/data/episodes-mini.csv')
    podcasts = reader.get_podcasts()
    chart1 = Chart(1, "Chart 1", podcasts)
    assert chart1.podcasts == podcasts
    new_podcasts = [my_podcast]
    chart1.podcasts = new_podcasts
    assert chart1.podcasts == new_podcasts
    with pytest.raises(TypeError) as exc_info:
        chart1.podcasts = [my_podcast, my_episode]
    assert str(exc_info.value) == "Podcasts item must be a Podcast object."
    assert chart1.podcasts == new_podcasts
