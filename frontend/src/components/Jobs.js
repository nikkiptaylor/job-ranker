import React, { useEffect, useState } from "react";
import DataTable from "./DataTable";
import Input from "./Input";
import "../styles/Jobs.css";

export default function Jobs() {
  const [jobs, setJobs] = useState(null);
  const [loading, setLoading] = useState(false);
  // const [progress, setProgress] = useState(0);
  const [totalJobs, setTotalJobs] = useState(0);

  const numToClassify = 2;

  const fetchNumJobs = async () => {
    await fetch("http://localhost:8000/num_jobs")
      .then((response) => {
        // const responseJson = response.json();
        console.log(response.num_jobs);
        // TODO: fix this, not working
        setTotalJobs(response.num_jobs);
        console.log(`Fetched total jobs: ${totalJobs}`);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  // Fetch all job classifications
  const fetchJobs = async () => {
    setLoading(true);
    await fetch(`http://localhost:8000/classify/${numToClassify}`)
      .then((response) => {
        const responseJson = response.json();
        console.log(responseJson.result);
        setLoading(false);
        setJobs(responseJson.result);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    // Fetch the total number of job on load
    fetchNumJobs();
  }, [totalJobs]);

  const [inputs, setInputs] = useState([]);

  return (
    <div>
      <Input onClassify={fetchJobs} />
      <div className="loading-container">
        {loading && <div className="loading"></div>}
      </div>
      <DataTable data={jobs} />
    </div>
  );
}
