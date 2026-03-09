
#!/usr/bin/env python3
"""
Feishu (Lark) document and wiki operations
"""

import os
import requests

# Load Feishu credentials from environment variables
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")

def get_tenant_access_token():
    """Get Feishu tenant access token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    if data.get("code") != 0:
        raise Exception(f"Failed to get access token: {data}")
    return data["tenant_access_token"]

def feishu_doc(action, **kwargs):
    """
    Perform Feishu document operations
    
    Actions:
    - read: Read document (doc_token required)
    - create_and_write: Create and write document (title, content required)
    - append: Append to document (doc_token, content required)
    """
    token = get_tenant_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    if action == "read":
        doc_token = kwargs.get("doc_token")
        if not doc_token:
            raise ValueError("doc_token required for read action")
        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/raw_content"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    elif action == "create_and_write":
        title = kwargs.get("title")
        content = kwargs.get("content")
        if not title or not content:
            raise ValueError("title and content required for create_and_write action")
        url = "https://open.feishu.cn/open-apis/docx/v1/documents"
        payload = {
            "title": title,
            "content": content
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    elif action == "append":
        doc_token = kwargs.get("doc_token")
        content = kwargs.get("content")
        if not doc_token or not content:
            raise ValueError("doc_token and content required for append action")
        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks"
        payload = {
            "children": [
                {
                    "block_type": 2,  # Text block
                    "text": {
                        "elements": [
                            {
                                "text_run": {
                                    "content": content
                                }
                            }
                        ]
                    }
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    else:
        raise ValueError(f"Unknown action: {action}")

def feishu_wiki(action, **kwargs):
    """
    Perform Feishu wiki operations
    
    Actions:
    - spaces: List knowledge spaces
    - nodes: List nodes in space (space_id required)
    - get: Get wiki page (token required)
    """
    token = get_tenant_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    if action == "spaces":
        url = "https://open.feishu.cn/open-apis/wiki/v2/spaces"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    elif action == "nodes":
        space_id = kwargs.get("space_id")
        if not space_id:
            raise ValueError("space_id required for nodes action")
        url = f"https://open.feishu.cn/open-apis/wiki/v2/spaces/{space_id}/nodes"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    elif action == "get":
        wiki_token = kwargs.get("token")
        if not wiki_token:
            raise ValueError("token required for get action")
        url = f"https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token={wiki_token}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    else:
        raise ValueError(f"Unknown action: {action}")

if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python feishu.py <action> [kwargs]")
        sys.exit(1)

    action = sys.argv[1]
    kwargs = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            kwargs[key] = value

    if action in ["read", "create_and_write", "append"]:
        result = feishu_doc(action, **kwargs)
    elif action in ["spaces", "nodes", "get"]:
        result = feishu_wiki(action, **kwargs)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))
