import of_requests as of


class Orders:

    def __init__(self, task_id, lon, lat, service_time, complete_after, complete_before, service, service_quantity):
        self.id = task_id
        self.destination_Lon = lon
        self.destination_Lat = lat
        self.duration = (service_time * 60)
        self.start = (complete_after / 1000)
        self.end = (complete_before / 1000)

        if service == 'pickup':
            self.pickup_quantity = service_quantity
            self.dropoff_quantity = 0
        elif service == 'dropoff':
            self.dropoff_quantity = service_quantity
            self.pickup_quantity = 0
        else:
            raise Exception("not sure if pickup or dropoff.")

        self.order_payload = {
              "id": self.id,
              # "cluster_label": "string",
              # "group_priority": null,
              # "order_priority": 1,
              "geometry": {
                # "zipcode": null,
                "coordinates": {
                  "lon": self.destination_Lon,
                  "lat": self.destination_Lat
                },
                # "curb": false
              },
              "service": {
                "pickup_quantities": self.pickup_quantity,
                "dropoff_quantities": self.dropoff_quantity,
                "duration": self.duration
              },
              "time_window": {
                "start": self.start,
                "end": self.end
              },
              # "paired_order": "string"
            }


# Call OF List Tasks and read data:
# taskId, destination long/lat, service time, completion window, quantity, pickup or dropoff
# Instantiate orders
def get_orders(api_key, task_from, task_state):
    orders = []
    tasks = of.list_tasks(api_key, task_from, task_state)

    for t in tasks:
        task_id = t['id']
        lon = t['destination']['location'][0]
        lat = t['destination']['location'][1]
        service_time = t['serviceTime']
        complete_after = t['completeAfter']
        complete_before = t['completeBefore']
        service_quantity = t['quantity']

        if t['pickupTask']:
            service = "pickup"
        else:
            service = "dropoff"

        order = Orders(task_id, lon, lat, service_time, complete_after, complete_before, service, service_quantity)

        orders.append(order.order_payload)

    return orders
