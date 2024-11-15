import os
from _testcapi import test_config
from pathlib import Path
from flask import Flask
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from podcast.adapters import repository_populate
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.service import memory_repository
# from podcast.domainmodel.model import Podcast

# local imports
import podcast.adapters.repository as repo
from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.adapters.repository_populate import populate
from podcast.adapters.orm import mapper_registry, map_model_to_tables

def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    app.debug = False

    app.config.from_object('config.Config')
    # data_path = Path('podcast') / 'adapters' / 'data'
    data_path = Path('adapters') / 'data'

    clear_mappers()

    # if not test_config:
    #     # Load test configuration, and override any configuration settings.
    #     app.config.from_mapping(test_config)
    #     data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = memory_repository.MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        repository_populate.populate(data_path, None, repo.repo_instance, database_mode)

    if app.config['REPOSITORY'] == 'database':
        # database_uri = 'sqlite:///podcasts.db'
        database_uri = app.config['DATABASE_URI']

        database_echo = app.config['SQLALCHEMY_ECHO']

        # Create a database engine and connect it to the specified database
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool, echo=database_echo)

        # Create the database session factory using sessionmaker
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

        # Set the repository instance to the SqlAlchemyRepository
        repo.repo_instance = SqlAlchemyRepository(session_factory)
        data_path = Path('adapters') / 'data'

        if app.config['TESTING'] == 'True' or len(inspect(database_engine).get_table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing or first-time use of the web application, reinitialize the database.
            clear_mappers()
            # Conditionally create database tables.
            mapper_registry.metadata.create_all(database_engine)
            # Remove any data from the tables.
            for table in reversed(mapper_registry.metadata.sorted_tables):
                with database_engine.connect() as conn:
                    conn.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            # Populate the repository within the populate function
            populate(data_path, session_factory, repo.repo_instance, database_mode=True)  # Pass the session_factory here
            print("REPOPULATING DATABASE... FINISHED")
        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .description import description
        app.register_blueprint(description.description_blueprint)

        from .podcasts import podcasts
        app.register_blueprint(podcasts.podcasts_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .account import account
        app.register_blueprint(account.account_blueprint)

    return app