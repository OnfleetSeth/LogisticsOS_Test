import requests
import pprint as p
from datetime import datetime, timedelta
import time
import base64
import json

of_api = "b4523670d4ba81be1c6a2084776093eb"

of_from = int(time.mktime((datetime.today() - timedelta(hours=24)).timetuple()) * 1000)  # See timedelta
of_state = 0  # Task state, 0 = Unassigned tasks


def encode_b64(to_encode):
    encoded_ascii = to_encode.encode('ascii')
    base64_bytes = base64.b64encode(encoded_ascii)
    encoded_b64 = base64_bytes.decode('ascii')

    return encoded_b64


def get_hub_id(teamid):

    url = f"https://onfleet.com/api/v2/teams/{teamid}"

    payload = {}
    headers = {
        'Authorization': 'Basic ' + encode_b64(of_api)
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    return response['hub']


def get_hub_address(hubid):
    url = "https://onfleet.com/api/v2/hubs"

    payload = {}
    headers = {
        'Authorization': 'Basic ' + encode_b64(of_api)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    for r in response.json():
        if r['id'] == hubid:
            hub_lon = r['location'][0]
            hub_lat = r['location'][1]
            break
        else:
            pass

    # print(hub_lon, hub_lat)
    return {"lon": hub_lon, "lat": hub_lat}


def get_workers(teamid):

    url = f"https://onfleet.com/api/v2/workers?teams={teamid}"

    payload = {}
    headers = {
        'Authorization': 'Basic ' + encode_b64(of_api)
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    return response


# For now, retrieves all unassigned tasks created since {of_from}, defaulted to -12 hours
def list_tasks():
    tasks = []
    lastid = ()

    payload = {}
    headers = {
        'Authorization': 'Basic ' + encode_b64(of_api)
    }

    i = 1
    while i > 0:
        if i == 1:
            url = f"https://onfleet.com/api/v2/tasks/all?from={of_from}&state={of_state}"

            response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

            lastid = response.get('lastId', '')

            tasks = tasks + response['tasks']

            i += 1

        elif lastid != "":

            url = f"https://onfleet.com/api/v2/tasks/all?from={of_from}&lastId={lastid}&state={of_state}"
            response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

            lastid = response.get('lastId', '')

            tasks = tasks + response['tasks']
            i += 1
        elif lastid == "":
            i = 0

    # p.pprint(len(tasks))
    return tasks


def assign_tasks(results):

    routes = results['routes']

    for r in routes:
        worker_id = r['summary']['vehicle_id']
        stops = r['stops']
        url = f"https://onfleet.com/api/v2/containers/workers/{worker_id}"

        taskids = []
        for s in stops:
            taskid = s['id']
            taskids.append(taskid)

        payload = json.dumps({"tasks": taskids})
        headers = {
            'Authorization': 'Basic ' + encode_b64(of_api)
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        # print(response.text)

    return
