import requests
import json
from base64 import b64encode
import urllib.parse

defSite = {
    "role": "SiteManager",
    "visibility": "PUBLIC",
    "guid": "b4cff62a-664d-4d45-9302-98723eac1319",
    "description": "This is a Sample Alfresco Team site.",
    "id": "swsdp",
    "preset": "site-dashboard",
    "title": "Sample: Web Site Design Project"
}
host = "http://35.178.166.45"
base_url = 'http://35.178.166.45/alfresco/api/-default-/public/alfresco/versions/1/'
admin_name = 'admin'
admin_password = 'i-0c09541dcba022c1e'
user_password = "preset-alfresco-2020"


def makeAuthHeader(username, password):
    userAndPass = b64encode(bytes("{}:{}".format(username, password), 'ascii')).decode("ascii")
    headers = {'Authorization': 'Basic %s' % userAndPass, 'content-type': 'application/json',
               'Accept': '*/*', 'Connection': 'keep-alive'}
    print(headers)
    return headers


def makeAdminHeader():
    return makeAuthHeader(admin_name, admin_password)


def createPerson(user):
    headers = makeAdminHeader()
    dict_user = json.loads(user.serialize())[0]
    payload = {}
    print(dict_user)
    payload['id'] = "user_" + str(dict_user['pk'])
    payload['email'] = dict_user['fields']['email']
    payload['firstName'] = dict_user['fields']['full_name']
    payload['password'] = user_password
    print(payload)
    url = base_url + 'people'
    requests.post(url, data=json.dumps(payload), headers=headers)

    registerToSite(payload)


    # create Projects Folder on Alfresco in the scope of 'user_id' folder
    user_id = payload['id']
    url = base_url + 'nodes/-root-?relativePath=User Homes/' + user_id + '&include=properties'
    r = requests.get(url, headers=headers)
    children = r.json()
    home_id = children['entry']['id']
    r = createFolder(home_id, 'Projects')
    return r


def registerToSite(userData):
    url = base_url + 'sites/' + defSite['id'] + '/members'
    body = [
        {
            "role": "SiteCollaborator",
            "id": userData['id']
        }
    ]
    print(json.dumps(body))
    headers = makeAdminHeader()
    r = requests.post(url, data=json.dumps(body), headers=headers)
    return r


def getAllSiteNodes():
    url = host + "/alfresco/service/slingshot/doclib/doclist/node/site/" + defSite['id'] + "/documentlibrary/"
    headers = makeAdminHeader()
    r = requests.get(url, headers=headers)

    dict_result = r.json()
    print(dict_result["totalRecords"])
    return r


# https://docs.alfresco.com/6.1/concepts/dev-api-by-language-alf-rest-list-children-root-folder.html

def findNodesFromHome(keyword):
    url = base_url + 'queries/nodes'
    headers = makeAdminHeader()
    params = {
        'term': keyword,
        'rootNodeId': '-my-'
    }
    r = requests.get(url, headers=headers, params=params)
    dict_result = r.json()
    return dict_result


def getUserHomeDirectory(request):
    dict_user = json.loads(request.user.serialize())[0]
    user_id = 'user_' + str(dict_user['pk'])
    print(user_id)
    url = base_url + 'nodes/-root-/children?relativePath=User Homes/' + user_id + '&include=properties'
    print(type(urllib.parse.quote_plus(url)))
    print(urllib.parse.quote_plus(url))
    headers = makeAdminHeader()
    r = requests.get(url, headers=headers)
    children = r.json()
    print(children['list']['entries'])
    return children['list']['entries']


def getUserHome(request):
    dict_user = json.loads(request.user.serialize())[0]
    user_id = 'user_' + str(dict_user['pk'])
    url = base_url + 'nodes/-root-?relativePath=User Homes/' + user_id + '&include=properties'

    headers = makeAdminHeader()
    r = requests.get(url, headers=headers)
    children = r.json()
    return children['entry']


def createNewProjectFolder(request, folder_name):
    print(request.user.id)
    project_home = getFolderByPath(request.user.id, '/Projects')
    created_folder = createFolder(project_home['id'], folder_name)
    return created_folder.json()


