import { useState, useRef, useEffect } from "react";
import style from "./addGameModal.module.css";

const AddGameModal = ({ setModalVisible, updateGameData }) => {
  const [inputs, setInput] = useState([]);
  const [mainGameName, setMainGameName] = useState("");
  const inputRefs = useRef([]);

  const handleMainGameNameChange = (e) => {
    setMainGameName(e.target.value);
  };

  const addInput = () => {
    setInput((prevInput) => [...prevInput, { id: Date.now(), value: "" }]);
  };

  const removeInput = (id) => {
    setInput((prevInputs) => prevInputs.filter((input) => input.id !== id));
    inputRefs.current.splice(inputRefs.length, 1);
  };

  const handleInputChange = (id, newValue) => {
    setInput((prevInputs) =>
      prevInputs.map((input) =>
        input.id === id ? { ...input, value: newValue } : input
      )
    );
  };

  const handleConfirm = async () => {
    const gameData = {
      mainName: mainGameName,
      additionalGames: inputs.map((input) => ({
        name: input.value,
        status: "none",
        time: 0,
      })),
    };
    try {
      const response = await fetch("http://localhost:3000/games", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(gameData),
      });

      if (response.ok) {
        updateGameData(); // Обновление данных в GameList
        setInput([]);
        setMainGameName("");
        setModalVisible(false);
      } else {
        console.error("Error saving data:", response.statusText);
      }
    } catch (error) {
      console.error("Error saving data:", error);
    }
  };

  const cancelConirm = () => {
    setInput([]);
    setMainGameName("");
    setModalVisible(false);
  };

  useEffect(() => {
    if (
      inputRefs.current.length > 0 &&
      inputRefs.current[inputRefs.current.length - 1]
    ) {
      inputRefs.current[inputRefs.current.length - 1].focus();
    }
  }, [inputs]);

  return (
    <div className={style.modal}>
      <img src="" alt="" />
      <input
        id="mainGameName"
        placeholder="Main game name"
        value={mainGameName}
        onChange={handleMainGameNameChange}
      />
      <div className={style.moreGames}>
        {inputs.map((input, index) => (
          <div key={input.id} style={{ display: "flex", alignItems: "center" }}>
            <input
              ref={(el) => (inputRefs.current[index] = el)}
              type="text"
              placeholder={`Game ${index + 1}`}
              value={input.value}
              onChange={(e) => handleInputChange(input.id, e.target.value)}
            />
            <button onClick={() => removeInput(input.id)}>X</button>
          </div>
        ))}
      </div>
      <button onClick={addInput}>+ add more game</button>
      <div className={style.modalButtons}>
        <button onClick={handleConfirm}>Confirm</button>
        <button onClick={cancelConirm}>Cancel</button>
      </div>
    </div>
  );
};

export default AddGameModal;
