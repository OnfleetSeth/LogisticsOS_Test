import OnfleetQueries as Oq
import orders as o
import vehicles as v
import json
import requests
import datetime
import time

#LogisticsOS API Key - Provided by Yuzhe
api_key = "esbZv0Yl6C2KmENg3xVkl1BNcxJo9U345DCIQ8h9"


def request(teamid):
    url = "https://api.logisticsos.com/latest/vrp"

    orders = o.get_orders()
    depot = v.depots(teamid)
    vehicles = v.get_vehicles(teamid)
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

    header = {"x-api-key": api_key}

    response = requests.request("POST", url=url, data=payload, headers=header).json()

    # print(response)
    return response['job_id']


def get_results(jobid):
    url = f"https://api.logisticsos.com/v1/vrp?job_id={jobid}"

    payload = {}
    headers = {
        'x-api-key': api_key
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    # print(response)
    return response

def main(teamid):

    job_id = request(teamid)
    time.sleep(1)

    start = datetime.datetime.now()
    timeout = 60
    while True:
        if (datetime.datetime.now() - start).total_seconds() > timeout:
            raise Exception(f"timed out after {timeout}")

        status = get_results(job_id)['status']

        if status == "IN_QUEUE" or status == 'IN_PROGRESS':
                print(status)
                time.sleep(3)
        elif status == "SUCCEED":
            break
        elif status == "FAILED":
            raise Exception("FAILED")
        else:
            raise Exception(f"unknown status occurred: {status}")

    results = get_results(job_id)
    print(results)

    Oq.assign_tasks(results)


teamid = "fNdxArKxuQophW2ACcg~8F8J"

if __name__ == '__main__':
    main(teamid)


