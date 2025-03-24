import React, { useState } from "react";
import axios from "axios";
import "./Create.css";
function Create() {
  const [task, setTask] = useState();
  const handleAdd = () => {
    if (!task) return;
    axios
      .post("http://localhost:5000/home", { task: task })
      .then((result) => {
        location.reload();
      })
      .catch((err) => console.log(err));
  };
  return (
    <div className="create_form">
      <input
        type="text"
        placeholder="Enter Task"
        onChange={(e) => setTask(e.target.value)}
      />
      <button type="button" onClick={handleAdd}>
        Add
      </button>
    </div>
  );
}
export default Create;
