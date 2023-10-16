import React, { useState } from "react";
import "../styles/Input.css";

const Input = ({ onClassify }) => {
  const [currentInput, setCurrentInput] = useState("");
  const [inputList, setInputList] = useState([]);

  const handleInputChange = (event) => {
    setCurrentInput(event.target.value);
  };

  const handleAddInput = () => {
    if (currentInput) {
      setInputList([...inputList, currentInput]);
      setCurrentInput("");
    }
  };

  return (
    <div className="input-container">
      <div className="input-box-container">
        <div className="input-instructions">
          <h2>Add labels for job classifications: </h2>
        </div>

        <input
          type="text"
          className="input-box"
          value={currentInput}
          onChange={handleInputChange}
          placeholder="Enter class label(s)"
        />
        <button className="add-button" onClick={handleAddInput}>
          +
        </button>
      </div>

      <div className="input-list-container">
        <div className="input-list">
          {inputList.map((input, index) => (
            <div key={index} className="input-list-item">
              {input}
            </div>
          ))}
        </div>
      </div>

      <button className="classify-button" onClick={() => onClassify()}>
        Submit
      </button>
    </div>
  );
};

export default Input;
