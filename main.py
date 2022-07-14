import los_requests as los

# The team of drivers to be assigned tasks
TEAM_ID = "h4BBAdzoj3AaVtuK0SwE3~rz"

OF_API_KEY = "24bb3ed7b12129427d449c91e948a7bb"
LOS_API_KEY = "esbZv0Yl6C2KmENg3xVkl1BNcxJo9U345DCIQ8h9"

# Value represents task create time in hours passed, i.e. from n hours ago until now (None=12)
TASK_FROM = 12

# State of tasks to retrieve - (0: Unassigned, 1: Assigned, 2: Active, 3: Complete). (None=0)
TASK_STATE = 0

if __name__ == '__main__':
    los.main(of_api_key=OF_API_KEY, los_api_key=LOS_API_KEY, team_id=TEAM_ID, task_from=TASK_FROM,
             task_state=TASK_STATE)
