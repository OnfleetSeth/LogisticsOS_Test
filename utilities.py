import base64
import time
from datetime import datetime, timedelta


def encode_b64(to_encode):
    encoded_ascii = to_encode.encode('ascii')
    base64_bytes = base64.b64encode(encoded_ascii)
    encoded_b64 = base64_bytes.decode('ascii')

    return encoded_b64


def calc_task_from(hours):
    task_from = int(time.mktime((datetime.today() - timedelta(hours=hours)).timetuple()) * 1000)

    return task_from
