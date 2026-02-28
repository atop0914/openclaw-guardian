#!/usr/bin/env python3
"""
Serper.dev Google Search API wrapper
Usage: python search.py "query" [--type TYPE] [--num NUM] [--gl GL] [--hl HL]
"""

import sys
import json
import urllib.request
import urllib.error
import os

# API Configuration
API_KEY = "705ae7b63a1b291cb4b7818fce2ffdc038719fec"
BASE_URL = "https://google.serper.dev"

def search(query, search_type="search", num=10, gl="us", hl="en"):
    """
    Perform web search using Serper.dev API
    
    Args:
        query: Search query string
        search_type: Type of search (search, news, images, places)
        num: Number of results (1-100)
        gl: Country code (us, cn, uk, etc.)
        hl: Language code (en, zh, ja, etc.)
    """
    url = f"{BASE_URL}/{search_type}"
    
    payload = {
        "q": query,
        "num": min(max(num, 1), 100),  # Clamp between 1-100
        "gl": gl,
        "hl": hl
    }
    
    headers = {
        'X-API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
            
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP Error {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

def format_results(data):
    """Format search results for display"""
    if "error" in data:
        return f"❌ {data['error']}"
    
    output = []
    
    # Answer Box (direct answer)
    if "answerBox" in data and data["answerBox"]:
        ab = data["answerBox"]
        output.append("📦 **Answer**")
        if "title" in ab:
            output.append(f"**{ab['title']}**")
        if "answer" in ab:
            output.append(ab['answer'])
        if "snippet" in ab:
            output.append(ab['snippet'])
        output.append("")
    
    # Knowledge Graph
    if "knowledgeGraph" in data and data["knowledgeGraph"]:
        kg = data["knowledgeGraph"]
        output.append("🧠 **Knowledge Graph**")
        if "title" in kg:
            output.append(f"**{kg['title']}**")
        if "description" in kg:
            output.append(kg['description'])
        output.append("")
    
    # Organic Results
    if "organic" in data and data["organic"]:
        output.append(f"🔍 **Search Results** ({len(data['organic'])} found)")
        output.append("")
        
        for i, result in enumerate(data["organic"][:10], 1):
            title = result.get("title", "No title")
            link = result.get("link", "")
            snippet = result.get("snippet", "No description")
            
            output.append(f"{i}. **{title}**")
            output.append(f"   {snippet}")
            output.append(f"   [Link]({link})")
            output.append("")
    
    # Related Searches
    if "relatedSearches" in data and data["relatedSearches"]:
        output.append("💡 **Related Searches**")
        related = [r.get("query", "") for r in data["relatedSearches"][:5]]
        output.append(", ".join(related))
    
    return "\n".join(output) if output else "No results found."

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Serper.dev Search')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--type', default='search', 
                       choices=['search', 'news', 'images', 'places'],
                       help='Search type')
    parser.add_argument('--num', type=int, default=10,
                       help='Number of results (1-100)')
    parser.add_argument('--gl', default='us',
                       help='Country code (us, cn, uk, etc.)')
    parser.add_argument('--hl', default='en',
                       help='Language code (en, zh, ja, etc.)')
    parser.add_argument('--json', action='store_true',
                       help='Output raw JSON')
    
    args = parser.parse_args()
    
    # Perform search
    result = search(args.query, args.type, args.num, args.gl, args.hl)
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_results(result))

if __name__ == "__main__":
    main()
