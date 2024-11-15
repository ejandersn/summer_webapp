import warnings

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from podcast.domainmodel.model import User, Podcast, Author, Episode, Review, Playlist, Category


# Helper functions to insert objects into the database

def insert_user(empty_session, values=None):
    new_name = "sarah"
    new_password = "Harper99"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute(text('INSERT INTO users (username, password) VALUES (:user_name, :password)'),
                          {'user_name': new_name, 'password': new_password})


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute(text('INSERT INTO users (username, password) VALUES (:user_name, :password)'),
                              {'user_name': value[0], 'password': value[1]})


def insert_podcast(empty_session, values=None):
    if values is not None:
        podcast_id = values[0]
        title = values[1]
        image = values[2]
        description = values[3]
        language = values[4]
        website = values[5]
        author = values[6]
        itunes_id = values[7]
    else:
        podcast_id = 498
        title = '95bFM: Grow Room Radio'
        image = "http://is3.mzstatic.com/image/thumb/Music111/v4/62/9a/31/629a319d-c635-2789-340f-a000f20ba9da/source/600x600bb.jpg"
        description = "The Grow Room is an Auckland-based collective, creative space, record label and radio show. Broadcast from Auckland, New Zealand on Saturdays from 9pm."
        language = 'English'
        website = "http://www.95bfm.co.nz/"
        author = 16
        itunes_id = 1223821754

    empty_session.execute(text(
        'INSERT INTO podcasts (podcast_id, title, image_url, description, language, website_url, author_id, itunes_id) VALUES (:podcast_id, :title, :image_url, :description, :language, :website_url, :author_id, :itunes_id)'),
        {'podcast_id': podcast_id, 'title': title, 'image_url': image, 'description': description,
         'language': language, 'website_url': website, 'author_id': author, 'itunes_id': itunes_id})

    return podcast_id


def insert_podcasts(empty_session, values):
    for value in values:
        empty_session.execute(text(
            'INSERT INTO podcasts (podcast_id, title, image_url, description, language, website_url, author_id, itunes_id) VALUES (:podcast_id, :title, :image_url, :description, :language, :website_url, :author_id, :itunes_id)'),
            {'podcast_id': value[0], 'title': value[1], 'image_url': value[2], 'description': value[3],
             'language': value[4], 'website_url': value[5], 'author_id': value[6],
             'itunes_id': value[7]})


def insert_episode(empty_session, values=None):
    if values is not None:
        episode_id = values[0]
        podcast_id = values[1]
        title = values[2]
        audio_length = values[3]
        publication_date = values[4]
        description = values[5]
        audio_link = values[6]
    else:
        episode_id = 4376
        podcast_id = 129
        title = 'In His Presence'
        audio_length = 1917
        publication_date = '2017-12-31'
        description = 'David Tennant'
        audio_link = 'http://download.yourstreamlive.com/gluster/yourstreamlive/4643/781126.mp3'

    empty_session.execute(text(
        'INSERT INTO episodes (episode_id, podcast_id, title, audio_length, publication_date, description, audio_link) VALUES (:episode_id, :podcast_id, :title, :audio_length, :publication_date, :description, :audio_link)'),
        {'episode_id': episode_id, 'podcast_id': podcast_id, 'title': title, 'audio_length': audio_length,
         'publication_date': publication_date, 'description': description, 'audio_link': audio_link})

    return episode_id


def insert_episodes(empty_session, values):
    for value in values:
        empty_session.execute(text(
            'INSERT INTO podcasts (episode_id, podcast_id, title, audio_length, publication_date, description, audio_link) VALUES (:episode_id, :podcast_id, :title, :audio_length, :publication_date, :description, :audio_link)'),
            {'episode_id': value[0], 'podcast_id': value[1], 'title': value[2], 'audio_length': value[3],
             'publication_date': value[4], 'description': value[5], 'audio_link': value[6]})


