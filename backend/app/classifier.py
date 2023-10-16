from transformers import pipeline

from huggingface_hub import login
import torch
import pandas as pd
from loguru import logger
from typing import List, Dict

JOBS_PATH = "../data/jobs"


# type = pipe(
#     desc,
#     [
#         "machine learning job",
#         "software engineering job",
#         "project management job",
#     ],
#     multiclass=multiclass,
# )

# exp = pipe(
#     desc,
#     [
#         "0-1 years experience",
#         "1-3 years experience",
#         "3-5 years experience",
#         "5+ years experience",
#     ],
# )
# industry = pipe(
#     desc,
#     [
#         "job at healthcare company",
#         "job at finance company",
#         "job at entertainment company",
#         "job at AI company",
#         "job at animation company",
#         "job at game development company",
#         "job at nonprofit company",
#     ],
#     multiclass=True,
# )
# type = pipe(
#     desc,
#     [
#         "machine learning job",
#         "software engineering job",
#         "project management job",
#     ],
#     multiclass=True,
# )


class JobsClassifier:
    def __init__(self) -> None:
        # Load classifier
        login(token="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")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli"
        )
        logger.info(f"Loaded model with device = {device}")

        # Load jobs
        self.jobs = pd.read_csv(f"{JOBS_PATH}/jobs.csv")
        logger.info(f"Loaded {len(self.jobs)} jobs")

        # Set table to display as original set of jobs to start
        self.display_cols = ["Job Title", "Company", "Job Listing URL"]
        self.classified_jobs = self.jobs[self.display_cols].copy()
        self.classified_jobs.rename({"Job Listing URL": "URL"}, axis=1, inplace=True)

    def classify_all(self, labels: List[str], multi_label: bool = False):
        descriptions = list(self.jobs["Job Description"])
        result = self.pipe(descriptions, labels)
        #  print(result)
        return result

    # todo - finish implementing classify all and use that + pollin instead of iterating

    # def classify_job(
    #     self, i: int, labels: List[str], multi_label: bool = False
    # ) -> Dict[tuple, Dict[str, float]]:
    #     logger.info(f"Classifying job {i}")
    #     desc = self.jobs.loc[i, "Job Description"]
    #     result = self.pipe(desc, labels, multi_label=multi_label)

    #     return self.format_result(i, result)

    # def format_result(
    #     self, i: int, result: Dict[str, float]
    # ) -> Dict[tuple, Dict[str, float]]:
    #     return {
    #         "Job Title": self.jobs.loc[i, "Job Title"],
    #         "Company": self.jobs.loc[i, "Company"],
    #         "URL": self.jobs.loc[i, "Job Listing URL"],
    #         **dict(zip(result["labels"], result["scores"])),
    #     }
