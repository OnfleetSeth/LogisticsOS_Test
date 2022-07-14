import requests
import json
from utilities import encode_b64


def get_hub_id(api_key, team_id):
    url = f"https://onfleet.com/api/v2/teams/{team_id}"
    payload = {}
    headers = {
        'Authorization': 'Basic ' + encode_b64(api_key)
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = response.json()

    return json_response['hub']


def get_hub_address(api_key, hub_id):
    url = "https://onfleet.com/api/v2/hubs"
    payload = {}
    headers = {
        'Authorization': 'Basic ' + encode_b64(api_key)
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    for r in response.json():
        if r['id'] == hub_id:
            hub_lon = r['location'][0]
            hub_lat = r['location'][1]
            return {"lon": hub_lon, "lat": hub_lat}
        else:
            pass


def get_workers(api_key, team_id):
    url = f"https://onfleet.com/api/v2/workers?teams={team_id}"
    payload = {}
    headers = {
        'Authorization': 'Basic ' + encode_b64(api_key)
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = response.json()
    return json_response


# For now, retrieves all unassigned tasks created since {of_from}, defaulted to -12 hours
def list_tasks(api_key, task_from, task_state):
    tasks = []
    last_id = ()
    payload = {}
    headers = {
        'Authorization': 'Basic ' + encode_b64(api_key)
    }

    i = 1
    while i > 0:
        if i == 1:
            url = f"https://onfleet.com/api/v2/tasks/all?from={task_from}&state={task_state}"
            response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
            last_id = response.get('lastId', '')
            tasks = tasks + response['tasks']
            i += 1
        elif last_id != "":
            url = f"https://onfleet.com/api/v2/tasks/all?from={task_from}&lastId={last_id}&state={task_state}"
            response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
            last_id = response.get('lastId', '')
            tasks = tasks + response['tasks']
            i += 1
        elif last_id == "":
            i = 0

    return tasks


def assign_tasks(results, api_key):
    routes = results['routes']

    for r in routes:
        worker_id = r['summary']['vehicle_id']
        stops = r['stops']
        url = f"https://onfleet.com/api/v2/containers/workers/{worker_id}"

        task_ids = []
        for s in stops:
            task_id = s['id']
            task_ids.append(task_id)

        payload = json.dumps({"tasks": task_ids})
        headers = {
            'Authorization': 'Basic ' + encode_b64(api_key)
        }
        requests.request("PUT", url, headers=headers, data=payload)

    return
