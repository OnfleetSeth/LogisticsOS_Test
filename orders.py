import OnfleetQueries as Oq


class Orders:

    def __init__(self, taskid, lon, lat, servicetime, completeafter, completebefore, service, servicequantity):
        self.id = taskid
        self.destinationLon = lon
        self.destinationLat = lat
        self.duration = (servicetime * 60)
        self.start = (completeafter / 1000)
        self.end = (completebefore / 1000)

        if service == 'pickup':
            self.pickupQuantity = servicequantity
            self.dropoffQuantity = 0
        elif service == 'dropoff':
            self.dropoffQuantity = servicequantity
            self.pickupQuantity = 0
        else:
            raise Exception("not sure if pickup or dropoff.")

        self.orderpayload = {
              "id": self.id,
              # "cluster_label": "string",
              # "group_priority": null,
              # "order_priority": 1,
              "geometry": {
                # "zipcode": null,
                "coordinates": {
                  "lon": self.destinationLon,
                  "lat": self.destinationLat
                },
                # "curb": false
              },
              "service": {
                "pickup_quantities": self.pickupQuantity,
                "dropoff_quantities": self.dropoffQuantity,
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
def get_orders():
    orders = []
    tasks = Oq.list_tasks()

    for t in tasks:
        taskid = t['id']
        lon = t['destination']['location'][0]
        lat = t['destination']['location'][1]
        servicetime = t['serviceTime']
        completeafter = t['completeAfter']
        completebefore = t['completeBefore']
        servicequantity = t['quantity']

        if t['pickupTask']:
            service = "pickup"
        else:
            service = "dropoff"

        order = Orders(taskid, lon, lat, servicetime, completeafter, completebefore, service, servicequantity)

        orders.append(order.orderpayload)

    return orders
