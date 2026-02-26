import db from "./db.json";

export const paths = {
  getNames() {
    const names = db.showcase.map((game) => ({
      name: game.name,
      extraName: game.extraName,
      shortName: game.shortName,
      color: game.color,
    }));

    return names;
  },
};
