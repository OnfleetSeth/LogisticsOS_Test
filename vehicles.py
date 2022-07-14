import of_queries as oq


class Vehicles:
    objectives = [
                "minimize_cost",
                "less_mileage",
                "less_duration",
                "fewer_vehicles"
              ]

    routing_profiles = [
                {
                  "name": "car",
                  "base_profile": "car"
                }
              ]

    units = {
                "distance": "mile",
                "duration": "second"
              }

    def __init__(self, worker_id, hub_id, hub_lon, hub_lat, vehicle_type, capacity):
        self.id = worker_id
        self.hub = hub_id
        self.hub_lon = hub_lon
        self.hub_lat = hub_lat
        self.vehicle_profile = vehicle_type.lower()
        self.capacity = capacity

        self.vehicle_payload = {
              "id": self.id,
              "profile": self.vehicle_profile,
              "count": 25,
              "capacity": self.capacity,
              "dispatch_after": 0,
              # "dismiss_before": "inf",
              # "max_distance": "inf",
              # "max_travel_time": "inf",
              # "max_total_time": "inf",
              "max_late_time": 0,
              "max_orders_per_route": 100,
              # "overtime_start_time": "inf",
              "avoid_wait_time": False,
              "use_all_vehicles": False,
              "depots": {
                "start_depot": self.hub,
                "end_depot": "any"
              }
        }


def get_vehicles(api_key, team_id):
    vehicles = []
    hub_id = oq.get_hub_id(api_key, team_id)
    hub_coord = oq.get_hub_address(api_key, hub_id)
    hub_lon = hub_coord['lon']
    hub_lat = hub_coord['lat']

    workers = oq.get_workers(api_key, team_id)

    for w in workers:
        worker_id = w['id']
        vehicle_type = w['vehicle']['type']
        capacity = w['capacity']
        vehicle = Vehicles(worker_id, hub_id, hub_lon, hub_lat, vehicle_type, capacity)
        vehicles.append(vehicle.vehicle_payload)

    return vehicles


def get_depots(api_key, team_id):
    hub_id = oq.get_hub_id(api_key, team_id)
    hub_lon = oq.get_hub_address(api_key, hub_id)['lon']
    hub_lat = oq.get_hub_address(api_key, hub_id)['lat']

    depots = [
        {
            "id": hub_id,
            "geometry": {
                "zipcode": "null",
                "coordinates": {
                    "lon": hub_lon,
                    "lat": hub_lat}
            }
        }
    ]

    return depots
