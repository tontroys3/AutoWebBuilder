import requests
import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class CloudflareAPI:
    def __init__(self):
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def test_connection(self, api_key: str, zone_id: str) -> Dict:
        """Test connection to Cloudflare API"""
        try:
            headers = {
                **self.headers,
                "Authorization": f"Bearer {api_key}"
            }
            
            response = requests.get(
                f"{self.base_url}/zones/{zone_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True, "message": "Connection successful"}
            else:
                return {"success": False, "error": f"API returned status {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_zone_info(self, api_key: str, zone_id: str) -> Dict:
        """Get zone information"""
        try:
            headers = {
                **self.headers,
                "Authorization": f"Bearer {api_key}"
            }
            
            response = requests.get(
                f"{self.base_url}/zones/{zone_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "zone_info": data.get("result", {})
                }
            else:
                return {"success": False, "error": f"Failed to get zone info: {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_dns_records(self, api_key: str, zone_id: str, domain: str) -> List[Dict]:
        """Get DNS records for a domain"""
        try:
            headers = {
                **self.headers,
                "Authorization": f"Bearer {api_key}"
            }
            
            response = requests.get(
                f"{self.base_url}/zones/{zone_id}/dns_records",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                records = data.get("result", [])
                
                # Filter records for the specific domain
                filtered_records = []
                for record in records:
                    if domain in record.get("name", ""):
                        filtered_records.append({
                            "type": record.get("type"),
                            "name": record.get("name"),
                            "content": record.get("content"),
                            "ttl": record.get("ttl"),
                            "proxied": record.get("proxied", False)
                        })
                
                return filtered_records
            else:
                return []
        
        except Exception as e:
            return []
    
    def create_dns_record(self, api_key: str, zone_id: str, record_data: Dict) -> Dict:
        """Create a DNS record"""
        try:
            headers = {
                **self.headers,
                "Authorization": f"Bearer {api_key}"
            }
            
            response = requests.post(
                f"{self.base_url}/zones/{zone_id}/dns_records",
                headers=headers,
                json=record_data,
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True, "message": "DNS record created successfully"}
            else:
                return {"success": False, "error": f"Failed to create DNS record: {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def deploy_site(self, api_key: str, zone_id: str, domain: str, site_data: Dict) -> Dict:
        """Deploy site to Cloudflare (mock implementation for MVP)"""
        try:
            # In a real implementation, this would:
            # 1. Upload site files to Cloudflare Pages
            # 2. Configure DNS records
            # 3. Set up SSL certificates
            # 4. Configure caching rules
            
            # For MVP, we'll simulate the deployment process
            deployment_steps = [
                "Validating site structure",
                "Uploading static assets",
                "Configuring DNS records",
                "Setting up SSL certificate",
                "Configuring caching rules",
                "Finalizing deployment"
            ]
            
            # Simulate deployment success
            return {
                "success": True,
                "message": "Site deployed successfully",
                "deployment_id": f"deploy_{int(datetime.now().timestamp())}",
                "steps_completed": deployment_steps,
                "domain": domain,
                "deployed_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_analytics(self, api_key: str, zone_id: str, domain: str) -> Dict:
        """Get analytics data for a domain"""
        try:
            headers = {
                **self.headers,
                "Authorization": f"Bearer {api_key}"
            }
            
            # Mock analytics data for MVP
            analytics_data = {
                "requests": {
                    "total": 15420,
                    "cached": 12336,
                    "uncached": 3084
                },
                "bandwidth": {
                    "total_gb": 45.7,
                    "cached_gb": 38.9,
                    "uncached_gb": 6.8
                },
                "threats": {
                    "total": 127,
                    "blocked": 127,
                    "country_breakdown": {
                        "CN": 45,
                        "RU": 32,
                        "US": 25,
                        "OTHER": 25
                    }
                },
                "performance": {
                    "avg_response_time": 289,
                    "cache_hit_ratio": 0.8,
                    "ssl_handshake_time": 45
                }
            }
            
            return {
                "success": True,
                "analytics": analytics_data,
                "domain": domain,
                "updated_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def configure_security(self, api_key: str, zone_id: str, security_settings: Dict) -> Dict:
        """Configure security settings"""
        try:
            headers = {
                **self.headers,
                "Authorization": f"Bearer {api_key}"
            }
            
            # Mock security configuration for MVP
            configured_settings = {
                "ssl_mode": security_settings.get("ssl_mode", "full"),
                "security_level": security_settings.get("security_level", "medium"),
                "challenge_passage": security_settings.get("challenge_passage", "1"),
                "browser_check": security_settings.get("browser_check", True),
                "hotlink_protection": security_settings.get("hotlink_protection", False),
                "ddos_protection": security_settings.get("ddos_protection", True)
            }
            
            return {
                "success": True,
                "message": "Security settings configured successfully",
                "settings": configured_settings,
                "updated_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_cache_stats(self, api_key: str, zone_id: str) -> Dict:
        """Get cache statistics"""
        try:
            # Mock cache statistics for MVP
            cache_stats = {
                "hit_ratio": 0.85,
                "total_requests": 25670,
                "cached_requests": 21819,
                "uncached_requests": 3851,
                "cache_size_gb": 12.4,
                "top_cached_files": [
                    {"file": "/css/style.css", "hits": 1250},
                    {"file": "/js/app.js", "hits": 1180},
                    {"file": "/images/logo.png", "hits": 980},
                    {"file": "/index.html", "hits": 750}
                ],
                "cache_by_type": {
                    "css": 35,
                    "js": 28,
                    "images": 25,
                    "html": 12
                }
            }
            
            return {
                "success": True,
                "cache_stats": cache_stats,
                "updated_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def purge_cache(self, api_key: str, zone_id: str, files: List[str] = None) -> Dict:
        """Purge cache for specific files or entire zone"""
        try:
            headers = {
                **self.headers,
                "Authorization": f"Bearer {api_key}"
            }
            
            purge_data = {}
            if files:
                purge_data["files"] = files
            else:
                purge_data["purge_everything"] = True
            
            # Mock cache purge for MVP
            return {
                "success": True,
                "message": "Cache purged successfully",
                "purged_files": files if files else ["all"],
                "purged_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
