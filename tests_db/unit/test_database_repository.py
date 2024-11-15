import pytest
from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.domainmodel.model import Podcast, Episode, Category, Author, Playlist, User, Review


@pytest.fixture
def temp_author():
    return Author(7, 'MarijuanaChurch')


@pytest.fixture
def temp_podcast(temp_author):
    return Podcast(140, temp_author, 'MarijuanaChurch', 'http://is5.mzstatic.com/image/thumb/Music118/v4/75/9c/c6/759cc6f9-43ae-06b1-d264-0373ef8ced1c/source/600x600bb.jpg', 'Podcast by MarijuanaChurch', 'http://soundcloud.com/user-519367239', 1326044305, 'English')


@pytest.fixture
def temp_episode(temp_podcast):
    return Episode(3385, temp_podcast, 'Functioning Multidimensionally', 985, '2017-12-15 08:23:10+00', 'Trans-dimensional, experiential, nonreligious life in the Jesus way.', 'http://feeds.soundcloud.com/stream/369843140-user-519367239-functioning-multidimensionally.mp3')


@pytest.fixture
def temp_user():
    return User(1, "Amazing User", "superpassword")


@pytest.fixture
def temp_review(temp_podcast):
    return Review(0, 5, "good podcast", User(1, "name", "pASSword12345"), temp_podcast)


def test_get_podcasts(session_factory, temp_podcast):  # tests the SqlAlchemyRepository's get_podcasts() method
    my_repository = SqlAlchemyRepository(session_factory)
    pod_list = my_repository.get_podcasts()
    assert len(pod_list) == 7
    assert pod_list[6] == temp_podcast


def test_get_podcast(session_factory, temp_podcast):  # tests the SqlAlchemyRepository's get_podcast() method
    my_repository = SqlAlchemyRepository(session_factory)
    got_podcast = my_repository.get_podcast(140)
    assert got_podcast == temp_podcast


def test_get_episodes_by_podcast_id(session_factory, temp_episode):  # tests the SqlAlchemyRepository's get_episodes_by_podcast_id() method
    my_repository = SqlAlchemyRepository(session_factory)
    got_episodes = my_repository.get_episodes_by_podcast_id(140)
    assert got_episodes[0] == temp_episode
    assert len(got_episodes) == 2


def test_add_user(session_factory, temp_user):  # tests the SqlAlchemyRepository's add_user() method
    my_repository = SqlAlchemyRepository(session_factory)
    my_repository.add_user(temp_user)
    assert my_repository.get_user(temp_user.username) == temp_user


def test_get_all_users(session_factory, temp_user):  # tests the SqlAlchemyRepository's get_all_users() method
    my_repository = SqlAlchemyRepository(session_factory)
    my_repository.add_user(temp_user)
    new_user = User(5, "cool user", "thispassword")
    my_repository.add_user(new_user)
    all_users = my_repository.get_all_users()
    assert len(all_users) == 2
    assert all_users[0] == temp_user
    assert all_users[1] == new_user


def test_get_user(session_factory, temp_user):  # tests the SqlAlchemyRepository's get_user() method
    my_repository = SqlAlchemyRepository(session_factory)
    my_repository.add_user(temp_user)
    assert my_repository.get_user(temp_user.username) == temp_user


def test_add_review(session_factory, temp_review, temp_podcast):  # tests the SqlAlchemyRepository's add_review() method
    my_repository = SqlAlchemyRepository(session_factory)
    my_repository.add_review(temp_review)
    assert temp_podcast.reviews == [temp_review, temp_review]


def test_get_all_reviews(session_factory, temp_user, temp_podcast, temp_review):  # tests the SqlAlchemyRepository's get_all_reviews() method
    my_repository = SqlAlchemyRepository(session_factory)
    my_rev = Review(1, 5, 'wow woah', temp_user, temp_podcast)
    my_repository.add_review(my_rev)
    my_repository.add_review(temp_review)
    all_revs = my_repository.get_all_reviews()
    assert len(all_revs) == 2


def test_get_user_reviews(session_factory, temp_user, temp_podcast, temp_review):  # tests the SqlAlchemyRepository's get_user_reviews() method
    my_repository = SqlAlchemyRepository(session_factory)
    temp_user = User(1, "name", "pASSword12345")
    my_repository.add_user(temp_user)
    assert my_repository.get_user_reviews(temp_user.username) == []
    my_repository.add_review(temp_review)
    assert len(my_repository.get_user_reviews(temp_user.username)) == 1


def test_get_authors(session_factory):  # tests the SqlAlchemyRepository's get_authors() method
    my_repository = SqlAlchemyRepository(session_factory)
    authors = my_repository.get_authors()
    assert authors[0] == Author(1, 'Dueling Genre Productions')
    assert authors[4] == Author(5, 'La Crosse Media Group')
    assert len(authors) == 7


