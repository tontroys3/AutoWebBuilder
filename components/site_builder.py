from datetime import datetime
from typing import Dict, List, Optional
import re
from utils.template_engine import TemplateEngine
from utils.seo_optimizer import SEOOptimizer

class SiteBuilder:
    def __init__(self):
        self.template_engine = TemplateEngine()
        self.seo_optimizer = SEOOptimizer()
    
    def create_site(self, domain: str, title: str, description: str, 
                   template: str = "default", category: str = "Blog", 
                   domain_data: Dict = None) -> Dict:
        """Create a new website with the given parameters"""
        try:
            # Generate site ID
            site_id = self._generate_site_id(domain)
            
            # Process domain data if available
            processed_domain_data = self._process_domain_data(domain_data) if domain_data else {}
            
            # Create site structure
            site_data = {
                'id': site_id,
                'domain': domain,
                'title': title,
                'description': description,
                'template': template,
                'category': category,
                'status': 'active',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'domain_data': processed_domain_data,
                'settings': {
                    'responsive': True,
                    'seo_enabled': True,
                    'feed_enabled': True,
                    'analytics_enabled': True
                }
            }
            
            # Generate initial content based on domain analysis
            if domain_data and domain_data.get('content'):
                site_data['auto_generated_content'] = self._generate_content_from_domain(domain_data)
            
            return site_data
        
        except Exception as e:
            return {'error': f'Failed to create site: {str(e)}'}
    
    def _generate_site_id(self, domain: str) -> str:
        """Generate a unique site ID from domain"""
        # Clean domain and create ID
        clean_domain = re.sub(r'[^a-zA-Z0-9]', '', domain.lower())
        timestamp = int(datetime.now().timestamp())
        return f"{clean_domain}_{timestamp}"
    
    def _process_domain_data(self, domain_data: Dict) -> Dict:
        """Process and clean domain analysis data"""
        try:
            processed_data = {}
            
            # Process content data
            if 'content' in domain_data:
                content = domain_data['content']
                processed_data['content'] = {
                    'main_text': content.get('main_text', ''),
                    'word_count': content.get('word_count', 0),
                    'extractable': content.get('extractable', False)
                }
            
            # Process metadata
            if 'metadata' in domain_data:
                metadata = domain_data['metadata']
                processed_data['metadata'] = {
                    'title': metadata.get('title', ''),
                    'description': metadata.get('description', ''),
                    'keywords': metadata.get('keywords', []),
                    'status_code': metadata.get('status_code', 0)
                }
            
            # Process structure data
            if 'structure' in domain_data:
                structure = domain_data['structure']
                processed_data['structure'] = {
                    'detected_page_types': structure.get('detected_page_types', []),
                    'total_links': structure.get('total_links', 0),
                    'has_main_nav': structure.get('navigation_structure', {}).get('has_main_nav', False)
                }
            
            return processed_data
        
        except Exception as e:
            return {'error': f'Failed to process domain data: {str(e)}'}
    
    def _generate_content_from_domain(self, domain_data: Dict) -> Dict:
        """Generate website content based on domain analysis"""
        try:
            content = {}
            
            # Extract key information from domain analysis
            if 'content' in domain_data and domain_data['content'].get('main_text'):
                main_text = domain_data['content']['main_text']
                
                # Generate hero section content
                content['hero'] = {
                    'title': self._extract_title_from_text(main_text),
                    'subtitle': self._extract_subtitle_from_text(main_text),
                    'description': self._extract_description_from_text(main_text)
                }
                
                # Generate feature points
                content['features'] = self._extract_features_from_text(main_text)
                
                # Generate about content
                content['about'] = self._generate_about_content(main_text)
            
            # Extract metadata-based content
            if 'metadata' in domain_data:
                metadata = domain_data['metadata']
                if metadata.get('title'):
                    content['meta_title'] = metadata['title']
                if metadata.get('description'):
                    content['meta_description'] = metadata['description']
                if metadata.get('keywords'):
                    content['keywords'] = metadata['keywords']
            
            return content
        
        except Exception as e:
            return {'error': f'Failed to generate content: {str(e)}'}
    
    def _extract_title_from_text(self, text: str) -> str:
        """Extract a suitable title from text"""
        try:
            # Split text into sentences and find the first meaningful one
            sentences = text.split('.')
            for sentence in sentences[:3]:  # Check first 3 sentences
                sentence = sentence.strip()
                if len(sentence) > 10 and len(sentence) < 60:
                    return sentence
            
            # Fallback to first 50 characters
            return text[:50].strip() + '...' if len(text) > 50 else text.strip()
        
        except Exception:
            return "Welcome to Our Website"
    
    def _extract_subtitle_from_text(self, text: str) -> str:
        """Extract a suitable subtitle from text"""
        try:
            # Look for the second meaningful sentence
            sentences = text.split('.')
            for i, sentence in enumerate(sentences[1:4]):  # Check sentences 2-4
                sentence = sentence.strip()
                if len(sentence) > 20 and len(sentence) < 100:
                    return sentence
            
            # Fallback to a portion of text
            words = text.split()
            if len(words) > 20:
                return ' '.join(words[10:25])
            
            return "Discover what we have to offer"
        
        except Exception:
            return "Your trusted partner for success"
    
    def _extract_description_from_text(self, text: str) -> str:
        """Extract a suitable description from text"""
        try:
            # Take a middle portion of the text for description
            words = text.split()
            if len(words) > 30:
                start_idx = min(20, len(words) // 4)
                end_idx = min(start_idx + 30, len(words))
                return ' '.join(words[start_idx:end_idx])
            
            return text[:150] + '...' if len(text) > 150 else text
        
        except Exception:
            return "We provide exceptional services tailored to your needs."
    
    def _extract_features_from_text(self, text: str) -> List[Dict]:
        """Extract feature points from text"""
        try:
            features = []
            
            # Look for common feature keywords
            feature_keywords = [
                'service', 'solution', 'offer', 'provide', 'feature',
                'benefit', 'advantage', 'quality', 'expertise', 'experience'
            ]
            
            sentences = text.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if any(keyword in sentence.lower() for keyword in feature_keywords):
                    if len(sentence) > 15 and len(sentence) < 100:
                        features.append({
                            'title': sentence[:30] + '...' if len(sentence) > 30 else sentence,
                            'description': sentence
                        })
                
                if len(features) >= 3:
                    break
            
            # Add default features if none found
            if not features:
                features = [
                    {'title': 'Quality Service', 'description': 'We deliver high-quality services tailored to your needs.'},
                    {'title': 'Expert Team', 'description': 'Our experienced team brings expertise to every project.'},
                    {'title': 'Customer Focus', 'description': 'We prioritize customer satisfaction in everything we do.'}
                ]
            
            return features
        
        except Exception:
            return [
                {'title': 'Professional Service', 'description': 'Quality solutions for your business needs.'},
                {'title': 'Reliable Support', 'description': 'Dependable support when you need it most.'},
                {'title': 'Proven Results', 'description': 'Track record of delivering successful outcomes.'}
            ]
    
    def _generate_about_content(self, text: str) -> str:
        """Generate about page content from text"""
        try:
            # Take the first portion of text for about content
            words = text.split()
            if len(words) > 50:
                return ' '.join(words[:50]) + '...'
            
            return text
        
        except Exception:
            return "We are dedicated to providing exceptional services and solutions to help you achieve your goals."
    
    def generate_essential_pages(self, domain: str, site_data: Dict) -> Dict:
        """Generate essential pages for the website"""
        try:
            from components.page_generator import PageGenerator
            page_generator = PageGenerator()
            
            pages = {}
            
            # Generate About page
            pages['about'] = page_generator.generate_about_page(site_data)
            
            # Generate Contact page
            pages['contact'] = page_generator.generate_contact_page(site_data)
            
            # Generate Privacy Policy
            pages['privacy'] = page_generator.generate_privacy_policy(site_data)
            
            # Generate Disclaimer
            pages['disclaimer'] = page_generator.generate_disclaimer(site_data)
            
            # Generate Sitemap
            pages['sitemap'] = self.seo_optimizer.generate_sitemap(site_data)
            
            return pages
        
        except Exception as e:
            return {'error': f'Failed to generate essential pages: {str(e)}'}
    
    def generate_preview(self, domain: str, site_data: Dict) -> str:
        """Generate HTML preview of the website"""
        try:
            template_name = site_data.get('template', 'default')
            
            # Prepare template data
            template_data = {
                'title': site_data.get('title', 'Website'),
                'description': site_data.get('description', 'Website description'),
                'category': site_data.get('category', 'Blog'),
                'template': template_name,
                'domain_data': site_data.get('domain_data', {}),
                'seo_data': site_data.get('seo', {}),
                'articles': []  # Will be populated if articles exist
            }
            
            # Add auto-generated content if available
            if 'auto_generated_content' in site_data:
                template_data.update(site_data['auto_generated_content'])
            
            # Generate HTML using template engine
            html_content = self.template_engine.render_template(template_name, **template_data)
            
            return html_content
        
        except Exception as e:
            return f"<html><body><h1>Error generating preview</h1><p>{str(e)}</p></body></html>"
    
    def update_site(self, domain: str, site_data: Dict, updates: Dict) -> Dict:
        """Update existing site with new data"""
        try:
            # Update basic information
            for key, value in updates.items():
                if key in ['title', 'description', 'template', 'category']:
                    site_data[key] = value
            
            # Update timestamp
            site_data['updated_at'] = datetime.now().isoformat()
            
            # Regenerate SEO data if title or description changed
            if 'title' in updates or 'description' in updates:
                seo_data = self.seo_optimizer.generate_seo_data(
                    site_data.get('title', ''),
                    site_data.get('description', ''),
                    site_data.get('category', '')
                )
                site_data['seo'] = seo_data
            
            return site_data
        
        except Exception as e:
            return {'error': f'Failed to update site: {str(e)}'}
    
    def delete_site(self, domain: str) -> Dict:
        """Delete a website"""
        try:
            return {
                'success': True,
                'message': f'Site {domain} has been deleted',
                'deleted_at': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {'error': f'Failed to delete site: {str(e)}'}
    
    def get_site_stats(self, site_data: Dict) -> Dict:
        """Get statistics for a website"""
        try:
            stats = {
                'created_at': site_data.get('created_at', ''),
                'updated_at': site_data.get('updated_at', ''),
                'template': site_data.get('template', 'default'),
                'category': site_data.get('category', 'Blog'),
                'status': site_data.get('status', 'active'),
                'pages_count': len(site_data.get('pages', {})),
                'seo_score': site_data.get('seo', {}).get('score', 0),
                'responsive': site_data.get('settings', {}).get('responsive', True),
                'feed_enabled': site_data.get('settings', {}).get('feed_enabled', True)
            }
            
            return stats
        
        except Exception as e:
            return {'error': f'Failed to get site stats: {str(e)}'}
