import OnfleetQueries as Oq


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

    def __init__(self, workerid, hubid, hublon, hublat, vehicle_type, capacity):
        self.id = workerid
        self.hub = hubid
        self.hublon = hublon
        self.hublat = hublat
        self.vehicleprofile = vehicle_type.lower()
        self.capacity = capacity

        self.vehiclepayload = {
              "id": self.id,
              "profile": self.vehicleprofile,
              "count": 1,
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


def get_vehicles(teamid):
    vehicles = []

    hubid = Oq.get_hub_id(teamid)
    hub_coord = Oq.get_hub_address(hubid)
    hub_lon = hub_coord['lon']
    hub_lat = hub_coord['lat']

    workers = Oq.get_workers(teamid)

    for w in workers:
        workerid = w['id']
        vehicle_type = w['vehicle']['type']
        capacity = w['capacity']

        vehicle = Vehicles(workerid, hubid, hub_lon, hub_lat, vehicle_type, capacity)

        vehicles.append(vehicle.vehiclepayload)

    return vehicles


def depots(teamid):
    hubid = Oq.get_hub_id(teamid)
    hublon = Oq.get_hub_address(hubid)['lon']
    hublat = Oq.get_hub_address(hubid)['lat']

    depots = [
        {
            "id": hubid,
            "geometry": {
                "zipcode": "null",
                "coordinates": {
                    "lon": hublon,
                    "lat": hublat}
            }
        }
    ]

    return depots