def test_get_categories(session_factory):  # tests the SqlAlchemyRepository's get_categories() method
    my_repository = SqlAlchemyRepository(session_factory)
    categories = my_repository.get_categories()
    assert categories == [Category(1, 'Tv & film'),
                          Category(2, 'Comedy'),
                          Category(3, 'Education'),
                          Category(4, 'Music'),
                          Category(5, 'Christianity'),
                          Category(6, 'Religion & spirituality')
                          ]


def test_get_episodes(session_factory, temp_episode):  # tests the SqlAlchemyRepository's get_episodes() method
    my_repository = SqlAlchemyRepository(session_factory)
    all_episodes = my_repository.get_episodes()
    assert len(all_episodes) == 11
    assert all_episodes[0] == temp_episode


def test_get_episode(session_factory, temp_episode):  # tests the SqlAlchemyRepository's get_episode() method
    my_repository = SqlAlchemyRepository(session_factory)
    got_episode = my_repository.get_episode(3385)
    assert got_episode == temp_episode


def test_add_episode(session_factory, temp_episode, temp_podcast):  # tests the SqlAlchemyRepository's add_episode() method
    my_repository = SqlAlchemyRepository(session_factory)
    new_ep = Episode(9999, temp_podcast, 'new_ep', 5, '2017-12-15 08:23:10+00', 'description', 'http://feeds.soundcloud.com/stream/369843140-user-519367239-functioning-multidimensionally.mp3')
    my_repository.add_episode(new_ep)
    all_episodes = my_repository.get_episodes()
    assert all_episodes[11] == new_ep


def test_search_podcast_by_title(session_factory, temp_podcast):  # tests the SqlAlchemyRepository's search_podcast_by_title() method
    my_repository = SqlAlchemyRepository(session_factory)
    title = temp_podcast.title
    assert my_repository.search_podcast_by_title(title) == [temp_podcast]


def test_search_podcast_by_author(session_factory, temp_podcast):  # tests the SqlAlchemyRepository's search_podcasts_by_author() method
    my_repository = SqlAlchemyRepository(session_factory)
    pod_list = my_repository.search_podcast_by_author('uanaChur')
    assert pod_list == [temp_podcast]
    pod_list = my_repository.search_podcast_by_author('100')
    assert pod_list == []


def test_search_podcast_by_author_id(session_factory, temp_podcast):  # tests the SqlAlchemyRepository's search_podcasts_by_author() method
    my_repository = SqlAlchemyRepository(session_factory)
    pod_list = my_repository.search_podcast_by_author_id('7')
    assert pod_list == [temp_podcast]
    pod_list = my_repository.search_podcast_by_author_id('100')
    assert pod_list == []


def test_search_podcast_by_category(session_factory, temp_podcast):  # tests the SqlAlchemyRepository's search_podcasts_by_category() method
    my_repository = SqlAlchemyRepository(session_factory)
    podcasts_in_category = my_repository.search_podcast_by_category('on & Spiritu')
    assert podcasts_in_category == [Podcast(718, Author(5, 'Maplewood Nazarene'), "Maplewood Nazarene's Podcast", 'http://is5.mzstatic.com/image/thumb/Music128/v4/fe/e2/7f/fee27f7d-2f9d-1597-2d64-53b14108c4c6/source/600x600bb.jpg', 'Sermons from Maplewood Nazarene in Springfield, Ohio', 'http://joedcase64243.podomatic.com', 1249890254, 'English'), temp_podcast]
    podcasts_in_category = my_repository.search_podcast_by_category('100')
    assert podcasts_in_category == []


def test_search_podcast_by_category_id(session_factory, temp_podcast):  # tests the SqlAlchemyRepository's search_podcasts_by_category_id() method
    my_repository = SqlAlchemyRepository(session_factory)
    podcasts_in_category = my_repository.search_podcast_by_category_id('6')
    assert podcasts_in_category == [Podcast(718, Author(5, 'Maplewood Nazarene'), "Maplewood Nazarene's Podcast", 'http://is5.mzstatic.com/image/thumb/Music128/v4/fe/e2/7f/fee27f7d-2f9d-1597-2d64-53b14108c4c6/source/600x600bb.jpg', 'Sermons from Maplewood Nazarene in Springfield, Ohio', 'http://joedcase64243.podomatic.com', 1249890254, 'English'), temp_podcast]
    podcasts_in_category = my_repository.search_podcast_by_category_id('100')
    assert podcasts_in_category == []


