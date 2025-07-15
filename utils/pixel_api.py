import requests
import json
import logging
from typing import Dict, List, Optional
import time
import random

class PixelAPI:
    def __init__(self, api_manager=None):
        self.api_manager = api_manager
        self.api_key = self._get_api_key()
        self.base_url = "https://api.pexels.com/v1"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}' if self.api_key else '',
            'User-Agent': 'AutoWebsiteBuilder/1.0'
        }
        
    def _get_api_key(self) -> Optional[str]:
        """Get Pexels API key from API manager"""
        if self.api_manager:
            return self.api_manager.get_api_key('PEXELS_API_KEY')
        return None
    
    def search_photos(self, query: str, per_page: int = 15, page: int = 1) -> List[Dict]:
        """Search photos on Pexels"""
        try:
            if not self.api_key:
                logging.warning("Pexels API key not found")
                return []
                
            url = f"{self.base_url}/search"
            params = {
                'query': query,
                'per_page': min(per_page, 80),  # Pexels API limit
                'page': page,
                'orientation': 'landscape'  # Prefer landscape images
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                photos = []
                
                for photo in data.get('photos', []):
                    photo_data = {
                        'id': photo.get('id'),
                        'url': photo.get('src', {}).get('original'),
                        'large_url': photo.get('src', {}).get('large'),
                        'medium_url': photo.get('src', {}).get('medium'),
                        'thumbnail_url': photo.get('src', {}).get('small'),
                        'width': photo.get('width'),
                        'height': photo.get('height'),
                        'photographer': photo.get('photographer'),
                        'photographer_url': photo.get('photographer_url'),
                        'alt_text': photo.get('alt', ''),
                        'description': f"Photo by {photo.get('photographer')} on Pexels",
                        'source': 'pexels',
                        'license': 'Pexels License (Free to use)'
                    }
                    photos.append(photo_data)
                
                return photos
                
            else:
                logging.error(f"Pexels API error: {response.status_code}")
                return []
                
        except Exception as e:
            logging.error(f"Error searching Pexels photos: {str(e)}")
            return []
    
    def get_curated_photos(self, per_page: int = 15, page: int = 1) -> List[Dict]:
        """Get curated photos from Pexels"""
        try:
            if not self.api_key:
                logging.warning("Pexels API key not found")
                return []
                
            url = f"{self.base_url}/curated"
            params = {
                'per_page': min(per_page, 80),
                'page': page
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                photos = []
                
                for photo in data.get('photos', []):
                    photo_data = {
                        'id': photo.get('id'),
                        'url': photo.get('src', {}).get('original'),
                        'large_url': photo.get('src', {}).get('large'),
                        'medium_url': photo.get('src', {}).get('medium'),
                        'thumbnail_url': photo.get('src', {}).get('small'),
                        'width': photo.get('width'),
                        'height': photo.get('height'),
                        'photographer': photo.get('photographer'),
                        'photographer_url': photo.get('photographer_url'),
                        'alt_text': photo.get('alt', ''),
                        'description': f"Photo by {photo.get('photographer')} on Pexels",
                        'source': 'pexels',
                        'license': 'Pexels License (Free to use)'
                    }
                    photos.append(photo_data)
                
                return photos
                
            else:
                logging.error(f"Pexels API error: {response.status_code}")
                return []
                
        except Exception as e:
            logging.error(f"Error getting curated photos: {str(e)}")
            return []
    
    def get_photo_details(self, photo_id: int) -> Optional[Dict]:
        """Get details of a specific photo"""
        try:
            if not self.api_key:
                logging.warning("Pexels API key not found")
                return None
                
            url = f"{self.base_url}/photos/{photo_id}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                photo = response.json()
                
                photo_data = {
                    'id': photo.get('id'),
                    'url': photo.get('src', {}).get('original'),
                    'large_url': photo.get('src', {}).get('large'),
                    'medium_url': photo.get('src', {}).get('medium'),
                    'thumbnail_url': photo.get('src', {}).get('small'),
                    'width': photo.get('width'),
                    'height': photo.get('height'),
                    'photographer': photo.get('photographer'),
                    'photographer_url': photo.get('photographer_url'),
                    'alt_text': photo.get('alt', ''),
                    'description': f"Photo by {photo.get('photographer')} on Pexels",
                    'source': 'pexels',
                    'license': 'Pexels License (Free to use)'
                }
                
                return photo_data
                
            else:
                logging.error(f"Pexels API error: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Error getting photo details: {str(e)}")
            return None
    
    def get_optimized_images(self, keyword: str, count: int = 5) -> List[Dict]:
        """Get optimized images for a keyword"""
        try:
            # Search for images
            images = self.search_photos(keyword, per_page=count * 2)  # Get more to filter
            
            if not images:
                # Fallback to curated photos if search fails
                images = self.get_curated_photos(per_page=count)
            
            # Filter and optimize images
            optimized_images = []
            
            for image in images:
                # Prefer landscape images with good aspect ratio
                width = image.get('width', 0)
                height = image.get('height', 0)
                
                if width > 0 and height > 0:
                    aspect_ratio = width / height
                    
                    # Prefer images with good web aspect ratios
                    if 1.2 <= aspect_ratio <= 2.0:
                        optimized_images.append(image)
                        
                        if len(optimized_images) >= count:
                            break
            
            # If not enough optimized images, add remaining
            if len(optimized_images) < count:
                remaining = count - len(optimized_images)
                for image in images:
                    if image not in optimized_images:
                        optimized_images.append(image)
                        remaining -= 1
                        if remaining <= 0:
                            break
            
            return optimized_images[:count]
            
        except Exception as e:
            logging.error(f"Error getting optimized images: {str(e)}")
            return []
    
    def validate_image_url(self, url: str) -> bool:
        """Validate if image URL is accessible"""
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
            
        except Exception as e:
            logging.debug(f"URL validation failed for {url}: {e}")
            return False
    
    def get_image_attribution(self, image_data: Dict) -> str:
        """Get proper attribution text for an image"""
        photographer = image_data.get('photographer', 'Unknown')
        photographer_url = image_data.get('photographer_url', '')
        
        if photographer_url:
            return f'Photo by <a href="{photographer_url}" target="_blank">{photographer}</a> on <a href="https://www.pexels.com" target="_blank">Pexels</a>'
        else:
            return f'Photo by {photographer} on Pexels'
    
    def test_connection(self) -> Dict:
        """Test the API connection"""
        try:
            if not self.api_key:
                return {
                    'success': False,
                    'error': 'Pexels API key not found'
                }
            
            # Test with a simple search
            response = requests.get(
                f"{self.base_url}/search",
                headers=self.headers,
                params={'query': 'nature', 'per_page': 1},
                timeout=5
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Pexels API connection successful'
                }
            else:
                return {
                    'success': False,
                    'error': f'API returned status code: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Connection test failed: {str(e)}'
            }