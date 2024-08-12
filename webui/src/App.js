import React, { useRef } from "react";

import "./App.css";

import FileUpload from "./components/FileUpload";
import CriteriaInput from "./components/CriteriaInput";

export default function App() {
  return (
    <div className="App App-header">
      <div>
        <div className="upload-section">
          <CriteriaInput />
        </div>
        <div className="upload-section">
          <FileUpload />
        </div>
        <div className="upload-section">
          <div>
            <button className="btn btn-primary">Submit</button>
          </div>
        </div>
      </div>
    </div>
  );
}