def insert_review(empty_session, values=None):
    if values is not None:
        review_id = values[0]
        user_id = values[1]
        podcast_id = values[2]
        comment = values[3]
        rating = values[4]
    else:
        review_id = 1
        user_id = 1
        podcast_id = 498
        comment = 'I love this podcast!'
        rating = 5
    empty_session.execute(text(
        'INSERT INTO reviews (review_id, user_id, podcast_id, comment, rating) VALUES (:review_id, :user_id, :podcast_id, :comment, :rating)'),
        {'review_id': review_id, 'user_id': user_id, 'podcast_id': podcast_id, 'comment': comment, 'rating': rating})
    insert_user(empty_session)
    insert_podcast(empty_session)

    return (review_id, podcast_id)


def insert_playlist(empty_session, values=None):
    insert_user(empty_session)
    if values is not None:
        id = values[0]
        user_id = values[1]
        title = values[2]
        description = values[3]
    else:
        id = 1
        user_id = 1
        title = "sarah's Playlist"
        description = "Save episodes and whole playlists to watch later!"
    empty_session.execute(text(
        'INSERT INTO playlists (id, user_id, title, description) VALUES (:id, :user_id, :title, :description)'),
        {'id': id, 'user_id': user_id, 'title': title, 'description': description})

    return id

def insert_category(empty_session, values=None):
    if values is not None:
        category_id = values[0]
        category_name = values[1]
    else:
        category_id = 1
        category_name = 'Music'
    empty_session.execute(text(
        'INSERT INTO categories (category_id, category_name) VALUES (:category_id, :category_name)'),
        {'category_id': category_id, 'category_name': category_name})

    return category_id


def insert_author(empty_session, values=None):
    if values is not None:
        author_id = values[0]
        name = values[1]
    else:
        author_id = 16
        name = '95bFM'
    empty_session.execute(text(
        'INSERT INTO authors (author_id, name) VALUES (:author_id, :name)'),
        {'author_id': author_id, 'name': name})

    return author_id


# Helper functions which insert objects into the database
# and create a relationship between them

def insert_podcast_with_category(empty_session):
    podcast_id = insert_podcast(empty_session)
    category_id = insert_category(empty_session)
    empty_session.execute(text(
        'INSERT INTO podcast_categories (podcast_id, category_id) VALUES (:podcast_id, :category_id)'),
        {'podcast_id': podcast_id, 'category_id': category_id})

    return [(podcast_id, category_id)]


def insert_podcast_with_author(empty_session):
    podcast_id = insert_podcast(empty_session)
    author_id = insert_author(empty_session)
    return [podcast_id, author_id]


def insert_podcast_with_episode(empty_session):
    episode_id = insert_episode(empty_session)
    podcast_id = 129
    insert_podcast(empty_session, (129,
                                   'Son Rise Church and Ministries',
                                   'http://is5.mzstatic.com/image/thumb/Music118/v4/68/33/c3/6833c3ca-28e5-bf93-a27a-451892c9251d/source/600x600bb.jpg',
                                   'Weekly Sermons from Son Rise Church and Ministries.',
                                   'English',
                                   'http://',
                                   'Son Rise Church and Ministries (Audio)',
                                   1257590036))

    return episode_id, podcast_id


def insert_user_with_playlist(empty_session):
    insert_user(empty_session)
    user_id = empty_session.execute(text('SELECT user_id FROM users')).scalar()
    playlist_id = insert_playlist(empty_session)

    return user_id, playlist_id


# Helper functions which create objects


def make_user():
    user = User(1, "sarah", "Harper99")
    return user


def make_podcast():
    podcast = Podcast(
        498,
        Author(16, '95bFM'),
        '95bFM: Grow Room Radio',
        'http://is3.mzstatic.com/image/thumb/Music111/v4/62/9a/31/629a319d-c635-2789-340f-a000f20ba9da/source/600x600bb.jpg',
        "The Grow Room is an Auckland-based collective, creative space, record label and radio show. Broadcast from Auckland, New Zealand on Saturdays from 9pm.",
        'http://www.95bfm.co.nz/',
        1223821754,
        'English')
    return podcast


