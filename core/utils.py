import math
import uuid
import datetime


def gen_uuid() -> str:
    return uuid.uuid4().hex


def gen_time() -> int:
    return math.floor(datetime.datetime.utcnow().timestamp())


def ensure_workflow_output(workflow, data, max_iterations=1):
    if max_iterations == 0:
        print("WARN: Exceeded retries limit but continuing. DATA:", data)
        # raise ValueError("Retried excessively, try different model")
    if max_iterations < 0:
        print("Retry no.", -max_iterations)

    # llm output may throw errors when it fails at the structure check stage
    try:
        return workflow.invoke(data)
    except ValueError:
        return ensure_workflow_output(workflow, data, max_iterations - 1)
