import math
import uuid
import datetime


def gen_uuid() -> str:
    return uuid.uuid4().hex


def gen_time() -> int:
    return math.floor(datetime.datetime.utcnow().timestamp())


def ensure_workflow_output(workflow, data, max_iterations=8):
    if max_iterations == 0:
        raise ValueError("Retried excessively, try different model")
    # llm output may throw errors when it fails at the structure check stage
    try:
        return workflow.invoke(data)
    except ValueError:
        return ensure_workflow_output(workflow, data, max_iterations - 1)
