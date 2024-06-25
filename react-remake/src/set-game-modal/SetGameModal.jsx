import { useState, useRef, useEffect } from "react";
import axios from "axios";
import style from "../addGameModal.module.css";

const AddGameModal = ({
  setModalVisible,
  updateGameData,
  selectedGameNames,
  mainGameNameToi,
  selectedGameID,
}) => {
  const [inputs, setInput] = useState([]);
  const [mainGameName, setMainGameName] = useState("");
  const inputRefs = useRef([]);

  useEffect(() => {
    setInput(selectedGameNames);
    setMainGameName(mainGameNameToi);
    console.log(selectedGameNames);
  }, []);

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
    // try {
    //   const response = await axios.get(
    //     `http://localhost:3000/games/${selectedGameID}`
    //   );
    //   const game = response.data;

    //   const updateAdditionalGames = game.additionalGames.map((game) =>
    //     game.name === selectedGameName
    //       ? { ...game, status: selectedStatus, time: parseInt(selectedTime) }
    //       : game
    //   );

    //   if (updateAdditionalGames.length !== 0) {
    //     await axios.put(`http://localhost:3000/games/${selectedGameID}`, {
    //       ...game,
    //       additionalGames: updateAdditionalGames,
    //     });
    //   } else {
    //     await axios.put(`http://localhost:3000/games/${selectedGameID}`, {
    //       ...game,
    //       mainStatus: selectedStatus,
    //     });
    //   }
    // } catch (error) {
    //   console.log("Ошибка при обновлении статуса игры: ", error);
    // }

    try {
      const response = await axios.get(
        `http://localhost:3000/games/${selectedGameID}`
      );

      const game = response.data;

      console.log(inputs);

      await axios.put(`http://localhost:3000/games/${selectedGameID}`, {
        ...game,
        mainName: mainGameName,
      });

      const updateAdditionalGames = inputs.map((input) => ({
        name: input.value,
        status: input.status,
        time: parseInt(input.time),
      }));

      console.log(updateAdditionalGames);

      if (updateAdditionalGames.length !== 0) {
        await axios.put(`http://localhost:3000/games/${selectedGameID}`, {
          ...game,
          additionalGames: updateAdditionalGames,
        });
      }
    } catch (error) {
      console.log("Ошибка при обновлении статуса игры: ", error);
    }

    updateGameData();
    setModalVisible(false);
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
  }, [inputs.length]);

  return (
    <div className={style.modal}>
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
