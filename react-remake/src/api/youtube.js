const BASE_URL = 'https://www.googleapis.com/youtube/v3';
const channelId = "UC2Y71nJHtoLzY88Wrrqm7Kw"
const API_KEY = "AIzaSyA5ErlvPrDU-QskKoYkyY60Ah5OyePHnwo"

async function getPlaylistId(channelId, playlistTitle) {
    let nextPageToken = null;
    
    do {
        const url = `${BASE_URL}/playlists?channelId=${channelId}&part=snippet&maxResults=50&key=${API_KEY}` + 
                    (nextPageToken ? `&pageToken=${nextPageToken}` : '');
        
        const response = await fetch(url);
        const data = await response.json();
        
        const found = data.items?.find(item => item.snippet.title === playlistTitle);
        if (found) {
            return found.id;
        }
        
        nextPageToken = data.nextPageToken || null;
    } while (nextPageToken);
    
    throw new Error(`Плейлист '${playlistTitle}' не найден.`);
}

async function getAllVideosFromPlaylist(playlistId) {
    const videos = [];
    let nextPageToken = null;
    let hasPrivate = false;
    
    do {
        const url = `${BASE_URL}/playlistItems?playlistId=${playlistId}&part=snippet,contentDetails&maxResults=50&key=${API_KEY}` +
                    (nextPageToken ? `&pageToken=${nextPageToken}` : '');
        
        const response = await fetch(url);
        const data = await response.json();
        
        for (const item of data.items || []) {
            if (item.snippet.title === "Private video") {
                hasPrivate = true;
            }

            videos.push({
                title: item.snippet.title,
                videoId: item.contentDetails.videoId,
                description: item.snippet.description,
                publishedAt: item.snippet.publishedAt
            });
        }
        
        nextPageToken = data.nextPageToken || null;
    } while (nextPageToken);
    
    console.log(videos)
    return {videos, hasPrivate};
}


const ytApi = {
    async getPlaylistInfo(name) {
        const playlistId = await getPlaylistId(channelId, name)
        const videosInfo = await getAllVideosFromPlaylist(playlistId)
        const videos = videosInfo.videos
        const hasPrivate = videosInfo.hasPrivate

        const lastVideoTitle = videos.at(-1).title
        let number = -1;
        
        if (lastVideoTitle.includes("•")) {
            const lastVideoEpisode = lastVideoTitle.split("•")[1];
            const match = lastVideoEpisode.match(/\d+/);
            number = match ? parseInt(match[0], 10) : -1;
        }

        return {lastEpisodeNumber: number, videosAmount: videos.length, hasPrivate}
    }
}

export default ytApi