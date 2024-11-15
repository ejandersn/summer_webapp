from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text, MetaData
)
from sqlalchemy.orm import registry, relationship
from datetime import datetime

from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist

# Global variable giving access to the MetaData (schema) information of the database
mapper_registry = registry()

metadata = MetaData()


authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('author_id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True)
)

podcast_table = Table(
    'podcasts',  mapper_registry.metadata,
    Column('podcast_id', Integer, primary_key=True, autoincrement=True),
    Column('title', Text, nullable=True),
    Column('image_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('language', String(255), nullable=True),
    Column('website_url', String(255), nullable=True),
    Column('author_id', ForeignKey('authors.author_id')),
    Column('itunes_id', Integer, nullable=True)
)

# Episodes should have links to its podcast through its foreign keys
episode_table = Table(
    'episodes',  mapper_registry.metadata,
    Column('episode_id', Integer, primary_key=True),
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id')),
    Column('title', Text, nullable=True),
    Column('audio_length', Integer, nullable=True),
    Column('publication_date', String(255), nullable=True),
    Column('description', String(255), nullable=True),
    Column('audio_link', String(255), nullable=True)
)

categories_table = Table(
    'categories',  mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True, autoincrement=True),
    Column('category_name', String(64))  #, nullable=False)
)

podcast_categories_table = Table(
    'podcast_categories',  mapper_registry.metadata,
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.category_id'), primary_key=True),
)

reviews_table = Table(
    'reviews',  mapper_registry.metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('comment', String(255), nullable=True),
    Column('rating', Integer, nullable=False),
)

users_table = Table(
    'users',  mapper_registry.metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(20),unique=True, nullable=False),
    Column('password', String(20), nullable=False),

)

playlist_table = Table(
    'playlists',  mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('title', String(31), nullable=False),  # 11 characters more than username, "[username]'s playlist"
    Column('description', String(255), nullable=True),
)

playlist_episodes_table = Table(
    'playlist_episodes',  mapper_registry.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id')),
    Column('episode_id', Integer, ForeignKey('episodes.episode_id')),
)

playlist_podcasts_table = Table(
    'playlist_podcasts', mapper_registry.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id')),
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id')),
)


def map_model_to_tables():
    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_id': authors_table.c.author_id,
        '_name': authors_table.c.name,
    })

    mapper_registry.map_imperatively(User, users_table, properties={
        '_id': users_table.c.user_id,
        '_username': users_table.c.username,
        '_password': users_table.c.password,
        '_User__reviews': relationship(Review, back_populates='_Review__user'),
        '_playlists': relationship(Playlist, back_populates='_user'),
    })

    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_id': categories_table.c.category_id,
        '_name': categories_table.c.category_name,
        '_podcasts': relationship(Podcast, secondary=podcast_categories_table, backref='categories'), #backwards populate dont DELETE!!
    })

    mapper_registry.map_imperatively(Podcast, podcast_table, properties={
        '_id': podcast_table.c.podcast_id,
        '_title': podcast_table.c.title,
        '_image': podcast_table.c.image_url,
        '_description': podcast_table.c.description,
        '_language': podcast_table.c.language,
        '_website': podcast_table.c.website_url,
        '_itunes_id': podcast_table.c.itunes_id,
        '_author': relationship(Author),
        '_episodes': relationship(Episode, back_populates='_podcast'),
        '_Podcast__reviews': relationship(Review, back_populates='_Review__podcast'),
        '_playlists': relationship(Playlist, secondary=playlist_podcasts_table, back_populates='_podcasts')
    })

    mapper_registry.map_imperatively(Episode, episode_table, properties={
        '_id': episode_table.c.episode_id,
        '_podcast': relationship(Podcast, back_populates='_episodes'),
        '_title': episode_table.c.title,
        '_audio_length': episode_table.c.audio_length,
        '_publication_date': episode_table.c.publication_date,
        '_description': episode_table.c.description,
        '_audio_link': episode_table.c.audio_link,
        '_playlists': relationship(Playlist, secondary=playlist_episodes_table, back_populates='_episodes')
    })

    mapper_registry.map_imperatively(Review, reviews_table, properties={
        '_Review__id': reviews_table.c.review_id,
        '_Review__comment': reviews_table.c.comment,
        '_Review__rating': reviews_table.c.rating,
        '_Review__user': relationship(User, back_populates='_User__reviews'),
        '_Review__podcast': relationship(Podcast, back_populates='_Podcast__reviews'),
    })

    mapper_registry.map_imperatively(Playlist, playlist_table, properties={
        '_id': playlist_table.c.id,
        '_user': relationship(User, back_populates='_playlists'),
        '_title': playlist_table.c.title,
        '_description': playlist_table.c.description,
        '_episodes': relationship(Episode, secondary=playlist_episodes_table),
        '_podcasts': relationship(Podcast, secondary=playlist_podcasts_table),
    })


