from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from database.mongo import collection
from pypdf import PdfReader
import os

app = FastAPI()

app.mount(
"/static",
StaticFiles(directory="static"),
name="static"
)

os.makedirs(
"uploads",
exist_ok=True
)

@app.get("/")
async def home():
    return FileResponse("frontend/index.html")

@app.post("/analyze")
async def analyze_resume(
    resumes: list[UploadFile] = File(...),
    job_description: str = Form(...)
):
    results = []

    jd_text = job_description.lower()

    jd_words = set(
        word.strip(".,()[]{}:;")
        for word in jd_text.split()
        if len(word) > 1
    )

    for resume in resumes:
        file_path = os.path.join(
            "uploads",
            resume.filename
        )

        with open(
            file_path,
            "wb"
        ) as file:
            file.write(
                await resume.read()
            )

        reader = PdfReader(file_path)

        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text.lower()

        resume_words = set(
            word.strip(".,()[]{}:;")
            for word in resume_text.split()
            if len(word) > 1
        )

        matched_words = sorted(
            list(
                jd_words.intersection(
                    resume_words
                )
            )
        )

        missing_words = sorted(
            list(
                jd_words - resume_words
            )
        )

        percentage = round(
            (
                len(matched_words)
                /
                max(len(jd_words), 1)
            ) * 100,
            2
        )

        result = {
            "filename": resume.filename,
            "percentage": percentage,
            "matched_words": matched_words,
            "missing_words": missing_words,
            "matched_count": len(matched_words)
        }

        mongo_result = result.copy()
        collection.insert_one(mongo_result)
        results.append(result)

    results.sort(
        key=lambda x: x["percentage"],
        reverse=True
    )
    best_candidate = results[0] if results else None

    return {
        "best_candidate": best_candidate,
        "ranking": results
    }