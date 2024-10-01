from django.urls import path, include

from . import views


app_name = 'blog'


urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('auth/', include('django.contrib.auth.urls')),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('profile/<str:username>/', views.ProfileDetailView.as_view(), name='profile'),
    
    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(), name='category_posts'),
 
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'),
    
    path('profile/edit_profile', views.edit_profile, name='edit_profile'),
#     path('profile/edit_profile', views.password_change, name='password_change'),
    
    # path('profile/edit_profile', views.password_change, name='password_change'),
    path('posts/create', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:post_id>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>', views.DeleteCommentView.as_view(), name='delete_comment'),
    
    
    path('posts/<int:post_id>/edit_post', views.PostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:post_id>/delete_post', views.edit_post, name='delete_post'),
    
#     path('posts/<int:post_id>/', views.PostDetailView.as_view(),
#          name='add_comment'),
    
    
    
    
]
