# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Twitter media downloader that uses Twitter's GraphQL API to scrape and download images and videos from Twitter users. The project is a fork/continuation of caolvchong-top/twitter_download with Chinese documentation and specialized configurations.

## Core Architecture

### Main Entry Points
- `main.py` - Primary downloader for user media (images/videos)
- `tag_down.py` - Advanced search and hashtag-based downloading
- `text_down.py` - Text-only tweet extraction
- `main2.py` - Alternative main entry (purpose unclear from codebase)

### Core Components
- `user_info.py` - User data model containing screen name, rest_id, display name, and metadata
- `csv_gen.py` - CSV generation for download statistics and metadata
- `cache_gen.py` - Download cache management using pickle to avoid re-downloading
- `url_utils.py` - URL encoding utilities for Twitter API calls

### Key Configuration
- `settings.json` - Main configuration file containing:
  - User list to download from
  - Cookie authentication (auth_token and ct0)
  - Download preferences (retweets, highlights, likes, video, image format)
  - Time range filtering
  - Proxy settings
  - Auto-sync capabilities

## Common Development Commands

### Setup and Installation
```bash
pip3 install -r requirements.txt
```

### Running the Application
```bash
# Main user media download
python3 main.py

# Tag/hashtag based download (configure tag_down.py first)
python3 tag_down.py

# Text-only extraction (configure text_down.py first)  
python3 text_down.py
```

### Configuration Management
```bash
# Backup current settings
cp settings.json settings.json.backup

# View current user list
cat settings.json | grep -A 10 "user_lst"
```

## API Integration Details

### Twitter GraphQL Endpoints Used
- `UserByScreenName` - Get user metadata and rest_id
- `UserTweets` - Get user tweets with media (includes retweets)
- `UserMedia` - Get only media tweets (excludes retweets, more efficient)
- `UserHighlightsTweets` - Get highlighted tweets
- `Likes` - Get user's liked tweets
- `SearchTimeline` - Search by hashtags/advanced filters

### Rate Limiting
- Twitter enforces API call limits per day per account
- Approximate formula: Total API calls ≈ Total tweets / 19 (with retweets)
- Rate limit errors show "Rate limit exceeded"
- Downloads don't count toward API limits

## File Organization

### Output Structure
```
twitter/
├── {username}/
│   ├── {date}-img_{count}.{format}
│   ├── {date}-vid_{count}.mp4
│   ├── {username}-{timestamp}.csv
│   └── cache_data.log
```

### Special Modes
- **Tag Mode**: `#{tag}/{datetime}_{@username}_{md5_hash}.{ext}`
- **Text Mode**: CSV files with tweet content only
- **Auto-sync**: Automatically detects latest local content and syncs newer tweets

## Authentication Requirements

The application requires Twitter authentication cookies:
- `auth_token` - Twitter authentication token
- `ct0` - Cross-site request forgery token

These must be manually extracted from browser developer tools and placed in `settings.json`.

## Error Handling Patterns

### Common Issues
- Rate limit exceeded - Wait 24 hours or use different account
- Cookie expired - Re-extract from browser
- Download failures - Reduce `max_concurrent_requests` in main.py line 16
- 404 errors on media - Twitter removed content or changed URLs

### Retry Logic
- Download failures automatically retry with exponential backoff
- Image format fallback: orig → 4096x4096 → PNG format
- API failures are logged but don't stop execution

## Development Notes

### Key Dependencies
- `httpx` - Async HTTP client for API calls and downloads
- `asyncio` - Concurrent download management
- Standard library: `json`, `csv`, `pickle`, `hashlib`, `re`

### Performance Considerations
- Default concurrent downloads: 10 (configurable)
- Async download pattern with semaphore-based throttling  
- Cache system prevents re-downloading existing content
- Memory-efficient streaming for large media files

### Localization
- Primary interface and documentation in Chinese
- Error messages in Chinese
- File naming uses Chinese date formats where applicable