import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def youtube_api_setup():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    os.listdir()
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "./src/my_client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube


def get_mss_uploaded_videos(youtube, playlist_id, page_token):
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=50,
        pageToken=page_token
    )
    response = request.execute()
    return response


def put_mss_video_in_playlist(youtube, playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "videoId": video_id,
                    "kind": "youtube#video"
                }
            }
        }
    )
    response = request.execute()
    return response
