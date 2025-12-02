"""Twitter API客户端模块"""
import httpx
import json
import time
from typing import Optional, Dict, Any
from utils import quote_url, extract_csrf_token, TWITTER_BEARER_TOKEN


class RateLimitError(Exception):
    """API速率限制错误"""
    pass


class TwitterAPIClient:
    """Twitter API客户端"""
    
    # API endpoints
    USER_BY_SCREEN_NAME = 'https://twitter.com/i/api/graphql/xc8f1g7BYqr6VTzTbvNlGw/UserByScreenName'
    USER_HIGHLIGHTS = 'https://twitter.com/i/api/graphql/w9-i9VNm_92GYFaiyGT1NA/UserHighlightsTweets'
    USER_LIKES = 'https://twitter.com/i/api/graphql/-fbTO1rKPa3nO6-XIRgEFQ/Likes'
    USER_TWEETS = 'https://twitter.com/i/api/graphql/2GIWTr7XwadIixZDtyXd4A/UserTweets'
    USER_MEDIA = 'https://twitter.com/i/api/graphql/Le6KlbilFmSu-5VltFND-Q/UserMedia'
    SEARCH_TIMELINE = 'https://twitter.com/i/api/graphql/tUJgNbJvuiieOXvq7OmHwA/SearchTimeline'
    
    def __init__(self, cookie: str, proxy: Optional[str] = None):
        self.cookie = cookie
        self.proxy = proxy
        self.request_count = 0
        
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'authorization': TWITTER_BEARER_TOKEN,
            'cookie': cookie,
            'x-csrf-token': extract_csrf_token(cookie)
        }
    
    def _make_request(self, url: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        发送API请求
        
        Args:
            url: 请求URL
            max_retries: 最大重试次数
            
        Returns:
            解析后的JSON响应
            
        Raises:
            RateLimitError: API速率限制
            httpx.HTTPError: 网络错误
        """
        for attempt in range(max_retries):
            try:
                response = httpx.get(
                    quote_url(url), 
                    headers=self.headers, 
                    proxy=self.proxy,
                    timeout=30.0
                )
                self.request_count += 1
                
                if response.status_code == 429:
                    raise RateLimitError("API次数已超限")
                
                response.raise_for_status()
                return json.loads(response.text)
                
            except json.JSONDecodeError as e:
                if 'Rate limit exceeded' in response.text:
                    raise RateLimitError("API次数已超限")
                
                if attempt == max_retries - 1:
                    print(f"JSON解析失败: {e}")
                    print(f"响应内容: {response.text[:500]}")
                    raise
                
                time.sleep(2 ** attempt)  # 指数退避
                
            except httpx.HTTPError as e:
                if attempt == max_retries - 1:
                    raise
                
                print(f"请求失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                time.sleep(2 ** attempt)
    
    def get_user_info(self, screen_name: str) -> Dict[str, Any]:
        """获取用户基本信息"""
        variables = {
            "screen_name": screen_name,
            "withSafetyModeUserFields": False
        }
        features = {
            "hidden_profile_likes_enabled": False,
            "hidden_profile_subscriptions_enabled": False,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "subscriptions_verification_info_verified_since_enabled": True,
            "highlights_tweets_tab_ui_enabled": True,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True
        }
        field_toggles = {"withAuxiliaryUserLabels": False}
        
        url = f'{self.USER_BY_SCREEN_NAME}?variables={json.dumps(variables)}&features={json.dumps(features)}&fieldToggles={json.dumps(field_toggles)}'
        
        data = self._make_request(url)
        user_data = data['data']['user']['result']
        
        return {
            'rest_id': user_data['rest_id'],
            'name': user_data['legacy']['name'],
            'screen_name': screen_name,
            'statuses_count': user_data['legacy']['statuses_count'],
            'media_count': user_data['legacy']['media_count']
        }
    
    def set_referer(self, screen_name: str) -> None:
        """设置referer头"""
        self.headers['referer'] = f'https://twitter.com/{screen_name}'
    
    def get_stats(self) -> Dict[str, int]:
        """获取API调用统计"""
        return {
            'request_count': self.request_count
        }
