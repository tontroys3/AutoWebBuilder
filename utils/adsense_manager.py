import os
import json
from typing import Dict, List, Optional
from datetime import datetime

class AdSenseManager:
    def __init__(self):
        self.ads_folder = "domain_configs"
        self.global_ads_txt = "ads.txt"
        
        # Ensure folder exists
        if not os.path.exists(self.ads_folder):
            os.makedirs(self.ads_folder)
    
    def get_domain_adsense_config(self, domain: str) -> Dict:
        """Get AdSense configuration for a domain"""
        config_file = os.path.join(self.ads_folder, f"{domain}_adsense.json")
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # Return default configuration
        return {
            "domain": domain,
            "adsense_enabled": False,
            "publisher_id": "",
            "widgets": {
                "header_banner": {
                    "enabled": False,
                    "ad_unit_id": "",
                    "size": "728x90",
                    "code": ""
                },
                "sidebar_rectangle": {
                    "enabled": False,
                    "ad_unit_id": "",
                    "size": "300x250",
                    "code": ""
                },
                "content_banner": {
                    "enabled": False,
                    "ad_unit_id": "",
                    "size": "728x90",
                    "code": ""
                },
                "mobile_banner": {
                    "enabled": False,
                    "ad_unit_id": "",
                    "size": "320x50",
                    "code": ""
                },
                "article_inline": {
                    "enabled": False,
                    "ad_unit_id": "",
                    "size": "728x90",
                    "code": ""
                },
                "footer_banner": {
                    "enabled": False,
                    "ad_unit_id": "",
                    "size": "728x90",
                    "code": ""
                }
            },
            "auto_ads": {
                "enabled": False,
                "code": ""
            },
            "ads_txt_entries": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    def save_domain_adsense_config(self, domain: str, config: Dict) -> Dict:
        """Save AdSense configuration for a domain"""
        try:
            config["updated_at"] = datetime.now().isoformat()
            config_file = os.path.join(self.ads_folder, f"{domain}_adsense.json")
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # Update global ads.txt
            self.update_global_ads_txt()
            
            return {
                "success": True,
                "message": "AdSense configuration saved successfully",
                "config": config
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to save AdSense configuration: {str(e)}"
            }
    
    def generate_ad_code(self, widget_type: str, ad_unit_id: str, size: str = "728x90") -> str:
        """Generate AdSense ad code for a widget"""
        if not ad_unit_id:
            return ""
        
        width, height = size.split('x')
        
        return f"""
<!-- {widget_type.replace('_', ' ').title()} Ad -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<ins class="adsbygoogle"
     style="display:inline-block;width:{width}px;height:{height}px"
     data-ad-client="ca-pub-XXXXXX"
     data-ad-slot="{ad_unit_id}"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({{}});
</script>
"""
    
    def generate_auto_ads_code(self, publisher_id: str) -> str:
        """Generate Auto Ads code"""
        if not publisher_id:
            return ""
        
        return f"""
<!-- Auto Ads -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={publisher_id}"
     crossorigin="anonymous"></script>
"""
    
    def get_widget_positions(self) -> List[Dict]:
        """Get available widget positions"""
        return [
            {
                "id": "header_banner",
                "name": "Header Banner",
                "description": "Banner at the top of the page",
                "recommended_size": "728x90",
                "sizes": ["728x90", "970x90", "320x50"]
            },
            {
                "id": "sidebar_rectangle",
                "name": "Sidebar Rectangle",
                "description": "Rectangle ad in sidebar",
                "recommended_size": "300x250",
                "sizes": ["300x250", "336x280", "300x600"]
            },
            {
                "id": "content_banner",
                "name": "Content Banner",
                "description": "Banner within content area",
                "recommended_size": "728x90",
                "sizes": ["728x90", "970x90", "320x50"]
            },
            {
                "id": "mobile_banner",
                "name": "Mobile Banner",
                "description": "Mobile-optimized banner",
                "recommended_size": "320x50",
                "sizes": ["320x50", "300x250", "728x90"]
            },
            {
                "id": "article_inline",
                "name": "Article Inline",
                "description": "Ad within article content",
                "recommended_size": "728x90",
                "sizes": ["728x90", "300x250", "336x280"]
            },
            {
                "id": "footer_banner",
                "name": "Footer Banner",
                "description": "Banner at the bottom of page",
                "recommended_size": "728x90",
                "sizes": ["728x90", "970x90", "320x50"]
            }
        ]
    
    def update_global_ads_txt(self) -> Dict:
        """Update global ads.txt file with all domain entries"""
        try:
            all_entries = set()
            
            # Collect ads.txt entries from all domains
            for filename in os.listdir(self.ads_folder):
                if filename.endswith('_adsense.json'):
                    domain = filename.replace('_adsense.json', '')
                    config = self.get_domain_adsense_config(domain)
                    
                    for entry in config.get('ads_txt_entries', []):
                        if entry.strip():
                            all_entries.add(entry.strip())
            
            # Write global ads.txt
            with open(self.global_ads_txt, 'w', encoding='utf-8') as f:
                f.write("# ads.txt - Auto-generated by AdSense Manager\n")
                f.write(f"# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for entry in sorted(all_entries):
                    f.write(f"{entry}\n")
            
            return {
                "success": True,
                "message": f"Global ads.txt updated with {len(all_entries)} entries",
                "entries_count": len(all_entries)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to update ads.txt: {str(e)}"
            }
    
    def validate_ad_unit_id(self, ad_unit_id: str) -> bool:
        """Validate AdSense ad unit ID format"""
        if not ad_unit_id:
            return False
        
        # Basic validation for AdSense ad unit ID
        return len(ad_unit_id) >= 10 and ad_unit_id.isdigit()
    
    def validate_publisher_id(self, publisher_id: str) -> bool:
        """Validate AdSense publisher ID format"""
        if not publisher_id:
            return False
        
        # Should start with ca-pub-
        return publisher_id.startswith('ca-pub-') and len(publisher_id) > 7
    
    def get_adsense_stats(self, domain: str) -> Dict:
        """Get AdSense statistics for a domain"""
        config = self.get_domain_adsense_config(domain)
        
        enabled_widgets = sum(1 for widget in config['widgets'].values() if widget.get('enabled', False))
        total_widgets = len(config['widgets'])
        
        return {
            "adsense_enabled": config.get('adsense_enabled', False),
            "total_widgets": total_widgets,
            "enabled_widgets": enabled_widgets,
            "auto_ads_enabled": config.get('auto_ads', {}).get('enabled', False),
            "ads_txt_entries": len(config.get('ads_txt_entries', [])),
            "last_updated": config.get('updated_at', 'Never')
        }
    
    def export_domain_ads(self, domain: str) -> str:
        """Export all ad codes for a domain"""
        config = self.get_domain_adsense_config(domain)
        
        if not config.get('adsense_enabled', False):
            return "<!-- AdSense not enabled for this domain -->"
        
        codes = []
        
        # Auto Ads
        if config.get('auto_ads', {}).get('enabled', False):
            publisher_id = config.get('publisher_id', '')
            if publisher_id:
                codes.append(self.generate_auto_ads_code(publisher_id))
        
        # Widget codes
        for widget_id, widget_config in config.get('widgets', {}).items():
            if widget_config.get('enabled', False):
                custom_code = widget_config.get('code', '')
                if custom_code:
                    codes.append(f"\n<!-- {widget_id.replace('_', ' ').title()} -->\n{custom_code}")
                else:
                    ad_unit_id = widget_config.get('ad_unit_id', '')
                    size = widget_config.get('size', '728x90')
                    if ad_unit_id:
                        codes.append(self.generate_ad_code(widget_id, ad_unit_id, size))
        
        return '\n'.join(codes)
    
    def get_all_domains_adsense(self) -> List[Dict]:
        """Get AdSense status for all domains"""
        domains = []
        
        if not os.path.exists(self.ads_folder):
            return domains
        
        for filename in os.listdir(self.ads_folder):
            if filename.endswith('_adsense.json'):
                domain = filename.replace('_adsense.json', '')
                stats = self.get_adsense_stats(domain)
                domains.append({
                    "domain": domain,
                    **stats
                })
        
        return domains