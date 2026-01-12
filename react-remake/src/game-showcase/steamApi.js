import axios from "axios";

const api = axios.create({
  baseURL: "/steam/api",
  timeout: 5000,
});

const steamApi = {
  async getAppsByName(name) {
    const response = await api.get(`/storesearch/?term=${name}&l=en&cc=us`);
    const items = response.data.items;
    console.log(items);
    return items;
  },

  async getAppDetailsByAppId(appid) {
    const response = await api.get(`/appdetails?appids=${appid}`);
    const appDetails = response.data[appid].data;
    return appDetails;
  },

  getSteamImages(id) {
    return {
      library600x900_2x: `https://cdn.akamai.steamstatic.com/steam/apps/${id}/library_600x900_2x.jpg`,
      header: `https://cdn.akamai.steamstatic.com/steam/apps/${id}/header.jpg`,
      logo: `https://cdn.akamai.steamstatic.com/steam/apps/${id}/logo.png`,
      libraryHero: `https://cdn.akamai.steamstatic.com/steam/apps/${id}/library_hero.jpg`,
      library600x900: `https://cdn.akamai.steamstatic.com/steam/apps/${id}/library_600x900.jpg`,
      pageBg: `https://cdn.akamai.steamstatic.com/steam/apps/${id}/page_bg_generated.jpg`,
      pageBgV6b: `https://cdn.akamai.steamstatic.com/steam/apps/${id}/page_bg_generated_v6b.jpg`,
      capsule616x353: `https://cdn.akamai.steamstatic.com/steam/apps/${id}/capsule_616x353.jpg`,
      capsule231x87: `https://cdn.akamai.steamstatic.com/steam/apps/${id}/capsule_231x87.jpg`,
    };
  },
};

export default steamApi;
