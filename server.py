from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    print("upload request:", files, criteria)
    file_info = []
    for file in files:
        file_info.append(
            {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(await file.read()),
            }
        )

    return {"status": "success"}
