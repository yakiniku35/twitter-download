"""Twitter下载器配置模块"""
import json
import os
from typing import Dict, Any, Optional


class Config:
    """配置管理类"""
    
    def __init__(self, config_path: str = 'settings.json'):
        self.config_path = config_path
        self._config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"配置文件 {self.config_path} 不存在。"
                "请复制 settings.json.template 并重命名为 settings.json，然后填入你的配置。"
            )
        
        with open(self.config_path, 'r', encoding='utf8') as f:
            config = json.load(f)
        
        # 设置默认值
        if not config.get('save_path'):
            config['save_path'] = os.getcwd()
        config['save_path'] = config['save_path'].rstrip(os.sep) + os.sep
        
        return config
    
    def _validate_config(self) -> None:
        """验证配置有效性"""
        required_fields = ['cookie', 'user_lst']
        
        for field in required_fields:
            if field not in self._config or not self._config[field]:
                raise ValueError(f"配置文件缺少必需字段: {field}")
        
        # 验证cookie格式
        cookie = self._config['cookie']
        if 'auth_token=' not in cookie or 'ct0=' not in cookie:
            raise ValueError("Cookie格式不正确，需要包含 auth_token 和 ct0 字段")
        
        # 验证用户列表
        if not isinstance(self._config['user_lst'], list):
            raise ValueError("user_lst 必须是列表")
        
        # 验证并发数
        max_concurrent = self._config.get('max_concurrent_requests', 10)
        if not isinstance(max_concurrent, int) or max_concurrent < 1:
            print(f"警告: max_concurrent_requests 设置不正确，使用默认值 10")
            self._config['max_concurrent_requests'] = 10
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self._config.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        """支持字典式访问"""
        return self._config[key]
    
    @property
    def save_path(self) -> str:
        return self._config['save_path']
    
    @property
    def cookie(self) -> str:
        return self._config['cookie']
    
    @property
    def user_list(self) -> list:
        return self._config['user_lst']
    
    @property
    def has_retweet(self) -> bool:
        return self._config.get('has_retweet', False)
    
    @property
    def has_highlights(self) -> bool:
        return self._config.get('high_lights', False)
    
    @property
    def has_likes(self) -> bool:
        return self._config.get('likes', False)
    
    @property
    def has_video(self) -> bool:
        return self._config.get('has_video', True)
    
    @property
    def time_range(self) -> Optional[str]:
        return self._config.get('time_range')
    
    @property
    def down_log(self) -> bool:
        return self._config.get('down_log', False)
    
    @property
    def auto_sync(self) -> bool:
        return self._config.get('autoSync', False)
    
    @property
    def log_output(self) -> bool:
        return self._config.get('log_output', False)
    
    @property
    def async_down(self) -> bool:
        return self._config.get('async_down', True)
    
    @property
    def max_concurrent_requests(self) -> int:
        return self._config.get('max_concurrent_requests', 10)
    
    @property
    def image_format(self) -> str:
        return self._config.get('image_format', 'png')
    
    @property
    def proxy(self) -> Optional[str]:
        proxy = self._config.get('proxy', '')
        return proxy if proxy else None
    
    @property
    def md_output(self) -> bool:
        return self._config.get('md_output', True)
    
    @property
    def media_count_limit(self) -> int:
        return self._config.get('media_count_limit', 0)
