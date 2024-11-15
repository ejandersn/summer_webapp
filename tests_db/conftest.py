import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from podcast.adapters import database_repository, repository_populate
from podcast.adapters.orm import map_model_to_tables, mapper_registry
from podcast.domainmodel.model import Category

from utils import get_project_root

TEST_DATA_PATH_DATABASE_FULL = get_project_root() / "podcast" / "adapters" / "data"
TEST_DATA_PATH_DATABASE_LIMITED = get_project_root() / "tests" / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///podcasts.db'


@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    mapper_registry.metadata.create_all(engine)  

    with engine.connect() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())

    map_model_to_tables()

    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)

    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True

    with session_factory() as session:
        if session.query(Category).count() == 0:  # Only populate if empty to not duplicate then fail unique error
            repository_populate.populate(TEST_DATA_PATH_DATABASE_LIMITED, session_factory, repo_instance, database_mode)

    yield engine
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    mapper_registry.metadata.create_all(engine)
    with engine.connect() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repository_populate.populate(TEST_DATA_PATH_DATABASE_LIMITED, session_factory,repo_instance, database_mode)
    yield session_factory
    mapper_registry. metadata.drop_all(engine)

@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    mapper_registry.metadata.create_all(engine)
    with engine.connect() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    mapper_registry.metadata.drop_all(engine)
