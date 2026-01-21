import praw
import google.generativeai as genai
import requests
import os

# 1. API Setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Reddit Setup (Free Tier)
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="ProfitFlowAI_Bot_1.0",
    check_for_async=False
)

LP_LINK = "https://profitflowai-in.lovable.app"

# Logic 1: Sniper Method (Finding leads)
def sniper_bot():
    subreddits = "startupsindia+ecommerce+shopify+IndiaInvestments"
    keywords = "inventory OR stockout OR cashflow OR RTO OR 'working capital'"
    
    # Pichle 24 ghante ke posts search karna
    for post in reddit.subreddit(subreddits).search(keywords, time_filter="day", limit=5):
        prompt = f"Analyze this post: '{post.title} {post.selftext}'. Is this an Indian D2C owner having inventory or cashflow problems? Answer ONLY 'YES' or 'NO'."
        analysis = model.generate_content(prompt).text.strip()
        
        if "YES" in analysis.upper():
            # Reply drafting logic
            reply_prompt = f"Write a short, helpful reply to this post: '{post.title}'. Mention ProfitFlowAI ({LP_LINK}) as a solution. Keep it friendly and not like an ad."
            suggested_reply = model.generate_content(reply_prompt).text
            
            msg = f"🎯 *SNIPER ALERT!*\n\n*Problem:* {post.title}\n*Link:* {post.url}\n\n*Suggested Reply:* {suggested_reply}"
            send_telegram(msg)

# Logic 2: Content Drafting (For manual posting)
def generate_drafts():
    prompt = f"Write 1 professional LinkedIn post and 1 Instagram caption with 5 hashtags for ProfitFlowAI. Focus on Indian D2C inventory pains. Landing Page: {LP_LINK}"
    content = model.generate_content(prompt).text
    
    send_telegram(f"📝 *NEW CONTENT DRAFTS:*\n\n{content}")

# Telegram Sending Function
def send_telegram(msg):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

if __name__ == "__main__":
    # Dono kaam ek saath
    sniper_bot()
    generate_drafts()
