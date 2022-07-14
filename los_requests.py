import json
import requests
from datetime import datetime
import time
from utilities import calc_task_from
import of_requests as oq
import orders as o
import vehicles as v


def request(of_api_key, los_api_key, team_id, task_from, task_state):
    url = "https://api.logisticsos.com/latest/vrp"
    task_from = calc_task_from(hours=task_from)

    print("Getting task data from Onfleet.")
    orders = o.get_orders(api_key=of_api_key, task_from=task_from, task_state=task_state)

    print("Getting worker data from Onfleet.")
    depot = v.get_depots(api_key=of_api_key, team_id=team_id)
    vehicles = v.get_vehicles(api_key=of_api_key, team_id=team_id)
    objectives = v.Vehicles.objectives
    # routing_profiles = v.Vehicles.routing_profiles
    units = v.Vehicles.units

    payload = json.dumps(
        {
        "orders": orders,
        "start_depots": depot,
        "vehicle_types": vehicles,
        "objectives": objectives,
        # "routing_profiles": routing_profiles,
        "units": units}
    )
    header = {"x-api-key": los_api_key}
    response = requests.request("POST", url=url, data=payload, headers=header)
    JSON_response = response.json()

    print(JSON_response)
    return JSON_response['job_id']


def get_results(job_id, los_api_key):
    url = f"https://api.logisticsos.com/v1/vrp?job_id={job_id}"
    payload = {}
    headers = {
        'x-api-key': los_api_key
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    JSON_response = response.json()

    # print(response)
    return JSON_response

def main(of_api_key, los_api_key, team_id, task_from=12, task_state=0):
    request_timestamp = datetime.now()
    job_id = request(of_api_key=of_api_key, los_api_key=los_api_key, team_id=team_id, task_from=task_from,
                     task_state=task_state)

    print("Request sent to LogisticsOS.", "Job_ID: " + job_id, "Timestamp: " + str(request_timestamp))
    time.sleep(1)

    start = datetime.now()
    timeout = 18000
    while True:
        if (datetime.now() - start).total_seconds() > timeout:
            raise Exception(f"timed out after {timeout}")

        status = get_results(job_id, los_api_key=los_api_key)['status']

        if status == "IN_QUEUE" or status == 'IN_PROGRESS':
                print(datetime.now(), status)
                time.sleep(3)
        elif status == "SUCCEED":
            completion_timestamp = datetime.now()
            print(status, "Time of completion: " + str(completion_timestamp))
            break
        elif status == "FAILED":
            raise Exception("FAILED")
        else:
            raise Exception(f"unknown status occurred: {status}")

    results = get_results(job_id, los_api_key=los_api_key)

    # with open('/Users/sethlipman/Desktop/data.json', 'x', encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=4)

    print("Assigning tasks to drivers.", datetime.now())
    oq.assign_tasks(results, api_key=of_api_key)

    print()
    print()
    print("Request time: " + str(request_timestamp) + ",", "Completion time: " + str(completion_timestamp) + ",",
          "Run Duration: " + str(completion_timestamp - request_timestamp))

    return


