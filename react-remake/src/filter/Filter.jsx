import { useState, useEffect } from "react";
import "../App.css";
import useFilterStore from "../store/filterStore";

const Filter = () => {
  const { statusComplete, statusBad, statusWait, toggleFilter } =
    useFilterStore();

  const handleFilterChange = (event) => {
    toggleFilter(event.target.id);
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
          checked={statusComplete}
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
          checked={statusBad}
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
          checked={statusWait}
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
