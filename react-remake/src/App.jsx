import { useState } from "react";
import AddGameModal from "./addGameModal.jsx";
import style from "./addGameModal.module.css";
import GameList from "./game-list/GameList.jsx";
import GameShowcase from "./game-showcase/GameShowcase.jsx";

const App = () => {
  const [isModalVisible, setModalVisible] = useState(false);

  // eslint-disable-next-line no-unused-vars
  const handleButtonClick = () => {
    setModalVisible(true);
  };

  return (
    <div className={style.modalButtonContainer}>
      {isModalVisible && <AddGameModal setModalVisible={setModalVisible} />}
      <GameShowcase />
      <GameList />
    </div>
  );
};

export default App;
