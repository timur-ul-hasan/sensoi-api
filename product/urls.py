from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('rename-file/<int:pk>', views.rename_file, name='rename_file'),
    path('add_file/<str:value>', views.add_file, name='add_file'),
    path('open-file/', views.open_file, name='open_file'),
    path('add-favorite/<int:pk>/', views.add_favorite, name='add_favorite'),
    path('favorite_list/', views.favorite_list, name='favorite_list'),
    path('open/<int:pk>/', views.open, name='open'),
    path('main-table/<str:parent_id>', views.main_table, name='main_table'),
    path('bottom-panel/<str:node_id>', views.bottom_panel, name='bottom_panel'),
    path('post-rating/<str:node_id>/<int:rating>', views.post_rating, name='post_rating'),
    path('file-manager/<str:parent_id>', views.file_manager, name='file_manager'),
    path('file-manager/open-file/<str:node_id>', views.browser_open_file, name='open_file'),
    path('file-manager/delete-files/', views.delete_files, name='delete_files'),
    path('create-folder/<str:parent_id>/<str:folder_name>', views.create_folder, name='create_folder'),
    path('api/new-project/<str:project_name>/create', views.create_new_project, name='create_new_project'),
    path('api/copy_ingested/', views.copy_ingested, name='copy_ingested'),
    path('post-tag/<str:node_id>/<str:tag>', views.post_tag, name='post_tag'),
    path('project/<str:project_name>/new', views.new_project_view, name='new_project_view'),
]
