import axios from "axios";

const app = axios.create({
  baseURL: "http://localhost:3000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

const api = {
  async getNames() {
    const names = await app.get("/get-names");
    return names.data.names;
  },

  async convertNames(names: string[], region: string) {
    const response = await app.post("/convert-names", { names, region });
    const convertedNames = response.data.converted;
    return convertedNames;
  },
};

export default api;
