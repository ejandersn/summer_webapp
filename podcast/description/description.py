from flask import Blueprint, render_template, request, current_app, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField, SubmitField
from wtforms.validators import DataRequired

import podcast
from podcast.authentication.authentication import login_required
from podcast.description import review_services
from flask import Blueprint, render_template, request, current_app, redirect, url_for
from podcast.adapters import repository as repo
description_blueprint = Blueprint('description_bp', __name__)


@description_blueprint.route('/description/<int:podcast_id>')
def description(podcast_id):
    page = request.args.get('page', 1, type=int)
    catalogue_page = request.args.get('catalogue_page', 1, type=int)
    search_title = request.args.get('search_title')
    category_id = request.args.get('category')
    author_id = request.args.get('author')
    title_id = request.args.get('title')
    per_page = 3

    repository = repo.repo_instance

    current_podcast = repository.get_podcast(podcast_id)

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

    start = (catalogue_page - 1) * per_page
    end = start + per_page
    paginated_podcasts = list_of_podcasts[start:end]

    if current_podcast:
        podcast_id = current_podcast.id
        list_of_episodes = repository.get_episodes_by_podcast_id(podcast_id)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_episodes = list_of_episodes[start:end]
        print(paginated_episodes)
        total_episodes = len(list_of_episodes)
        total_pages = (total_episodes + per_page - 1) // per_page

        reviews = repository.get_reviews_by_podcast(podcast_id)

        recently_added_episode = repository.get_recently_added_episode()
        recently_added_podcast = repository.get_recently_added_podcast()

        average_rating = repository.get_average_rating(podcast_id)

        return render_template(
            'podcastDescription.html',
            podcast=current_podcast,
            episodes=paginated_episodes,
            reviews=reviews,
            page=page,
            total_pages=total_pages,
            catalogue_page=catalogue_page,
            search_title=search_title,
            category_id=category_id,
            author_id=author_id,
            podcasts=paginated_podcasts,
            recently_added_episode=recently_added_episode,
            recently_added_podcast=recently_added_podcast,
            av_rating=average_rating
        )
    else:
        return "Podcast not found", 404


@description_blueprint.route('/description/<int:podcast_id>/new_review', methods=['GET', 'POST'])
@login_required
def new_review(podcast_id):
    username = session['username']
    repository = repo.repo_instance
    form = ReviewForm()
    error_message = None

    if form.rating.data == 0:
        form.rating.data = 1

    if form.validate_on_submit():
        try:
            review_services.add_review(int(podcast_id), username, str(form.comment.data), int(form.rating.data), repository)
            return redirect(url_for('description_bp.description', podcast_id=podcast_id))
        except review_services.UnknownUserException:
            error_message = "User unknown"
        except review_services.NonExistentPodcastException:
            error_message = "This podcast does not exist"

    if form.errors:
        error_message = form.errors

    return render_template(
        'addReview.html',
        podcast=repository.get_podcast(podcast_id),
        error_message=error_message,
        form=form,
        podcast_id=podcast_id,
    )


class ReviewForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired('Please enter your comment.')])
    rating = IntegerField('Rating', [
        DataRequired('Please enter your rating.')])
    submit = SubmitField('Submit')


@description_blueprint.route('/perform_episode_action/<int:episode_id>', methods=['POST'])
@login_required
def perform_episode_action(episode_id):
    repository = repo.repo_instance

    episode = repository.get_episode(episode_id)
    username = session['username']
    user = repository.get_user(username)

    if episode:
        repository.add_episode_to_playlist(episode, user)
        repository.recently_added_episode_to_playlist(episode_id)
        return redirect(request.referrer or url_for('description_bp.description', podcast_id=episode.podcast.id))
    else:
        return "Episode not found", 404


@description_blueprint.route('/perform_podcast_action/<int:podcast_id>', methods=['POST'])
@login_required
def perform_podcast_action(podcast_id):
    repository = repo.repo_instance
    podcast = repository.get_podcast(podcast_id)
    username = session['username']
    user = repository.get_user(username)

    if podcast:
        repository.add_podcast_to_playlist(podcast, user)
        repository.recently_added_podcast_to_playlist(podcast_id)
        return redirect(request.referrer or url_for('description_bp.description', podcast_id=podcast_id))
    else:
        return "Podcast not found", 404
