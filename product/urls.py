from django.urls import path
from . import views
from django.conf.urls import include,url


urlpatterns = [
    path('dashboard/rename-file/<int:pk>', views.rename_file, name='rename_file'),
    path('dashboard/add_file/<str:value>', views.add_file, name='add_file'),
    path('dashboard/open-file/', views.open_file, name='open_file'),
    path('dashboard/add-favorite/<int:pk>/', views.add_favorite, name='add_favorite'),
    path('dashboard/favorite_list/', views.favorite_list, name='favorite_list'),
    path('dashboard/open/<int:pk>/', views.open, name='open'),
    path('dashboard/main-table/<str:parent_id>', views.main_table, name='main_table'),
    path('dashboard/bottom-panel/<str:node_id>', views.bottom_panel, name='bottom_panel'),
    path('dashboard/post-rating/<str:node_id>/<int:rating>', views.post_rating, name='post_rating'),
    path('dashboard/file-manager/<str:parent_id>', views.file_manager, name='file_manager'),
    path('dashboard/file-manager/open-file/<str:node_id>', views.browser_open_file, name='open_file'),
    path('dashboard/file-manager/delete-files/', views.delete_files, name='delete_files'),
    path('dashboard/create-folder/<str:parent_id>/<str:folder_name>', views.create_folder, name='create_folder'),
    path('dashboard/api/new-project/<str:project_name>/create', views.create_new_project, name='create_new_project'),
    path('dashboard/api/copy_ingested/', views.copy_ingested, name='copy_ingested'),
    path('dashboard/post-tag/<str:node_id>/<str:tag>', views.post_tag, name='post_tag'),
    path('dashboard/project/<str:project_name>/new', views.new_project_view, name='new_project_view'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
]
