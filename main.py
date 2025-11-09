import os
import yt_dlp

def make_alpha_numeric(string):
    return ''.join(char for char in string if char.isalnum())

link = input("Input your link to playlist or video: ")

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'outtmpl': '%(title)s.%(ext)s',
    'noplaylist': False,
    'verbose': True,
    'cookiefile': 'cookies.txt', #-> add in directory with python script your text file with cookies to pretend authentication failures during the download 
    'quiet': False,
    'postprocessors': [
        {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}
    ]
}

if "playlist" in link:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(link, download=False)
        playlist_title = make_alpha_numeric(playlist_info['title'])

        if not os.path.exists(playlist_title):
            os.mkdir(playlist_title)

        totalVideoCount = len(playlist_info['entries'])
        print("Total videos in playlist: 🎦", totalVideoCount)

        ydl_opts['outtmpl'] = os.path.join(playlist_title, '%(title)s.%(ext)s')

        with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
            for index, video in enumerate(playlist_info['entries'], start=1):
                try:
                    print(f"\nDownloading: {video['title']}")
                    ydl2.download([video['webpage_url']])  # Use 'webpage_url' here
                    print(f"Downloaded: {video['title']} ✨ successfully!")
                    print("Remaining Videos:", totalVideoCount - index)
                except Exception as e:
                    print(f"Error downloading {video['title']}: {e}")

    print("\nAll videos downloaded successfully! 🎉")
else:
    ydl_opts['noplaylist'] = True
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(link, download=False)
            print(f"Downloading a film: 🎬 {info['title']}")
            ydl.download([link])
            print(f"Film '{info['title']}' was successfully downloaded!")
        except Exception as e:
            print(f"Error downloading {info['title']}: {e}")
