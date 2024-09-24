from __future__ import annotations

import dataclasses
import json
import os
from dataclasses import dataclass

from fastapi import FastAPI, UploadFile, File, Form, WebSocket, WebSocketException
from fastapi.middleware.cors import CORSMiddleware

from core.cv_evaluator import score_cv_eligibility_verbose, score_cv_eligibility
from core.cv_interface import create_structured_cv_from_path
from core.cv_structures import CriteriaCV
from core.cv_tools import cache_path
from core.utils import gen_uuid

app = FastAPI()
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# todo: rewrite to use postgres instead of filesystem
@dataclass
class BatchResumeManualEvaluationTask:
    batchId: str
    criteria: str
    resume_file_paths: list[str]


# todo: rewrite to use postgres instead of filesystem
@dataclass
class CompletedResumeEvaluation:
    parentId: str  # batch or requester
    resume_file_path: str
    is_eligible: bool
    explanation: str | None  # only available with verbose mode, compute-heavy


def serialize_evaluation(
    evaluation_to_serialize: CompletedResumeEvaluation,
):
    evaluation_json = dataclasses.asdict(evaluation_to_serialize)
    return json.dumps(evaluation_json)


batch_evaluation_queue: list[BatchResumeManualEvaluationTask] = []
observers: list[WebSocket] = []


evaluations_filepath = "evaluations.json"


def load_evaluated_resumes() -> list[str]:
    try:
        with open(cache_path + evaluations_filepath, "r") as file:
            dict_list = json.load(file)
            return dict_list
    except FileNotFoundError:
        return []


def save_evaluated_resumes():
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path + evaluations_filepath, "w") as file:
        serialized = json.dumps(evaluated_resumes)
        file.write(serialized)


# storing as string for now as they'll be only ever read in that format for now
evaluated_resumes: list[str] = load_evaluated_resumes()


def add_evaluated_resume(evaluation: CompletedResumeEvaluation):
    serialized_evaluation = serialize_evaluation(evaluation)
    evaluated_resumes.append(serialized_evaluation)
    save_evaluated_resumes()
    for observer in observers:
        try:
            observer.send_text(serialized_evaluation)
        except WebSocketException:
            observer.close()
            observers.remove(observer)


@app.post("/resume_manual_evaluation")
async def resume_manual_evaluation(
    files: list[UploadFile] = File(...), criteria: str = Form(...)
):
    batch_id = gen_uuid()
    criteria_json = json.loads(criteria)
    criteria_object = CriteriaCV().load(criteria_json)

    verbose_mode = False

    for file in files:
        file_contents = await file.read()
        file_name = file.filename

        f = open(cache_path + file_name, "wb")
        f.write(file_contents)
        f.close()

        structured_cv = create_structured_cv_from_path(file_name)

        # todo: move to an async queue asap, this can't remain here!!!
        if verbose_mode:
            eligibility_output = score_cv_eligibility_verbose(
                structured_cv, criteria_object
            )
        else:
            eligibility_output = score_cv_eligibility(structured_cv, criteria_object)

        add_evaluated_resume(
            CompletedResumeEvaluation(
                parentId=batch_id,
                resume_file_path=file_name,
                is_eligible=eligibility_output.is_eligible,
                explanation=(
                    eligibility_output.decision_explanation
                    if "decision_explanation" in eligibility_output
                    else None
                ),
            )
        )

    return {"status": "success"}


@app.websocket("/get_resume_evaluation_results")
async def get_resume_evaluation_results(websocket: WebSocket):
    await websocket.accept()
    # 1. send all evaluated resumes
    # 2. send each new collected resume via completion callbacks

    for resume in evaluated_resumes:
        await websocket.send_text(resume)

    observers.append(websocket)
