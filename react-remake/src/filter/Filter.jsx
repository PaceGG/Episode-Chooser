import { useState, useEffect } from "react";
import axios from "axios";

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
    <div style={{ display: "flex", flexDirection: "column" }}>
      <label>
        <input
          type="checkbox"
          name="statusFilter"
          id="statusComplete"
          checked={filter.statusComplete}
          onChange={handleFilterChange}
        />
        Complete
      </label>
      <label>
        <input
          type="checkbox"
          name="statusFilter"
          id="statusBad"
          checked={filter.statusBad}
          onChange={handleFilterChange}
        />
        Bad
      </label>
      <label>
        <input
          type="checkbox"
          name="statusFilter"
          id="statusWait"
          checked={filter.statusWait}
          onChange={handleFilterChange}
        />
        Wait
      </label>
    </div>
  );
};
export default Filter;