def make_podcast_for_episode():
    podcast = Podcast(
        129,
        Author(707, 'Son Rise Church and Ministries'),
        'Son Rise Church and Ministries (Audio)',
        'http://is5.mzstatic.com/image/thumb/Music118/v4/68/33/c3/6833c3ca-28e5-bf93-a27a-451892c9251d/source/600x600bb.jpg',
        'Weekly Sermons from Son Rise Church and Ministries.',
        'http://',
        1257590036,
        'English')

    return podcast


def make_podcast_with_category():
    podcast = make_podcast()
    category = Category(1, 'Music')
    podcast.add_category(category)
    return podcast


def make_episode():
    episode = Episode(4376, make_podcast_for_episode(), 'In His Presence', 1917, '2017-12-31', 'David Tennant',
                      'http://download.yourstreamlive.com/gluster/yourstreamlive/4643/781126.mp3')
    return episode


def make_review():
    review = Review(1, 5, 'I love this podcast!', make_user(), make_podcast())
    return review


def make_playlist():
    user = make_user()
    playlist = Playlist(1, user, "sarah's Playlist", "Save episodes and whole playlists to watch later!", [], [])
    return playlist


def make_category():
    category = Category(1, 'Music')
    return category


def make_author():
    author = Author(16, '95bFM')
    return author


# TESTING BEGINS

# Testing that objects properly save and load to the database


