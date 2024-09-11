import React, { useEffect, useMemo, useRef, useState } from "react";
import axios from "axios";

import "./App.css";

import FileUpload from "./components/FileUpload";
import CriteriaInput from "./components/CriteriaInput";
import CompletionDisplay from "./components/CompletionDisplay";

export default function App() {
  const files = useRef([]);
  const criteria = useRef({});
  const [results, setResults] = useState([]);

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

  const socket = useMemo(
    () => new WebSocket("ws://localhost:8000/get_resume_evaluation_results"),
    [],
  );

  useEffect(() => {
    socket.addEventListener("open", () => {
      console.log("Connection established");
    });

    socket.addEventListener("message", (event) => {
      console.log("Received resume:", event.data);

      const combinedResults = [...results, event.data];
      console.log("All completions so far:", combinedResults);

      setResults(combinedResults);
    });
  }, [results, socket]);

  return (
    <div className="root grid grid-cols-2 gap-2 p-2">
      <CriteriaInput criteriaRef={criteria} />
      <div className="grid grid-rows-[auto_auto_1fr] gap-2 h-full">
        <FileUpload filesRef={files} />
        <div className="section">
          <h1 className="inline ml-2 mr-4">
            Start processing uploaded resumes
          </h1>
          <button className="btn btn-primary" onClick={handleSubmit}>
            Submit
          </button>
        </div>
        <CompletionDisplay />
      </div>
    </div>
  );
}
