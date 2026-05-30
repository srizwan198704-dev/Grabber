import time
import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        video_url = ""
        
        def handle_request(request):
            nonlocal video_url
            url = request.url
            
            # মূল ওয়েবসাইটের পেজ ইউআরএল বাদ দিয়ে শুধু আসল মিডিয়া স্ট্রিম খোঁজা
            if ("videoPlayPage" not in url) and (".m3u8" in url or ".mp4" in url or ".ts" in url or "master" in url or "playlist" in url):
                if not video_url:
                    video_url = url
                    print(f"[+] Actual Video Stream Found: {video_url}")

        page.on("request", handle_request)
        
        target_link = "https://netfilm.world/spa/videoPlayPage/movies/drishyam-3-cam-QwhMMBvOxn8?id=7033131017150384600&type=/movie/detail&detailSe=&detailEp=&lang=en"
        print(f"Opening page: {target_link}")
        
        # পেজ ওপেন করে ১০ সেকেন্ড অপেক্ষা করা যাতে প্লেয়ার লোড হতে পারে
        page.goto(target_link, timeout=90000)
        time.sleep(15) 
        
        browser.close()

        if video_url:
            # যদি সরাসরি mp4 হয়
            if ".mp4" in video_url:
                import urllib.request
                print("Downloading MP4 file...")
                urllib.request.urlretrieve(video_url, "downloaded_video.mp4")
            # যদি m3u8 স্ট্রিম হয়, তবে শুধু লিঙ্কটি টেক্সট ফাইলে সেভ রাখা হবে যাতে ffmpeg সরাসরি ডাউনলোড করতে পারে
            else:
                print("Saving m3u8 link for FFmpeg...")
                with open("stream_link.txt", "w") as f:
                    f.write(video_url)
        else:
            print("[-] No valid stream link captured.")
            exit(1)

if __name__ == "__main__":
    run()
