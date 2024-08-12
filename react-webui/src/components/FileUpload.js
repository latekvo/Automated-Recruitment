import React, { useState } from "react";

export default function FileUpload() {
  const [files, setFiles] = useState([]);

  const handleFileChange = (event) => {
    setFiles([...event.target.files]);
  };

  const handleUpload = () => {
    // Logic to handle file upload, e.g., sending files to a server
    console.log(files);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Multi File Upload</h1>
      <div className="mb-4">
        <input
          type="file"
          multiple
          onChange={handleFileChange}
          className="file-input file-input-bordered file-input-primary w-full max-w-xs"
        />
      </div>
      <div className="mb-4">
        <button onClick={handleUpload} className="btn btn-primary">
          Upload
        </button>
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