def test_search_podcasts_by_query(session_factory, temp_podcast):  # tests the SqlAlchemyRepository's search_podcasts_by_query() method
    my_repository = SqlAlchemyRepository(session_factory)
    assert my_repository.search_podcasts_by_query('MarijuanaChurch') == [temp_podcast]
    assert my_repository.search_podcasts_by_query('uanaC') == [temp_podcast]
    assert my_repository.search_podcasts_by_query('eling Ge') == [Podcast(748, Author(1, 'Dueling Genre Productions'), "Lord of the Rings Minute", 'http://is4.mzstatic.com/image/thumb/Music62/v4/1a/a1/ea/1aa1eaf2-9366-0817-c4be-41f37d5f6eb7/source/600x600bb.jpg', 'The daily podcast in which hosts Cassandra and Norman analyze the Lord of the Rings (Extended Edition) trilogy one minute at a time.', 'http://www.duelinggenre.com/category/podcasts/movies-by-minute/lotr-minute/', 1155980634, 'English')]
    assert my_repository.search_podcasts_by_query('Religion & Spirituality')[1] == temp_podcast
    assert my_repository.search_podcasts_by_query('ligion & S')[1] == temp_podcast
    assert my_repository.search_podcasts_by_query('Dueling Genre Productions') == [Podcast(748, Author(1, 'Dueling Genre Productions'), "Lord of the Rings Minute", 'http://is4.mzstatic.com/image/thumb/Music62/v4/1a/a1/ea/1aa1eaf2-9366-0817-c4be-41f37d5f6eb7/source/600x600bb.jpg', 'The daily podcast in which hosts Cassandra and Norman analyze the Lord of the Rings (Extended Edition) trilogy one minute at a time.', 'http://www.duelinggenre.com/category/podcasts/movies-by-minute/lotr-minute/', 1155980634, 'English')]


def search_podcast_by_language():  # empty method, placeholder test for possible future implementation
    pass


def test_create_playlist(session_factory, temp_user):  # tests the SqlAlchemyRepository's create_playlist() method
    my_repository = SqlAlchemyRepository(session_factory)
    my_repository.create_playlist(temp_user)
    assert my_repository.get_all_playlists() == [Playlist(1, temp_user, temp_user.username + "'s Playlist", "Save episodes and whole playlists to watch later!", [], [])]
    my_repository.create_playlist(temp_user)
    assert my_repository.get_all_playlists() == [Playlist(1, temp_user, temp_user.username + "'s Playlist", "Save episodes and whole playlists to watch later!", [], [])]


def test_get_all_playlists(session_factory, temp_user):  # tests the SqlAlchemyRepository's get_all_playlists() method
    my_repository = SqlAlchemyRepository(session_factory)
    my_repository.create_playlist(temp_user)
    assert my_repository.get_all_playlists() == [Playlist(1, temp_user, temp_user.username + "'s Playlist", "Save episodes and whole playlists to watch later!", [], [])]
    new_user = User(90, 'helloooo', 'passworD1234')
    my_repository.create_playlist(new_user)
    assert my_repository.get_all_playlists() == [Playlist(1, temp_user, temp_user.username + "'s Playlist", "Save episodes and whole playlists to watch later!", [], []), Playlist(2, new_user, new_user.username + "'s Playlist", "Save episodes and whole playlists to watch later!", [], [])]


def test_get_playlist(session_factory, temp_user):  # tests the SqlAlchemyRepository's get_playlist() method
    my_repository = SqlAlchemyRepository(session_factory)
    my_repository.create_playlist(temp_user)
    assert my_repository.get_playlist(temp_user) == Playlist(1, temp_user, temp_user.username + "'s Playlist", "Save episodes and whole playlists to watch later!", [], [])


def test_add_episode_to_playlist(session_factory, temp_episode, temp_podcast, temp_user):  # tests the SqlAlchemyRepository's add_episode_to_playlist() method
    my_repository = SqlAlchemyRepository(session_factory)
    with pytest.raises(ValueError) as exc_info:
        my_repository.add_episode_to_playlist(temp_episode, temp_user)
    assert str(exc_info.value) == "User does not have playlist."
    my_repository.create_playlist(temp_user)
    assert len(my_repository.get_all_playlists()) == 1
    with pytest.raises(TypeError) as exc_info:
        my_repository.add_episode_to_playlist(temp_podcast, temp_user)
    assert str(exc_info.value) == "Episode must be a Episode object."


