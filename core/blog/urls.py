from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView


app_name = "blog"
urlpatterns = [
    path('cbv-index',views.IndexView.as_view(),name='cbv-index'),
    # path("go-to-maktabkhooneh",views.RedirecTOMaktab.as_view(),name='redirect-to-maktabkhooneh'),
    path("api/v1/", include("blog.api.v1.urls")),
    path("post/", views.PostListView.as_view(), name="post_list"),
    path(
        "post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"
    ),
    path("post/create/", views.PostCreateView.as_view(), name="post_create"),
    path(
        "post/<int:pk>/edit/",
        views.PostUpdateView.as_view(),
        name="post_edit",
    ),
    path(
        "post/<int:pk>/delete/",
        views.PostDeleteView.as_view(),
        name="post_delete",
    ),
]

