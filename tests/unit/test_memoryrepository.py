import pytest
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
def temp_episode(temp_podcast):
    return Episode(3385, temp_podcast, 'Functioning Multidimensionally', 985, '2017-12-15 08:23:10+00', 'Trans-dimensional, experiential, nonreligious life in the Jesus way.', 'http://feeds.soundcloud.com/stream/369843140-user-519367239-functioning-multidimensionally.mp3')

@pytest.fixture
def temp_user():
    return User(1, "Amazing User", "superpassword")


@pytest.fixture
def temp_review(temp_podcast):
    return Review(0, 5, "good podcast", User(1, "name", "pASSword12345"), temp_podcast)


def test_initialisation(csv_reader):  # Tests __init__, note: some __init__ functions tested below are omitted here
    repository = MemoryRepository()
    assert isinstance(repository, MemoryRepository)
    assert repository.users == []
    assert repository.reviews == []
    assert repository.all_playlists == []
    assert repository.recently_added_episode == -1
    assert repository.recently_added_podcast == -1


def test_load_data():  # Placeholder test for the MemoryRepository's load_data()
    pass  # test_load_podcasts(), test_load_episodes(), test_load_categories(), test_load_authors() working implies that this also works


def test_load_podcasts(my_repository, csv_reader):  # tests the MemoryRepository's load_podcasts() method
    my_repository.load_data(csv_reader)
    assert len(my_repository.podcasts) == 7
    assert isinstance(my_repository.podcasts[0], Podcast)
    assert repr(my_repository.podcasts[0]) == "<Podcast 748: 'Lord of the Rings Minute' by Dueling Genre Productions>"


def test_load_episodes(my_repository, csv_reader):  # tests the MemoryRepository's load_episodes() method
    my_repository.load_data(csv_reader)
    assert len(my_repository.episodes) == 11
    assert isinstance(my_repository.episodes[0], Episode)
    assert repr(my_repository.episodes[0]) == "<Episode 3385: Functioning Multidimensionally>"


def test_load_categories(my_repository, csv_reader):  # tests the MemoryRepository's load_categories() method
    my_repository.load_data(csv_reader)
    assert my_repository.categories == {'tv & film': Category(1, 'Tv & film'),
                                        'comedy': Category(2, 'Comedy'),
                                        'education': Category(3, 'Education'),
                                        'music': Category(4, 'Music'),
                                        'christianity': Category(5, 'Christianity'),
                                        'religion & spirituality': Category(6, 'Religion & Spirituality'),
                                        }


def test_load_authors(my_repository, csv_reader):  # tests the MemoryRepository's load_authors() method
    my_repository.load_data(csv_reader)
    assert my_repository.authors == {'Dueling Genre Productions': Author(1, 'Dueling Genre Productions'),
                                     'Lost at Home Podcast Network': Author(2, 'Lost at Home Podcast Network'),
                                     'LSU Communication across the Curriculum and LSU College of Science': Author(3, 'LSU Communication across the Curriculum and LSU College of Science'),
                                     'Crit The Bed': Author(4, 'Crit The Bed'),
                                     'La Crosse Media Group': Author(5, 'La Crosse Media Group'),
                                     'Maplewood Nazarene': Author(6, 'Maplewood Nazarene'),
                                     'MarijuanaChurch': Author(7, 'MarijuanaChurch')
                                     }


def test_create_podcast(my_repository, csv_reader, temp_podcast):  # tests the MemoryRepository's create_podcast() method
    my_repository.load_data(csv_reader)
    podcasts_data = csv_reader.get_podcasts()
    created_podcast = my_repository._create_podcast(podcasts_data[6])
    assert created_podcast == temp_podcast


def test_create_episode(my_repository, csv_reader, temp_podcast, temp_episode):  # tests the MemoryRepository's create_episode() method
    my_repository.load_data(csv_reader)
    episodes_data = my_repository.csv_reader.get_episodes()
    created_episode = my_repository._create_episode(episodes_data[0])
    assert created_episode == temp_episode


