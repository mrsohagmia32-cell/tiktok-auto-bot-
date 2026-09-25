import json
import os
import sys
import time
import urllib.request
from playwright.sync_api import sync_playwright


# অনলাইন থেকে ফ্রি ও লাইভ প্রক্সি সংগ্রহ করার ফাংশন
def get_free_proxy():
  try:
    print(
        "🔍 অনলাইন থেকে নতুন ফ্রি পাবলিক প্রক্সি (Public IP/Proxy) খোঁজা হচ্ছে..."
    )
    # ফ্রি প্রক্সি প্রভাইডার এপিআই থেকে প্রক্সি লিস্ট ফেচ করা
    url = "https://proxylist.geonode.com/api/proxy-list?limit=5&sort_by=lastChecked&sort_type=desc&protocols=http%2Chttps"
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
      data = json.loads(response.read().decode())
      proxies = data.get("data", [])
      if proxies:
        # যেকোনো একটি ভালো আইপি এবং পোর্ট সিলেক্ট করা
        p_ip = proxies[0]["ip"]
        p_port = proxies[0]["port"]
        proxy_url = f"http://{p_ip}:{p_port}"
        print(f"✅ লাইভ প্রক্সি পাওয়া গেছে: {proxy_url}")
        return proxy_url
  except Exception as e:
    print(
        "⚠️ প্রক্সি ফেচ করতে সমস্যা হয়েছে, সরাসরি গিটহাব আইপি দিয়ে চেষ্টা করা"
        " হচ্ছে..."
    )

  return None  # কোনো প্রক্সি না পেলে ফেইলসেফ হিসেবে সরাসরি নেটওয়ার্ক ব্যবহার করবে


def run_order():
  service_type = os.environ.get("SERVICE_TYPE", "Followers")
  target_input = os.environ.get("TARGET_INPUT", "").strip()
  count_str = os.environ.get("ACTION_COUNT", "1")
  cookies_json = os.environ.get("BOT_COOKIES")

  if not target_input:
    print("❌ কোনো টার্গেট ইনপুট (ইউজারনেম বা লিংক) পাওয়া যায়নি!")
    sys.exit(1)

  try:
    action_count = int(count_str)
  except ValueError:
    action_count = 1

  # রানিং টাইমে লাইভ প্রক্সি নেওয়া
  selected_proxy = get_free_proxy()

  with sync_playwright() as p:
    browser_args = ["--no-sandbox", "--disable-setuid-sandbox"]
    launch_options = {
        "headless": True,
        "args": browser_args,
    }

    if selected_proxy:
      launch_options["proxy"] = {"server": selected_proxy}
    else:
      print("🌐 কোনো প্রক্সি ব্যবহার করা হচ্ছে না (Direct Connection)।")

    browser = p.chromium.launch(**launch_options)
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
        print("🍪 ইনস্টাগ্রাম বট অ্যাকাউন্টের কুকি সফলভাবে লোড হয়েছে।")
      except Exception as e:
        print("⚠️ কুকি পার্স করতে সমস্যা হয়েছে:", e)

    page = context.new_page()

    try:
      if service_type == "Followers":
        username = target_input.lstrip("@")
        target_url = f"https://www.instagram.com/{username}/"
        print(
            f"🎯 ইনস্টাগ্রাম সার্ভিস: ফলোয়ার | টার্গেট: @{username} | পরিমাণ:"
            f" {action_count}"
        )

        print("🔗 প্রোফাইলে যাওয়া হচ্ছে...")
        page.goto(target_url, timeout=60000)
        time.sleep(6)

        follow_btn = page.locator(
            "button:has-text('Follow'), button:has-text('Follow Back')"
        ).first
        if follow_btn.is_visible():
          text = follow_btn.inner_text().strip()
          if "Follow" in text and "Following" not in text:
            follow_btn.click()
            time.sleep(4)
            print(f"✅ সফলভাবে ফলো করা হয়েছে!")
          else:
            print("⚠️ অ্যাকাউন্টটি ইতিমধ্যে ফলো করা আছে।")
        else:
          print("⚠️ ফলো বাটন পাওয়া যায়নি।")

      elif service_type == "Likes":
        target_url = target_input
        print(
            f"🎯 ইনস্টাগ্রাম সার্ভিস: লাইক | পোস্ট লিংক: {target_url} | পরিমাণ:"
            f" {action_count}"
        )

        print("🔗 পোস্ট পেজে যাওয়া হচ্ছে...")
        page.goto(target_url, timeout=60000)
        time.sleep(6)

        like_btn = page.locator(
            "svg[aria-label='Like'], svg[aria-label='Unlike']"
        ).first
        if like_btn.is_visible():
          like_btn.click()
          time.sleep(4)
          print(f"❤️ সফলভাবে ইনস্টাগ্রাম পোস্টে লাইক দেওয়া হয়েছে!")
        else:
          print("⚠️ লাইক বাটন পাওয়া যায়নি।")

    except Exception as e:
      print("❌ ত্রুটি ঘটেছে:", e)
      sys.exit(1)
    finally:
      browser.close()


if __name__ == "__main__":
  run_order()
