from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.database import add_submission

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


@app.post("/submit_answer")
def submit_answer(submission: SubmissionRequest):
    filename = None
    add_submission(
        application_uuid=submission.application_uuid,
        task_uuid=submission.task_uuid,
        filename=filename,
    )


@app.get("/get_question_by_task_uuid")
def submit_answer(task_uuid: str) -> str:
    return "Example question"


class RecruitationScoresResponse(BaseModel):
    video: str
    question: str


@app.get("/get_recruitation_scores")
def submit_answer(recruitment_uuid: str) -> RecruitationScoresResponse:
    pass


class CreateRecruitationRequest(BaseModel):
    title: str
    company: str


@app.post("/add_recruitation")
def submit_answer(req: CreateRecruitationRequest):
    pass
