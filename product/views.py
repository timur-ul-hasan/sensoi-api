from django.shortcuts import render, redirect, reverse, get_object_or_404
from product.forms import FileInputForm, RenameForm, SearchForm, ProjectFileInputForm
from django.contrib import messages
from .models import Files_upload, ProjectFilesUpload
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
from pdf2image import convert_from_path, convert_from_bytes
from django.http import JsonResponse
from django.core.files import File
from Util import alfresco
import subprocess
import os
from rest_framework.decorators import api_view, permission_classes, schema, parser_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from .serializers import (
    FileInputSerializer,
    NodesSerializer,
    FileUploadSerializer,
    ProjectFileInputSerializer,
    ProjectFileInputSerializerSwagger,
    IngestedSerializer,
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

type_choices = {
    'csv': {'csv', 'xlsx', 'xls'},
    'pdf': {'pdf', 'txt'},
    'jpg': {'pdf', 'jpeg', 'jpg'},
    'jpeg': {'pdf', 'jpeg', 'jpg'}
}

main_table_data = {}
current_folder = ''


def getProjectFiles(request, name):
    files = default_storage.listdir(f'users/{request.user}/{name}')[1]
    return files


@swagger_auto_schema(method=['GET', 'POST'])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    global main_table_data
    sorted = False
    value = None
    is_old = 0
    data = Files_upload.objects.filter(
        user=request.user).order_by('name').all()

    if request.method == 'POST':
        is_old = 1
        form = SearchForm(request.POST or None)
        if form.is_valid():
            value = form.cleaned_data.get('search')
            data = data.filter(name__icontains=value)
    if request.GET.get('sorted'):
        # data = data.order_by('-date')
        sorted = True
    if request.session.get('folder', None) is not None:
        entries = alfresco.getFolderChild(request.session['folder'])
        folder = {'id': request.session['folder'],
                  'parentId': request.session['parent']}
    else:
        entries = alfresco.getUserHomeDirectory(request)
        folder = alfresco.getUserHome(request)
        request.session['folder'] = folder['id']
        request.session['parent'] = folder['parentId']

    # data = alfresco.getDetailedData(entries)
    project_home = alfresco.getFolderByPath(request.user.id, '/Projects')['id']
    projects = []
    main_table_data = entries
    context = {'projects': projects, 'data': FileUploadSerializer(data, many=True).data, 'sorted': sorted, 'title': 'Sensai|Dashboard', "value": value, 'entries': entries,
               'parent_id': folder['parentId'], 'folder_id': folder['id'], "is_old": is_old}
    return Response(context)


@swagger_auto_schema(method=['GET', 'POST'])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def main_table(request, parent_id):
    global main_table_data, current_folder
    if parent_id == "open-project-view":
        project_name = request.GET.get('prj_name')
        files = getProjectFiles(request, project_name)
        entries = files
        data = {
            'sorted': sorted,
            'title': 'Sensai|Dashboard',
            "value": "value",
            'entries': entries,
            'parent_id': parent_id
        }
        return Response(data)

    else:
        entries = alfresco.getFolderChild(parent_id)
        node = alfresco.getNode(parent_id)
        request.session['folder'] = parent_id
        request.session['parent'] = node['parentId']
        data = {'sorted': sorted, 'title': 'Sensai|Dashboard', "value": "value", 'entries': entries,
                'parent_id': parent_id}

    main_table_data = entries
    return Response(data)


@swagger_auto_schema(method=['GET', 'POST'])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def file_manager(request, parent_id):
    global main_table_data

    if parent_id:
        entries = alfresco.getFolderChild(parent_id)

    node_entry = alfresco.getNode(parent_id)
    if "parentId" not in node_entry:
        node_entry['parentId'] = "-root-"

    folder = alfresco.getUserHome(request)
    if folder['parentId'] == node_entry['id']:
        return HttpResponse(status=500)

    # html = render_to_string('product/partial/file-manager-modal.html',
    #                         {'entries': entries, 'modal_parent_id': node_entry['parentId'], 'folder_id': parent_id})

    data = {'entries': entries,
            'modal_parent_id': node_entry['parentId'], 'folder_id': parent_id}

    main_table_data = entries
    return Response(data)


@swagger_auto_schema(method=['GET', 'POST'])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def browser_open_file(request, node_id):
    global main_table_data
    node_entry = alfresco.getNode(node_id)
    if "qshare:sharedId" not in node_entry['properties']:
        link_id = alfresco.createSharedLink(node_id)
    else:
        link_id = node_entry['properties']["qshare:sharedId"]
    return Response({"link_id": link_id})


@swagger_auto_schema(method=['GET', 'POST'])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def create_folder(request, parent_id, folder_name):
    alfresco.createFolder(parent_id, folder_name)
    return Response({})


@swagger_auto_schema(method=['GET', 'POST'])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def bottom_panel(request, node_id):
    global main_table_data
    if node_id == "null":
        return Response({})

    print(node_id)
    for item in main_table_data:
        print(item)
        if node_id == item['entry']['id']:
            data = item['entry']
    tags = alfresco.getTags(node_id)

    ratings = alfresco.getRating(request, node_id)
    print("=========rating of node =============")
    print(ratings)
    if "qshare:sharedId" in data['properties']:
        link_id = data['properties']['qshare:sharedId']
    else:
        link_id = alfresco.createSharedLink(node_id)
    unreadable = [
        "qshare:sharedId",
        "cm:likesRatingSchemeCount",
        "cm:lastThumbnailModification",
        "cm:taggable",
        "cm:fiveStarRatingSchemeCount",
        "cm:fiveStarRatingSchemeTotal",
        "cm:likesRatingSchemeTotal",
        "qshare:sharedBy"

    ]
    context = {"data": data, "tags": tags, "unreadable_keys": unreadable,
               'link_id': link_id, 'ratings': ratings}
 
    return Response(context)


@swagger_auto_schema(method=[ 'POST'])
@api_view([ 'POST'])
@permission_classes([IsAuthenticated])
def post_rating(request, node_id, rating):
    print(request.user)
    user = json.loads(request.user.serialize())[0]
    pk = str(user['pk'])
    print(pk)
    resp = alfresco.putRating('user_' + pk, node_id, rating)
    data = {
        'message': 'sucess'
    }
    return Response(data)


@swagger_auto_schema(method=[ 'POST'])
@api_view([ 'POST'])
@permission_classes([IsAuthenticated])
def post_tag(request, node_id, tag):
    alfresco.putTag(node_id, tag)
    data = {
        'message': 'sucess'
    }
    return Response(data)


@swagger_auto_schema(
    methods=['POST'],
    parser_classes=(MultiPartParser),
    request_body=FileInputSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def add_file(request):
    data = FileInputSerializer(data=request.data)
    if data.is_valid():
        file = data.validated_data["up_file"]
        filename = str(file)
        value_type = filename.split('.')[-1]

        final_file = Files_upload(
            user=request.user,
            up_file=file,
            data_type=value_type,
            name=filename
        )
        final_file.save()
        alfresco.createFile(data.validated_data["node_id"], filename, file)

        return Response(data={
            'filename': filename
        }, status=201)
    return Response(data.errors)


@swagger_auto_schema(
    methods=['POST'],
    parser_classes=(JSONParser),
    request_body=NodesSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def delete_files(request):
    data = NodesSerializer(data=request.data)
    if data.is_valid():
        for node in data.data['nodes']:
            alfresco.deleteNode(node)
        return Response({
            'message': 'success'
        }, 204)
    return Response(data.errors)


@swagger_auto_schema(method=['POST'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def open_file(request):
    files = Files_upload.objects.filter(user=request.user).all()
    file_name = {}
    for file in files:
        file_name[file.id] = str(file.up_file).split('/')[-1]
    context = {
        "files": FileUploadSerializer(files, many=True).data,
        "file_name": file_name
    }
    return Response(context, status=200)


@swagger_auto_schema(methods=['GET', 'POST'])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def rename_file(request, pk):
    file = Files_upload.objects.get(pk=pk)
    if request.user == file.user:
        form = RenameForm()
        if request.method == "POST":
            form = RenameForm(request.POST or None)
            if form.is_valid():
                file.name = form.cleaned_data['new_name']
                file.save()
                return redirect('dashboard')
        return render(request, 'product/rename_file.html', {'form': form, 'file': file})
    else:
        return redirect('dashboard')


@swagger_auto_schema(method=['GET', 'POST'])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def close(request):
    pass


@swagger_auto_schema(method=['GET', 'POST'])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def open(request, pk):
    file = get_object_or_404(Files_upload, pk=pk)
    if file.data_type == 'pdf':
        pages = convert_from_path(f'{file.up_file}')
        for page in pages:
            page.save('images/out.jpg', 'JPEG')
    elif file.data_type in ('jpeg', 'jpg', 'png'):
        images = file.up_file
    else:
        images = ''
    data = {'images': images}
    return Response(data)


@swagger_auto_schema(method=['GET', 'POST'])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def import_project(request):
    pass


@swagger_auto_schema(method=['GET', 'POST'])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def export_project(request):
    pass


@swagger_auto_schema(method=['GET', 'POST'])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def open_recent(request):
    pass


@swagger_auto_schema(
    methods=['POST'],
    parser_classes=(JSONParser),
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def add_favorite(request, pk):
    file = Files_upload.objects.get(pk=pk)
    if file.user == request.user and file.favorite == False:
        file.favorite = True
        file.save()
    else:
        file.favorite = False
        file.save()
    return Response(status=201)


@swagger_auto_schema(method=['GET'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_list(request):
    queryset = Files_upload.objects.filter(user=request.user, favorite=True)
    files = FileUploadSerializer(queryset, many=True).data
    return Response(files)


@swagger_auto_schema(method=['POST'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_project(request, project_name):
    alfresco.createNewProjectFolder(request, project_name)
    data = {
        'message': 'success'
    }
    return Response(data)


@swagger_auto_schema(
    methods=['POST'],
    request_body=IngestedSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def copy_ingested(request):
    request_data = IngestedSerializer(data=request.data)
    if request_data.is_valid():
        # payload = json.loads(request.body.decode('utf-8'))
        project_name = request_data['project_name']
        project_dir = f'media/users/{request.user}/{project_name}'
        mypath = os.path.join(BASE_DIR, project_dir)
        subprocess.call([f'{BASE_DIR}/preprocess.sh', "-i", mypath])
        for file_id in request_data['ingested']:
            files_upload = Files_upload.objects.get(pk=int(file_id))
            print("==================")
            print(files_upload.up_file)
            content = default_storage.open(files_upload.up_file)
            default_storage.save(
                f'users/{request.user}/{project_name}/{files_upload.name}', content)
            print(files_upload)
        data = {
            'message': 'success'
        }
        return Response(data)
    else:
        return Response(data.errors,status=400)


   


@swagger_auto_schema(
    methods=['POST'],
    parser_classes=[MultiPartParser, FormParser],
    request_body=ProjectFileInputSerializerSwagger,
    operation_description="""
        Create new project,due to drf-yasf limitation we cannot send multiple files
        through swagger, so please use postman to test this API.
        Current documentation is just basic skelton for request body.
    """
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def new_project_view(request, project_name):
    home = alfresco.getUserHome(request)['id']
    request_data = ProjectFileInputSerializer(data=request.data)
    if request_data.is_valid():
        up_files = request_data.validated_data.get('up_files', [])
        txo_files = request_data.validated_data.get('txo_files', [])

        for file in up_files:
            name = str(file).split('/')[-1]
            final_file = ProjectFilesUpload(
                user=request.user, up_file=file, name=name, project_name=project_name)
            alfresco.createFile(home, name, file)
            final_file.save()

        for file in txo_files:
            name = str(file).split('/')[-1]
            final_file = ProjectFilesUpload(
                user=request.user, taxo_file=file, name=name, project_name=project_name
            )
            alfresco.createFile(home, name, file)
            final_file.save()
        return Response(status=201)
    return Response(request_data.errors)


@swagger_auto_schema(
    methods=['GET'],
    parser_classes=[JSONParser],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def get_new_project_view(request, project_name):
    files = Files_upload.objects.filter(user=request.user)
    file_name = {}
    for file in files:
        file_name[file.id] = str(file.up_file).split('/')[-1]
    context = {
        "files": FileUploadSerializer(files, many=True).data,
        'file_name': file_name,
        'user_id': request.user.id,
        'project_name': project_name
    }
    return Response(context)
