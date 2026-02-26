import { paths } from "@/storage/paths";
import GameSerivce from "./GameService";

export default function Application() {
    const games = paths.getGames().map((game) => new GameSerivce(game.name, game.extraName, game.shortName, game.color))
    console.log(games);

    return;
}