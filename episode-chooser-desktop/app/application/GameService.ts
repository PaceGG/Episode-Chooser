import { paths } from "@/storage/paths";

export default class GameSerivce {
  readonly name: string;
  readonly safeName: string;
  readonly shortName: string;
  readonly extraName: string | null;
  readonly fullName: string;

  constructor(
    name: string,
    extraName: string | null,
    shortName: string | null,
    kwargs: Record<string, any> = {},
  ) {
    this.name = name;
    this.safeName = kwargs.safeName || name.replace(":", "");
    this.shortName = shortName || this.getShortName();
    this.extraName = extraName;
    this.fullName = `${name}${this.extraName ? `: ${extraName}` : ""}`;
  }

  private getShortName(): string {
    let result = "";
    const breakChars = [":", "["];

    for (const char of this.name) {
      if (breakChars.includes(char) || !isNaN(parseInt(char))) break;
      result += char;
    }

    let processedName = result.trim();

    const words = processedName.split(" ");
    const breakWords = ["Remastered", "II"];
    const filteredWords: string[] = [];

    for (const word of words) {
      if (breakWords.includes(word)) break;
      filteredWords.push(word);
    }

    if (filteredWords.length <= 2) {
      processedName = filteredWords.join(" ");
    } else {
      processedName = filteredWords.map((word) => word[0] || "").join("");
    }

    return processedName;
  }
}
