const Search = require("youtube-search-api");
const ytdlp = require("yt-dlp-exec");

exports.search = async (query) => {
    // YouTube'da ara
    const result = await Search.GetListByKeyword(query, false, 1);

    if (
        !result.items ||
        result.items.length === 0 ||
        !result.items[0].id
    ) {
        throw new Error("Şarkı bulunamadı.");
    }

    const video = result.items[0];
    const videoUrl = `https://www.youtube.com/watch?v=${video.id}`;

    // yt-dlp ile ses URL'sini al
    const info = await ytdlp(videoUrl, {
        dumpSingleJson: true,
        noWarnings: true,
        noCheckCertificates: true,
        preferFreeFormats: true,
        youtubeSkipDashManifest: true
    });

    const audio = info.formats
        .filter(f => f.acodec !== "none" && f.url)
        .sort((a, b) => (b.abr || 0) - (a.abr || 0))[0];

    if (!audio) {
        throw new Error("Ses bulunamadı.");
    }

    return {
        title: info.title,
        artist: info.uploader,
        cover: info.thumbnail,
        media_url: audio.url
    };
};
