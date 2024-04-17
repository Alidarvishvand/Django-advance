
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "api-v1"


router = DefaultRouter()
router.register(r'posts',views.PostModelsViewset,basename='post'),
router.register('category',views.CategoryModelViewSet,basename='category')
urlpatterns = router.urls
# urlpatterns = [

#     path('post/',views.PostList.as_view(),name='post_list'),
#     path('post/<int:pk>/',views.PostDetail.as_view(),name='post_detail'),
#     path('post/',views.PostViewset.as_view({'get':'retrieve', 'post':'create'}),name='post_list'),
#     path('post/<int:pk>/',views.PostViewset.as_view({'get':'list','put':'update','patch':'partial_update','delete':'destroy'}),name='post_detail'),
# ]
