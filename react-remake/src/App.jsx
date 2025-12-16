import "./App.css";
import HomePage from "./HomePage";
import MonthlyStats from "./recap/MonthlyStats";
import Recap from "./recap/Recap";
import recap from "./recap/recaps/25-11.json";

const App = () => {
  return (
    <>
      <HomePage />
      {/* <MonthlyStats data={recap} /> */}
      {/* <Recap data={recap} /> */}
    </>
  );
};

export default App;