def test_create_category(my_repository, csv_reader):  # tests the MemoryRepository's create_category() method
    my_repository.load_data(csv_reader)
    goal_category = Category(3, 'Education')
    created_category = my_repository._create_category('Education')
    assert created_category == goal_category


def test_add_category_to_podcast(my_repository, csv_reader):  # tests the MemoryRepository's add_category_to_podcast() method
    my_repository.load_data(csv_reader)
    podcast_data = my_repository.csv_reader.get_podcasts()
    categories = my_repository._add_category_to_podcast(podcast_data[4])
    assert categories == [Category(4, 'Music'), Category(1, 'Tv & film'), Category(2, 'Comedy')]


def test_get_podcast(my_repository, csv_reader, temp_podcast):  # tests the MemoryRepository's get_podcast() method
    my_repository.load_data(csv_reader)
    got_podcast = my_repository.get_podcast(140)
    assert got_podcast == temp_podcast


def test_get_episode(my_repository, csv_reader, temp_episode):  # tests the MemoryRepository's get_episode() method
    my_repository.load_data(csv_reader)
    got_episode = my_repository.get_episode(3385)
    assert got_episode == temp_episode


def test_get_podcasts(my_repository, csv_reader, temp_podcast):  # tests the MemoryRepository's get_podcasts() method
    my_repository.load_data(csv_reader)
    all_podcasts = my_repository.get_podcasts()
    assert all_podcasts[6] == temp_podcast
    assert len(all_podcasts) == 7


def test_get_categories(my_repository, csv_reader):  # tests the MemoryRepository's get_categories() method
    my_repository.load_data(csv_reader)
    categories = my_repository.get_categories()
    assert categories == [Category(5, 'Christianity'),
                          Category(2, 'Comedy'),
                          Category(3, 'Education'),
                          Category(4, 'Music'),
                          Category(6, 'Religion & spirituality'),
                          Category(1, 'Tv & film')
                          ]


def test_search_podcast_by_category_id(my_repository, csv_reader, temp_podcast):  # tests the MemoryRepository's get_podcast_by_category() method
    my_repository.load_data(csv_reader)
    podcasts_in_category = my_repository.search_podcast_by_category_id('6')
    assert podcasts_in_category == [Podcast(718, Author(5, 'Maplewood Nazarene'), "Maplewood Nazarene's Podcast", 'http://is5.mzstatic.com/image/thumb/Music128/v4/fe/e2/7f/fee27f7d-2f9d-1597-2d64-53b14108c4c6/source/600x600bb.jpg', 'Sermons from Maplewood Nazarene in Springfield, Ohio', 'http://joedcase64243.podomatic.com', 1249890254, 'English'), temp_podcast]
    podcasts_in_category = my_repository.search_podcast_by_category_id('100')
    assert podcasts_in_category == []


def test_get_authors(my_repository, csv_reader):  # tests the MemoryRepository's get_authors() method
    my_repository.load_data(csv_reader)
    authors = my_repository.get_authors()
    assert authors[0] == Author(1, 'Dueling Genre Productions')
    assert authors[4] == Author(5, 'La Crosse Media Group')
    assert len(authors) == 7


# def test_get_author(my_repository, temp_author):
#     assert temp_author == my_repository.get_author(7)


def test_search_podcast_by_author_id(my_repository, csv_reader, temp_podcast):  # tests the MemoryRepository's get_podcasts_by_author() method
    my_repository.load_data(csv_reader)
    pod_list = my_repository.search_podcast_by_author_id(7)
    assert pod_list == [temp_podcast]
    pod_list = my_repository.search_podcast_by_author_id(100)
    assert pod_list == []


# def test_get_podcasts_by_category_and_author(my_repository, csv_reader, temp_podcast):  # tests the MemoryRepository's get_podcasts_by_category_and_author() method
#     my_repository.load_data(csv_reader)
#     pod_list = my_repository.get_podcasts_by_category_and_author(6, 7)
#     assert pod_list == [temp_podcast]
#     pod_list = my_repository.get_podcasts_by_category_and_author(5, 7)
#     assert pod_list == []
#     pod_list = my_repository.get_podcasts_by_category_and_author(100, 100)
#     assert pod_list == []


