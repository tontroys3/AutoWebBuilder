import requests
import trafilatura
from urllib.parse import urlparse, urljoin
import re
from typing import Dict, List, Optional

class DomainAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def analyze_domain(self, domain: str) -> Dict:
        """Analyze a domain to extract content and structure information"""
        try:
            # Ensure domain has protocol
            if not domain.startswith(('http://', 'https://')):
                domain = f'https://{domain}'
            
            # Extract main content
            content = self._extract_content(domain)
            
            # Extract metadata
            metadata = self._extract_metadata(domain)
            
            # Analyze structure
            structure = self._analyze_structure(domain)
            
            return {
                'domain': domain,
                'content': content,
                'metadata': metadata,
                'structure': structure,
                'analysis_timestamp': str(datetime.now())
            }
        
        except Exception as e:
            return {
                'domain': domain,
                'error': str(e),
                'analysis_timestamp': str(datetime.now())
            }
    
    def _extract_content(self, url: str) -> Dict:
        """Extract main text content from the website"""
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(downloaded)
                title = trafilatura.extract(downloaded, include_comments=False, include_tables=False, only_with_metadata=True)
                
                return {
                    'main_text': text[:2000] if text else "",  # Limit to 2000 chars
                    'title': title,
                    'word_count': len(text.split()) if text else 0,
                    'extractable': True
                }
            else:
                return {'extractable': False, 'error': 'Failed to download content'}
        
        except Exception as e:
            return {'extractable': False, 'error': str(e)}
    
    def _extract_metadata(self, url: str) -> Dict:
        """Extract metadata from the website"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Extract basic metadata
            metadata = {
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'server': response.headers.get('server', ''),
                'title': '',
                'description': '',
                'keywords': []
            }
            
            # Parse HTML for meta tags
            html_content = response.text
            
            # Extract title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
            if title_match:
                metadata['title'] = title_match.group(1).strip()
            
            # Extract meta description
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
            if desc_match:
                metadata['description'] = desc_match.group(1).strip()
            
            # Extract meta keywords
            keywords_match = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
            if keywords_match:
                metadata['keywords'] = [kw.strip() for kw in keywords_match.group(1).split(',')]
            
            return metadata
        
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_structure(self, url: str) -> Dict:
        """Analyze website structure and pages"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            html_content = response.text
            
            # Extract internal links
            links = self._extract_internal_links(html_content, url)
            
            # Analyze navigation structure
            nav_structure = self._analyze_navigation(html_content)
            
            # Detect common page types
            page_types = self._detect_page_types(links)
            
            return {
                'internal_links': links[:20],  # Limit to 20 links
                'navigation_structure': nav_structure,
                'detected_page_types': page_types,
                'total_links': len(links)
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_internal_links(self, html_content: str, base_url: str) -> List[str]:
        """Extract internal links from HTML content"""
        try:
            parsed_base = urlparse(base_url)
            base_domain = parsed_base.netloc
            
            # Find all href attributes
            href_pattern = r'href=["\']([^"\']*)["\']'
            matches = re.findall(href_pattern, html_content, re.IGNORECASE)
            
            internal_links = []
            for link in matches:
                # Skip empty links, anchors, javascript, and external links
                if not link or link.startswith('#') or link.startswith('javascript:') or link.startswith('mailto:'):
                    continue
                
                # Convert relative links to absolute
                if link.startswith('/'):
                    full_url = urljoin(base_url, link)
                elif link.startswith('http'):
                    parsed_link = urlparse(link)
                    if parsed_link.netloc != base_domain:
                        continue  # Skip external links
                    full_url = link
                else:
                    full_url = urljoin(base_url, link)
                
                if full_url not in internal_links:
                    internal_links.append(full_url)
            
            return internal_links
        
        except Exception as e:
            return []
    
    def _analyze_navigation(self, html_content: str) -> Dict:
        """Analyze navigation structure"""
        try:
            nav_structure = {
                'has_main_nav': False,
                'has_footer_nav': False,
                'menu_items': []
            }
            
            # Look for navigation elements
            nav_patterns = [
                r'<nav[^>]*>(.*?)</nav>',
                r'<div[^>]*class=["\'][^"\']*nav[^"\']*["\'][^>]*>(.*?)</div>',
                r'<ul[^>]*class=["\'][^"\']*menu[^"\']*["\'][^>]*>(.*?)</ul>'
            ]
            
            for pattern in nav_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
                if matches:
                    nav_structure['has_main_nav'] = True
                    break
            
            # Look for footer navigation
            footer_pattern = r'<footer[^>]*>(.*?)</footer>'
            footer_match = re.search(footer_pattern, html_content, re.IGNORECASE | re.DOTALL)
            if footer_match:
                footer_content = footer_match.group(1)
                if re.search(r'<a[^>]*href', footer_content, re.IGNORECASE):
                    nav_structure['has_footer_nav'] = True
            
            return nav_structure
        
        except Exception as e:
            return {'error': str(e)}
    
    def _detect_page_types(self, links: List[str]) -> List[str]:
        """Detect common page types from links"""
        page_types = []
        
        common_pages = {
            'about': ['about', 'about-us', 'about_us'],
            'contact': ['contact', 'contact-us', 'contact_us'],
            'privacy': ['privacy', 'privacy-policy', 'privacy_policy'],
            'terms': ['terms', 'terms-of-service', 'terms_of_service'],
            'blog': ['blog', 'news', 'articles'],
            'services': ['services', 'products', 'offerings'],
            'portfolio': ['portfolio', 'work', 'projects'],
            'faq': ['faq', 'help', 'support']
        }
        
        for page_type, keywords in common_pages.items():
            for link in links:
                link_lower = link.lower()
                if any(keyword in link_lower for keyword in keywords):
                    if page_type not in page_types:
                        page_types.append(page_type)
        
        return page_types
    
    def generate_content_suggestions(self, domain_data: Dict) -> List[str]:
        """Generate content suggestions based on domain analysis"""
        suggestions = []
        
        if 'content' in domain_data and domain_data['content'].get('main_text'):
            text = domain_data['content']['main_text']
            
            # Extract key topics
            words = text.lower().split()
            word_freq = {}
            for word in words:
                if len(word) > 4:  # Only consider words longer than 4 chars
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top keywords
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
            for keyword, freq in top_keywords:
                suggestions.append(f"Create content about {keyword} (mentioned {freq} times)")
        
        if 'structure' in domain_data and domain_data['structure'].get('detected_page_types'):
            page_types = domain_data['structure']['detected_page_types']
            for page_type in page_types:
                suggestions.append(f"Consider adding a {page_type} page")
        
        return suggestions
