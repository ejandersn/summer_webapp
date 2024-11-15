from sqlalchemy import select, inspect
from podcast.adapters.orm import mapper_registry


def test_database_populate_inspect_table_names(database_engine):  # tests if the tables have been created and the names are as expected
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == [
        'authors', 'categories', 'episodes', 'playlist_episodes',
        'playlist_podcasts', 'playlists', 'podcast_categories',
        'podcasts', 'reviews', 'users'
    ]


def test_database_populate_select_all_tags(database_engine):  # tests if the column names are as expected
    inspector = inspect(database_engine)
    tables = inspector.get_table_names()
    name_of_tags_table = 'authors'

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_tags_table])
        result = connection.execute(select_statement)

        actual_column_names = result.keys()

        expected_column_names = ['author_id', 'name']
        assert list(actual_column_names) == expected_column_names


def test_database_populate_select_all_authors(database_engine):  # tests if authors populate properly
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_authors_table])
        result = connection.execute(select_statement)

        all_authors = {}
        for row in result.mappings():
            all_authors[row['author_id']] = row['name']

        assert len(all_authors) > 0
        assert all_authors.get(1) is not None


def test_database_populate_select_all_podcasts(database_engine):  # tests if podcasts populate properly
    inspector = inspect(database_engine)
    name_of_podcasts_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_podcasts_table])
        result = connection.execute(select_statement)

        all_podcasts = {}
        for row in result.mappings():
            all_podcasts[row['podcast_id']] = row['title']

        assert len(all_podcasts) > 0
        assert all_podcasts[140] is not None


def test_database_populate_select_all_categories(database_engine):  # tests if authors categories properly
    inspector = inspect(database_engine)
    name_of_categories_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_categories_table])
        result = connection.execute(select_statement)

        all_categories = {}
        for row in result.mappings():
            all_categories[row['category_id']] = row['category_name']

        assert len(all_categories) > 0
        assert all_categories[3] is not None


def test_database_populate_select_all_episodes(database_engine):  # tests if episodes populate properly
    inspector = inspect(database_engine)
    name_of_episodes_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_episodes_table])
        result = connection.execute(select_statement)

        all_episodes = {}
        for row in result.mappings():
            all_episodes[row['episode_id']] = row['title']
        print(all_episodes)
        assert len(all_episodes) > 0
        assert all_episodes[4509] is not None


def test_database_populate_select_all_podcast_categories(database_engine):  # tests if podcast categories (assoc table) populate properly
    inspector = inspect(database_engine)
    name_of_podcast_categories_table = inspector.get_table_names()[6]
    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_podcast_categories_table])
        result = connection.execute(select_statement)

        all_podcast_categories = {}
        for row in result.mappings():
            all_podcast_categories[row['podcast_id']] = row['category_id']

        print(all_podcast_categories)

        assert len(all_podcast_categories) > 0
        assert all_podcast_categories[140] is not None

