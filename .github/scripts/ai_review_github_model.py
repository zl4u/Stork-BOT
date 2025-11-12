import os
import requests
import json

# ✅ 模型名称：可以是 gpt-4o-mini 或 gpt-4o
MODEL_NAME = "gpt-4o-mini"

# ✅ 传入要审查的代码
code_diff = """
def add(a, b):
    return a + b
"""

print("🔍 Calling GitHub Models API...")

url = f"https://api.github.com/models/{MODEL_NAME}/responses"

headers = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    "Content-Type": "application/json",
}

payload = {
    "input": [
        {
            "role": "user",
            "content": f"请帮我做代码review：\n{code_diff}"
        }
    ]
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()
print("Response data:", json.dumps(data, indent=2, ensure_ascii=False))

# ✅ 解析结果
if "output" in data and len(data["output"]) > 0:
    review_text = data["output"][0]["content"][0]["text"]
    print("\n✅ AI Review Result:\n", review_text)
else:
    print("⚠️ Unexpected API response format.")
    exit(1)
