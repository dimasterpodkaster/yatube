from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("follow/", views.follow_index, name="follow_index"),
    path("image/<int:post_id>/", views.view_image, name='view_image'),
    path("<str:username>/", views.profile, name='profile'),
    path("<str:username>/<int:post_id>/", views.post_view, name='post'),
    path("<str:username>/<int:post_id>/edit/", views.post_edit, name='post_edit'),
    path("<str:username>/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("<str:username>/follow/", views.profile_follow, name="profile_follow"),
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
]

