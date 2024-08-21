import React, { useState } from "react";

const formFields = [
  {
    name: "jobTitle",
    label: "Job Title",
    type: "text",
    defaultValue: "",
  },
  {
    name: "jobDescription",
    label: "Job Description",
    type: "textarea",
    defaultValue: "",
  },
  {
    name: "requiredTechnologies",
    label: "Required Technologies (comma separated)",
    type: "text",
    defaultValue: "",
  },
  {
    name: "requiredSkills",
    label: "Required Skills (comma separated)",
    type: "text",
    defaultValue: "",
  },
  {
    name: "education",
    label: "Education",
    type: "text",
    defaultValue: "",
  },
  {
    name: "totalExperience",
    label: "Total Experience",
    type: "text",
    defaultValue: "",
  },
  {
    name: "commercialExperience",
    label: "Commercial Experience",
    type: "text",
    defaultValue: "",
  },
  {
    name: "privateExperience",
    label: "Private Experience",
    type: "text",
    defaultValue: "",
  },
];

export default function CriteriaInput({ criteriaRef }) {
  const [formData, setFormData] = useState({
    jobTitle: "not specified",
    jobDescription: "not specified",
    requiredTechnologies: "",
    requiredSkills: "",
    education: "",
    totalExperience: "",
    commercialExperience: "",
    privateExperience: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    criteriaRef.current = formData;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Split comma-separated fields into arrays
    const formattedData = {
      ...formData,
      requiredTechnologies: formData.requiredTechnologies
        .split(",")
        .map((item) => item.trim()),
      requiredSkills: formData.requiredSkills
        .split(",")
        .map((item) => item.trim()),
    };
    console.log(formattedData);
    // Handle form submission, e.g., send data to a server
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Job Form</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {formFields.map((field) => (
          <div className="criteria-entry" key={field.name}>
            <label className="label" htmlFor={field.name}>
              {field.label}
            </label>
            {field.type === "textarea" ? (
              <textarea
                id={field.name}
                name={field.name}
                value={formData[field.name]}
                onChange={handleChange}
                className="textarea textarea-bordered "
              />
            ) : (
              <input
                type={field.type}
                id={field.name}
                name={field.name}
                value={formData[field.name]}
                onChange={handleChange}
                className="input input-bordered"
              />
            )}
          </div>
        ))}
      </form>
    </div>
  );
}
