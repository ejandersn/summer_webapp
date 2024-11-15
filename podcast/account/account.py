from flask import Blueprint, render_template, request, current_app, url_for, redirect
from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from podcast.domainmodel.model import Playlist, User
from podcast.authentication.authentication import login_required
import podcast.adapters.repository as repo

account_blueprint = Blueprint('account_bp', __name__)


@login_required
@account_blueprint.route('/account/<string:username>')
def account(username):
    repository = repo.repo_instance
    user = repository.get_user(username)

    page_ep = request.args.get('page', 1, type=int)
    page_pod = request.args.get('page_pod', 1, type=int)
    per_page_ep = 4
    per_page_pod = 2

    my_playlist = repository.get_playlist(user)
    reviews = repository.get_user_reviews(username)

    # Pagination for episodes
    list_of_episodes = my_playlist.episodes
    start_ep = (page_ep - 1) * per_page_ep
    end_ep = start_ep + per_page_ep
    paginated_episodes = list_of_episodes[start_ep:end_ep]
    total_episodes = len(my_playlist.episodes)
    total_pages_ep = (total_episodes + per_page_ep - 1) // per_page_ep

    # Pagination for podcasts
    list_of_podcasts = my_playlist.podcasts
    start_pod = (page_pod - 1) * per_page_pod
    end_pod = start_pod + per_page_pod
    paginated_podcasts = list_of_podcasts[start_pod:end_pod]
    total_podcasts = len(list_of_podcasts)
    total_pages_pod = (total_podcasts + per_page_pod - 1) // per_page_pod

    # back button for podcastDescription link
    catalogue_page = request.args.get('catalogue_page', 1, type=int)

    return render_template(
        'account.html',
        username=username,
        user=user,
        playlist=my_playlist,
        reviews=reviews,
        episodes=paginated_episodes,
        page=page_ep,
        total_pages=total_pages_ep,
        total_episodes=total_episodes,
        per_page_ep=per_page_ep,
        podcasts=paginated_podcasts,
        page_pod=page_pod,
        total_pages_pod=total_pages_pod,
        total_podcasts=total_podcasts,
        per_page_pod=per_page_pod,

        cat_page=catalogue_page
    )


@account_blueprint.route('/delete_podcast_action/<int:podcast_id>', methods=['POST'])
def delete_podcast_action(podcast_id):
    page_ep = int(request.form.get('page_ep'))
    page_pod = int(request.form.get('page_pod'))
    total_podcasts = int(request.form.get('total_podcasts'))
    per_page_pod = int(request.form.get('per_page_pod'))
    username = str(request.form.get('username'))

    repository = repo.repo_instance
    podcast = repository.get_podcast(podcast_id)

    new_total_pages_pod = (total_podcasts - 1 + per_page_pod - 1) // per_page_pod
    new_page_pod = min(page_pod, new_total_pages_pod)

    if podcast:
        repository.delete_podcast_from_playlist(podcast, repository.get_user(username))
        return redirect(url_for('account_bp.account', username=username, page=page_ep, page_pod=new_page_pod))
    else:
        return "Podcast not found", 404


@account_blueprint.route('/delete_episode_action/<int:episode_id>', methods=['POST'])
def delete_episode_action(episode_id):
    page_ep = int(request.form.get('page_ep'))
    page_pod = int(request.form.get('page_pod'))
    total_episodes = int(request.form.get('total_episodes'))
    per_page_ep = int(request.form.get('per_page_ep'))
    username = str(request.form.get('username'))

    repository = repo.repo_instance
    episode = repository.get_episode(episode_id)
    user = repository.get_user(username)

    new_total_pages_ep = (total_episodes - 1 + per_page_ep - 1) // per_page_ep
    new_page_ep = min(page_ep, new_total_pages_ep)

    if episode:
        repository.delete_episode_from_playlist(episode, user)
        return redirect(url_for('account_bp.account', username=username, page=new_page_ep, page_pod=page_pod))
    else:
        return "Episode not found", 404


@account_blueprint.route('/account/<string:username>/reviews')
def user_reviews(username):
    repository = repo.repo_instance
    user = repository.get_user(username)
    reviews = repository.get_user_reviews(username)

    return render_template('account_reviews.html', username=username, user=user, reviews=reviews)