def test_assign_episodes_to_podcasts(my_repository, csv_reader, temp_podcast, temp_episode):  # tests the MemoryRepository's assign_episodes_to_podcasts() method
    my_repository.load_data(csv_reader)
    assert my_repository.podcasts[6].episodes[0] == temp_episode


def test_search_podcasts_by_query(my_repository, csv_reader, temp_podcast):  # tests the MemoryRepository's search_podcasts_by_query() method
    my_repository.load_data(csv_reader)
    assert my_repository.search_podcasts_by_query('MarijuanaChurch') == [temp_podcast]
    assert my_repository.search_podcasts_by_query('uanaC') == [temp_podcast]
    assert my_repository.search_podcasts_by_query('Religion & Spirituality')[1] == temp_podcast
    assert my_repository.search_podcasts_by_query('ligion & S')[1] == temp_podcast
    assert my_repository.search_podcasts_by_query('Dueling Genre Productions') == [Podcast(748, Author(1, 'Dueling Genre Productions'), "Lord of the Rings Minute", 'http://is4.mzstatic.com/image/thumb/Music62/v4/1a/a1/ea/1aa1eaf2-9366-0817-c4be-41f37d5f6eb7/source/600x600bb.jpg', 'The daily podcast in which hosts Cassandra and Norman analyze the Lord of the Rings (Extended Edition) trilogy one minute at a time.', 'http://www.duelinggenre.com/category/podcasts/movies-by-minute/lotr-minute/', 1155980634, 'English')]
    assert my_repository.search_podcasts_by_query('eling Ge') == [Podcast(748, Author(1, 'Dueling Genre Productions'), "Lord of the Rings Minute", 'http://is4.mzstatic.com/image/thumb/Music62/v4/1a/a1/ea/1aa1eaf2-9366-0817-c4be-41f37d5f6eb7/source/600x600bb.jpg', 'The daily podcast in which hosts Cassandra and Norman analyze the Lord of the Rings (Extended Edition) trilogy one minute at a time.', 'http://www.duelinggenre.com/category/podcasts/movies-by-minute/lotr-minute/', 1155980634, 'English')]


def test_add_user(my_repository, csv_reader):  # tests the MemoryRepository's add_user() method
    my_repository.load_data(csv_reader)
    my_repository.add_user(User(0, "User", "password"))
    assert my_repository.users == [User(0, "User", "password")]
    my_repository.add_user(User(1, "User2", "password2"))
    assert my_repository.users == [User(0, "User", "password"), User(1, "User2", "password2")]


def test_get_user(my_repository, csv_reader):  # tests the MemoryRepository's get_user() method
    my_repository.load_data(csv_reader)
    my_repository.add_user(User(0, "User", "password"))
    my_repository.add_user(User(1, "User2", "password2"))
    assert my_repository.get_user("User") == User(0, "User", "password")
    assert my_repository.get_user("User2") == User(1, "User2", "password2")
    assert my_repository.users == [User(0, "User", "password"), User(1, "User2", "password2")]


def test_get_all_users(my_repository, csv_reader):  # tests the MemoryRepository's get_all_users() method
    my_repository.load_data(csv_reader)
    my_repository.add_user(User(0, "User", "password"))
    my_repository.add_user(User(1, "User2", "password2"))
    assert my_repository.get_all_users() == [User(0, "User", "password"), User(1, "User2", "password2")]


def test_get_user_reviews(my_repository, csv_reader, temp_podcast, temp_review):  # tests the MemoryRepository's get_user_reviews() method
    my_repository.load_data(csv_reader)
    temp_user = User(1, "name", "pASSword12345")
    my_repository.users.append(temp_user)
    assert my_repository.get_user_reviews(temp_user.username) == []
    my_repository.reviews.append(temp_review)
    assert my_repository.get_user_reviews(temp_user.username) == [temp_review]


def test_add_review(my_repository, csv_reader, temp_review):  # tests the MemoryRepository's add_review() method
    my_repository.load_data(csv_reader)
    my_repository.add_review(temp_review)
    assert my_repository.reviews == [temp_review]


