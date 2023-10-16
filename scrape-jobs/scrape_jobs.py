from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
from time import perf_counter, sleep
from os import makedirs
from typing import List
from tqdm import tqdm
from datetime import datetime
from json import dump, load
import re

JOBS_PATH = "../data/jobs"


class JobScraper:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        try:
            makedirs("./jobs/urls")
        except:
            print("Jobs directory already exists, not creating new")

    @staticmethod
    def get_link_text(l: str):
        return l.get_attribute("href")

    def get_urls(self, max_pages=150) -> List[str]:
        """Get initial list of URls by going through all pages

        Args:
            max_pages (int, optional): Max number of pages to scrape from. Defaults to 10.
            only_sf (bool, optional): Pre-filter by jobs 50 miles within SF or remote

        Returns:
            List[str]: List of URL strings of jobs
        """
        print(f"Finding URLs from max {max_pages} pages.")
        t1_start = perf_counter()
        all_job_urls = []

        # Iterate through pages to get job links
        for page in tqdm(range(1, max_pages + 1)):
            url = f"https://www.employbl.com/jobs?page={page}"

            try:
                self.driver.get(url)
            except Exception as e:
                print(f"Exception getting page {page} at url {url}: {e}. Stopping now.")
                break
            # TODO: make this actually wait until elements render, currently just estimating
            sleep(1)

            # Find links by html tag
            links = self.driver.find_elements(By.TAG_NAME, "a")
            link_texts = list(map(self.get_link_text, links))
            job_urls = [l for l in link_texts if re.search(".*/jobs/\w", l)]

            # Only match jobs link within employabl
            if not job_urls:
                print(f"No job urls found on page {page}. Stopping.")
                break
            else:
                all_job_urls.extend(job_urls)

        t1_stop = perf_counter()
        print(
            f"Found {len(all_job_urls)} jobs in {page} pages in {t1_stop - t1_start} seconds"
        )

        # Save to versioned json
        save_file = f"jobs/urls/{datetime.now().strftime('%Y_%m_%d_%H_%M')}.json"
        with open(save_file, "w") as f:
            dump({"urls": all_job_urls, "pages_searched": page}, f)
        return all_job_urls

    def get_job_data(self, job_url: str) -> List[str]:
        """Get dataframe of content for a given job url

        Args:
            job_url (str): URL for job page

        Returns:
            List[str]: list with with content of job page
        """
        self.driver.get(job_url)
        sleep(1)
        job_text = str(self.driver.find_element(By.XPATH, "/html/body").text)
        formatted = self.format_job_data(job_text.split("\n"))
        if formatted:
            return {**formatted, "Employabl URL": job_url}
        else:
            return {}

    @staticmethod
    def format_job_data(job_contents: List[str]) -> pd.DataFrame:
        try:
            desc_end = ["View Job Listing" in x for x in job_contents].index(True)
            description = "/n".join(job_contents[23:desc_end])
            return {
                "Company": job_contents[10],
                "Job Title": job_contents[11],
                "Location": job_contents[19],
                "Job Listing URL": job_contents[21],
                "Job Description": description,
                "Headquarters Location": job_contents[desc_end + 2],
                "Company Size": job_contents[desc_end + 5],
                "Founded Year": job_contents[desc_end + 7],
            }
        except:
            print(f"View job listing not found in {job_contents}. Saving empty dict")
            return {}

    def create_job_dataframe(self, urls: List[str] = None) -> None:
        """Create a dataframe with job data for the given urls. Only retrieve data for URLs not already in saved job dataframe.

        Args:
            urls (List[str]): List of urls
        """
        if not urls:
            urls = self.get_urls()

        # Only get data for new jobs
        try:
            existing_df = pd.read_csv(f"{JOBS_PATH}//jobs.csv")
            url_subset = [
                url for url in urls if url not in list(existing_df["Employabl URL"])
            ]
        except Exception as e:
            print(e)
            print("No existing jobs df. Starting fresh")
            existing_df = pd.DataFrame()
            url_subset = urls

        try:
            all_data = []
            print(f"Getting job data for {len(url_subset)} jobs.")
            for url in tqdm(url_subset):
                all_data.append(self.get_job_data(url))
        except Exception as e:
            print(f"Stopped: error {e}")

        df = pd.DataFrame.from_records(all_data)
        combined_df = pd.concat([df, existing_df])
        combined_df.to_csv("jobs/jobs.csv")


# Separate script
# TODO: Parse out interesting parts of job description

# TODO: Set up chatgpt with api to do a rating of how qualified I am, how much I would like it.

# TODO: sort by how qualified

# t2_start = perf_counter()
# for job_url in job_link_texts[0:5]:

# t2_stop = perf_counter()
# print(f"Time for 5 jobs: {t2_stop - t2_start} seconds")
if __name__ == "__main__":
    print("Starting...")
    j = JobScraper()
    urls = load(open(f"{JOBS_PATH}//urls/2023_07_24_20_54.json", "r"))["urls"]
    j.create_job_dataframe(urls)
