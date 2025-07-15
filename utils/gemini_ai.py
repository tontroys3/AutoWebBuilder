import os
import json
import logging
from typing import Dict, List, Optional
from google import genai
from google.genai import types
import random
import time

class GeminiAI:
    def __init__(self, api_manager=None):
        self.api_manager = api_manager
        self.client = None
        self.model = "gemini-2.5-flash"
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize Gemini client with API key"""
        try:
            if self.api_manager:
                api_key = self.api_manager.get_api_key('GEMINI_API_KEY')
            else:
                api_key = os.environ.get("GEMINI_API_KEY")
            
            if api_key:
                self.client = genai.Client(api_key=api_key)
            else:
                logging.warning("Gemini API key not found. Content generation will be limited.")
        except Exception as e:
            logging.error(f"Failed to initialize Gemini client: {str(e)}")
            self.client = None
        
    def generate_article_content(self, title: str, keywords: List[str], target_length: int = 1000) -> Dict:
        """Generate article content with SEO optimization"""
        try:
            if not self.client:
                return {'error': 'Gemini API client not initialized. Please check your API key.'}
                
            # Check if API key is available
            if self.api_manager:
                api_key = self.api_manager.get_api_key('GEMINI_API_KEY')
                if not api_key:
                    return {'error': 'Gemini API key not found. Please add your API key to apikey.txt file.'}
            # Create comprehensive prompt for article generation
            prompt = f"""
            Write a comprehensive, SEO-optimized article with the following specifications:
            
            Title: {title}
            Target Keywords: {', '.join(keywords)}
            Target Length: {target_length} words
            
            Requirements:
            1. Create an engaging introduction that hooks readers
            2. Use the target keywords naturally throughout the content
            3. Include relevant headings and subheadings (H2, H3)
            4. Add bullet points or numbered lists where appropriate
            5. Include a strong conclusion
            6. Make the content informative and valuable to readers
            7. Ensure proper keyword density (1-2% for main keyword)
            8. Write in a professional yet accessible tone
            
            Format the response as a complete article with proper HTML structure.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            content = response.text if response.text else ""
            
            # Generate meta description
            meta_desc_prompt = f"""
            Create a compelling meta description (150-160 characters) for this article:
            Title: {title}
            Keywords: {', '.join(keywords)}
            
            The meta description should:
            - Be engaging and click-worthy
            - Include the main keyword naturally
            - Stay within 150-160 characters
            - Encourage users to click
            """
            
            meta_response = self.client.models.generate_content(
                model=self.model,
                contents=meta_desc_prompt
            )
            
            meta_description = meta_response.text if meta_response.text else ""
            
            return {
                'title': title,
                'content': content,
                'meta_description': meta_description.strip(),
                'keywords': keywords,
                'word_count': len(content.split()) if content else 0,
                'generated_at': time.time()
            }
            
        except Exception as e:
            return {'error': f'Failed to generate article: {str(e)}'}
    
    def generate_article_titles(self, topic: str, count: int = 10) -> List[str]:
        """Generate SEO-optimized article titles for a given topic"""
        try:
            prompt = f"""
            Generate {count} SEO-optimized article titles for the topic: "{topic}"
            
            Requirements:
            1. Each title should be 50-60 characters long
            2. Include power words that increase click-through rates
            3. Make them search-engine friendly
            4. Include relevant keywords naturally
            5. Make them engaging and informative
            6. Use numbers, questions, or "how-to" formats where appropriate
            7. Ensure they're unique and compelling
            
            Return only the titles, one per line, without numbering.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            if response.text:
                titles = [title.strip() for title in response.text.split('\n') if title.strip()]
                return titles[:count]
            
            return []
            
        except Exception as e:
            logging.error(f"Error generating titles: {str(e)}")
            return []
    
    def generate_keywords(self, topic: str, count: int = 20) -> List[str]:
        """Generate relevant keywords for a topic"""
        try:
            prompt = f"""
            Generate {count} relevant SEO keywords for the topic: "{topic}"
            
            Include a mix of:
            1. Short-tail keywords (1-2 words)
            2. Long-tail keywords (3-5 words)
            3. Question-based keywords
            4. Commercial intent keywords
            5. Informational keywords
            
            Focus on keywords that:
            - Have good search volume potential
            - Are relevant to the topic
            - Have reasonable competition
            - Would be used by people searching for this topic
            
            Return only the keywords, one per line, without numbering.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            if response.text:
                keywords = [kw.strip() for kw in response.text.split('\n') if kw.strip()]
                return keywords[:count]
            
            return []
            
        except Exception as e:
            logging.error(f"Error generating keywords: {str(e)}")
            return []
    
    def optimize_content_for_seo(self, content: str, target_keyword: str) -> Dict:
        """Optimize existing content for SEO"""
        try:
            prompt = f"""
            Optimize the following content for SEO with the target keyword: "{target_keyword}"
            
            Content to optimize:
            {content}
            
            Optimization requirements:
            1. Ensure target keyword appears in title, meta description, and naturally in content
            2. Add relevant heading structure (H1, H2, H3)
            3. Include semantic keywords and related terms
            4. Optimize keyword density (1-2% for main keyword)
            5. Add internal linking suggestions
            6. Improve readability and structure
            7. Add call-to-action where appropriate
            
            Return the optimized content with proper HTML structure.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            optimized_content = response.text if response.text else content
            
            return {
                'optimized_content': optimized_content,
                'target_keyword': target_keyword,
                'optimization_suggestions': [
                    'Content optimized for target keyword',
                    'Improved heading structure',
                    'Enhanced readability',
                    'Added semantic keywords'
                ]
            }
            
        except Exception as e:
            return {'error': f'Failed to optimize content: {str(e)}'}
    
    def generate_image_alt_text(self, image_context: str, main_keyword: str) -> str:
        """Generate SEO-optimized alt text for images"""
        try:
            prompt = f"""
            Generate SEO-optimized alt text for an image in the context of: "{image_context}"
            Main keyword: "{main_keyword}"
            
            Requirements:
            1. Keep it under 125 characters
            2. Include the main keyword naturally
            3. Be descriptive and helpful for accessibility
            4. Avoid keyword stuffing
            5. Make it relevant to the image and content
            
            Return only the alt text, no additional formatting.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text.strip() if response.text else f"Image related to {main_keyword}"
            
        except Exception as e:
            return f"Image related to {main_keyword}"
    
    def generate_schema_markup(self, article_data: Dict) -> str:
        """Generate JSON-LD schema markup for articles"""
        try:
            prompt = f"""
            Generate JSON-LD schema markup for an article with the following data:
            
            Title: {article_data.get('title', '')}
            Description: {article_data.get('meta_description', '')}
            Keywords: {', '.join(article_data.get('keywords', []))}
            Author: {article_data.get('author', 'Admin')}
            
            Create proper Article schema markup that includes:
            1. Article type
            2. Headline and description
            3. Author information
            4. Date published and modified
            5. Keywords
            6. Publisher information
            
            Return only the JSON-LD code without markdown formatting.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text.strip() if response.text else ""
            
        except Exception as e:
            return ""