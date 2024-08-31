from __future__ import annotations

import json
from dataclasses import dataclass

from fastapi import FastAPI, UploadFile, File, Form, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from core.cv_evaluator import score_cv_eligibility_verbose, score_cv_eligibility
from core.cv_interface import create_structured_cv_from_path
from core.cv_structures import CriteriaCV
from core.cv_tools import cache_path
from core.utils import gen_uuid

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
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


batch_evaluation_queue = []
evaluated_resumes = []


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

        evaluated_resumes.append(
            CompletedResumeEvaluation(
                parentId=batch_id,
                resume_file_path=file_name,
                is_eligible=eligibility_output.is_eligible,
                explanation=eligibility_output.decision_explanation or None,
            )
        )

    return {"status": "success"}


@app.websocket("/get_resume_evaluation_results")
async def get_resume_evaluation_results(websocket: WebSocket):
    await websocket.accept()
    # 1. send all evaluated resumes
    # 2. send each new collected resume

    await websocket.send_text(f"Hello world")
