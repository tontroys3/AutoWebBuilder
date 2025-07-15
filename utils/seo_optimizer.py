import re
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urlparse

class SEOOptimizer:
    def __init__(self):
        self.stop_words = {
            'en': ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will', 'with']
        }
    
    def generate_seo_data(self, title: str, description: str, category: str) -> Dict:
        """Generate comprehensive SEO data for a site"""
        try:
            # Generate keywords from title and description
            keywords = self._extract_keywords(f"{title} {description}")
            
            # Generate meta tags
            meta_tags = self._generate_meta_tags(title, description, keywords)
            
            # Generate structured data
            structured_data = self._generate_structured_data(title, description, category)
            
            # Generate OpenGraph tags
            og_tags = self._generate_og_tags(title, description)
            
            # Generate Twitter Card tags
            twitter_tags = self._generate_twitter_tags(title, description)
            
            return {
                'title': title,
                'description': description,
                'keywords': keywords,
                'meta_tags': meta_tags,
                'structured_data': structured_data,
                'og_tags': og_tags,
                'twitter_tags': twitter_tags,
                'generated_at': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords from text"""
        try:
            # Clean text
            text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
            words = text.split()
            
            # Remove stop words
            filtered_words = [word for word in words if word not in self.stop_words['en'] and len(word) > 2]
            
            # Count word frequency
            word_freq = {}
            for word in filtered_words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Sort by frequency and return top keywords
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [word for word, freq in sorted_words[:max_keywords]]
        
        except Exception as e:
            return []
    
    def _generate_meta_tags(self, title: str, description: str, keywords: List[str]) -> str:
        """Generate HTML meta tags"""
        try:
            meta_tags = f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="keywords" content="{', '.join(keywords)}">
<meta name="author" content="Auto Website Builder">
<meta name="robots" content="index, follow">
<meta name="language" content="English">
<meta name="revisit-after" content="7 days">"""
            
            return meta_tags
        
        except Exception as e:
            return f"<!-- Error generating meta tags: {str(e)} -->"
    
    def _generate_structured_data(self, title: str, description: str, category: str) -> str:
        """Generate JSON-LD structured data"""
        try:
            if category.lower() == 'business':
                structured_data = {
                    "@context": "https://schema.org",
                    "@type": "LocalBusiness",
                    "name": title,
                    "description": description,
                    "url": "https://example.com",
                    "sameAs": []
                }
            elif category.lower() == 'blog':
                structured_data = {
                    "@context": "https://schema.org",
                    "@type": "Blog",
                    "name": title,
                    "description": description,
                    "url": "https://example.com",
                    "publisher": {
                        "@type": "Organization",
                        "name": title
                    }
                }
            else:
                structured_data = {
                    "@context": "https://schema.org",
                    "@type": "WebSite",
                    "name": title,
                    "description": description,
                    "url": "https://example.com"
                }
            
            import json
            return f'<script type="application/ld+json">{json.dumps(structured_data, indent=2)}</script>'
        
        except Exception as e:
            return f"<!-- Error generating structured data: {str(e)} -->"
    
    def _generate_og_tags(self, title: str, description: str) -> str:
        """Generate OpenGraph meta tags"""
        try:
            og_tags = f"""<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://example.com">
<meta property="og:image" content="https://example.com/og-image.jpg">
<meta property="og:site_name" content="{title}">
<meta property="og:locale" content="en_US">"""
            
            return og_tags
        
        except Exception as e:
            return f"<!-- Error generating OG tags: {str(e)} -->"
    
    def _generate_twitter_tags(self, title: str, description: str) -> str:
        """Generate Twitter Card meta tags"""
        try:
            twitter_tags = f"""<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://example.com/twitter-image.jpg">
<meta name="twitter:creator" content="@website">
<meta name="twitter:site" content="@website">"""
            
            return twitter_tags
        
        except Exception as e:
            return f"<!-- Error generating Twitter tags: {str(e)} -->"
    
    def analyze_site_seo(self, site_data: Dict) -> Dict:
        """Analyze SEO performance of a site"""
        try:
            score = 0
            max_score = 100
            recommendations = []
            
            # Check title
            title = site_data.get('title', '')
            if title:
                if 30 <= len(title) <= 60:
                    score += 20
                else:
                    recommendations.append(f"Title length should be 30-60 characters (current: {len(title)})")
            else:
                recommendations.append("Add a title to your site")
            
            # Check description
            description = site_data.get('description', '')
            if description:
                if 120 <= len(description) <= 160:
                    score += 20
                else:
                    recommendations.append(f"Description length should be 120-160 characters (current: {len(description)})")
            else:
                recommendations.append("Add a meta description to your site")
            
            # Check SEO data
            seo_data = site_data.get('seo', {})
            if seo_data.get('keywords'):
                score += 15
            else:
                recommendations.append("Add relevant keywords to your site")
            
            if seo_data.get('structured_data'):
                score += 15
            else:
                recommendations.append("Add structured data (JSON-LD) to your site")
            
            if seo_data.get('og_tags'):
                score += 10
            else:
                recommendations.append("Add OpenGraph tags for better social media sharing")
            
            if seo_data.get('twitter_tags'):
                score += 10
            else:
                recommendations.append("Add Twitter Card tags for better Twitter sharing")
            
            # Check pages
            pages = site_data.get('pages', {})
            if 'sitemap' in pages:
                score += 10
            else:
                recommendations.append("Generate a sitemap for better search engine indexing")
            
            return {
                'score': min(score, max_score),
                'max_score': max_score,
                'recommendations': recommendations,
                'analyzed_at': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def generate_meta_tags(self, title: str, description: str = "", keywords: str = "") -> str:
        """Generate meta tags for a specific page"""
        try:
            keyword_list = [kw.strip() for kw in keywords.split(',') if kw.strip()] if keywords else []
            
            meta_tags = f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>"""
            
            if description:
                meta_tags += f'\n<meta name="description" content="{description}">'
            
            if keyword_list:
                meta_tags += f'\n<meta name="keywords" content="{", ".join(keyword_list)}">'
            
            meta_tags += """
<meta name="robots" content="index, follow">
<meta name="author" content="Auto Website Builder">"""
            
            return meta_tags
        
        except Exception as e:
            return f"<!-- Error generating meta tags: {str(e)} -->"
    
    def generate_sitemap(self, site_data: Dict, articles: List[Dict] = None) -> str:
        """Generate XML sitemap"""
        try:
            domain = site_data.get('domain', 'https://example.com')
            if not domain.startswith('http'):
                domain = f'https://{domain}'
            
            sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
            sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            
            # Add main pages
            main_pages = ['', 'about', 'contact', 'privacy', 'disclaimer']
            for page in main_pages:
                url = f"{domain}/{page}" if page else domain
                sitemap_xml += f'  <url>\n'
                sitemap_xml += f'    <loc>{url}</loc>\n'
                sitemap_xml += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
                sitemap_xml += f'    <changefreq>weekly</changefreq>\n'
                sitemap_xml += f'    <priority>0.8</priority>\n'
                sitemap_xml += f'  </url>\n'
            
            # Add articles
            if articles:
                for article in articles:
                    article_slug = re.sub(r'[^a-zA-Z0-9\s]', '', article.get('title', '')).replace(' ', '-').lower()
                    url = f"{domain}/articles/{article_slug}"
                    sitemap_xml += f'  <url>\n'
                    sitemap_xml += f'    <loc>{url}</loc>\n'
                    sitemap_xml += f'    <lastmod>{article.get("created_at", datetime.now().strftime("%Y-%m-%d"))}</lastmod>\n'
                    sitemap_xml += f'    <changefreq>monthly</changefreq>\n'
                    sitemap_xml += f'    <priority>0.6</priority>\n'
                    sitemap_xml += f'  </url>\n'
            
            sitemap_xml += '</urlset>'
            
            return sitemap_xml
        
        except Exception as e:
            return f"<!-- Error generating sitemap: {str(e)} -->"
    
    def optimize_images(self, image_data: Dict) -> Dict:
        """Generate image optimization recommendations"""
        try:
            recommendations = []
            
            # Check image alt text
            if not image_data.get('alt'):
                recommendations.append("Add descriptive alt text to images")
            
            # Check image size
            if image_data.get('size_kb', 0) > 500:
                recommendations.append("Optimize image size (current size is too large)")
            
            # Check image format
            if image_data.get('format', '').lower() not in ['webp', 'avif']:
                recommendations.append("Consider using modern image formats (WebP, AVIF)")
            
            # Check image dimensions
            width = image_data.get('width', 0)
            height = image_data.get('height', 0)
            if width > 1920 or height > 1080:
                recommendations.append("Consider reducing image dimensions for web use")
            
            return {
                'recommendations': recommendations,
                'optimized': len(recommendations) == 0
            }
        
        except Exception as e:
            return {'error': str(e)}
