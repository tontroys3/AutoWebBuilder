import time
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random
from utils.gemini_ai import GeminiAI
from utils.bing_image_scraper import BingImageScraper
from utils.seo_optimizer import SEOOptimizer
import threading

class AutoContentManager:
    def __init__(self, api_manager=None):
        self.api_manager = api_manager
        self.gemini_ai = GeminiAI(api_manager)
        self.image_scraper = BingImageScraper(api_manager)
        self.seo_optimizer = SEOOptimizer()
        self.auto_posting_active = {}
        self.posting_threads = {}
        self.content_queue = {}
        
        # Trending topics and micro-niche categories
        self.trending_topics = [
            "artificial intelligence trends",
            "sustainable living tips",
            "remote work productivity",
            "healthy lifestyle habits",
            "digital marketing strategies",
            "blockchain technology",
            "mental health awareness",
            "personal finance management",
            "social media marketing",
            "web development trends"
        ]
        
        self.micro_niches = {
            "technology": [
                "AI automation tools",
                "cybersecurity best practices",
                "cloud computing solutions",
                "mobile app development",
                "data analytics insights"
            ],
            "health": [
                "nutrition for busy professionals",
                "home workout routines",
                "stress management techniques",
                "sleep optimization tips",
                "natural remedy guides"
            ],
            "business": [
                "small business marketing",
                "entrepreneur success stories",
                "freelancing strategies",
                "startup funding tips",
                "productivity hacks"
            ],
            "lifestyle": [
                "minimalist living",
                "sustainable fashion",
                "home organization",
                "travel planning tips",
                "cooking healthy meals"
            ]
        }
    
    def start_auto_posting(self, domain: str, settings: Dict) -> Dict:
        """Start automatic posting for a domain"""
        try:
            if domain in self.auto_posting_active and self.auto_posting_active[domain]:
                return {"error": "Auto posting already active for this domain"}
            
            self.auto_posting_active[domain] = True
            
            # Create posting thread
            thread = threading.Thread(
                target=self._auto_posting_worker,
                args=(domain, settings),
                daemon=True
            )
            thread.start()
            self.posting_threads[domain] = thread
            
            return {
                "success": True,
                "message": f"Auto posting started for {domain}",
                "settings": settings,
                "started_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to start auto posting: {str(e)}"}
    
    def stop_auto_posting(self, domain: str) -> Dict:
        """Stop automatic posting for a domain"""
        try:
            if domain not in self.auto_posting_active:
                return {"error": "Auto posting not active for this domain"}
            
            self.auto_posting_active[domain] = False
            
            return {
                "success": True,
                "message": f"Auto posting stopped for {domain}",
                "stopped_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to stop auto posting: {str(e)}"}
    
    def _auto_posting_worker(self, domain: str, settings: Dict):
        """Worker thread for automatic posting"""
        try:
            posting_interval = settings.get('interval_hours', 6)  # Default 6 hours
            max_posts_per_day = settings.get('max_posts_per_day', 4)
            category = settings.get('category', 'general')
            
            posts_today = 0
            last_post_date = None
            
            while self.auto_posting_active.get(domain, False):
                try:
                    current_date = datetime.now().date()
                    
                    # Reset daily counter
                    if last_post_date != current_date:
                        posts_today = 0
                        last_post_date = current_date
                    
                    # Check if we've reached daily limit
                    if posts_today >= max_posts_per_day:
                        # Wait until next day
                        time.sleep(3600)  # Sleep for 1 hour
                        continue
                    
                    # Generate and post content
                    result = self.generate_auto_content(domain, category, settings)
                    
                    if result.get('success'):
                        posts_today += 1
                        logging.info(f"Auto-posted article for {domain}: {result.get('title', 'Unknown')}")
                    
                    # Wait for next posting interval
                    time.sleep(posting_interval * 3600)  # Convert hours to seconds
                    
                except Exception as e:
                    logging.error(f"Error in auto posting worker for {domain}: {str(e)}")
                    time.sleep(1800)  # Wait 30 minutes before retrying
                    
        except Exception as e:
            logging.error(f"Auto posting worker crashed for {domain}: {str(e)}")
    
    def generate_auto_content(self, domain: str, category: str, settings: Dict) -> Dict:
        """Generate automatic content for a domain"""
        try:
            # Get trending keyword
            keyword = self.get_trending_keyword(category)
            
            # Generate SEO-optimized title
            titles = self.gemini_ai.generate_article_titles(keyword, count=5)
            if not titles:
                return {"error": "Failed to generate titles"}
            
            title = titles[0]  # Use the first generated title
            
            # Generate keywords
            keywords = self.gemini_ai.generate_keywords(keyword, count=10)
            if not keywords:
                keywords = [keyword]
            
            # Generate article content
            article_data = self.gemini_ai.generate_article_content(
                title=title,
                keywords=keywords[:5],  # Use top 5 keywords
                target_length=settings.get('article_length', 1000)
            )
            
            if 'error' in article_data:
                return article_data
            
            # Get optimized images
            images = self.image_scraper.get_optimized_images(
                keyword=keyword,
                article_content=article_data['content'],
                count=settings.get('images_per_article', 3)
            )
            
            # Process images with lazy loading and alt text
            processed_images = []
            for img in images:
                alt_text = self.gemini_ai.generate_image_alt_text(
                    image_context=title,
                    main_keyword=keyword
                )
                
                processed_images.append({
                    **img,
                    'alt_text': alt_text,
                    'lazy_placeholder': self.image_scraper.get_lazy_load_placeholder(),
                    'optimized': True
                })
            
            # Generate schema markup
            schema_markup = self.gemini_ai.generate_schema_markup(article_data)
            
            # Create complete article data
            complete_article = {
                'title': title,
                'content': article_data['content'],
                'meta_description': article_data['meta_description'],
                'keywords': keywords,
                'images': processed_images,
                'schema_markup': schema_markup,
                'category': category,
                'auto_generated': True,
                'seo_optimized': True,
                'created_at': datetime.now().isoformat(),
                'domain': domain
            }
            
            # Add to content queue
            if domain not in self.content_queue:
                self.content_queue[domain] = []
            self.content_queue[domain].append(complete_article)
            
            return {
                'success': True,
                'title': title,
                'article': complete_article,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to generate auto content: {str(e)}"}
    
    def get_trending_keyword(self, category: str) -> str:
        """Get trending keyword based on category"""
        try:
            # Get category-specific topics
            if category.lower() in self.micro_niches:
                topics = self.micro_niches[category.lower()]
            else:
                topics = self.trending_topics
            
            # Add some randomness to avoid repetition
            return random.choice(topics)
            
        except Exception:
            return "trending topics"
    
    def optimize_existing_content(self, article_data: Dict) -> Dict:
        """Optimize existing article for better SEO"""
        try:
            content = article_data.get('content', '')
            title = article_data.get('title', '')
            
            # Extract main keyword from title
            words = title.lower().split()
            main_keyword = ' '.join(words[:2])  # Use first 2 words as main keyword
            
            # Optimize content
            optimization_result = self.gemini_ai.optimize_content_for_seo(
                content=content,
                target_keyword=main_keyword
            )
            
            if 'error' in optimization_result:
                return optimization_result
            
            # Update article data
            article_data['content'] = optimization_result['optimized_content']
            article_data['seo_optimized'] = True
            article_data['optimization_suggestions'] = optimization_result.get('optimization_suggestions', [])
            article_data['optimized_at'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'optimized_article': article_data,
                'suggestions': optimization_result.get('optimization_suggestions', [])
            }
            
        except Exception as e:
            return {"error": f"Failed to optimize content: {str(e)}"}
    
    def check_and_replace_broken_images(self, article_data: Dict) -> Dict:
        """Check for broken images and replace them"""
        try:
            images = article_data.get('images', [])
            replaced_count = 0
            
            for i, image in enumerate(images):
                url = image.get('url', '')
                
                # Check if image is still available
                if not self.image_scraper.check_image_availability(url):
                    # Find replacement
                    replacement = self.image_scraper.find_replacement_image(
                        original_keyword=article_data.get('title', ''),
                        broken_url=url
                    )
                    
                    if replacement:
                        # Update image with replacement
                        images[i] = {
                            **replacement,
                            'alt_text': image.get('alt_text', ''),
                            'lazy_placeholder': self.image_scraper.get_lazy_load_placeholder(),
                            'replaced': True,
                            'replaced_at': datetime.now().isoformat()
                        }
                        replaced_count += 1
                    else:
                        # Mark as unavailable
                        images[i]['unavailable'] = True
                        images[i]['unavailable_at'] = datetime.now().isoformat()
            
            article_data['images'] = images
            article_data['images_checked_at'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'replaced_count': replaced_count,
                'total_images': len(images),
                'article': article_data
            }
            
        except Exception as e:
            return {"error": f"Failed to check images: {str(e)}"}
    
    def generate_robots_txt(self, domain: str, site_settings: Dict) -> str:
        """Generate robots.txt file for the domain"""
        try:
            sitemap_url = f"https://{domain}/sitemap.xml"
            
            robots_content = f"""User-agent: *
Allow: /

# Sitemap location
Sitemap: {sitemap_url}

# Crawl delay (optional)
Crawl-delay: 1

# Disallow admin pages
Disallow: /admin/
Disallow: /private/
Disallow: /temp/

# Allow specific bot optimizations
User-agent: Googlebot
Allow: /
Crawl-delay: 1

User-agent: Bingbot
Allow: /
Crawl-delay: 1

# SEO optimizations
User-agent: *
Disallow: /search?
Disallow: /*?print=1
Disallow: /*?share=
Disallow: /wp-admin/
Disallow: /wp-includes/
Disallow: /wp-content/plugins/
Disallow: /wp-content/themes/
Allow: /wp-content/uploads/

# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Auto Website Builder - Optimized for SEO
"""
            
            return robots_content
            
        except Exception as e:
            return f"# Error generating robots.txt: {str(e)}"
    
    def get_content_queue(self, domain: str) -> List[Dict]:
        """Get content queue for a domain"""
        return self.content_queue.get(domain, [])
    
    def clear_content_queue(self, domain: str) -> Dict:
        """Clear content queue for a domain"""
        try:
            if domain in self.content_queue:
                del self.content_queue[domain]
            
            return {
                'success': True,
                'message': f'Content queue cleared for {domain}',
                'cleared_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to clear content queue: {str(e)}"}
    
    def get_auto_posting_status(self, domain: str) -> Dict:
        """Get auto posting status for a domain"""
        try:
            is_active = self.auto_posting_active.get(domain, False)
            queue_length = len(self.content_queue.get(domain, []))
            
            return {
                'domain': domain,
                'auto_posting_active': is_active,
                'queue_length': queue_length,
                'has_thread': domain in self.posting_threads,
                'checked_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to get status: {str(e)}"}