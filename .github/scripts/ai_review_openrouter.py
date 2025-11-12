import os
import requests
import json

# ==============================
# 1️⃣ 获取 PR Diff
# ==============================
repo = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("GITHUB_PR_NUMBER")

print(f"🔍 Fetching diff for PR #{pr_number} in {repo}...")

headers = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    "Accept": "application/vnd.github.v3.diff",
}

url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
diff_response = requests.get(url, headers=headers)

if diff_response.status_code != 200:
    print("❌ Failed to fetch PR diff:", diff_response.text)
    exit(1)

code_diff = diff_response.text
print(f"✅ Diff fetched, {len(code_diff)} characters")

# ==============================
# 2️⃣ 调用 OpenRouter 模型
# ==============================
MODEL = "kwaipilot/kat-coder-pro:free"  # 可改为 claude-3.5-sonnet, gemini-2-pro 等
AI_URL = "https://openrouter.ai/api/v1/chat/completions"
print("🔑 OPENROUTER_API_KEY exists:", bool(os.getenv("OPENROUTER_API_KEY")))
ai_headers = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "HTTP-Referer": "https://github.com",  # 按 OpenRouter 要求添加
    "X-Title": "GitHub AI Review Action",
    "Content-Type": "application/json",
}

prompt = f"""
你是一名高级后端工程师，请针对以下代码改动进行 Code Review。
重点指出潜在问题、可优化点、逻辑漏洞、安全风险、可读性或性能改进建议。

代码 diff 如下：
{code_diff[:20000]}  # 限制最大字符数，避免 token 超限
"""

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "You are a senior code reviewer."},
        {"role": "user", "content": prompt}
    ]
}

print("🚀 Calling OpenRouter model...")
ai_response = requests.post(AI_URL, headers=ai_headers, json=payload)
data = ai_response.json()

if "choices" not in data:
    print("❌ Unexpected API response:", data)
    exit(1)

review_text = data["choices"][0]["message"]["content"]
print("✅ AI Review Generated")

# ==============================
# 3️⃣ 自动评论到 Pull Request
# ==============================
comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

comment_body = {
    "body": f"🤖 **AI Code Review** by OpenRouter:\n\n{review_text}"
}

gh_headers = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    "Accept": "application/vnd.github+json",
}

print("💬 Posting review comment to GitHub...")
comment_resp = requests.post(comment_url, headers=gh_headers, json=comment_body)

if comment_resp.status_code == 201:
    print("✅ Comment posted successfully!")
else:
    print("❌ Failed to post comment:", comment_resp.text)
    exit(1)
