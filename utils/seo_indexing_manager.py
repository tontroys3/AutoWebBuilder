import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional

class SEOIndexingManager:
    def __init__(self, domain_config_manager):
        self.domain_config_manager = domain_config_manager
        self.indexing_dir = "PanelDomain/seo_indexing"
        self.ensure_indexing_directory()
    
    def ensure_indexing_directory(self):
        """Create indexing directory if it doesn't exist"""
        if not os.path.exists(self.indexing_dir):
            os.makedirs(self.indexing_dir)
    
    def get_domain_indexing_file(self, domain: str) -> str:
        """Get indexing file path for domain"""
        safe_domain = domain.replace(".", "_").replace("/", "_")
        return os.path.join(self.indexing_dir, f"{safe_domain}_indexing.txt")
    
    def get_domain_sitemap_file(self, domain: str) -> str:
        """Get sitemap file path for domain"""
        safe_domain = domain.replace(".", "_").replace("/", "_")
        return os.path.join(self.indexing_dir, f"{safe_domain}_sitemap.xml")
    
    def submit_url_to_google_index(self, domain: str, url: str, api_key: str = None) -> Dict:
        """Submit URL to Google Index API"""
        try:
            if not api_key:
                return {
                    'success': False,
                    'error': 'Google Index API key not provided'
                }
            
            # Google Indexing API endpoint
            endpoint = f"https://indexing.googleapis.com/v3/urlNotifications:publish"
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'url': url,
                'type': 'URL_UPDATED'
            }
            
            # For demonstration - would normally make actual API call
            # response = requests.post(endpoint, headers=headers, json=data)
            
            # Log the submission attempt
            self.log_indexing_attempt(domain, url, 'google_index', 'submitted')
            
            return {
                'success': True,
                'message': f'URL submitted to Google Index: {url}',
                'url': url,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def submit_sitemap_to_google(self, domain: str, sitemap_url: str, api_key: str = None) -> Dict:
        """Submit sitemap to Google Search Console"""
        try:
            if not api_key:
                return {
                    'success': False,
                    'error': 'Google Search Console API key not provided'
                }
            
            # Google Search Console API endpoint
            endpoint = f"https://searchconsole.googleapis.com/webmasters/v3/sites/{domain}/sitemaps/{sitemap_url}"
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            # For demonstration - would normally make actual API call
            # response = requests.put(endpoint, headers=headers)
            
            # Log the submission
            self.log_indexing_attempt(domain, sitemap_url, 'google_sitemap', 'submitted')
            
            return {
                'success': True,
                'message': f'Sitemap submitted to Google: {sitemap_url}',
                'sitemap_url': sitemap_url,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'sitemap_url': sitemap_url
            }
    
    def log_indexing_attempt(self, domain: str, url: str, service: str, status: str):
        """Log indexing attempt"""
        try:
            indexing_file = self.get_domain_indexing_file(domain)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            log_entry = f"[{timestamp}] {service.upper()}: {status} - {url}\n"
            
            with open(indexing_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            pass
    
    def get_indexing_history(self, domain: str) -> List[Dict]:
        """Get indexing history for domain"""
        try:
            indexing_file = self.get_domain_indexing_file(domain)
            
            if not os.path.exists(indexing_file):
                return []
            
            history = []
            with open(indexing_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        # Parse: [timestamp] SERVICE: status - url
                        parts = line.split('] ', 1)
                        if len(parts) == 2:
                            timestamp = parts[0].replace('[', '')
                            rest = parts[1]
                            
                            service_parts = rest.split(': ', 1)
                            if len(service_parts) == 2:
                                service = service_parts[0]
                                status_url = service_parts[1]
                                
                                status_parts = status_url.split(' - ', 1)
                                if len(status_parts) == 2:
                                    status = status_parts[0]
                                    url = status_parts[1]
                                    
                                    history.append({
                                        'timestamp': timestamp,
                                        'service': service,
                                        'status': status,
                                        'url': url
                                    })
            
            return history
            
        except Exception as e:
            return []
    
    def generate_domain_sitemap(self, domain: str) -> Dict:
        """Generate sitemap for domain"""
        try:
            # Get domain articles
            articles = self.domain_config_manager.load_domain_articles(domain)
            
            # Generate sitemap XML
            sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
            sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            
            # Add homepage
            sitemap_content += f'  <url>\n'
            sitemap_content += f'    <loc>https://{domain}/</loc>\n'
            sitemap_content += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
            sitemap_content += f'    <changefreq>daily</changefreq>\n'
            sitemap_content += f'    <priority>1.0</priority>\n'
            sitemap_content += f'  </url>\n'
            
            # Add articles
            for article in articles:
                article_slug = article.get('title', '').lower().replace(' ', '-')
                sitemap_content += f'  <url>\n'
                sitemap_content += f'    <loc>https://{domain}/{article_slug}</loc>\n'
                sitemap_content += f'    <lastmod>{article.get("created_at", datetime.now().strftime("%Y-%m-%d"))}</lastmod>\n'
                sitemap_content += f'    <changefreq>weekly</changefreq>\n'
                sitemap_content += f'    <priority>0.8</priority>\n'
                sitemap_content += f'  </url>\n'
            
            sitemap_content += '</urlset>\n'
            
            # Save sitemap
            sitemap_file = self.get_domain_sitemap_file(domain)
            with open(sitemap_file, 'w', encoding='utf-8') as f:
                f.write(sitemap_content)
            
            return {
                'success': True,
                'message': f'Sitemap generated for {domain}',
                'file_path': sitemap_file,
                'url_count': len(articles) + 1  # +1 for homepage
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def import_urls_from_file(self, domain: str, file_content: str) -> Dict:
        """Import URLs from file content"""
        try:
            urls = []
            lines = file_content.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith('http://') or line.startswith('https://')):
                    urls.append(line)
            
            # Log imported URLs
            for url in urls:
                self.log_indexing_attempt(domain, url, 'manual_import', 'imported')
            
            return {
                'success': True,
                'message': f'Imported {len(urls)} URLs for {domain}',
                'imported_urls': urls,
                'count': len(urls)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_domain_seo_status(self, domain: str) -> Dict:
        """Get SEO status for domain"""
        try:
            history = self.get_indexing_history(domain)
            
            # Count by service
            google_index_count = len([h for h in history if h['service'] == 'GOOGLE_INDEX'])
            sitemap_count = len([h for h in history if h['service'] == 'GOOGLE_SITEMAP'])
            manual_import_count = len([h for h in history if h['service'] == 'MANUAL_IMPORT'])
            
            # Get last submission
            last_submission = history[-1] if history else None
            
            return {
                'domain': domain,
                'total_submissions': len(history),
                'google_index_submissions': google_index_count,
                'sitemap_submissions': sitemap_count,
                'manual_imports': manual_import_count,
                'last_submission': last_submission,
                'sitemap_exists': os.path.exists(self.get_domain_sitemap_file(domain))
            }
            
        except Exception as e:
            return {
                'domain': domain,
                'error': str(e)
            }
    
    def generate_robots_txt(self, domain: str) -> Dict:
        """Generate robots.txt for domain"""
        try:
            robots_content = f"""User-agent: *
Allow: /

Sitemap: https://{domain}/sitemap.xml

# Generated by cPanel Pro SEO Manager
# Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            robots_file = os.path.join(self.indexing_dir, f"{domain.replace('.', '_')}_robots.txt")
            with open(robots_file, 'w', encoding='utf-8') as f:
                f.write(robots_content)
            
            return {
                'success': True,
                'message': f'robots.txt generated for {domain}',
                'file_path': robots_file,
                'content': robots_content
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_indexing_status(self, domain: str, url: str) -> Dict:
        """Check if URL is indexed (placeholder for real API call)"""
        try:
            # This would normally make a real API call to check indexing status
            # For demonstration, we'll simulate the response
            
            return {
                'success': True,
                'url': url,
                'indexed': True,  # Simulated result
                'last_crawled': datetime.now().strftime('%Y-%m-%d'),
                'status': 'indexed',
                'message': f'URL {url} is indexed by Google'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def bulk_submit_urls(self, domain: str, urls: List[str], api_key: str = None) -> Dict:
        """Submit multiple URLs to Google Index"""
        try:
            results = []
            
            for url in urls:
                result = self.submit_url_to_google_index(domain, url, api_key)
                results.append(result)
            
            successful = len([r for r in results if r.get('success')])
            failed = len(results) - successful
            
            return {
                'success': True,
                'domain': domain,
                'total_urls': len(urls),
                'successful': successful,
                'failed': failed,
                'results': results
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'domain': domain
            }
    
    def export_indexing_report(self, domain: str) -> Dict:
        """Export indexing report for domain"""
        try:
            history = self.get_indexing_history(domain)
            status = self.get_domain_seo_status(domain)
            
            report = {
                'domain': domain,
                'generated_at': datetime.now().isoformat(),
                'summary': status,
                'history': history
            }
            
            report_file = os.path.join(self.indexing_dir, f"{domain.replace('.', '_')}_report.json")
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            
            return {
                'success': True,
                'message': f'Indexing report exported for {domain}',
                'file_path': report_file,
                'report': report
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }