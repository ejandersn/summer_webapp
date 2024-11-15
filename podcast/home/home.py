from flask import Blueprint, render_template, current_app
import podcast.adapters.repository as repo
from podcast.domainmodel.model import Chart

home_blueprint = Blueprint('home_bp', __name__)


def create_podcasts():
    repository = repo.repo_instance
    podcasts_list = list(repository.get_podcasts())
    return podcasts_list


@home_blueprint.route('/home', methods=['GET'])
def home():
    list_of_podcasts = create_podcasts()
    chart_list = []
    chart_1 = Chart(1, "Trending Now", [list_of_podcasts[139], list_of_podcasts[1], list_of_podcasts[2], list_of_podcasts[3], list_of_podcasts[4]])
    chart_2 = Chart(1, "Editor's Picks", [list_of_podcasts[93], list_of_podcasts[77], list_of_podcasts[2], list_of_podcasts[3], list_of_podcasts[4]])
    chart_list.append(chart_1)
    chart_list.append(chart_2)

    return render_template('layout.html', podcasts=list_of_podcasts, charts=chart_list)


@home_blueprint.route('/', methods=['GET'])
def layout():
    list_of_podcasts = create_podcasts()
    chart_list = []
    chart_1 = Chart(1, "Trending Now", [list_of_podcasts[139], list_of_podcasts[1], list_of_podcasts[2], list_of_podcasts[3], list_of_podcasts[4]])
    chart_2 = Chart(1, "Editor's Picks", [list_of_podcasts[93], list_of_podcasts[77], list_of_podcasts[2], list_of_podcasts[3], list_of_podcasts[4]])
    chart_list.append(chart_1)
    chart_list.append(chart_2)


    return render_template('layout.html', podcasts=list_of_podcasts, charts=chart_list)
