---
name: "feishu-docs"
description: "Feishu (Lark) document and wiki operations. Read, create, append to docs, and manage wiki spaces."
---

# Feishu Docs Skill

Operations for Feishu (Lark) documents and wikis.

## Prerequisites
- Feishu API credentials (app ID and app secret)
- Required permissions: document reading/writing, wiki access

## Document Operations
### Read Document
```python
feishu_doc(action="read", doc_token="文档token")
# Token from URL: /docx/XXX 中的 XXX
```

### Create and Write Document
```python
feishu_doc(action="create_and_write", title="文档标题", content="Markdown内容")
```

### Append Content
```python
feishu_doc(action="append", doc_token="xxx", content="追加的内容")
```

## Wiki Operations
### List Knowledge Spaces
```python
feishu_wiki(action="spaces")
```

### List Nodes in Space
```python
feishu_wiki(action="nodes", space_id="xxx")
```

### Read Wiki Page
```python
feishu_wiki(action="get", token="wiki_token")
```
