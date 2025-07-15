import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import uuid
from utils.auto_content_manager import AutoContentManager
from utils.seo_optimizer import SEOOptimizer
from utils.cloudflare_api import CloudflareAPI

class MultiDomainManager:
    def __init__(self, api_manager=None):
        self.api_manager = api_manager
        self.auto_content_manager = AutoContentManager(api_manager)
        self.seo_optimizer = SEOOptimizer()
        self.cloudflare_api = CloudflareAPI()
        self.domain_settings = {}
        self.active_domains = {}
        
        # Performance and caching settings
        self.cache_settings = {
            'enable_caching': True,
            'cache_duration': 3600,  # 1 hour
            'lazy_loading': True,
            'image_optimization': True,
            'minify_css': True,
            'minify_js': True,
            'gzip_compression': True
        }
    
    def create_domain_panel(self, domain: str, user_settings: Dict) -> Dict:
        """Create a new domain panel with settings"""
        try:
            domain_id = str(uuid.uuid4())
            
            # Default settings for new domain
            default_settings = {
                'domain_id': domain_id,
                'domain': domain,
                'title': user_settings.get('title', f'Website for {domain}'),
                'description': user_settings.get('description', ''),
                'template': user_settings.get('template', 'default'),
                'category': user_settings.get('category', 'Blog'),
                'auto_posting': {
                    'enabled': False,
                    'interval_hours': 6,
                    'max_posts_per_day': 4,
                    'article_length': 1000,
                    'images_per_article': 3,
                    'seo_optimization': True
                },
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
                },
                'content_settings': {
                    'auto_image_replacement': True,
                    'alt_text_generation': True,
                    'content_optimization': True,
                    'broken_link_check': True
                },
                'cloudflare': {
                    'enabled': False,
                    'api_key': '',
                    'zone_id': '',
                    'auto_deploy': False
                },
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'status': 'active'
            }
            
            # Merge user settings with defaults
            domain_settings = {**default_settings, **user_settings}
            domain_settings['domain_id'] = domain_id
            
            # Store domain settings
            self.domain_settings[domain] = domain_settings
            self.active_domains[domain] = True
            
            return {
                'success': True,
                'domain_id': domain_id,
                'domain': domain,
                'settings': domain_settings,
                'panel_url': f'/domain/{domain_id}',
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Failed to create domain panel: {str(e)}'}
    
    def get_domain_panel(self, domain: str) -> Dict:
        """Get domain panel settings and status"""
        try:
            if domain not in self.domain_settings:
                return {'error': 'Domain not found'}
            
            settings = self.domain_settings[domain]
            
            # Get auto posting status
            auto_posting_status = self.auto_content_manager.get_auto_posting_status(domain)
            
            # Get content queue
            content_queue = self.auto_content_manager.get_content_queue(domain)
            
            # Get performance metrics
            performance_metrics = self.get_performance_metrics(domain)
            
            return {
                'domain': domain,
                'settings': settings,
                'auto_posting_status': auto_posting_status,
                'content_queue_length': len(content_queue),
                'performance_metrics': performance_metrics,
                'last_updated': settings.get('updated_at', ''),
                'status': settings.get('status', 'unknown')
            }
            
        except Exception as e:
            return {'error': f'Failed to get domain panel: {str(e)}'}
    
    def update_domain_settings(self, domain: str, updates: Dict) -> Dict:
        """Update domain settings"""
        try:
            if domain not in self.domain_settings:
                return {'error': 'Domain not found'}
            
            # Update settings
            self.domain_settings[domain].update(updates)
            self.domain_settings[domain]['updated_at'] = datetime.now().isoformat()
            
            # Handle auto posting changes
            if 'auto_posting' in updates:
                auto_posting_settings = updates['auto_posting']
                if auto_posting_settings.get('enabled', False):
                    self.auto_content_manager.start_auto_posting(domain, auto_posting_settings)
                else:
                    self.auto_content_manager.stop_auto_posting(domain)
            
            return {
                'success': True,
                'domain': domain,
                'updated_settings': self.domain_settings[domain],
                'updated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Failed to update domain settings: {str(e)}'}
    
    def get_all_domains(self) -> List[Dict]:
        """Get all managed domains"""
        try:
            domains = []
            
            for domain, settings in self.domain_settings.items():
                # Get quick stats
                auto_posting_status = self.auto_content_manager.get_auto_posting_status(domain)
                content_queue_length = len(self.auto_content_manager.get_content_queue(domain))
                
                domains.append({
                    'domain': domain,
                    'domain_id': settings.get('domain_id', ''),
                    'title': settings.get('title', ''),
                    'template': settings.get('template', 'default'),
                    'category': settings.get('category', 'Blog'),
                    'status': settings.get('status', 'unknown'),
                    'auto_posting_active': auto_posting_status.get('auto_posting_active', False),
                    'content_queue_length': content_queue_length,
                    'created_at': settings.get('created_at', ''),
                    'updated_at': settings.get('updated_at', '')
                })
            
            return domains
            
        except Exception as e:
            return [{'error': f'Failed to get domains: {str(e)}'}]
    
    def delete_domain(self, domain: str) -> Dict:
        """Delete a domain and all its settings"""
        try:
            if domain not in self.domain_settings:
                return {'error': 'Domain not found'}
            
            # Stop auto posting
            self.auto_content_manager.stop_auto_posting(domain)
            
            # Clear content queue
            self.auto_content_manager.clear_content_queue(domain)
            
            # Remove from settings
            del self.domain_settings[domain]
            if domain in self.active_domains:
                del self.active_domains[domain]
            
            return {
                'success': True,
                'message': f'Domain {domain} deleted successfully',
                'deleted_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Failed to delete domain: {str(e)}'}
    
    def get_performance_metrics(self, domain: str) -> Dict:
        """Get performance metrics for a domain"""
        try:
            # Mock performance data - in production, this would come from real monitoring
            return {
                'page_load_time': 1.2,  # seconds
                'cache_hit_ratio': 0.85,
                'image_optimization_ratio': 0.92,
                'seo_score': 88,
                'mobile_friendly': True,
                'https_enabled': True,
                'gzip_compression': True,
                'lazy_loading_active': True,
                'last_checked': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Failed to get performance metrics: {str(e)}'}
    
    def optimize_domain_performance(self, domain: str) -> Dict:
        """Optimize domain performance"""
        try:
            if domain not in self.domain_settings:
                return {'error': 'Domain not found'}
            
            settings = self.domain_settings[domain]
            optimizations = []
            
            # Enable caching if not already enabled
            if not settings.get('performance', {}).get('cache_enabled', False):
                settings['performance']['cache_enabled'] = True
                optimizations.append('Enabled caching')
            
            # Enable lazy loading
            if not settings.get('performance', {}).get('lazy_loading', False):
                settings['performance']['lazy_loading'] = True
                optimizations.append('Enabled lazy loading')
            
            # Enable image optimization
            if not settings.get('performance', {}).get('image_optimization', False):
                settings['performance']['image_optimization'] = True
                optimizations.append('Enabled image optimization')
            
            # Enable minification
            if not settings.get('performance', {}).get('minification', False):
                settings['performance']['minification'] = True
                optimizations.append('Enabled CSS/JS minification')
            
            # Update timestamp
            settings['updated_at'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'domain': domain,
                'optimizations': optimizations,
                'performance_settings': settings.get('performance', {}),
                'optimized_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Failed to optimize domain: {str(e)}'}
    
    def generate_domain_robots_txt(self, domain: str) -> str:
        """Generate robots.txt for a specific domain"""
        try:
            if domain not in self.domain_settings:
                return f"# Error: Domain {domain} not found"
            
            settings = self.domain_settings[domain]
            
            return self.auto_content_manager.generate_robots_txt(domain, settings)
            
        except Exception as e:
            return f"# Error generating robots.txt: {str(e)}"
    
    def deploy_to_cloudflare(self, domain: str) -> Dict:
        """Deploy domain to Cloudflare"""
        try:
            if domain not in self.domain_settings:
                return {'error': 'Domain not found'}
            
            settings = self.domain_settings[domain]
            cloudflare_settings = settings.get('cloudflare', {})
            
            if not cloudflare_settings.get('enabled', False):
                return {'error': 'Cloudflare not enabled for this domain'}
            
            api_key = cloudflare_settings.get('api_key', '')
            zone_id = cloudflare_settings.get('zone_id', '')
            
            if not api_key or not zone_id:
                return {'error': 'Cloudflare API key and Zone ID required'}
            
            # Deploy to Cloudflare
            result = self.cloudflare_api.deploy_site(api_key, zone_id, domain, settings)
            
            if result.get('success'):
                settings['cloudflare']['last_deployed'] = datetime.now().isoformat()
                settings['updated_at'] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            return {'error': f'Failed to deploy to Cloudflare: {str(e)}'}
    
    def get_domain_analytics(self, domain: str) -> Dict:
        """Get analytics for a domain"""
        try:
            if domain not in self.domain_settings:
                return {'error': 'Domain not found'}
            
            settings = self.domain_settings[domain]
            cloudflare_settings = settings.get('cloudflare', {})
            
            if cloudflare_settings.get('enabled', False):
                api_key = cloudflare_settings.get('api_key', '')
                zone_id = cloudflare_settings.get('zone_id', '')
                
                if api_key and zone_id:
                    return self.cloudflare_api.get_analytics(api_key, zone_id, domain)
            
            # Return basic analytics if Cloudflare not available
            return {
                'success': True,
                'analytics': {
                    'page_views': 0,
                    'unique_visitors': 0,
                    'bounce_rate': 0,
                    'average_session_duration': 0
                },
                'note': 'Basic analytics - enable Cloudflare for detailed metrics'
            }
            
        except Exception as e:
            return {'error': f'Failed to get analytics: {str(e)}'}
    
    def export_domain_settings(self, domain: str) -> Dict:
        """Export domain settings"""
        try:
            if domain not in self.domain_settings:
                return {'error': 'Domain not found'}
            
            settings = self.domain_settings[domain]
            
            # Remove sensitive data
            export_settings = settings.copy()
            if 'cloudflare' in export_settings:
                export_settings['cloudflare'] = {
                    'enabled': export_settings['cloudflare'].get('enabled', False),
                    'auto_deploy': export_settings['cloudflare'].get('auto_deploy', False)
                }
            
            return {
                'success': True,
                'domain': domain,
                'settings': export_settings,
                'exported_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Failed to export settings: {str(e)}'}
    
    def import_domain_settings(self, domain: str, settings: Dict) -> Dict:
        """Import domain settings"""
        try:
            # Validate settings
            if not isinstance(settings, dict):
                return {'error': 'Invalid settings format'}
            
            # Create or update domain
            if domain not in self.domain_settings:
                self.domain_settings[domain] = {}
            
            # Update with imported settings
            self.domain_settings[domain].update(settings)
            self.domain_settings[domain]['domain'] = domain
            self.domain_settings[domain]['updated_at'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'domain': domain,
                'imported_at': datetime.now().isoformat(),
                'message': 'Settings imported successfully'
            }
            
        except Exception as e:
            return {'error': f'Failed to import settings: {str(e)}'}
    
    def get_domain_grid_view(self) -> List[Dict]:
        """Get simplified grid view of all domains"""
        try:
            domains = []
            
            for domain, settings in self.domain_settings.items():
                auto_posting_status = self.auto_content_manager.get_auto_posting_status(domain)
                performance_metrics = self.get_performance_metrics(domain)
                
                domains.append({
                    'domain': domain,
                    'title': settings.get('title', domain),
                    'template': settings.get('template', 'default'),
                    'status': settings.get('status', 'active'),
                    'auto_posting': auto_posting_status.get('auto_posting_active', False),
                    'seo_score': performance_metrics.get('seo_score', 0),
                    'performance_score': self.calculate_performance_score(performance_metrics),
                    'last_updated': settings.get('updated_at', ''),
                    'article_count': len(self.auto_content_manager.get_content_queue(domain))
                })
            
            return domains
            
        except Exception as e:
            return [{'error': f'Failed to get grid view: {str(e)}'}]
    
    def calculate_performance_score(self, metrics: Dict) -> int:
        """Calculate overall performance score"""
        try:
            score = 0
            
            # Page load time (max 30 points)
            load_time = metrics.get('page_load_time', 5.0)
            if load_time < 1.0:
                score += 30
            elif load_time < 2.0:
                score += 25
            elif load_time < 3.0:
                score += 20
            else:
                score += 10
            
            # Cache hit ratio (max 25 points)
            cache_ratio = metrics.get('cache_hit_ratio', 0.0)
            score += int(cache_ratio * 25)
            
            # Image optimization (max 20 points)
            img_ratio = metrics.get('image_optimization_ratio', 0.0)
            score += int(img_ratio * 20)
            
            # Other factors (max 25 points)
            if metrics.get('mobile_friendly', False):
                score += 8
            if metrics.get('https_enabled', False):
                score += 8
            if metrics.get('gzip_compression', False):
                score += 5
            if metrics.get('lazy_loading_active', False):
                score += 4
            
            return min(score, 100)
            
        except Exception:
            return 0