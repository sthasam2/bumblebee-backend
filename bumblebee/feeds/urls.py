"""
comment-crud
comment-list
comment-detail
"""

from django.urls import path

from bumblebee.feeds.api.views.feed_views import (
    FeedBuzzListView,
    FeedFollowSuggestionsListView,
)

urlpatterns = [
    # retrieve
    path(
        "post",
        FeedBuzzListView.as_view(),
        name="feed-post-list",
    ),
    path(
        "follow_suggestions",
        FeedFollowSuggestionsListView.as_view(),
        name="feed-suggestions-list",
    ),
]
