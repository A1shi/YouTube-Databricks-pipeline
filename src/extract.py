import os
import json
from datetime import datetime, timezone

from dotenv import load_dotenv
from googleapiclient.discovery import build


# Load environment variables
load_dotenv("/mnt/d/DE PROJECT/YouTube DataBricks Pipeline/.env")

API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY is missing from .env")

if not CHANNEL_ID:
    raise ValueError("YOUTUBE_CHANNEL_ID is missing from .env")


def get_youtube_client():
    """Create and return the YouTube API client."""
    return build(
        "youtube",
        "v3",
        developerKey=API_KEY
    )


def get_uploads_playlist_id(youtube):
    """Get the uploads playlist ID for the channel."""

    response = youtube.channels().list(
        part="contentDetails",
        id=CHANNEL_ID
    ).execute()

    if not response.get("items"):
        raise ValueError("Channel not found.")

    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_channel_videos(youtube, max_videos=500):
    """Fetch videos from the channel's uploads playlist."""

    playlist_id = get_uploads_playlist_id(youtube)

    videos = []
    next_page_token = None

    while len(videos) < max_videos:

        response = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response.get("items", []):

            videos.append({
                "video_id": item["contentDetails"]["videoId"],
                "title": item["snippet"]["title"],
                "published_at": item["contentDetails"]["videoPublishedAt"],
                "channel_id": item["snippet"]["channelId"],
                "channel_title": item["snippet"]["channelTitle"]
            })

            if len(videos) >= max_videos:
                break

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return videos

def get_video_details(youtube, videos):
    """Fetch statistics and content details for extracted videos."""

    enriched_videos = []

    # YouTube API allows up to 50 video IDs per request
    for i in range(0, len(videos), 50):

        batch = videos[i:i + 50]

        video_ids = ",".join(
            video["video_id"] for video in batch
        )

        response = youtube.videos().list(
            part="statistics,contentDetails,snippet",
            id=video_ids
        ).execute()

        details = {
            item["id"]: item
            for item in response.get("items", [])
        }

        for video in batch:

            detail = details.get(video["video_id"])

            if not detail:
                continue

            statistics = detail.get("statistics", {})
            content = detail.get("contentDetails", {})

            video["view_count"] = int(
                statistics.get("viewCount", 0)
            )

            video["like_count"] = int(
                statistics.get("likeCount", 0)
            )

            video["comment_count"] = int(
                statistics.get("commentCount", 0)
            )

            video["duration"] = content.get(
                "duration"
            )

            video["definition"] = content.get(
                "definition"
            )

            video["caption"] = content.get(
                "caption"
            )

            video["category_id"] = detail.get(
                "snippet", {}
            ).get("categoryId")

            enriched_videos.append(video)

    return enriched_videos


def save_raw_data(data):
    """Save extracted data as raw JSON."""

    os.makedirs("raw", exist_ok=True)

    output = {
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "record_count": len(data),
        "videos": data
    }

    with open("raw/youtube_raw.json", "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2, ensure_ascii=False)

    print(f"Successfully extracted {len(data)} videos.")
    print("Saved to raw/youtube_raw.json")


def main():
    youtube = get_youtube_client()

    videos = get_channel_videos(youtube, max_videos=500)

    save_raw_data(videos)

    print(f"Extracted {len(videos)} videos.")

    videos = get_video_details(
        youtube,
        videos
    )

    print(
        f"Enriched {len(videos)} videos with statistics."
    )

    save_raw_data(videos)


if __name__ == "__main__":
    main()