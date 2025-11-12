import os
import subprocess
import requests

# 1️⃣ 获取当前 PR diff
diff = subprocess.getoutput("git fetch origin main && git diff origin/main...HEAD --unified=0")

if not diff.strip():
    print("No code changes detected.")
    exit(0)

# 2️⃣ 构建审查提示词
prompt = f"""
You are a senior backend engineer doing a code review.
Please review the following git diff and provide concise feedback:
- Identify potential bugs or risky logic
- Suggest performance or readability improvements
- Keep comments short and clear

Diff:
{diff[:6000]}  # 防止太长
"""

# 3️⃣ 调用 GitHub Models API
headers = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    "Accept": "application/vnd.github+json",
}
payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "You are an expert code reviewer."},
        {"role": "user", "content": prompt}
    ]
}

print("🔍 Calling GitHub Models API...")
response = requests.post("https://api.github.com/models/gpt-4o-mini/completions", headers=headers, json=payload)
data = response.json()
print("Response data:", data)
review_text = data["choices"][0]["message"]["content"]
print("✅ Review result:\n", review_text)

# 4️⃣ 自动评论回 PR
# 获取 PR 号（通过环境变量 GITHUB_REF）
pr_number = os.getenv("GITHUB_REF").split("/")[-1]
repo = os.getenv("GITHUB_REPOSITORY")

comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

requests.post(
    comment_url,
    headers=headers,
    json={"body": f"🤖 **AI Code Review Result (via GitHub Models)**:\n\n{review_text}"}
)
