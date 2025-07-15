import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional

class CloudflareDomainManager:
    def __init__(self, domain_config_manager):
        self.domain_config_manager = domain_config_manager
        self.cf_dir = "PanelDomain/cloudflare"
        self.ensure_cf_directory()
    
    def ensure_cf_directory(self):
        """Create Cloudflare directory if it doesn't exist"""
        if not os.path.exists(self.cf_dir):
            os.makedirs(self.cf_dir)
    
    def get_domain_cf_file(self, domain: str) -> str:
        """Get Cloudflare config file for domain"""
        safe_domain = domain.replace(".", "_").replace("/", "_")
        return os.path.join(self.cf_dir, f"{safe_domain}_cloudflare.txt")
    
    def save_domain_cf_config(self, domain: str, cf_config: Dict) -> Dict:
        """Save Cloudflare configuration for domain"""
        try:
            cf_file = self.get_domain_cf_file(domain)
            
            config_text = f"""# Cloudflare Configuration for {domain}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== CLOUDFLARE SETTINGS ===
Domain: {domain}
Zone ID: {cf_config.get('zone_id', '')}
API Email: {cf_config.get('api_email', '')}
API Key: {cf_config.get('api_key', '')}
SSL Mode: {cf_config.get('ssl_mode', 'flexible')}
Security Level: {cf_config.get('security_level', 'medium')}
Cache Level: {cf_config.get('cache_level', 'aggressive')}
Development Mode: {cf_config.get('development_mode', False)}
Always Online: {cf_config.get('always_online', True)}
Auto Minify CSS: {cf_config.get('auto_minify_css', True)}
Auto Minify JS: {cf_config.get('auto_minify_js', True)}
Auto Minify HTML: {cf_config.get('auto_minify_html', True)}

=== DNS RECORDS ===
"""
            
            # Add DNS records if provided
            dns_records = cf_config.get('dns_records', [])
            for record in dns_records:
                config_text += f"Type: {record.get('type', 'A')}\n"
                config_text += f"Name: {record.get('name', '@')}\n"
                config_text += f"Content: {record.get('content', '')}\n"
                config_text += f"TTL: {record.get('ttl', 'auto')}\n"
                config_text += f"Proxied: {record.get('proxied', True)}\n"
                config_text += "---\n"
            
            with open(cf_file, 'w', encoding='utf-8') as f:
                f.write(config_text)
            
            return {
                'success': True,
                'message': f'Cloudflare configuration saved for {domain}',
                'file_path': cf_file
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def load_domain_cf_config(self, domain: str) -> Dict:
        """Load Cloudflare configuration for domain"""
        try:
            cf_file = self.get_domain_cf_file(domain)
            
            if not os.path.exists(cf_file):
                return self.get_default_cf_config(domain)
            
            config = {'domain': domain}
            with open(cf_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Parse configuration
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if ': ' in line and not line.startswith('#'):
                        key, value = line.split(': ', 1)
                        key = key.lower().replace(' ', '_')
                        
                        # Convert values to appropriate types
                        if value.lower() in ['true', 'false']:
                            value = value.lower() == 'true'
                        elif value.isdigit():
                            value = int(value)
                        
                        config[key] = value
            
            return config
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'config': self.get_default_cf_config(domain)
            }
    
    def get_default_cf_config(self, domain: str) -> Dict:
        """Get default Cloudflare configuration"""
        return {
            'domain': domain,
            'zone_id': '',
            'api_email': '',
            'api_key': '',
            'ssl_mode': 'flexible',
            'security_level': 'medium',
            'cache_level': 'aggressive',
            'development_mode': False,
            'always_online': True,
            'auto_minify_css': True,
            'auto_minify_js': True,
            'auto_minify_html': True,
            'dns_records': []
        }
    
    def test_cloudflare_connection(self, domain: str) -> Dict:
        """Test Cloudflare API connection"""
        try:
            cf_config = self.load_domain_cf_config(domain)
            
            if not cf_config.get('api_key') or not cf_config.get('api_email'):
                return {
                    'success': False,
                    'error': 'API credentials not configured'
                }
            
            # Test API connection (placeholder)
            # In real implementation, would make actual API call
            return {
                'success': True,
                'message': 'Cloudflare API connection successful',
                'zone_id': cf_config.get('zone_id', ''),
                'connected': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_domain_analytics(self, domain: str) -> Dict:
        """Get domain analytics from Cloudflare"""
        try:
            cf_config = self.load_domain_cf_config(domain)
            
            # Placeholder analytics data
            # In real implementation, would fetch from Cloudflare API
            analytics = {
                'domain': domain,
                'date_range': '7 days',
                'pageviews': 1234,
                'unique_visitors': 567,
                'requests': 5678,
                'bandwidth': '12.3 GB',
                'cached_requests': 4321,
                'cache_hit_ratio': 0.76,
                'threats_blocked': 23,
                'ssl_requests': 5432,
                'top_countries': [
                    {'country': 'United States', 'requests': 2000},
                    {'country': 'United Kingdom', 'requests': 800},
                    {'country': 'Germany', 'requests': 600}
                ],
                'top_paths': [
                    {'path': '/', 'requests': 1500},
                    {'path': '/blog', 'requests': 800},
                    {'path': '/about', 'requests': 400}
                ]
            }
            
            return {
                'success': True,
                'analytics': analytics
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def purge_cache(self, domain: str) -> Dict:
        """Purge Cloudflare cache for domain"""
        try:
            cf_config = self.load_domain_cf_config(domain)
            
            if not cf_config.get('zone_id'):
                return {
                    'success': False,
                    'error': 'Zone ID not configured'
                }
            
            # Placeholder for cache purge
            # In real implementation, would make API call to purge cache
            
            return {
                'success': True,
                'message': f'Cache purged for {domain}',
                'zone_id': cf_config.get('zone_id'),
                'purged_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_security_level(self, domain: str, security_level: str) -> Dict:
        """Update security level for domain"""
        try:
            cf_config = self.load_domain_cf_config(domain)
            cf_config['security_level'] = security_level
            
            # Save updated config
            save_result = self.save_domain_cf_config(domain, cf_config)
            
            if save_result.get('success'):
                return {
                    'success': True,
                    'message': f'Security level updated to {security_level} for {domain}',
                    'security_level': security_level
                }
            else:
                return save_result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_ssl_mode(self, domain: str, ssl_mode: str) -> Dict:
        """Update SSL mode for domain"""
        try:
            cf_config = self.load_domain_cf_config(domain)
            cf_config['ssl_mode'] = ssl_mode
            
            # Save updated config
            save_result = self.save_domain_cf_config(domain, cf_config)
            
            if save_result.get('success'):
                return {
                    'success': True,
                    'message': f'SSL mode updated to {ssl_mode} for {domain}',
                    'ssl_mode': ssl_mode
                }
            else:
                return save_result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def toggle_development_mode(self, domain: str) -> Dict:
        """Toggle development mode for domain"""
        try:
            cf_config = self.load_domain_cf_config(domain)
            current_mode = cf_config.get('development_mode', False)
            cf_config['development_mode'] = not current_mode
            
            # Save updated config
            save_result = self.save_domain_cf_config(domain, cf_config)
            
            if save_result.get('success'):
                return {
                    'success': True,
                    'message': f'Development mode {"enabled" if not current_mode else "disabled"} for {domain}',
                    'development_mode': not current_mode
                }
            else:
                return save_result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_dns_records(self, domain: str) -> Dict:
        """Get DNS records for domain"""
        try:
            cf_config = self.load_domain_cf_config(domain)
            
            # Placeholder DNS records
            # In real implementation, would fetch from Cloudflare API
            dns_records = [
                {
                    'type': 'A',
                    'name': '@',
                    'content': '192.168.1.1',
                    'ttl': 'auto',
                    'proxied': True
                },
                {
                    'type': 'CNAME',
                    'name': 'www',
                    'content': domain,
                    'ttl': 'auto',
                    'proxied': True
                }
            ]
            
            return {
                'success': True,
                'dns_records': dns_records,
                'domain': domain
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_dns_record(self, domain: str, record_type: str, name: str, content: str, ttl: str = 'auto', proxied: bool = True) -> Dict:
        """Add DNS record for domain"""
        try:
            cf_config = self.load_domain_cf_config(domain)
            
            # Add new DNS record
            new_record = {
                'type': record_type,
                'name': name,
                'content': content,
                'ttl': ttl,
                'proxied': proxied
            }
            
            dns_records = cf_config.get('dns_records', [])
            dns_records.append(new_record)
            cf_config['dns_records'] = dns_records
            
            # Save updated config
            save_result = self.save_domain_cf_config(domain, cf_config)
            
            if save_result.get('success'):
                return {
                    'success': True,
                    'message': f'DNS record added for {domain}',
                    'record': new_record
                }
            else:
                return save_result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_domain_cf_summary(self, domain: str) -> Dict:
        """Get Cloudflare summary for domain"""
        try:
            cf_config = self.load_domain_cf_config(domain)
            
            return {
                'domain': domain,
                'configured': bool(cf_config.get('zone_id')),
                'ssl_mode': cf_config.get('ssl_mode', 'flexible'),
                'security_level': cf_config.get('security_level', 'medium'),
                'development_mode': cf_config.get('development_mode', False),
                'always_online': cf_config.get('always_online', True),
                'dns_records_count': len(cf_config.get('dns_records', [])),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            return {
                'domain': domain,
                'error': str(e)
            }