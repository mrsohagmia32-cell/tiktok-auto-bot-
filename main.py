import json
import os
import sys
import time
from playwright.sync_api import sync_playwright


def run_order():
  username = os.environ.get("TARGET_USERNAME")
  follow_count_str = os.environ.get("FOLLOW_COUNT", "1")
  cookies_json = os.environ.get("BOT_COOKIES")

  if not username:
    print("❌ কোনো ইউজারনেম পাওয়া যায়নি!")
    sys.exit(1)

  try:
    follow_count = int(follow_count_str)
  except ValueError:
    follow_count = 1

  target_url = f"https://www.tiktok.com/@{username}"
  print(f"🎯 টার্গেট অ্যাকাউন্ট: {target_url}")
  print(f"📊 টার্গেট পরিমাণ (Follow Count): {follow_count}")

  with sync_playwright() as p:
    # ব্রাউজার ওপেন করার সময় কিছু আর্গুমেন্ট যোগ করা হয়েছে যাতে গিটহাব সার্ভারে ক্র্যাশ না করে
    browser = p.chromium.launch(
        headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"]
    )
    context = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
            " like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
    )

    if cookies_json:
      try:
        cookies = json.loads(cookies_json)
        context.add_cookies(cookies)
        print("🍪 বট অ্যাকাউন্টের কুকি সফলভাবে লোড হয়েছে।")
      except Exception as e:
        print("⚠️ কুকি পার্স করতে সমস্যা হয়েছে:", e)

    page = context.new_page()

    try:
      print("🔗 প্রোফাইলে যাওয়া হচ্ছে...")
      page.goto(target_url, timeout=60000)
      time.sleep(6)

      # নির্দিষ্ট পরিমাণ ফলো বা প্রসেস চালানোর লজিক
      for i in range(follow_count):
        print(
            f"🔄 প্রসেস চলছে: {i+1} / {follow_count}..."
        )

        # টিকটকের ফলো বাটন খুঁজে ক্লিক করা
        follow_btn = page.locator(
            "button:has-text('Follow'), button:has-text('Follow back')"
        ).first
        if follow_btn.is_visible():
          follow_btn.click()
          time.sleep(4)
          print(f"✅ সফলভাবে ফলো করা হয়েছে ({i+1})!")
        else:
          print("⚠️ ফলো বাটন পাওয়া যায়নি বা অলরেডি ফলো করা আছে।")
          break

    except Exception as e:
      print("❌ ত্রুটি ঘটেছে:", e)
      sys.exit(1)
    finally:
      browser.close()


if __name__ == "__main__":
  run_order()
