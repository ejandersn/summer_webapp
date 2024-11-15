import os
from pathlib2 import Path

from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.repository import AbstractRepository


def populate(data_path: Path, session_factory, repo: AbstractRepository, database_mode: bool):
    dir_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.'))

    podcast_filename = os.path.join(dir_name, str(Path(data_path) / "podcasts.csv"))
    episode_filename = os.path.join(dir_name, str(Path(data_path) / "episodes.csv"))

    csv_reader = CSVDataReader(
        podcasts_file=podcast_filename,
        episodes_file=episode_filename
    )
    if database_mode:
        repository = SqlAlchemyRepository(session_factory)
        repository.load_data(csv_reader)
    else:
        repo.load_data(csv_reader)