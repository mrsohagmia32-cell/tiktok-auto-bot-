import json
import os
import sys
import time
from playwright.sync_api import sync_playwright


def run_order():
  # গিটহাব ইনপুট থেকে ইউজারের ইউজারনেম নেওয়া
  username = os.environ.get("TARGET_USERNAME")
  # গিটহাব সিক্রেট থেকে বট কুকিজ নেওয়া
  cookies_json = os.environ.get("BOT_COOKIES")

  if not username:
    print("❌ কোনো ইউজারনেম পাওয়া যায়নি!")
    sys.exit(1)

  target_url = f"https://www.tiktok.com/@{username}"
  print(f"🎯 অর্ডার রিসিভ হয়েছে! টার্গেট অ্যাকাউন্ট: {target_url}")

  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
            " like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    )

    # গিটহাব সিক্রেট থেকে আসা কুকিগুলো ব্রাউজারে সেট করা
    if cookies_json:
      try:
        cookies = json.loads(cookies_json)
        context.add_cookies(cookies)
        print("🍪 বট অ্যাকাউন্টের কুকি সফলভাবে লোড হয়েছে।")
      except Exception as e:
        print("⚠️ কুকি পার্স করতে সমস্যা হয়েছে:", e)

    page = context.new_page()

    try:
      print(f"🔗 প্রোফাইলে যাওয়া হচ্ছে...")
      page.goto(target_url, timeout=60000)
      time.sleep(5)

      # টিকটকের ফলো বাটন খুঁজে ক্লিক করার লজিক
      follow_btn = page.locator("button:has-text('Follow')").first
      if follow_btn.is_visible():
        follow_btn.click()
        time.sleep(3)
        print(f"✅ সফলভাবে @{username} কে ফলো করা সম্পন্ন হয়েছে!")
      else:
        print("⚠️ ফলো বাটন পাওয়া যায়নি বা ইতিমধ্যে ফলো করা আছে।")

    except Exception as e:
      print("❌ ত্রুটি ঘটেছে:", e)
      sys.exit(1)
    finally:
      browser.close()


if __name__ == "__main__":
  run_order()
