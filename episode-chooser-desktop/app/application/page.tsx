import { paths } from "@/storage/paths";
import GameSerivce from "./GameService";

export default function Application() {
    const games = paths.getNames().map((gameName) => new GameSerivce(gameName.name, gameName.extraName, gameName.shortName))
    console.log(games);

    return;
}