import json

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.cv_evaluator import score_cv_eligibility
from core.cv_interface import create_structured_cv_from_path
from core.cv_structures import CriteriaCV
from core.cv_tools import cache_path

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SubmissionRequest(BaseModel):
    application_uuid: str
    task_uuid: str
    video: str


@app.post("/resume_manual_evaluation")
async def resume_manual_evaluation(
    files: list[UploadFile] = File(...), criteria: str = Form(...)
):
    criteria_json = json.loads(criteria)
    criteria_object = CriteriaCV().load(criteria_json)

    processed_resumes = []

    for file in files:
        file_contents = await file.read()
        file_name = file.filename

        f = open(cache_path + file_name, "wb")
        f.write(file_contents)
        f.close()

        structured_cv = create_structured_cv_from_path(file_name)

        # todo: move to an async queue asap, this can't remain here!!!
        eligibility_output = score_cv_eligibility(structured_cv, criteria_object)

        processed_resumes.append(
            {
                "filename": file_name,
                "decision_explanation": eligibility_output.decision_explanation,
                "is_eligible": eligibility_output.is_eligible,
            }
        )

    return {"processed_resumes": processed_resumes}
