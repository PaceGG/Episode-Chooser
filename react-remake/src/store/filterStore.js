import { create } from "zustand";
import { persist } from "zustand/middleware";

const useFilterStore = create(
  persist(
    (set) => ({
      statusComplete: false,
      statusBad: false,
      statusWait: false,

      toggleFilter: (id) =>
        set((state) => ({
          [id]: !state[id],
        })),

      setFilter: (filters) =>
        set(filters),
    }),
    {
      name: "filter-storage",
    }
  )
);

export default useFilterStore;