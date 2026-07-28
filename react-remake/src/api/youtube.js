const BASE_URL = "https://www.googleapis.com/youtube/v3";
const channelId = "UC2Y71nJHtoLzY88Wrrqm7Kw";
const API_KEY = "AIzaSyA5ErlvPrDU-QskKoYkyY60Ah5OyePHnwo";

async function getPlaylistId(channelId, playlistTitle) {
  let nextPageToken = null;

  do {
    const url =
      `${BASE_URL}/playlists?channelId=${channelId}&part=snippet&maxResults=50&key=${API_KEY}` +
      (nextPageToken ? `&pageToken=${nextPageToken}` : "");

    const response = await fetch(url);
    const data = await response.json();

    const found = data.items?.find(
      (item) => item.snippet.title === playlistTitle,
    );
    if (found) {
      return found.id;
    }

    nextPageToken = data.nextPageToken || null;
  } while (nextPageToken);

  throw new Error(`Плейлист '${playlistTitle}' не найден.`);
}

function isDigit(char) {
  return /\d/.test(char);
}

function getNumber(numberStr) {
  let number = "";
  for (const char of numberStr) {
    if (isDigit(char)) number += char;
  }

  return Number(number);
}

function getTitleParts(title) {
  const parts = title.split("•");
  const episodeTitle = parts[0]?.trim() || "";
  const number = getNumber(parts[1]?.trim() || -1);
  const gameName = parts[2]?.trim() || "";
  return { episodeTitle, number, gameName };
}

async function getAllVideosFromPlaylist(playlistId) {
  const videos = [];
  let nextPageToken = null;

  do {
    const url =
      `${BASE_URL}/playlistItems?playlistId=${playlistId}&part=snippet,contentDetails&maxResults=50&key=${API_KEY}` +
      (nextPageToken ? `&pageToken=${nextPageToken}` : "");

    const response = await fetch(url);
    const data = await response.json();

    for (const item of data.items || []) {
      const title = item.snippet.title;
      const parts = getTitleParts(title);

      videos.push({
        videoTitle: title,
        ...parts,
        videoId: item.contentDetails.videoId,
        description: item.snippet.description,
        publishedAt: item.snippet.publishedAt,
      });
    }

    nextPageToken = data.nextPageToken || null;
  } while (nextPageToken);

  console.log(videos);
  return videos;
}

function isCorrectOrder(a, b) {
  return a + 1 === b || b === 1;
}

function validateVideos(videos, playlistName) {
  let hasPrivate = false;
  let wrongGame = false;
  let wrongOrder = false;

  let prevNumber = 0;
  videos.forEach((video) => {
    if (video.videoTitle === "Private video") hasPrivate = true;
    if (!video.gameName.includes(playlistName)) wrongGame = true;
    if (!isCorrectOrder(prevNumber, video.number)) wrongOrder = true;

    prevNumber = video.number;
  });

  return { hasPrivate, wrongGame, wrongOrder };
}

const ytApi = {
  async getPlaylistInfo(name) {
    const playlistId = await getPlaylistId(channelId, name);
    const videos = await getAllVideosFromPlaylist(playlistId);

    // lastEpisodeNumber
    const lastVideo = videos.at(-1);
    const lastEpisodeNumber = lastVideo.number;

    // validation
    const warnings = validateVideos(videos, name);

    return { lastEpisodeNumber, videosAmount: videos.length, warnings };
  },
};

export default ytApi;
