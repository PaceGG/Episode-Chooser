import { useState, useEffect } from "react";
import axios from "axios";

const Links = () => {
  const [links, setGames] = useState([]);

  useEffect(() => {
    fetchGames(); // Изначальная загрузка данных при монтировании компонента
  }, []);

  const fetchGames = async () => {
    try {
      const response = await axios.get("http://localhost:3000/links"); // URL вашего json-server
      setGames(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="links">
      {links.map((link) => (
        <a key={link.id} href={link.name} target="_blank">
          <img src={link.img} alt="" />
        </a>
      ))}
    </div>
  );
};

export default Links;
