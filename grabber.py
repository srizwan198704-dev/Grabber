import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # মানুষের মতো ব্রাউজার উইন্ডো সেটআপ করা
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        video_url = ""
        
        # নেটওয়ার্ক রিকোয়েস্ট মনিটর করার ফাংশন
        def handle_request(request):
            nonlocal video_url
            url = request.url
            
            # মিডিয়া স্ট্রিমের সম্ভাব্য কি-ওয়ার্ড ফিল্টার
            if "videoPlayPage" not in url:
                if any(ext in url for ext in [".m3u8", ".mp4", ".ts", "master.mpd", "playlist"]):
                    if not video_url:
                        video_url = url
                        print(f"[+] Successfully Grabbed Stream URL: {video_url}")

        page.on("request", handle_request)
        
        target_link = "https://netfilm.world/spa/videoPlayPage/movies/drishyam-3-cam-QwhMMBvOxn8?id=7033131017150384600&type=/movie/detail&detailSe=&detailEp=&lang=en"
        print(f"Opening page: {target_link}")
        
        # পেজে প্রবেশ করা (ভিপিএন-এর কারণে নেটওয়ার্ক আইডল হওয়া পর্যন্ত অপেক্ষা করার জন্য 'networkidle' দেওয়া হয়েছে)
        page.goto(target_link, wait_until="networkidle", timeout=120000)
        
        # ১. পেজ সম্পূর্ণ রেডি হওয়ার জন্য ৫ সেকেন্ড অপেক্ষা
        time.sleep(5)
        
        # ২. ভিডিও প্লেয়ার বা প্লে বাটনে ক্লিক করার চেষ্টা (অটো-প্লে ট্রিগার করতে)
        try:
            play_button = page.locator("video, .video-player, .play-btn, button").first
            if play_button.is_visible():
                play_button.click()
                print("[*] Clicked on the video player/button to start stream...")
        except Exception as e:
            print(f"[*] Note: Could not click play button, trying manual wait. ({str(e)})")
        
        # ৩. স্ট্রিম লিংক ব্যাকগ্রাউন্ডে ধরার জন্য আরও ১৫ সেকেন্ড অপেক্ষা করা
        time.sleep(15)
        
        # ডিবাগিংয়ের জন্য একটি স্ক্রিনশট নেওয়া (ভিপিএন কাজ করছে কিনা তা নিশ্চিত হতে)
        page.screenshot(path="page_screenshot.png")
        print("[*] Debug screenshot saved as page_screenshot.png")
        
        browser.close()

        # লিঙ্ক হ্যান্ডলিং এবং সংরক্ষণ
        if video_url:
            if ".mp4" in video_url:
                import urllib.request
                print("Downloading MP4 file...")
                urllib.request.urlretrieve(video_url, "downloaded_video.mp4")
            else:
                print("Saving m3u8 link for FFmpeg...")
                with open("stream_link.txt", "w") as f:
                    f.write(video_url)
        else:
            print("[-] No valid stream link captured. Website might be blocking cloud runners.")
            exit(1)

if __name__ == "__main__":
    run()
