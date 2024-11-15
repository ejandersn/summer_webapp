import pytest
from podcast.adapters.datareader.csvdatareader import CSVDataReader

# CSVDataReader Tests


def test_csv_data_reader_initialization():  # checks if CSVDataReader() will initialise
    reader = CSVDataReader('podcast/adapters/data/podcasts-mini.csv', 'podcast/adapters/data/episodes-mini.csv')
    assert isinstance(reader, CSVDataReader)
    assert reader.podcasts_file == 'podcast/adapters/data/podcasts-mini.csv'
    assert reader.episodes_file == 'podcast/adapters/data/episodes-mini.csv'


def test_get_podcasts():  # checks if a sample podcast from the podcasts-mini.csv can be created
    reader = CSVDataReader('podcast/adapters/data/podcasts-mini.csv', 'podcast/adapters/data/episodes-mini.csv')
    podcasts = reader.get_podcasts()

    assert len(podcasts) == 7
    assert podcasts[0]["id"] == '748'
    assert podcasts[0]["title"] == "Lord of the Rings Minute"
    assert podcasts[0]["image"] == "http://is4.mzstatic.com/image/thumb/Music62/v4/1a/a1/ea/1aa1eaf2-9366-0817-c4be-41f37d5f6eb7/source/600x600bb.jpg"
    assert podcasts[0]["description"].startswith("The daily podcast in which hosts Cassandra and Norman analyze")
    assert podcasts[0]["language"] == "English"
    assert podcasts[0]['categories'] == "TV & Film"
    assert podcasts[0]["website"] == 'http://www.duelinggenre.com/category/podcasts/movies-by-minute/lotr-minute/'
    assert podcasts[0]['author'] == "Dueling Genre Productions"
    assert podcasts[0]['itunes_id'] == '1155980634'


def test_get_episodes():  # tests CSVDataReader's get_episodes() method
    reader = CSVDataReader('podcast/adapters/data/podcasts-mini.csv', 'podcast/adapters/data/episodes-mini.csv')
    episodes = reader.get_episodes()

    assert len(episodes) == 11
    assert episodes[0]['id'] == '3385'
    assert episodes[0]['podcast_id'] == '140'
    assert episodes[0]['title'] == 'Functioning Multidimensionally'
    assert episodes[0]['audio'] == 'http://feeds.soundcloud.com/stream/369843140-user-519367239-functioning-multidimensionally.mp3'
    assert episodes[0]['audio_length'] == '985'
    assert episodes[0]['description'] == 'Trans-dimensional, experiential, nonreligious life in the Jesus way.'
    assert episodes[0]['pub_date'] == '2017-12-15 08:23:10+00'
