import os
import json
import logging
from typing import Dict, List, Optional
import requests
from pathlib import Path

class APIManager:
    def __init__(self):
        self.api_keys = {}
        self.load_api_keys()
        
    def load_api_keys(self):
        """Load API keys from apikey.txt file"""
        try:
            api_file = Path("apikey.txt")
            if api_file.exists():
                with open(api_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            self.api_keys[key.strip()] = value.strip()
                            
                logging.info(f"Loaded {len(self.api_keys)} API keys from apikey.txt")
            else:
                logging.warning("apikey.txt not found. Creating template file.")
                self.create_template_file()
                
        except Exception as e:
            logging.error(f"Error loading API keys: {str(e)}")
            
    def create_template_file(self):
        """Create template apikey.txt file"""
        template_content = """# API Keys Configuration
# Format: SERVICE_NAME=your_api_key_here

# Gemini API Key (from Google AI Studio)
GEMINI_API_KEY=your_gemini_api_key_here

# Bing Image Search API Keys (from Microsoft Azure Cognitive Services)
BING_API_KEY_1=your_bing_api_key_1_here
BING_API_KEY_2=your_bing_api_key_2_here
BING_API_KEY_3=your_bing_api_key_3_here

# Pexels API Key (for high-quality stock photos)
PEXELS_API_KEY=your_pexels_api_key_here

# Cloudflare API Key (optional)
CLOUDFLARE_API_KEY=your_cloudflare_api_key_here

# Instructions:
# 1. Replace 'your_api_key_here' with your actual API keys
# 2. Remove lines starting with # (comments)
# 3. Save the file
# 4. The system will automatically load these keys
"""
        
        with open("apikey.txt", 'w') as f:
            f.write(template_content)
            
    def get_api_key(self, service_name: str) -> Optional[str]:
        """Get API key for a specific service"""
        key = self.api_keys.get(service_name)
        if not key or key.startswith('your_'):
            return None
        return key
        
    def get_bing_api_keys(self) -> List[str]:
        """Get all Bing API keys"""
        keys = []
        for i in range(1, 4):  # BING_API_KEY_1, BING_API_KEY_2, BING_API_KEY_3
            key = self.get_api_key(f'BING_API_KEY_{i}')
            if key:
                keys.append(key)
        return keys
        
    def update_api_key(self, service_name: str, api_key: str) -> bool:
        """Update API key for a service"""
        try:
            self.api_keys[service_name] = api_key
            
            # Update the file
            lines = []
            file_path = Path("apikey.txt")
            
            if file_path.exists():
                with open(file_path, 'r') as f:
                    lines = f.readlines()
            
            # Update or add the key
            updated = False
            for i, line in enumerate(lines):
                if line.strip().startswith(f'{service_name}='):
                    lines[i] = f'{service_name}={api_key}\n'
                    updated = True
                    break
            
            if not updated:
                lines.append(f'{service_name}={api_key}\n')
            
            with open(file_path, 'w') as f:
                f.writelines(lines)
                
            return True
            
        except Exception as e:
            logging.error(f"Error updating API key: {str(e)}")
            return False
            
    def test_gemini_api(self) -> Dict:
        """Test Gemini API connection"""
        try:
            api_key = self.get_api_key('GEMINI_API_KEY')
            if not api_key:
                return {'success': False, 'error': 'Gemini API key not found'}
            
            # Simple test request
            from google import genai
            client = genai.Client(api_key=api_key)
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents="Say 'API connection successful'"
            )
            
            if response.text:
                return {'success': True, 'message': 'Gemini API connection successful'}
            else:
                return {'success': False, 'error': 'Empty response from Gemini API'}
                
        except Exception as e:
            return {'success': False, 'error': f'Gemini API test failed: {str(e)}'}
            
    def test_bing_api(self) -> Dict:
        """Test Bing Image Search API connection"""
        try:
            api_keys = self.get_bing_api_keys()
            if not api_keys:
                return {'success': False, 'error': 'No Bing API keys found'}
            
            # Test first API key
            api_key = api_keys[0]
            
            headers = {
                'Ocp-Apim-Subscription-Key': api_key,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            params = {
                'q': 'test',
                'count': 1,
                'safeSearch': 'Moderate'
            }
            
            response = requests.get(
                'https://api.bing.microsoft.com/v7.0/images/search',
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return {'success': True, 'message': f'Bing API connection successful. Found {len(api_keys)} API keys.'}
            else:
                return {'success': False, 'error': f'Bing API returned status code: {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': f'Bing API test failed: {str(e)}'}
            
    def get_api_status(self) -> Dict:
        """Get status of all APIs"""
        status = {
            'gemini': self.test_gemini_api(),
            'bing': self.test_bing_api(),
            'total_keys': len(self.api_keys),
            'available_keys': []
        }
        
        for key, value in self.api_keys.items():
            if value and not value.startswith('your_'):
                status['available_keys'].append(key)
                
        return status
        
    def search_bing_images_json(self, query: str, count: int = 10) -> List[Dict]:
        """Search Bing images using JSON query system"""
        try:
            api_keys = self.get_bing_api_keys()
            if not api_keys:
                return []
            
            # Use first available API key
            api_key = api_keys[0]
            
            headers = {
                'Ocp-Apim-Subscription-Key': api_key,
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # JSON query parameters
            search_params = {
                'q': query,
                'count': min(count, 150),
                'safeSearch': 'Moderate',
                'imageType': 'Photo',
                'freshness': 'Month',
                'size': 'Large',
                'aspect': 'Wide'
            }
            
            response = requests.get(
                'https://api.bing.microsoft.com/v7.0/images/search',
                headers=headers,
                params=search_params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                images = []
                
                for item in data.get('value', []):
                    images.append({
                        'url': item.get('contentUrl', ''),
                        'thumbnail_url': item.get('thumbnailUrl', ''),
                        'name': item.get('name', ''),
                        'width': item.get('width', 0),
                        'height': item.get('height', 0),
                        'size': item.get('contentSize', ''),
                        'format': item.get('encodingFormat', ''),
                        'host_url': item.get('hostPageUrl', ''),
                        'date_published': item.get('datePublished', ''),
                        'is_family_friendly': item.get('isFamilyFriendly', True)
                    })
                
                return images
                
            else:
                logging.error(f"Bing API error: {response.status_code}")
                return []
                
        except Exception as e:
            logging.error(f"Error searching Bing images: {str(e)}")
            return []