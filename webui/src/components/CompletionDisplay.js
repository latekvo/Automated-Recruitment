import React, { useState } from "react";

export default function CompletionDisplay() {
  const [eligibleResumeCount] = useState(0);
  const [nonEligibleResumeCount] = useState(0);
  const [completedResumes] = useState(
    new Array(0).fill(1).map((v, i) => v * i),
  );

  // Part 1: statistics
  // Part 2: individual results + multi-format download: CSV, spreadsheet, etc.

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
        {completedResumes.length > 0 ? (
          completedResumes.map((value) => <li>Resume entry no. {value}</li>)
        ) : (
          <span>Analyzed resumes will appear here</span>
        )}
      </ul>
    </div>
  );
}
