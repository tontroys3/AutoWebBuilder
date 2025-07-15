import requests
import json
import time
import random
import logging
from typing import Dict, List, Optional
from urllib.parse import urlparse, urlencode
import re
from bs4 import BeautifulSoup
import urllib.request
import urllib.error

class BingImageSearch:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
        ]
        
    def get_random_user_agent(self):
        """Get a random user agent"""
        return random.choice(self.user_agents)
        
    def search_images(self, query: str, count: int = 10, safe_search: str = "moderate") -> List[Dict]:
        """Search for images using Bing Image Search without API"""
        try:
            # Build search URL
            search_url = f"https://www.bing.com/images/search?q={query}&count={count}&safeSearch={safe_search}"
            
            headers = {
                'User-Agent': self.get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # Add random delay to avoid being blocked
            time.sleep(random.uniform(1.0, 3.0))
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                logging.error(f"Bing search failed with status code: {response.status_code}")
                return []
                
            # Parse HTML to extract image URLs
            soup = BeautifulSoup(response.text, 'html.parser')
            images = []
            
            # Find image containers
            img_containers = soup.find_all('a', {'class': 'iusc'})
            
            for container in img_containers[:count]:
                try:
                    # Extract image data from the container
                    m_attr = container.get('m')
                    if m_attr:
                        img_data = json.loads(m_attr)
                        
                        image_info = {
                            'url': img_data.get('murl', ''),
                            'thumbnail_url': img_data.get('turl', ''),
                            'title': img_data.get('t', ''),
                            'width': img_data.get('w', 0),
                            'height': img_data.get('h', 0),
                            'size': img_data.get('s', ''),
                            'content_type': 'image/jpeg',
                            'host_page_url': img_data.get('purl', ''),
                            'description': img_data.get('d', ''),
                            'alt_text': img_data.get('t', ''),
                            'source': 'bing_search'
                        }
                        
                        # Validate image URL
                        if image_info['url'] and self.validate_image_url(image_info['url']):
                            images.append(image_info)
                            
                except (json.JSONDecodeError, KeyError) as e:
                    logging.warning(f"Error parsing image data: {e}")
                    continue
            
            # If no images found with first method, try alternative parsing
            if not images:
                images = self._parse_images_alternative(soup, count)
                
            return images[:count]
            
        except Exception as e:
            logging.error(f"Error searching images: {str(e)}")
            return []
    
    def _parse_images_alternative(self, soup, count: int) -> List[Dict]:
        """Alternative method to parse images from Bing search"""
        images = []
        
        try:
            # Look for img tags with specific attributes
            img_tags = soup.find_all('img', {'class': ['mimg', 'rms_img']})
            
            for img_tag in img_tags[:count]:
                try:
                    src = img_tag.get('src') or img_tag.get('data-src')
                    if src and src.startswith('http'):
                        image_info = {
                            'url': src,
                            'thumbnail_url': src,
                            'title': img_tag.get('alt', ''),
                            'width': int(img_tag.get('width', 0) or 0),
                            'height': int(img_tag.get('height', 0) or 0),
                            'size': f"{img_tag.get('width', 0)}x{img_tag.get('height', 0)}",
                            'content_type': 'image/jpeg',
                            'host_page_url': '',
                            'description': img_tag.get('alt', ''),
                            'alt_text': img_tag.get('alt', ''),
                            'source': 'bing_search_alt'
                        }
                        
                        if self.validate_image_url(image_info['url']):
                            images.append(image_info)
                            
                except (ValueError, TypeError) as e:
                    logging.warning(f"Error parsing alternative image: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error in alternative image parsing: {e}")
            
        return images
    
    def validate_image_url(self, url: str) -> bool:
        """Validate if image URL is accessible"""
        try:
            if not url or not url.startswith('http'):
                return False
                
            # Check if URL is a valid image URL
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
            url_lower = url.lower()
            
            # Check for image extensions or image-related keywords
            has_image_ext = any(ext in url_lower for ext in image_extensions)
            has_image_keyword = any(keyword in url_lower for keyword in ['image', 'img', 'photo', 'picture'])
            
            if not (has_image_ext or has_image_keyword):
                return False
                
            # Make a quick HEAD request to check if URL is accessible
            headers = {'User-Agent': self.get_random_user_agent()}
            response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '').lower()
                return content_type.startswith('image/')
                
        except Exception as e:
            logging.debug(f"URL validation failed for {url}: {e}")
            
        return False
    
    def get_optimized_images(self, keyword: str, article_content: str, count: int = 5) -> List[Dict]:
        """Get optimized images for article content"""
        try:
            # Generate search queries based on keyword and content
            search_queries = self.generate_search_queries(keyword, article_content)
            
            all_images = []
            
            for query in search_queries[:3]:  # Limit to 3 queries to avoid overload
                images = self.search_images(query, count=count)
                all_images.extend(images)
                
                # Add delay between queries
                time.sleep(random.uniform(2.0, 4.0))
            
            # Remove duplicates and score images
            unique_images = self.remove_duplicates(all_images)
            scored_images = self.score_images(unique_images, keyword)
            
            return scored_images[:count]
            
        except Exception as e:
            logging.error(f"Error getting optimized images: {str(e)}")
            return []
    
    def generate_search_queries(self, keyword: str, content: str) -> List[str]:
        """Generate relevant search queries from content"""
        queries = [keyword]
        
        # Extract important words from content
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        word_freq = {}
        
        for word in words:
            if word not in ['that', 'with', 'have', 'this', 'will', 'your', 'from', 'they', 'know', 'want', 'been', 'good', 'much', 'some', 'time', 'very', 'when', 'come', 'here', 'just', 'like', 'long', 'make', 'many', 'over', 'such', 'take', 'than', 'them', 'well', 'were']:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top frequent words
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Create additional queries
        for word, freq in sorted_words[:5]:
            if freq > 1:
                queries.append(f"{keyword} {word}")
                queries.append(f"{word} {keyword}")
        
        return queries[:10]  # Limit to 10 queries
    
    def remove_duplicates(self, images: List[Dict]) -> List[Dict]:
        """Remove duplicate images based on URL"""
        seen_urls = set()
        unique_images = []
        
        for image in images:
            url = image.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_images.append(image)
        
        return unique_images
    
    def score_images(self, images: List[Dict], keyword: str) -> List[Dict]:
        """Score images based on relevance to keyword"""
        keyword_lower = keyword.lower()
        
        for image in images:
            score = 0
            
            # Title relevance
            title = image.get('title', '').lower()
            if keyword_lower in title:
                score += 30
            
            # Description relevance
            description = image.get('description', '').lower()
            if keyword_lower in description:
                score += 20
            
            # Alt text relevance
            alt_text = image.get('alt_text', '').lower()
            if keyword_lower in alt_text:
                score += 25
            
            # URL relevance
            url = image.get('url', '').lower()
            if keyword_lower in url:
                score += 15
            
            # Image size preference (larger images get higher score)
            width = image.get('width', 0)
            height = image.get('height', 0)
            if width > 800 and height > 600:
                score += 10
            elif width > 500 and height > 400:
                score += 5
            
            image['relevance_score'] = score
        
        # Sort by relevance score
        return sorted(images, key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    def check_image_availability(self, url: str) -> bool:
        """Check if image URL is still available"""
        return self.validate_image_url(url)
    
    def find_replacement_image(self, original_keyword: str, broken_url: str) -> Optional[Dict]:
        """Find replacement for broken image"""
        try:
            images = self.search_images(original_keyword, count=5)
            
            # Filter out the broken URL
            available_images = [img for img in images if img.get('url') != broken_url]
            
            if available_images:
                return available_images[0]
                
        except Exception as e:
            logging.error(f"Error finding replacement image: {str(e)}")
            
        return None
    
    def get_lazy_load_placeholder(self, width: int = 800, height: int = 400) -> str:
        """Generate lazy load placeholder image"""
        return f"data:image/svg+xml;base64,PHN2ZyB3aWR0aD0ie3dpZHRofSIgaGVpZ2h0PSJ7aGVpZ2h0fSIgdmlld0JveD0iMCAwIHt3aWR0aH0ge2hlaWdodH0iIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSJ7d2lkdGh9IiBoZWlnaHQ9Int3aWR0aH0iIGZpbGw9IiNmNWY1ZjUiLz4KPHN2ZyB4PSJ7d2lkdGgvMi0xMn0iIHk9Int3aWR0aC8yLTEyfSIgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0IiB2aWV3Qm94PSIwIDAgMjQgMjQiIGZpbGw9IiNjY2MiPgo8cGF0aCBkPSJNMjEgMTlWNWMwLTEuMS0uOS0yLTItMkg1Yy0xLjEgMC0yIC45LTIgMnYxNGMwIDEuMSAuOSAyIDIgMmgxNGMxLjEgMCAyLS45IDItMnpNOC41IDEzLjVsMS41IDEuNSAxLjUtLjVMOC41IDEzLjV6bTIuNSAyLjVsMS41LTIgMi41IDMuNUg3bDQtNXoiLz4KPC9zdmc+Cjwvc3ZnPg=="