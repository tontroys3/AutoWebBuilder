import requests
import json
import time
import random
import logging
from typing import Dict, List, Optional
from urllib.parse import urlparse
import os
from datetime import datetime, timedelta

class BingImageScraper:
    def __init__(self, api_manager=None):
        self.api_manager = api_manager
        self.api_keys = self._get_api_keys()
        self.current_key_index = 0
        self.base_url = "https://api.bing.microsoft.com/v7.0/images/search"
        self.request_counts = {}
        self.last_request_time = {}
        self.max_requests_per_hour = 1000  # Adjust based on your API limits
        
    def _get_api_keys(self):
        """Get API keys from API manager or environment"""
        if self.api_manager:
            return self.api_manager.get_bing_api_keys()
        else:
            keys = [
                os.environ.get("BING_API_KEY_1"),
                os.environ.get("BING_API_KEY_2"),
                os.environ.get("BING_API_KEY_3")
            ]
            return [key for key in keys if key]  # Remove None values
        
    def rotate_api_key(self):
        """Rotate to next API key to avoid rate limits"""
        if len(self.api_keys) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            logging.info(f"Rotated to API key index: {self.current_key_index}")
    
    def get_current_api_key(self):
        """Get current API key"""
        if not self.api_keys:
            return None
        return self.api_keys[self.current_key_index]
    
    def check_rate_limit(self):
        """Check if we're approaching rate limits"""
        current_key = self.get_current_api_key()
        if not current_key:
            return False
            
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        
        # Clean old requests
        if current_key in self.request_counts:
            self.request_counts[current_key] = [
                req_time for req_time in self.request_counts[current_key] 
                if req_time > hour_ago
            ]
        
        # Check if we're near the limit
        request_count = len(self.request_counts.get(current_key, []))
        if request_count >= self.max_requests_per_hour - 10:  # Buffer of 10 requests
            return True
        
        return False
    
    def record_request(self):
        """Record a request for rate limiting"""
        current_key = self.get_current_api_key()
        if current_key:
            if current_key not in self.request_counts:
                self.request_counts[current_key] = []
            self.request_counts[current_key].append(datetime.now())
    
    def search_images(self, query: str, count: int = 10, safe_search: str = "Moderate") -> List[Dict]:
        """Search for images using Bing Image Search API"""
        try:
            # Check rate limits and rotate if needed
            if self.check_rate_limit():
                self.rotate_api_key()
            
            current_key = self.get_current_api_key()
            if not current_key:
                return []
            
            headers = {
                'Ocp-Apim-Subscription-Key': current_key,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            params = {
                'q': query,
                'count': min(count, 150),  # Bing API limit
                'safeSearch': safe_search,
                'imageType': 'Photo',
                'freshness': 'Month',
                'size': 'Large',
                'aspect': 'Wide'
            }
            
            # Add delay to avoid hitting rate limits
            time.sleep(random.uniform(0.5, 1.5))
            
            response = requests.get(self.base_url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 429:  # Rate limit hit
                logging.warning("Rate limit hit, rotating API key")
                self.rotate_api_key()
                time.sleep(5)  # Wait before retrying
                return self.search_images(query, count, safe_search)
            
            if response.status_code != 200:
                logging.error(f"Bing API error: {response.status_code}")
                return []
            
            self.record_request()
            data = response.json()
            
            images = []
            for item in data.get('value', []):
                try:
                    image_data = {
                        'url': item.get('contentUrl'),
                        'thumbnail_url': item.get('thumbnailUrl'),
                        'name': item.get('name', ''),
                        'width': item.get('width', 0),
                        'height': item.get('height', 0),
                        'size': item.get('contentSize', ''),
                        'host_page_url': item.get('hostPageUrl', ''),
                        'encoding_format': item.get('encodingFormat', ''),
                        'date_published': item.get('datePublished', ''),
                        'is_family_friendly': item.get('isFamilyFriendly', True)
                    }
                    
                    # Validate image URL
                    if self.validate_image_url(image_data['url']):
                        images.append(image_data)
                        
                except Exception as e:
                    logging.error(f"Error processing image item: {str(e)}")
                    continue
            
            return images
            
        except Exception as e:
            logging.error(f"Error searching images: {str(e)}")
            return []
    
    def validate_image_url(self, url: str) -> bool:
        """Validate if image URL is accessible"""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Check for common image extensions
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
            if not any(url.lower().endswith(ext) for ext in valid_extensions):
                # Check if URL has image-related keywords
                if not any(keyword in url.lower() for keyword in ['image', 'img', 'photo', 'pic']):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def get_optimized_images(self, keyword: str, article_content: str, count: int = 5) -> List[Dict]:
        """Get optimized images for article content"""
        try:
            # Generate multiple search queries based on content
            search_queries = self.generate_search_queries(keyword, article_content)
            
            all_images = []
            for query in search_queries[:3]:  # Limit to 3 queries to avoid API overuse
                images = self.search_images(query, count=count)
                all_images.extend(images)
            
            # Remove duplicates and sort by relevance
            unique_images = self.remove_duplicates(all_images)
            
            # Score images based on relevance
            scored_images = self.score_images(unique_images, keyword)
            
            return scored_images[:count]
            
        except Exception as e:
            logging.error(f"Error getting optimized images: {str(e)}")
            return []
    
    def generate_search_queries(self, keyword: str, content: str) -> List[str]:
        """Generate relevant search queries from content"""
        try:
            queries = [keyword]
            
            # Add keyword variations
            queries.extend([
                f"{keyword} professional",
                f"{keyword} business",
                f"{keyword} modern",
                f"{keyword} illustration",
                f"{keyword} concept"
            ])
            
            # Extract important words from content
            words = content.lower().split()
            important_words = []
            
            # Look for nouns and important terms
            for word in words:
                if (len(word) > 4 and 
                    word.isalpha() and 
                    word not in ['this', 'that', 'with', 'from', 'they', 'have', 'were', 'will', 'your', 'what', 'when', 'where', 'which', 'their', 'would', 'there', 'could', 'other']):
                    important_words.append(word)
            
            # Add combinations with important words
            for word in important_words[:5]:  # Limit to avoid too many queries
                queries.append(f"{keyword} {word}")
            
            return queries[:10]  # Limit total queries
            
        except Exception as e:
            logging.error(f"Error generating search queries: {str(e)}")
            return [keyword]
    
    def remove_duplicates(self, images: List[Dict]) -> List[Dict]:
        """Remove duplicate images based on URL"""
        seen_urls = set()
        unique_images = []
        
        for image in images:
            url = image.get('url', '')
            if url not in seen_urls:
                seen_urls.add(url)
                unique_images.append(image)
        
        return unique_images
    
    def score_images(self, images: List[Dict], keyword: str) -> List[Dict]:
        """Score images based on relevance to keyword"""
        try:
            for image in images:
                score = 0
                
                # Score based on filename/name
                name = image.get('name', '').lower()
                if keyword.lower() in name:
                    score += 10
                
                # Score based on image dimensions (prefer landscape for articles)
                width = image.get('width', 0)
                height = image.get('height', 0)
                if width > height:  # Landscape
                    score += 5
                if width >= 800:  # High resolution
                    score += 5
                
                # Score based on format (prefer modern formats)
                format_type = image.get('encoding_format', '').lower()
                if format_type in ['jpeg', 'jpg', 'png', 'webp']:
                    score += 3
                
                # Score based on family-friendly content
                if image.get('is_family_friendly', True):
                    score += 2
                
                image['relevance_score'] = score
            
            # Sort by score
            return sorted(images, key=lambda x: x.get('relevance_score', 0), reverse=True)
            
        except Exception as e:
            logging.error(f"Error scoring images: {str(e)}")
            return images
    
    def check_image_availability(self, url: str) -> bool:
        """Check if image URL is still available"""
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def find_replacement_image(self, original_keyword: str, broken_url: str) -> Optional[Dict]:
        """Find replacement for broken image"""
        try:
            # Search for replacement
            replacement_images = self.search_images(f"{original_keyword} replacement", count=5)
            
            # Filter out the broken URL
            valid_images = [
                img for img in replacement_images 
                if img.get('url') != broken_url and self.check_image_availability(img.get('url', ''))
            ]
            
            return valid_images[0] if valid_images else None
            
        except Exception as e:
            logging.error(f"Error finding replacement image: {str(e)}")
            return None
    
    def get_lazy_load_placeholder(self, width: int = 800, height: int = 400) -> str:
        """Generate lazy load placeholder image"""
        return f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {width} {height}'%3E%3Crect width='100%25' height='100%25' fill='%23f0f0f0'/%3E%3Ctext x='50%25' y='50%25' text-anchor='middle' dy='0.35em' fill='%23999'%3ELoading...%3C/text%3E%3C/svg%3E"