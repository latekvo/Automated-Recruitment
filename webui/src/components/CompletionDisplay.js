import React, { useState } from "react";

export default function CompletionDisplay() {
  const [eligibleResumeCount] = useState(0);
  const [nonEligibleResumeCount] = useState(0);
  const [completedResumes] = useState([]);

  // Part 1: statistics
  // Part 2: individual results + multi-format download: CSV, spreadsheet, etc.

  return (
    <div className="container mx-auto p-4 flex flex-row">
      <ul>
        <li>Eligible resumes: {eligibleResumeCount}</li>
        <li>Non-eligible resumes: {nonEligibleResumeCount}</li>
      </ul>
      <ul>
        {completedResumes.map(() => (
          <li>Resume entry</li>
        ))}
      </ul>
    </div>
  );
}
