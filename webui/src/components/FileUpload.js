import React, { useState } from "react";

export default function FileUpload({ filesRef }) {
  const [files, setFiles] = useState([]);
  filesRef.current = files;

  const handleFileChange = (event) => {
    setFiles([...event.target.files]);
    filesRef.current = files;
  };

  return (
    <div className="section container">
      <h1 className="text-2xl font-bold mb-4">Select resumes to analyze</h1>
      <div className="mb-4">
        <input
          type="file"
          multiple
          onChange={handleFileChange}
          className="file-input file-input-bordered file-input-primary w-full max-w-xs"
        />
      </div>
      {files.length > 0 && (
        <div className="mt-4">
          <h2 className="text-lg font-medium mb-2">Selected Files:</h2>
          <ul className="list-disc pl-5">
            {files.length > 0 ? (
              <span>Uploaded resumes: {files.length}</span>
            ) : (
              <span>No resumes uploaded</span>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