def test_add_podcast_to_playlist(session_factory, temp_episode, temp_podcast, temp_user):  # tests the SqlAlchemyRepository's add_episode_to_playlist() method
    my_repository = SqlAlchemyRepository(session_factory)
    with pytest.raises(ValueError) as exc_info:
        my_repository.add_podcast_to_playlist(temp_podcast, temp_user)
    assert str(exc_info.value) == "User does not have playlist."
    my_repository.create_playlist(temp_user)
    assert len(my_repository.get_all_playlists()) == 1
    with pytest.raises(TypeError) as exc_info:
        my_repository.add_podcast_to_playlist(temp_episode, temp_user)
    assert str(exc_info.value) == "Podcast must be a Podcast object."


def test_delete_episode_from_playlist(session_factory, temp_episode, temp_podcast, temp_user):  # tests the SqlAlchemyRepository's delete_episode_from_playlist() method
    my_repository = SqlAlchemyRepository(session_factory)
    my_repository.create_playlist(temp_user)
    with pytest.raises(ValueError) as exc_info:
        my_repository.delete_episode_from_playlist(temp_episode, temp_user)
    assert str(exc_info.value) == "Episode not in Playlist."
    with pytest.raises(TypeError) as exc_info:
        my_repository.delete_episode_from_playlist(temp_podcast, temp_user)
    assert str(exc_info.value) == "Episode must be a Episode object."


def test_delete_podcast_from_playlist(session_factory, temp_episode, temp_podcast, temp_user):  # tests the SqlAlchemyRepository's delete_podcast_from_playlist() method
    my_repository = SqlAlchemyRepository(session_factory)
    my_repository.create_playlist(temp_user)
    with pytest.raises(ValueError) as exc_info:
        my_repository.delete_podcast_from_playlist(temp_podcast, temp_user)
    assert str(exc_info.value) == "Podcast not in Playlist."
    with pytest.raises(TypeError) as exc_info:
        my_repository.delete_podcast_from_playlist(temp_episode, temp_user)
    assert str(exc_info.value) == "Podcast must be a Podcast object."


def test_recently_added_episode_to_playlist(session_factory):  # tests the SqlAlchemyRepository's recently_added_episode_to_playlist() method
    my_repository = SqlAlchemyRepository(session_factory)
    assert my_repository.recently_added_episode == -1
    my_repository.recently_added_episode_to_playlist(3385)
    assert my_repository.recently_added_episode == 3385
    my_repository.recently_added_episode_to_playlist(3386)
    assert my_repository.recently_added_episode == 3386


def test_get_recently_added_episode(session_factory):  # tests the SqlAlchemyRepository's get_recently_added_episode() method
    my_repository = SqlAlchemyRepository(session_factory)
    assert my_repository.get_recently_added_episode() == -1
    my_repository.recently_added_episode_to_playlist(3385)
    assert my_repository.get_recently_added_episode() == 3385


def test_recently_added_podcast_to_playlist(session_factory):  # tests the SqlAlchemyRepository's recently_added_podcast_to_playlist() method
    my_repository = SqlAlchemyRepository(session_factory)
    assert my_repository.recently_added_podcast == -1
    my_repository.recently_added_podcast_to_playlist(3385)
    assert my_repository.recently_added_podcast == 3385
    my_repository.recently_added_podcast_to_playlist(3386)
    assert my_repository.recently_added_podcast == 3386


def test_get_recently_added_podcast(session_factory):  # tests the SqlAlchemyRepository's get_recently_added_podcast() method
    my_repository = SqlAlchemyRepository(session_factory)
    assert my_repository.get_recently_added_podcast() == -1
    my_repository.recently_added_podcast_to_playlist(140)
    assert my_repository.get_recently_added_podcast() == 140


def test_get_reviews_by_podcast(session_factory, temp_podcast, temp_review):  # tests the SqlAlchemyRepository's get_reviews_by_podcast() method
    my_repository = SqlAlchemyRepository(session_factory)
    assert my_repository.get_reviews_by_podcast(temp_podcast.id) == []
    my_repository.add_review(temp_review)
    assert len(my_repository.get_reviews_by_podcast(temp_podcast.id)) == 1
    assert my_repository.get_reviews_by_podcast(718) == []


def test_get_average_rating(session_factory, temp_podcast, temp_review, temp_user):  # tests the SqlAlchemyRepository's get_average_rating() method
    my_repository = SqlAlchemyRepository(session_factory)
    assert my_repository.get_average_rating(temp_podcast.id) == 'No ratings yet!'
    my_repository.add_review(temp_review)
    assert my_repository.get_average_rating(temp_podcast.id) == '5.0'
    new_review = Review(1, 4, "alright", temp_user, temp_podcast)
    new_review2 = Review(2, 8, "fantastic", temp_user, temp_podcast)
    my_repository.add_review(new_review)
    my_repository.add_review(new_review2)
    assert my_repository.get_average_rating(temp_podcast.id) == '5.7'

