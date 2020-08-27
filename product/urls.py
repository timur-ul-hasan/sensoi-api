from django.urls import path
from . import views
from django.conf.urls import include,url


urlpatterns = [
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url('rename-file/<int:pk>', views.rename_file, name='rename_file'),
    url('add_file/<str:value>', views.add_file, name='add_file'),
    url('open-file/', views.open_file, name='open_file'),
    url('add-favorite/<int:pk>/', views.add_favorite, name='add_favorite'),
    url('favorite_list/', views.favorite_list, name='favorite_list'),
    url('open/<int:pk>/', views.open, name='open'),
    url('main-table/<str:parent_id>', views.main_table, name='main_table'),
    url('bottom-panel/<str:node_id>', views.bottom_panel, name='bottom_panel'),
    url('post-rating/<str:node_id>/<int:rating>', views.post_rating, name='post_rating'),
    url('file-manager/<str:parent_id>', views.file_manager, name='file_manager'),
    url('file-manager/open-file/<str:node_id>', views.browser_open_file, name='open_file'),
    url('file-manager/delete-files/', views.delete_files, name='delete_files'),
    url('create-folder/<str:parent_id>/<str:folder_name>', views.create_folder, name='create_folder'),
    url('api/new-project/<str:project_name>/create', views.create_new_project, name='create_new_project'),
    url('api/copy_ingested/', views.copy_ingested, name='copy_ingested'),
    url('post-tag/<str:node_id>/<str:tag>', views.post_tag, name='post_tag'),
    url('project/<str:project_name>/new', views.new_project_view, name='new_project_view'),
]
