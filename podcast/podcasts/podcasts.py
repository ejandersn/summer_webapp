from flask import Blueprint, render_template, request, current_app
from podcast.adapters import repository as repo

podcasts_blueprint = Blueprint('podcasts_bp', __name__)

@podcasts_blueprint.route('/podcasts', methods=['GET'])
def podcasts():
    page = request.args.get('page', 1, type=int)
    per_page = 24
    search_title = request.args.get('search_title')
    category_id = request.args.get('category')
    author_id = request.args.get('author')
    title_id = request.args.get('title')

    repository = repo.repo_instance

    if search_title:
        list_of_podcasts = repository.search_podcasts_by_query(search_title)
    elif title_id:
        list_of_podcasts = [repository.get_podcast(int(title_id))]
    elif category_id:
        list_of_podcasts = repository.search_podcast_by_category_id(category_id)
    elif author_id:
        list_of_podcasts = repository.search_podcast_by_author_id(author_id)
    else:
        list_of_podcasts = repository.get_podcasts()
    if not list_of_podcasts:
        return render_template('catalogue.html', no_podcasts_found=True)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_podcasts = list_of_podcasts[start:end]
    total_podcasts = len(list_of_podcasts)
    total_pages = (total_podcasts + per_page - 1) // per_page

    categories = repository.get_categories()
    authors = repository.get_authors()
    unique_podcasts = list(set(repository.get_podcasts()))

    no_podcasts_found = total_podcasts == 0

    return render_template('catalogue.html',
                           podcasts=paginated_podcasts,
                           page=page,
                           total_pages=total_pages,
                           categories=categories,
                           authors=authors,
                           unique_podcasts=unique_podcasts,
                           no_podcasts_found=no_podcasts_found)
