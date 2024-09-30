import React, { useContext, useEffect, useMemo, useRef, useState } from "react";
import UrlContext from "../context/UrlContext";

export default function CompletionDisplay() {
  const storedResumes = useRef([]);
  const [displayedResumes, setDisplayedResumes] = useState([]);
  const urlContext = useContext(UrlContext);

  // Part 1: statistics
  // Part 2: individual results + multi-format download: CSV, spreadsheet, etc.

  useEffect(() => {
    const socket = new WebSocket(
      urlContext.websocketUrl + "get_resume_evaluation_results"
    );

    storedResumes.current = [];
    socket.onmessage = (event) => {
      const deserialized_data = JSON.parse(event.data);

      storedResumes.current.push(deserialized_data);
      setDisplayedResumes([...storedResumes.current]);
    };
  }, [setDisplayedResumes]);

  let eligibleResumeCount = 0;
  let nonEligibleResumeCount = 0;

  for (const resume of displayedResumes) {
    if (resume["is_eligible"]) {
      eligibleResumeCount++;
    } else {
      nonEligibleResumeCount++;
    }
  }

  return (
    <div className="section container grid grid-rows-[auto_auto_1fr] h-full">
      <div>
        <h1 className="text-2xl font-bold mb-4 mr-4 break w-full">
          Evaluation results
        </h1>
        <ul>
          <li>Eligible resumes: {eligibleResumeCount}</li>
          <li>Non-eligible resumes: {nonEligibleResumeCount}</li>
        </ul>
      </div>
      <div className="divider"></div>
      <ul className="overflow-scroll h-full">
        {displayedResumes.length > 0 ? (
          displayedResumes.map((resume) => (
            <li key={resume["resume_file_path"]}>{JSON.stringify(resume)}</li>
          ))
        ) : (
          <span>Analyzed resumes will appear here</span>
        )}
      </ul>
    </div>
  );
}
