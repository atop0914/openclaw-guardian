---
name: serper-search
description: "Web search via Serper.dev Google Search API. Use when: user asks to search the web, find information online, or look up current events. Supports general search, news, images, and more."
---

# Serper Search Skill

Web search powered by Serper.dev (Google Search API).

## When to Use

✅ **USE this skill when:**
- "Search for..."
- "Look up..."
- "Find information about..."
- "What's the latest on..."
- "Search web for..."

## Commands

### General Search

```python
python skills/serper-search/search.py "your search query"
```

### Search with Options

```python
python skills/serper-search/search.py "query" --type news --num 10
```

### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `--type` | Search type: `search`, `news`, `images`, `places` | `search` |
| `--num` | Number of results (1-100) | `10` |
| `--gl` | Country code (e.g., `us`, `cn`, `uk`) | `us` |
| `--hl` | Language code (e.g., `en`, `zh`, `ja`) | `en` |

## Examples

```bash
# Basic search
python skills/serper-search/search.py "OpenClaw AI"

# Search news
python skills/serper-search/search.py "latest tech" --type news

# Search in Chinese
python skills/serper-search/search.py "人工智能" --hl zh --gl cn

# Get 20 results
python skills/serper-search/search.py "machine learning" --num 20
```

## API Key

Stored in: `~/.openclaw/config/serper.key`

## Output Format

Returns JSON with:
- `organic` - Regular search results
- `knowledgeGraph` - Knowledge panel (if available)
- `relatedSearches` - Related queries
- `answerBox` - Direct answers (if available)

## Notes

- Free tier: 100 queries/month
- Rate limit: 1 query/second
- No attribution required
