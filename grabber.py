import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # হেডলেস ব্রাউজার চালু করা
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        video_url = ""
        
        # নেটওয়ার্ক রিকোয়েস্ট ট্র্যাক করার ফাংশন (1DM+ এর মতো)
        def handle_request(request):
            nonlocal video_url
            url = request.url
            # ভিডিওর সম্ভাব্য এক্সটেনশন বা স্ট্রিম লিংক ফিল্টার করা
            if ".m3u8" in url or ".mp4" in url or "video" in url:
                if not video_url: # প্রথম যে ভিডিও লিংকটি পাওয়া যাবে
                    video_url = url
                    print(f"[+] Found Video Stream Link: {video_url}")

        # নেটওয়ার্ক রিকোয়েস্ট মনিটর করা শুরু
        page.on("request", handle_request)
        
        # আপনার দেওয়া কাঙ্ক্ষিত লিংকটি ওপেন করা
        target_link = "https://netfilm.world/spa/videoPlayPage/movies/drishyam-3-cam-QwhMMBvOxn8?id=7033131017150384600&type=/movie/detail&detailSe=&detailEp=&lang=en"
        print(f"Opening page: {target_link}")
        page.goto(target_link, timeout=60000)
        
        # পেজ লোড হওয়া এবং ভিডিও প্লেয়ার চালু হওয়ার জন্য কিছু সময় অপেক্ষা করা
        time.sleep(15) 
        
        browser.close()

        # লিংক পাওয়া গেলে সেটি ডাউনলোড করার জন্য সেভ করা
        if video_url:
            with open("video_source.txt", "w") as f:
                f.write(video_url)
            
            # সরাসরি ফাইল হলে ডাউনলোড করা, নতুবা m3u8 হলে পরবর্তীতে ffmpeg সামলে নেবে
            import urllib.request
            if ".mp4" in video_url:
                print("Downloading MP4 file...")
                urllib.request.urlretrieve(video_url, "downloaded_video.mp4")
            else:
                # m3u8 লিংক হলে একটি লোকাল প্লেলিস্ট ফাইল তৈরি করা
                with open("stream.m3u8", "w") as f:
                    f.write(video_url)
        else:
            print("[-] Could not grab any video link. The player might be protected or requires interaction.")

if __name__ == "__main__":
    run()
