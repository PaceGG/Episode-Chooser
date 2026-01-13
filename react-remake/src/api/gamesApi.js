import api from ".";

const gamesApi = {
  async getAll() {
    const games = await api.get("/games");
    return games.data;
  },

  async getByStatus(status) {
    const games = await this.getAll();

    const statusGames = [];

    games.forEach((game) => {
      if (game.additionalGames.length === 0) {
        if (status === "none") {
          if (!game.mainStatus) {
            statusGames.push({ ...game, name: game.mainName });
          }
        } else {
          if (game.mainStatus === status) {
            statusGames.push(game);
          }
        }
      } else {
        game.additionalGames.forEach((additionalGame, i) => {
          if (additionalGame.status === status) {
            statusGames.push({ ...additionalGame, id: `${game.id}${i}` });
          }
        });
      }
    });

    return statusGames;
  },
};

export default gamesApi;