def getFolderByPath(user_id, path):
    url = base_url + 'nodes/-root-?relativePath=User Homes/user_' + str(user_id) + path + '&include=properties'
    print("================get folder by path================================")
    print(url)
    headers = makeAdminHeader()
    r = requests.get(url, headers=headers)
    print(r)
    children = r.json()
    return children['entry']


def getFolderChild(node_id):
    print("============get folder child====================")
    print(node_id)
    url = base_url + 'nodes/' + node_id + '/children?include=properties'
    headers = makeAdminHeader()
    r = requests.get(url, headers=headers)
    children = r.json()
    print(children['list']['entries'])
    return children['list']['entries']


def createFolder(node_id, name):

    url = base_url + 'nodes/' + node_id + '/children'
    # url = "http://35.178.166.45/alfresco/api/-default-/public/alfresco/versions/1/nodes/7cdee468-7261-4642-bf11-5b75e863a3dc/children"
    headers = makeAdminHeader()
    print("============creating folder================")
    print(node_id)
    print(name)
    body = {
        "name": str(name),
        "nodeType": "cm:folder"
    }
    r = requests.post(url, data=json.dumps(body), headers=headers)

    print(r)
    return r

def createProjectFile(user_id,project_id, name, file):
    folder_id = getFolderByPath(user_id, '/Projects/'+project_id)['id']
    createFile(folder_id, name, file)

def createFile(node_id, name, file):

    url = base_url + 'nodes/' + node_id + '/children'
    headers = makeAdminHeader()
    headers['content-type'] = None
    print("======uploading file on Alfresco======")
    print(type(file))
    print(headers)
    print("============")
    files = {
        'filedata': file
    }
    data = {
        "name": name,
        "nodeType": "cm:content"
    }

    r = requests.post(url, data=data, headers=headers, files=files)
    if r.status_code == 200:
        result = r.json()
        created_id = result['entry']['id']
        createSharedLink(created_id)
        print(result)
        return result
    else:
        return None


def createSharedLink(node_id):
    print("==========creating sharedLink of node")
    url = base_url + 'shared-links'
    headers = makeAdminHeader()
    data = {
        "nodeId": node_id
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r)
    shared_link_id = r.json()['entry']['id']

    return shared_link_id


def getNode(node_id):
    url = base_url + 'nodes/' + node_id
    headers = makeAdminHeader()
    r = requests.get(url, headers=headers)
    resp = r.json()

    return resp['entry']


def getTags(node_id):
    url = base_url + 'nodes/' + node_id + '/tags'
    headers = makeAdminHeader()
    r = requests.get(url, headers=headers).json()
    return r['list']['entries']


def putTag(node_id, tag):
    url = base_url + 'nodes/' + node_id + '/tags'
    headers = makeAdminHeader()
    body = {"tag": tag}
    r = requests.post(url, data=json.dumps(body), headers=headers).json()
    return r


def getRating(request, node_id):
    url = base_url + 'nodes/' + node_id + '/ratings'
    user = request.user
    dict_user = json.loads(user.serialize())[0]
    user_id = "user_" + str(dict_user['pk'])
    headers = makeAuthHeader(user_id, user_password)

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        resp = r.json()
        return resp['list']['entries']
    else:
        return []


def putRating(user_id, node_id, rating):
    url = base_url + 'nodes/' + node_id + '/ratings'
    headers = makeAuthHeader(user_id, user_password)
    if rating == 100:
        body = {
            "id": "likes",
            "myRating": True
        }
    elif rating == 200:
        print("===========deleting rating from node=================")

        r = requests.delete(url+'/likes', headers=headers)
        print(r)
        return r
    else:
        body = {
            "id": "fiveStar",
            "myRating": int(rating)
        }
    print(body)
    r = requests.post(url, data=json.dumps(body), headers=headers)
    print(r)
    return r


def getDetailedData(entries):
    for item in entries:
        item['tag'] = getTags(item['entry']['id'])
        item['rating'] = getRating(item['entry']['id'])
    return entries


def deleteNode(node_id):
    url = base_url + 'nodes/' + node_id
    headers = makeAdminHeader()
    r = requests.delete(url, headers=headers)
    return r
