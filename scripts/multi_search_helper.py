
#!/usr/bin/env python3
"""
Multi-Search-Engine Helper Script
Makes it easier to use the multi-search-engine skill
"""

import argparse
import sys

# Search engine URLs from multi-search-engine skill
SEARCH_ENGINES = {
    "baidu": "https://www.baidu.com/s?wd={keyword}",
    "bing_cn": "https://cn.bing.com/search?q={keyword}&ensearch=0",
    "bing_int": "https://cn.bing.com/search?q={keyword}&ensearch=1",
    "360": "https://www.so.com/s?q={keyword}",
    "sogou": "https://sogou.com/web?query={keyword}",
    "wechat": "https://wx.sogou.com/weixin?type=2&query={keyword}",
    "toutiao": "https://so.toutiao.com/search?keyword={keyword}",
    "jisilu": "https://www.jisilu.cn/explore/?keyword={keyword}",
    "google": "https://www.google.com/search?q={keyword}",
    "google_hk": "https://www.google.com.hk/search?q={keyword}",
    "duckduckgo": "https://duckduckgo.com/html/?q={keyword}",
    "yahoo": "https://search.yahoo.com/search?p={keyword}",
    "startpage": "https://www.startpage.com/sp/search?query={keyword}",
    "brave": "https://search.brave.com/search?q={keyword}",
    "ecosia": "https://www.ecosia.org/search?q={keyword}",
    "qwant": "https://www.qwant.com/?q={keyword}",
    "wolframalpha": "https://www.wolframalpha.com/input?i={keyword}",
}

def main():
    parser = argparse.ArgumentParser(description="Multi-Search-Engine Helper")
    parser.add_argument("keyword", nargs="?", help="Search keyword")
    parser.add_argument("-e", "--engine", default="baidu", choices=SEARCH_ENGINES.keys(), help="Search engine to use (default: baidu)")
    parser.add_argument("-l", "--list", action="store_true", help="List all available search engines")
    
    args = parser.parse_args()
    
    if args.list:
        print("Available search engines:")
        for engine in sorted(SEARCH_ENGINES.keys()):
            print(f"  - {engine}")
        sys.exit(0)
    
    if not args.keyword:
        print("Error: keyword is required unless --list is used")
        parser.print_help()
        sys.exit(1)
    
    # Build the search URL
    url = SEARCH_ENGINES[args.engine].format(keyword=args.keyword)
    print(f"Search URL: {url}")
    print("\nUse web_fetch to get the results:")
    print(f'web_fetch({{"url": "{url}"}})')

if __name__ == "__main__":
    main()
