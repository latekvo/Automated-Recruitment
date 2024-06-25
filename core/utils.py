import math
import uuid
import datetime


def gen_uuid() -> str:
    return uuid.uuid4().hex


def gen_time() -> int:
    return math.floor(datetime.datetime.utcnow().timestamp())