def test_saving_of_user(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT username, password FROM users')))
    assert rows == [("sarah", "Harper99")]


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User(1, "andrew", "1234"),
        User(2, "cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_podcasts(empty_session):
    podcast = make_podcast()
    empty_session.add(podcast)
    empty_session.commit()

    rows = list(empty_session.execute(text(
        'SELECT podcast_id, title, image_url, description, language, website_url, author_id, itunes_id from PODCASTS')))
    assert rows == [(
        498,
        '95bFM: Grow Room Radio',
        'http://is3.mzstatic.com/image/thumb/Music111/v4/62/9a/31/629a319d-c635-2789-340f-a000f20ba9da/source/600x600bb.jpg',
        "The Grow Room is an Auckland-based collective, creative space, record label and radio show. Broadcast from Auckland, New Zealand on Saturdays from 9pm.",
        'English',
        'http://www.95bfm.co.nz/',
        16,
        1223821754)]


def test_loading_of_podcast(empty_session):
    insert_podcast(empty_session)
    assert empty_session.query(Podcast).one() == make_podcast()


def test_saving_of_episode(empty_session):
    episode = make_episode()
    empty_session.add(episode)
    empty_session.commit()

    rows = list(empty_session.execute(text(
        'SELECT episode_id, podcast_id, title, audio_length, publication_date, description, audio_link FROM episodes')))
    assert rows == [(4376, 129, 'In His Presence', 1917, '2017-12-31', 'David Tennant',
                     'http://download.yourstreamlive.com/gluster/yourstreamlive/4643/781126.mp3')
                    ]


def test_loading_of_episode(empty_session):
    insert_episode(empty_session)
    assert empty_session.query(Episode).one() == make_episode()


def test_saving_of_review(empty_session):
    review = make_review()
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute(text(
        'SELECT review_id, user_id, podcast_id, comment, rating FROM reviews')))
    assert rows == [(1, 1, 498, 'I love this podcast!', 5)]


def test_loading_of_review(empty_session):
    insert_review(empty_session)
    db_review = empty_session.query(Review).one()
    object_review = make_review()
    assert db_review.user == object_review.user


def test_saving_of_playlist(empty_session):
    playlist = make_playlist()
    empty_session.add(playlist)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT id, user_id, title, description FROM playlists')))
    assert rows == [(1, 1, "sarah's Playlist", "Save episodes and whole playlists to watch later!")]


def test_loading_of_playlist(empty_session):
    insert_playlist(empty_session)
    assert empty_session.query(Playlist).one() == make_playlist()


def test_saving_of_category(empty_session):
    category = make_category()
    empty_session.add(category)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT category_id, category_name FROM categories')))
    assert rows == [(1, 'Music')]


def test_loading_of_category(empty_session):
    insert_category(empty_session)
    assert empty_session.query(Category).one() == make_category()


def test_saving_of_author(empty_session):
    author = make_author()
    empty_session.add(author)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT author_id, name FROM authors')))
    assert rows == [(16, '95bFM')]


def test_loading_of_author(empty_session):
    insert_author(empty_session)
    assert empty_session.query(Author).one() == make_author()


def test_saving_of_common_usernames(empty_session):
    insert_user(empty_session, ("Sarah", "Harper99"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        insert_user(empty_session, ("Sarah", "Harper99"))
        empty_session.commit()


# Testing that object relationships properly save to the db and load from the db

def test_saving_podcast_category_association(empty_session):
    result = insert_podcast_with_category(empty_session)
    rows = list(empty_session.execute(text('SELECT podcast_id, category_id FROM podcast_categories')))

    assert result == rows


def test_loading_podcast_category_association(empty_session):
    insert_podcast_with_category(empty_session)
    podcast = empty_session.query(Podcast).one()
    category = make_category()

    assert podcast.categories[0] == category


def test_saving_podcast_author_association(empty_session):
    expected = insert_podcast_with_author(empty_session)
    author_id = list(empty_session.execute(text('SELECT author_id FROM authors')))

    assert expected[1] == author_id[0][0]


def test_loading_podcast_author_association(empty_session):
    insert_podcast_with_author(empty_session)
    podcast = empty_session.query(Podcast).one()
    author = empty_session.query(Author).one()

    assert podcast.author == author


def test_saving_podcast_episode_association(empty_session):
    expected = insert_podcast_with_episode(empty_session)
    podcast_id = list(empty_session.execute(text('SELECT podcast_id FROM podcasts')))
    episode_podcast_id = list(empty_session.execute(text('SELECT podcast_id FROM episodes')))

    assert expected[1] == podcast_id[0][0] == episode_podcast_id[0][0]


def test_loading_podcast_episode_association(empty_session):
    insert_podcast_with_episode(empty_session)
    podcast = empty_session.query(Podcast).one()
    episode = empty_session.query(Episode).one()

    assert episode.podcast == podcast


def test_saving_podcast_review_association(empty_session):
    expected = insert_review(empty_session)
    podcast_id = list(empty_session.execute(text('SELECT podcast_id FROM podcasts')))
    review_podcast_id = list(empty_session.execute(text('SELECT podcast_id FROM reviews')))

    assert expected[1] == podcast_id[0][0] == review_podcast_id[0][0]


def test_loading_user_podcast_review_association(empty_session):
    with warnings.catch_warnings(action="ignore"):
        podcast_id = insert_podcast(empty_session)
        podcast = empty_session.query(Podcast).one()
        user = make_user()
        user_id = user.id
        review = Review(1, 5, "Awesome podcast", user, podcast)
        empty_session.add(review)
        empty_session.commit()

        rows = list(empty_session.execute(text('SELECT user_id, podcast_id, comment FROM reviews')))
        assert rows == [(user_id, podcast_id, "Awesome podcast")]


def test_saving_user_review_association(empty_session):
    podcast = make_podcast()
    user = make_user()
    review = Review(1, 5, "Awesome user", user, podcast)
    empty_session.add(review)
    empty_session.add(user)
    empty_session.commit()

    review_data = list(empty_session.execute(text('SELECT user_id FROM reviews')))
    user_data = list(empty_session.execute(text('SELECT user_id FROM users')))

    assert review_data == user_data


def test_saving_user_playlist_association(empty_session):
    insert_playlist(empty_session)
    user_id = list(empty_session.execute(text('SELECT user_id FROM users')))
    playlist_user_id = list(empty_session.execute(text('SELECT user_id FROM playlists')))

    assert user_id[0][0] == playlist_user_id[0][0]

