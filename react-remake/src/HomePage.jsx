import AddGameModal from "./addGameModal.jsx";
import style from "./addGameModal.module.css";
import GameList from "./game-list/GameList.jsx";
import GameShowcase from "./game-showcase/GameShowcase.jsx";
import Links from "./links/Links.jsx";
import Filter from "./filter/Filter.jsx";
import { useState } from "react";

export default function HomePage() {
  const [isModalVisible, setModalVisible] = useState(false);

  // eslint-disable-next-line no-unused-vars
  const handleButtonClick = () => {
    setModalVisible(true);
  };

  return (
    <div className={style.modalButtonContainer}>
      {isModalVisible && <AddGameModal setModalVisible={setModalVisible} />}
      <div className="main-content">
        <div className="useful-links">
          <Links />
        </div>
        <div className="games-list">
          <div className="header">Games List</div>
          <div className="game-content">
            <GameShowcase />
            <GameList />
          </div>
        </div>
        <Filter />
      </div>
    </div>
  );
}
