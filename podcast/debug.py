from podcast import MemoryRepository, CSVDataReader
from podcast.description.description import description_blueprint

csv_reader = CSVDataReader(
    podcasts_file="podcast/adapters/data/podcasts.csv",
    episodes_file="podcast/adapters/data/episodes.csv"
)
@description_blueprint.route('/debug')
def debug():
    repository = MemoryRepository(csv_reader)
    repository.load_podcasts()
    repository.load_episodes()
    repository.print_podcasts()
    repository.print_episodes()
    return "Debug information printed to console."