def test_get_review(my_repository, csv_reader, temp_review):  # tests the MemoryRepository's get_review() method
    my_repository.load_data(csv_reader)
    my_repository.add_review(temp_review)
    assert my_repository.get_review(0) == temp_review


def test_get_all_reviews(my_repository, csv_reader, temp_review, temp_podcast):  # tests the MemoryRepository's get_all_reviews() method
    my_repository.load_data(csv_reader)
    my_repository.add_review(temp_review)
    assert my_repository.get_all_reviews() == [temp_review]
    my_repository.add_review(temp_review)
    assert my_repository.get_all_reviews() == [temp_review, temp_review]
    new_review = Review(5, 4, "ok podcast", User(2, "name2", "pASSword123456"), temp_podcast)
    my_repository.add_review(new_review)
    assert my_repository.get_all_reviews() == [temp_review, temp_review, new_review]


def test_get_reviews_by_podcast(my_repository, csv_reader, temp_podcast, temp_review):  # tests the MemoryRepository's get_reviews_by_podcast() method
    my_repository.load_data(csv_reader)
    assert my_repository.get_reviews_by_podcast(temp_podcast.id) == []
    my_repository.add_review(temp_review)
    assert my_repository.get_reviews_by_podcast(temp_podcast.id) == [temp_review]
    assert my_repository.get_reviews_by_podcast(718) == []


def test_create_playlist(my_repository, csv_reader, temp_user):  # tests the MemoryRepository's create_playlist() method
    my_repository.load_data(csv_reader)
    my_repository.create_playlist(temp_user)
    assert my_repository.all_playlists == [Playlist(0, temp_user, temp_user.username + "'s Playlist", "Save episodes and whole playlists to watch later!", [], [])]
    my_repository.create_playlist(temp_user)
    assert my_repository.all_playlists == [Playlist(0, temp_user, temp_user.username + "'s Playlist", "Save episodes and whole playlists to watch later!", [], [])]


def test_get_playlist(my_repository, csv_reader, temp_user):  # tests the MemoryRepository's get_playlist() method
    my_repository.load_data(csv_reader)
    my_repository.create_playlist(temp_user)
    assert my_repository.get_playlist(temp_user) == Playlist(0, temp_user, temp_user.username + "'s Playlist", "Save episodes and whole playlists to watch later!", [], [])


def test_add_episode_to_playlist(my_repository, csv_reader, temp_episode, temp_podcast, temp_user):  # tests the MemoryRepository's add_episode_to_playlist() method
    my_repository.load_data(csv_reader)
    with pytest.raises(ValueError) as exc_info:
        my_repository.add_episode_to_playlist(temp_episode, temp_user)
    assert str(exc_info.value) == "User does not have playlist."
    my_repository.create_playlist(temp_user)
    my_repository.add_episode_to_playlist(temp_episode, temp_user)
    assert my_repository.all_playlists[0].episodes == [temp_episode]
    with pytest.raises(TypeError) as exc_info:
        my_repository.add_episode_to_playlist(temp_podcast, temp_user)
    assert str(exc_info.value) == "Episode must be a Episode object."


def test_add_podcast_to_playlist(my_repository, csv_reader, temp_episode, temp_podcast, temp_user):  # tests the MemoryRepository's add_podcast_to_playlist() method
    my_repository.load_data(csv_reader)
    with pytest.raises(ValueError) as exc_info:
        my_repository.add_podcast_to_playlist(temp_podcast, temp_user)
    assert str(exc_info.value) == "User does not have playlist."
    my_repository.create_playlist(temp_user)
    my_repository.add_podcast_to_playlist(temp_podcast, temp_user)
    assert my_repository.all_playlists[0].podcasts == [temp_podcast]
    with pytest.raises(TypeError) as exc_info:
        my_repository.add_podcast_to_playlist(temp_episode, temp_user)
    assert str(exc_info.value) == "Podcast must be a Podcast object."


