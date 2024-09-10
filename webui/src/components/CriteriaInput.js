import React, { useState } from "react";

const formFields = [
  {
    name: "job_title",
    label: "Job Title",
    type: "text",
    defaultValue: "",
  },
  {
    name: "job_description",
    label: "Job Description",
    type: "textarea",
    defaultValue: "",
  },
  {
    name: "required_technologies",
    label: "Required Technologies (comma separated)",
    type: "text",
    defaultValue: "",
  },
  {
    name: "required_skills",
    label: "Required Skills (comma separated)",
    type: "text",
    defaultValue: "",
  },
  {
    name: "education",
    label: "Education requirements",
    type: "text",
    defaultValue: "",
  },
  {
    name: "total_experience",
    label: "Expected minimal experience",
    type: "text",
    defaultValue: "",
  },
  {
    name: "commercial_experience",
    label: "Preferred commercial experience",
    type: "text",
    defaultValue: "",
  },
  {
    name: "private_experience",
    label: "Preferred additional experience",
    type: "text",
    defaultValue: "",
  },
];

export default function CriteriaInput({ criteriaRef }) {
  const [formData, setFormData] = useState({
    job_title: "not specified",
    job_description: "not specified",
    required_technologies: "",
    required_skills: "",
    education: "",
    total_experience: "",
    commercial_experience: "",
    private_experience: "",
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
    <div className="container mx-auto p-4 h-full">
      <h1 className="text-2xl font-bold mb-4">Candidate requirements</h1>
      <form onSubmit={handleSubmit} className=" justify-evenly">
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
