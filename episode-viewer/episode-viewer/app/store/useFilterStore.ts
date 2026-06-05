import { create } from "zustand";
import { persist } from "zustand/middleware";

const useFilterStore = create(
  persist(
    (set) => ({
      statusComplete: true,
      statusBad: true,
      statusWait: true,

      toggleFilter: (id) =>
        set((state) => ({
          [id]: !state[id],
        })),

      setFilter: (filters) => set(filters),
    }),
    {
      name: "filter-storage",
    },
  ),
);

export default useFilterStore;