def test_delete_episode_from_playlist(my_repository, csv_reader, temp_episode, temp_podcast, temp_user):  # tests the MemoryRepository's delete_episode_from_playlist() method
    my_repository.load_data(csv_reader)
    my_repository.create_playlist(temp_user)
    my_repository.add_episode_to_playlist(temp_episode, temp_user)
    assert my_repository.all_playlists[0].episodes == [temp_episode]
    my_repository.delete_episode_from_playlist(temp_episode, temp_user)
    assert my_repository.all_playlists[0].episodes == []

    with pytest.raises(ValueError) as exc_info:
        my_repository.delete_episode_from_playlist(temp_episode, temp_user)
    assert str(exc_info.value) == "Episode not in Playlist."

    with pytest.raises(TypeError) as exc_info:
        my_repository.delete_episode_from_playlist(temp_podcast, temp_user)
    assert str(exc_info.value) == "Episode must be a Episode object."


def test_delete_podcast_from_playlist(my_repository, csv_reader, temp_episode, temp_podcast, temp_user):  # tests the MemoryRepository's delete_podcast_from_playlist() method
    my_repository.load_data(csv_reader)
    my_repository.create_playlist(temp_user)
    my_repository.add_podcast_to_playlist(temp_podcast, temp_user)
    assert my_repository.all_playlists[0].podcasts == [temp_podcast]
    my_repository.delete_podcast_from_playlist(temp_podcast, temp_user)
    assert my_repository.all_playlists[0].podcasts == []

    with pytest.raises(ValueError) as exc_info:
        my_repository.delete_podcast_from_playlist(temp_podcast, temp_user)
    assert str(exc_info.value) == "Podcast not in Playlist."

    with pytest.raises(TypeError) as exc_info:
        my_repository.delete_podcast_from_playlist(temp_episode, temp_user)
    assert str(exc_info.value) == "Podcast must be a Podcast object."


def test_recently_added_episode_to_playlist(my_repository, csv_reader):  # tests the MemoryRepository's recently_added_episode_to_playlist() method
    my_repository.load_data(csv_reader)
    assert my_repository.recently_added_episode == -1
    my_repository.recently_added_episode_to_playlist(3385)
    assert my_repository.recently_added_episode == 3385
    my_repository.recently_added_episode_to_playlist(3386)
    assert my_repository.recently_added_episode == 3386


def test_get_recently_added_episode(my_repository, csv_reader):  # tests the MemoryRepository's get_recently_added_episode() method
    my_repository.load_data(csv_reader)
    assert my_repository.get_recently_added_episode() == -1
    my_repository.recently_added_episode_to_playlist(3385)
    assert my_repository.get_recently_added_episode() == 3385


def test_recently_added_podcast_to_playlist(my_repository, csv_reader):  # tests the MemoryRepository's recently_added_podcast_to_playlist() method
    my_repository.load_data(csv_reader)
    assert my_repository.recently_added_podcast == -1
    my_repository.recently_added_podcast_to_playlist(3385)
    assert my_repository.recently_added_podcast == 3385
    my_repository.recently_added_podcast_to_playlist(3386)
    assert my_repository.recently_added_podcast == 3386


def test_get_recently_added_podcast(my_repository, csv_reader):  # tests the MemoryRepository's get_recently_added_podcast() method
    my_repository.load_data(csv_reader)
    assert my_repository.get_recently_added_podcast() == -1
    my_repository.recently_added_podcast_to_playlist(140)
    assert my_repository.get_recently_added_podcast() == 140


def test_get_average_rating(my_repository, csv_reader, temp_podcast, temp_review, temp_user):  # tests the MemoryRepository's get_average_rating() method
    my_repository.load_data(csv_reader)
    assert my_repository.get_average_rating(temp_podcast.id) == 'No ratings yet!'
    my_repository.add_review(temp_review)
    assert my_repository.get_average_rating(temp_podcast.id) == '5.0'
    new_review = Review(1, 4, "alright", temp_user, temp_podcast)
    new_review2 = Review(2, 8, "fantastic", temp_user, temp_podcast)
    my_repository.add_review(new_review)
    my_repository.add_review(new_review2)
    assert my_repository.get_average_rating(temp_podcast.id) == '5.7'
