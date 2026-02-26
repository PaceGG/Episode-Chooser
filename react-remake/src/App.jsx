import "./App.css";
import HomePage from "./HomePage";
import Schedule from "./schedule/Schedule";
import MonthlyStats from "./recap/MonthlyStats";
import Recap from "./recap/Recap";
import recap from "./recap/recaps/25-11.json";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import DragAndDropDemo from "./schedule/Draggable";

const App = () => {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/recap" element={<Recap data={recap} />} />
          <Route path="/stats" element={<MonthlyStats data={recap} />} />
          <Route path="/plan" element={<Schedule />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
