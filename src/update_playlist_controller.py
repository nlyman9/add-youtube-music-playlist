from update_playlist_service import *
from secrets import *
import sys
import datetime

# CHANGE THE DATE BEFORE RUNNING SO THE VIDEOS DON'T OVERLAP BECAUSE THEY WILL


class AddToPlaylist:
    client_secret = None
    api_key = None
    mss_channel_id = None
    mss_uploads_playlist_id = None
    target_playlist_id = None
    test_playlist_id = None

    def main(self):
        if not verify_args():
            return
        # Get secrets.py
        self.get_secrets()
        youtube = youtube_api_setup()
        # Call api to get videos from MrSuicideSheep Channel
        get_videos_since_date = datetime.datetime(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
        # Initialize publish time
        # Get and filter the videos
        full_video_id_list = self.fetch_and_filter_videos(youtube, get_videos_since_date)
        print("Length of full video list: " + str(len(full_video_id_list)))
        # Add the video list to a new playlist or append to current playlist
        # Get the title of the first and last video being added to the playlist
        full_video_id_list = reversed(full_video_id_list)
        counter = 1
        for video_id in full_video_id_list:
            put_vid_in_playlist = put_mss_video_in_playlist(youtube, self.target_playlist_id, video_id)
            print(str(counter) + ": " + put_vid_in_playlist["snippet"]["title"] + " : " + put_vid_in_playlist["snippet"]["publishedAt"])
            counter += 1

    def convert_to_datetime(self, time):
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

    def fetch_and_filter_videos(self, youtube, get_videos_since_date):
        full_video_id_list = []
        page_token = None
        last_vid_publish_time = datetime.datetime.today()
        while last_vid_publish_time > get_videos_since_date:
            mss_uploaded_videos = get_mss_uploaded_videos(youtube, self.mss_uploads_playlist_id, page_token)
            page_token = mss_uploaded_videos["nextPageToken"]
            last_vid_publish_time = self.convert_to_datetime(
                mss_uploaded_videos["items"][-1]["contentDetails"]["videoPublishedAt"])
            if last_vid_publish_time < get_videos_since_date:  # Capture within the set of 50 which videos might be valid
                for video in mss_uploaded_videos["items"]:
                    if self.convert_to_datetime(video["contentDetails"]["videoPublishedAt"]) > get_videos_since_date:
                        full_video_id_list.append(video["contentDetails"]["videoId"])
                    else:
                        break
            else:
                for video in mss_uploaded_videos["items"]:
                    full_video_id_list.append(video["contentDetails"]["videoId"])

        return full_video_id_list

    def get_secrets(self):
        secrets = get_secrets()
        self.client_secret = secrets[2]
        self.api_key = secrets[0]
        self.mss_channel_id = secrets[3]
        self.mss_uploads_playlist_id = secrets[4]
        self.target_playlist_id = secrets[5]
        self.test_playlist_id = secrets[6]


def verify_args():
    if len(sys.argv) < 4:
        print("Must give date arguments as YYYY MM DD, not enough arguments")
        return False
    if len(sys.argv[1]) != 4:
        print("Must give date arguments as YYYY MM DD, arg 1 not correct length")
        return False
    if len(sys.argv[2]) != 2:
        print("Must give date arguments as YYYY MM DD, arg 2 not correct length")
        return False
    if len(sys.argv[3]) != 2:
        print("Must give date arguments as YYYY MM DD, arg 3 not correct length")
        return False
    return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    AddToPlaylist().main()
