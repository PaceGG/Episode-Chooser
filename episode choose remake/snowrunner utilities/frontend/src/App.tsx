import { useEffect, useState } from "react";
import InputForm from "./components/InputForm";
import api from "./api";

function App() {
  const [questNames, setQuestNames] = useState<string>("");

  const fetchNames = async () => {
    const names = await api.getNames();
    const namesString = names.join("\n");
    setQuestNames(namesString);
  };

  useEffect(() => {
    fetchNames();
  }, []);

  const reload = () => {
    console.log("reloading...");
    setQuestNames("");
    fetchNames();
  };

  const convertQuestNames = async (names: string, regionName: string) => {
    const questNamesList = names.split("\n");
    const convertedNames = await api.convertNames(questNamesList, regionName);
    const convertedNamesString = convertedNames.join("\n");
    setQuestNames(convertedNamesString);
  };

  return (
    <>
      <InputForm
        label="Name"
        value={questNames}
        onConfirm={convertQuestNames}
        onReload={reload}
        isLoading={questNames.length === 0}
      />
    </>
  );
}

export default App;
