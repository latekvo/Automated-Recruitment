import React, { useRef } from "react";
import axios from "axios";

import "./App.css";

import FileUpload from "./components/FileUpload";
import CriteriaInput from "./components/CriteriaInput";

export default function App() {
  const files = useRef([]);
  const criteria = useRef({});

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    files.current.forEach((file) => {
      formData.append(`files`, file);
    });
    formData.append("criteria", JSON.stringify(criteria.current));

    try {
      const response = await axios.post(
        "http://localhost:8000/resume_manual_evaluation",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );
      console.log("File uploaded successfully:", response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="App App-header">
      <div>
        <div className="upload-section">
          <CriteriaInput criteriaRef={criteria} />
        </div>
        <div className="upload-section">
          <FileUpload filesRef={files} />
        </div>
        <div className="upload-section">
          <div>
            <button className="btn btn-primary" onClick={handleSubmit}>
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
