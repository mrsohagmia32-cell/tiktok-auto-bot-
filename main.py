import os
import sys
import time
from playwright.sync_api import sync_playwright

def run_automation():
    # গিটহাব সিক্রেট থেকে টার্গেট লিংক এবং কুকিজ নেওয়া হবে
    target_url = os.environ.get("TARGET_URL")
    
    if not target_url:
        print("❌ কোনো টার্গেট লিংক পাওয়া যায়নি!")
        sys.exit(1)

    print(f"🚀 গিটহাব অ্যাকশনস থেকে কাজ শুরু হচ্ছে...")
    print(f"🔗 টার্গেট লিংক: {target_url}")

    with sync_playwright() as p:
        # গিটহাব সার্ভারে ব্রাউজার রান করার জন্য হেডলেস মোড True রাখতে হবে
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(target_url, timeout=60000)
            time.sleep(5)
            
            # এখানে আপনার অটোমেশন বা ক্লিকের কোড থাকবে
            print("🎯 পেজ সফলভাবে লোড হয়েছে এবং প্রসেসিং সম্পন্ন!")
            
        except Exception as e:
            print("❌ ত্রুটি ঘটেছে:", e)
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run_automation()
