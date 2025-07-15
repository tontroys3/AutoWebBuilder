import os
import json
from datetime import datetime
from typing import Dict, List, Optional

class DomainConfigManager:
    def __init__(self):
        self.config_dir = "PanelDomain"
        self.ensure_config_directory()
    
    def ensure_config_directory(self):
        """Create config directory if it doesn't exist"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def get_config_file_path(self, domain: str) -> str:
        """Get config file path for domain"""
        safe_domain = domain.replace(".", "_").replace("/", "_")
        return os.path.join(self.config_dir, f"{safe_domain}_config.txt")
    
    def get_keywords_file_path(self, domain: str) -> str:
        """Get keywords file path for domain"""
        safe_domain = domain.replace(".", "_").replace("/", "_")
        return os.path.join(self.config_dir, f"{safe_domain}_keywords.txt")
    
    def get_articles_file_path(self, domain: str) -> str:
        """Get articles file path for domain"""
        safe_domain = domain.replace(".", "_").replace("/", "_")
        return os.path.join(self.config_dir, f"{safe_domain}_articles.txt")
    
    def save_domain_config(self, domain: str, config: Dict) -> Dict:
        """Save domain configuration to text file"""
        try:
            config_path = self.get_config_file_path(domain)
            config_text = self.dict_to_text(config, domain)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(config_text)
            
            return {
                'success': True,
                'message': f'Configuration saved for {domain}',
                'file_path': config_path
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def load_domain_config(self, domain: str) -> Dict:
        """Load domain configuration from text file"""
        try:
            config_path = self.get_config_file_path(domain)
            
            if not os.path.exists(config_path):
                return self.get_default_config(domain)
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config_text = f.read()
            
            return self.text_to_dict(config_text, domain)
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'config': self.get_default_config(domain)
            }
    
    def save_domain_keywords(self, domain: str, keywords: List[str]) -> Dict:
        """Save keywords for domain"""
        try:
            keywords_path = self.get_keywords_file_path(domain)
            
            with open(keywords_path, 'w', encoding='utf-8') as f:
                f.write(f"# Keywords for {domain}\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for i, keyword in enumerate(keywords, 1):
                    f.write(f"{i}. {keyword}\n")
                
                f.write(f"\n# Total keywords: {len(keywords)}\n")
            
            return {
                'success': True,
                'message': f'Keywords saved for {domain}',
                'file_path': keywords_path,
                'count': len(keywords)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def load_domain_keywords(self, domain: str) -> List[str]:
        """Load keywords for domain"""
        try:
            keywords_path = self.get_keywords_file_path(domain)
            
            if not os.path.exists(keywords_path):
                return []
            
            keywords = []
            with open(keywords_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Extract keyword from numbered list
                        if '. ' in line:
                            keyword = line.split('. ', 1)[1]
                            keywords.append(keyword)
            
            return keywords
        except Exception as e:
            return []
    
    def save_domain_articles(self, domain: str, articles: List[Dict]) -> Dict:
        """Save articles for domain"""
        try:
            articles_path = self.get_articles_file_path(domain)
            
            with open(articles_path, 'w', encoding='utf-8') as f:
                f.write(f"# Articles for {domain}\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for i, article in enumerate(articles, 1):
                    f.write(f"=== Article {i} ===\n")
                    f.write(f"Title: {article.get('title', 'Untitled')}\n")
                    f.write(f"Category: {article.get('category', 'General')}\n")
                    f.write(f"Keywords: {', '.join(article.get('keywords', []))}\n")
                    f.write(f"Word Count: {article.get('word_count', 0)}\n")
                    f.write(f"Generated: {article.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n")
                    f.write(f"Content:\n{article.get('content', '')}\n\n")
                    f.write("-" * 50 + "\n\n")
                
                f.write(f"# Total articles: {len(articles)}\n")
            
            return {
                'success': True,
                'message': f'Articles saved for {domain}',
                'file_path': articles_path,
                'count': len(articles)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def load_domain_articles(self, domain: str) -> List[Dict]:
        """Load articles for domain"""
        try:
            articles_path = self.get_articles_file_path(domain)
            
            if not os.path.exists(articles_path):
                return []
            
            articles = []
            with open(articles_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Simple parsing - split by article markers
                article_sections = content.split('=== Article ')[1:]  # Skip header
                
                for section in article_sections:
                    if '===' in section:
                        lines = section.split('\n')
                        article = {}
                        
                        # Parse article data
                        for line in lines:
                            if line.startswith('Title: '):
                                article['title'] = line.replace('Title: ', '')
                            elif line.startswith('Category: '):
                                article['category'] = line.replace('Category: ', '')
                            elif line.startswith('Keywords: '):
                                keywords_str = line.replace('Keywords: ', '')
                                article['keywords'] = [k.strip() for k in keywords_str.split(',')]
                            elif line.startswith('Word Count: '):
                                article['word_count'] = int(line.replace('Word Count: ', ''))
                            elif line.startswith('Generated: '):
                                article['created_at'] = line.replace('Generated: ', '')
                            elif line.startswith('Content:'):
                                # Get content after "Content:" line
                                content_start = section.find('Content:\n') + len('Content:\n')
                                content_end = section.find('\n' + '-' * 50)
                                if content_end == -1:
                                    content_end = len(section)
                                article['content'] = section[content_start:content_end].strip()
                        
                        if article.get('title'):
                            articles.append(article)
            
            return articles
        except Exception as e:
            return []
    
    def dict_to_text(self, config: Dict, domain: str) -> str:
        """Convert config dict to readable text format"""
        text = f"# Domain Configuration for {domain}\n"
        text += f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Basic settings
        text += "=== BASIC SETTINGS ===\n"
        text += f"Domain: {domain}\n"
        text += f"Title: {config.get('title', '')}\n"
        text += f"Description: {config.get('description', '')}\n"
        text += f"Template: {config.get('template', 'default')}\n"
        text += f"Category: {config.get('category', 'Blog')}\n"
        text += f"Status: {config.get('status', 'active')}\n\n"
        
        # Auto posting settings
        auto_posting = config.get('auto_posting', {})
        text += "=== AUTO POSTING ===\n"
        text += f"Enabled: {auto_posting.get('enabled', False)}\n"
        text += f"Interval Hours: {auto_posting.get('interval_hours', 6)}\n"
        text += f"Max Posts Per Day: {auto_posting.get('max_posts_per_day', 4)}\n"
        text += f"Article Length: {auto_posting.get('article_length', 1000)}\n"
        text += f"Images Per Article: {auto_posting.get('images_per_article', 3)}\n"
        text += f"SEO Optimization: {auto_posting.get('seo_optimization', True)}\n"
        text += f"Manual Keywords: {', '.join(auto_posting.get('manual_keywords', []))}\n"
        text += f"Manual Titles: {', '.join(auto_posting.get('manual_titles', []))}\n\n"
        
        # SEO settings
        seo_settings = config.get('seo_settings', {})
        text += "=== SEO SETTINGS ===\n"
        text += f"Auto Meta Generation: {seo_settings.get('auto_meta_generation', True)}\n"
        text += f"Schema Markup: {seo_settings.get('schema_markup', True)}\n"
        text += f"Sitemap Auto Update: {seo_settings.get('sitemap_auto_update', True)}\n"
        text += f"Robots TXT: {seo_settings.get('robots_txt', True)}\n"
        text += f"Keyword Optimization: {seo_settings.get('keyword_optimization', True)}\n\n"
        
        # Performance settings
        performance = config.get('performance', {})
        text += "=== PERFORMANCE ===\n"
        text += f"Cache Enabled: {performance.get('cache_enabled', True)}\n"
        text += f"Lazy Loading: {performance.get('lazy_loading', True)}\n"
        text += f"Image Optimization: {performance.get('image_optimization', True)}\n"
        text += f"Minification: {performance.get('minification', True)}\n\n"
        
        # Feed settings
        text += "=== FEED SETTINGS ===\n"
        text += f"Feed Enabled: {config.get('feed_enabled', True)}\n"
        text += f"Sitemap Enabled: {config.get('sitemap_enabled', True)}\n\n"
        
        return text
    
    def text_to_dict(self, text: str, domain: str) -> Dict:
        """Convert text back to config dict (simplified)"""
        config = self.get_default_config(domain)
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('=== ') and line.endswith(' ==='):
                current_section = line.replace('=== ', '').replace(' ===', '').lower()
            elif ': ' in line and not line.startswith('#'):
                key, value = line.split(': ', 1)
                key = key.lower().replace(' ', '_')
                
                # Convert string values to appropriate types
                if value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                elif ',' in value and key.endswith('keywords') or key.endswith('titles'):
                    value = [v.strip() for v in value.split(',') if v.strip()]
                
                # Place value in appropriate section
                if current_section == 'basic_settings':
                    config[key] = value
                elif current_section == 'auto_posting':
                    config['auto_posting'][key] = value
                elif current_section == 'seo_settings':
                    config['seo_settings'][key] = value
                elif current_section == 'performance':
                    config['performance'][key] = value
                elif current_section == 'feed_settings':
                    if key == 'feed_enabled':
                        config['feed_enabled'] = value
                    elif key == 'sitemap_enabled':
                        config['sitemap_enabled'] = value
        
        return config
    
    def get_default_config(self, domain: str) -> Dict:
        """Get default configuration for domain"""
        return {
            'title': f"Website for {domain}",
            'description': f"Professional website for {domain}",
            'template': 'default',
            'category': 'Blog',
            'status': 'active',
            'auto_posting': {
                'enabled': False,
                'interval_hours': 6,
                'max_posts_per_day': 4,
                'article_length': 1000,
                'images_per_article': 3,
                'seo_optimization': True,
                'manual_keywords': [],
                'manual_titles': []
            },
            'feed_enabled': True,
            'sitemap_enabled': True,
            'seo_settings': {
                'auto_meta_generation': True,
                'schema_markup': True,
                'sitemap_auto_update': True,
                'robots_txt': True,
                'keyword_optimization': True
            },
            'performance': {
                'cache_enabled': True,
                'lazy_loading': True,
                'image_optimization': True,
                'minification': True
            }
        }
    
    def get_all_domain_configs(self) -> List[str]:
        """Get list of all domain configs"""
        try:
            configs = []
            for filename in os.listdir(self.config_dir):
                if filename.endswith('_config.txt'):
                    domain = filename.replace('_config.txt', '').replace('_', '.')
                    configs.append(domain)
            return configs
        except Exception as e:
            return []
    
    def delete_domain_config(self, domain: str) -> Dict:
        """Delete domain configuration file"""
        try:
            config_path = self.get_config_file_path(domain)
            keywords_path = self.get_keywords_file_path(domain)
            articles_path = self.get_articles_file_path(domain)
            
            deleted_files = []
            
            if os.path.exists(config_path):
                os.remove(config_path)
                deleted_files.append(config_path)
            
            if os.path.exists(keywords_path):
                os.remove(keywords_path)
                deleted_files.append(keywords_path)
            
            if os.path.exists(articles_path):
                os.remove(articles_path)
                deleted_files.append(articles_path)
            
            return {
                'success': True,
                'message': f'Configuration deleted for {domain}',
                'deleted_files': deleted_files
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_domain_stats(self, domain: str) -> Dict:
        """Get domain statistics"""
        try:
            config = self.load_domain_config(domain)
            keywords = self.load_domain_keywords(domain)
            articles = self.load_domain_articles(domain)
            
            return {
                'domain': domain,
                'config_exists': os.path.exists(self.get_config_file_path(domain)),
                'keywords_count': len(keywords),
                'articles_count': len(articles),
                'status': config.get('status', 'unknown'),
                'auto_posting_enabled': config.get('auto_posting', {}).get('enabled', False),
                'template': config.get('template', 'default'),
                'category': config.get('category', 'Blog')
            }
        except Exception as e:
            return {
                'domain': domain,
                'error': str(e)
            }