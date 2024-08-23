import { useState, useEffect } from "react";
import axios from "axios";
import "../App.css";

const Filter = () => {
  const [filter, setFilter] = useState({
    statusComplete: false,
    statusBad: false,
    statusWait: false,
  });

  const handleFilterChange = async (event) => {
    const { id, checked } = event.target;
    setFilter((prevFilter) => ({
      ...prevFilter,
      [id]: checked,
    }));
    try {
      // Update server state
      await axios.put(`http://localhost:3000/filters`, {
        ...filter,
        [id]: checked,
      });
    } catch (error) {
      console.error("Error updating filter on server:", error);
    }
  };

  useEffect(() => {
    fetchGames();
  }, []);

  useEffect(() => {}, []);

  const fetchGames = async () => {
    try {
      const response = await axios.get("http://localhost:3000/filters"); // URL вашего json-server
      setFilter(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div
      style={{ display: "flex", flexDirection: "column" }}
      className="filters"
    >
      <label className="filter">
        <input
          type="checkbox"
          name="statusFilter"
          id="statusComplete"
          checked={filter.statusComplete}
          onChange={handleFilterChange}
        />
        <span className="checkmark"></span>
        <span className="textmark complete-textmark"></span>
        <span className="complete-checkbox checkbox-text">Complete</span>
      </label>
      <label className="filter">
        <input
          type="checkbox"
          name="statusFilter"
          id="statusBad"
          checked={filter.statusBad}
          onChange={handleFilterChange}
        />
        <span className="checkmark"></span>
        <span className="textmark complete-textmark"></span>
        <span className="bad-checkbox checkbox-text">Bad</span>
      </label>
      <label className="filter">
        <input
          type="checkbox"
          name="statusFilter"
          id="statusWait"
          checked={filter.statusWait}
          onChange={handleFilterChange}
        />
        <span className="checkmark"></span>
        <span className="textmark complete-textmark"></span>
        <span className="wait-checkbox checkbox-text">Wait</span>
      </label>
    </div>
  );
};
export default Filter;
