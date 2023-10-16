from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .classifier import JobsClassifier
from loguru import logger

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "*localhost:3000",
    "http://127.0.0.1",
    "http://10.0.0.225:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome."}


clf = JobsClassifier()

label_sets = [
    {
        "labels": [
            "machine learning job",
            "software engineering job",
            "project management job",
        ],
        "multi_label": True,
    },
    {
        "labels": [
            "0-1 years experience",
            "1-3 years experience",
            "3-5 years experience",
            "5+ years experience",
        ],
        "multi_label": False,
    },
]


@app.get("/num_jobs")
async def num_jobs():
    return {"num_jobs": len(clf.jobs)}


# TODO: post method to set the labels

# TODO: get method to get the current progress, if possible

@app.get("/jobs")
async def get_jobs():
    


@app.get("/classify/{num_jobs}")
async def classify_jobs(num_jobs: int):
    # all_results = {"Job Title": "titile", "URL": 123, "class": 0.234}
    results_list = []
    for i in range(num_jobs):
        all_results = {}
        for labels in label_sets:
            all_results = {**all_results, **clf.classify_job(i, **labels)}
        results_list.append(all_results)
    logger.info(f"Classified all job at index i.")
    return_val = {"result": results_list}
    logger.info(f"result: {return_val}")
    return return_val


# @app.get("/num_jobs/{i}")
# async def classify_job_index(i: int):
#     n_jobs = 1
#     await websocket.send_json({"loading": True, "total_jobs": n_jobs})
#     all_results = {}

#     for i in range(n_jobs):
#         for labels in EXAMPLE_LABELS:
#             # Update the progress
#             progress = i + 1
#             all_results = {
#                 **all_results,
#                 **clf.classify_job(i, **labels),
#             }
#             await websocket.send_json({"progress": progress})
#     logger.info(f"Classified all {n_jobs} jobs.")
#     await websocket.send_json({"result": all_results})


# @app.get("/jobs", tags=["jobs"])
# async def get_jobs() -> dict:
#     return {"data": classify_jobs(1)}
