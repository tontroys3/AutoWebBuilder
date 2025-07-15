from datetime import datetime
from typing import Dict, List, Optional
import re
import uuid

class ArticleManager:
    def __init__(self):
        self.article_categories = [
            'General', 'Technology', 'Business', 'Lifestyle', 'News', 
            'Health', 'Education', 'Entertainment', 'Sports', 'Travel'
        ]
    
    def create_article(self, title: str, content: str, category: str = "General", 
                      tags: List[str] = None, image_url: str = None, 
                      author: str = "Admin") -> Dict:
        """Create a new article"""
        try:
            # Generate article ID
            article_id = str(uuid.uuid4())
            
            # Clean and validate input
            title = title.strip()
            content = content.strip()
            category = category if category in self.article_categories else "General"
            tags = tags or []
            
            # Generate article slug
            slug = self._generate_slug(title)
            
            # Calculate reading time
            reading_time = self._calculate_reading_time(content)
            
            # Generate excerpt
            excerpt = self._generate_excerpt(content)
            
            # Create article data
            article_data = {
                'id': article_id,
                'title': title,
                'slug': slug,
                'content': content,
                'excerpt': excerpt,
                'category': category,
                'tags': tags,
                'author': author,
                'image_url': image_url,
                'reading_time': reading_time,
                'word_count': len(content.split()),
                'status': 'published',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'views': 0,
                'likes': 0
            }
            
            return article_data
        
        except Exception as e:
            return {'error': f'Failed to create article: {str(e)}'}
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title"""
        try:
            # Convert to lowercase and replace spaces with hyphens
            slug = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
            slug = re.sub(r'\s+', '-', slug.strip())
            
            # Remove multiple hyphens
            slug = re.sub(r'-+', '-', slug)
            
            # Remove leading/trailing hyphens
            slug = slug.strip('-')
            
            return slug
        
        except Exception:
            return f"article-{int(datetime.now().timestamp())}"
    
    def _calculate_reading_time(self, content: str) -> int:
        """Calculate estimated reading time in minutes"""
        try:
            words = len(content.split())
            # Average reading speed: 200 words per minute
            reading_time = max(1, round(words / 200))
            return reading_time
        
        except Exception:
            return 1
    
    def _generate_excerpt(self, content: str, length: int = 150) -> str:
        """Generate article excerpt"""
        try:
            if len(content) <= length:
                return content
            
            # Find the last complete sentence within the length limit
            excerpt = content[:length]
            last_sentence_end = max(
                excerpt.rfind('.'),
                excerpt.rfind('!'),
                excerpt.rfind('?')
            )
            
            if last_sentence_end > 0:
                excerpt = excerpt[:last_sentence_end + 1]
            else:
                # Find the last space to avoid cutting words
                last_space = excerpt.rfind(' ')
                if last_space > 0:
                    excerpt = excerpt[:last_space] + '...'
            
            return excerpt
        
        except Exception:
            return content[:150] + '...' if len(content) > 150 else content
    
    def update_article(self, article_id: str, articles: List[Dict], updates: Dict) -> Dict:
        """Update an existing article"""
        try:
            # Find the article
            article_index = None
            for i, article in enumerate(articles):
                if article.get('id') == article_id:
                    article_index = i
                    break
            
            if article_index is None:
                return {'error': 'Article not found'}
            
            # Update article data
            article = articles[article_index]
            
            # Update allowed fields
            updatable_fields = ['title', 'content', 'category', 'tags', 'image_url', 'author']
            for field in updatable_fields:
                if field in updates:
                    article[field] = updates[field]
            
            # Regenerate derived fields if content changed
            if 'title' in updates:
                article['slug'] = self._generate_slug(updates['title'])
            
            if 'content' in updates:
                article['excerpt'] = self._generate_excerpt(updates['content'])
                article['reading_time'] = self._calculate_reading_time(updates['content'])
                article['word_count'] = len(updates['content'].split())
            
            # Update timestamp
            article['updated_at'] = datetime.now().isoformat()
            
            return article
        
        except Exception as e:
            return {'error': f'Failed to update article: {str(e)}'}
    
    def delete_article(self, article_id: str, articles: List[Dict]) -> Dict:
        """Delete an article"""
        try:
            # Find and remove the article
            article_index = None
            for i, article in enumerate(articles):
                if article.get('id') == article_id:
                    article_index = i
                    break
            
            if article_index is None:
                return {'error': 'Article not found'}
            
            deleted_article = articles.pop(article_index)
            
            return {
                'success': True,
                'message': f'Article "{deleted_article.get("title", "Unknown")}" has been deleted',
                'deleted_at': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {'error': f'Failed to delete article: {str(e)}'}
    
    def get_articles_by_category(self, articles: List[Dict], category: str) -> List[Dict]:
        """Get articles filtered by category"""
        try:
            return [article for article in articles if article.get('category') == category]
        
        except Exception as e:
            return []
    
    def get_articles_by_tag(self, articles: List[Dict], tag: str) -> List[Dict]:
        """Get articles filtered by tag"""
        try:
            return [article for article in articles if tag in article.get('tags', [])]
        
        except Exception as e:
            return []
    
    def search_articles(self, articles: List[Dict], query: str) -> List[Dict]:
        """Search articles by title and content"""
        try:
            query = query.lower()
            results = []
            
            for article in articles:
                title = article.get('title', '').lower()
                content = article.get('content', '').lower()
                tags = [tag.lower() for tag in article.get('tags', [])]
                
                if (query in title or 
                    query in content or 
                    any(query in tag for tag in tags)):
                    results.append(article)
            
            return results
        
        except Exception as e:
            return []
    
    def get_article_stats(self, articles: List[Dict]) -> Dict:
        """Get statistics about articles"""
        try:
            if not articles:
                return {
                    'total_articles': 0,
                    'total_words': 0,
                    'average_reading_time': 0,
                    'categories': {},
                    'tags': {},
                    'recent_articles': []
                }
            
            total_articles = len(articles)
            total_words = sum(article.get('word_count', 0) for article in articles)
            average_reading_time = sum(article.get('reading_time', 0) for article in articles) / total_articles
            
            # Category distribution
            categories = {}
            for article in articles:
                category = article.get('category', 'General')
                categories[category] = categories.get(category, 0) + 1
            
            # Tag distribution
            tags = {}
            for article in articles:
                for tag in article.get('tags', []):
                    tags[tag] = tags.get(tag, 0) + 1
            
            # Recent articles (last 5)
            recent_articles = sorted(
                articles,
                key=lambda x: x.get('created_at', ''),
                reverse=True
            )[:5]
            
            return {
                'total_articles': total_articles,
                'total_words': total_words,
                'average_reading_time': round(average_reading_time, 1),
                'categories': categories,
                'tags': dict(sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]),
                'recent_articles': recent_articles
            }
        
        except Exception as e:
            return {'error': f'Failed to get article stats: {str(e)}'}
    
    def sort_articles(self, articles: List[Dict], sort_by: str = 'created_at', 
                     reverse: bool = True) -> List[Dict]:
        """Sort articles by specified field"""
        try:
            valid_sort_fields = ['created_at', 'updated_at', 'title', 'views', 'likes', 'word_count']
            
            if sort_by not in valid_sort_fields:
                sort_by = 'created_at'
            
            return sorted(articles, key=lambda x: x.get(sort_by, ''), reverse=reverse)
        
        except Exception as e:
            return articles
    
    def get_related_articles(self, article: Dict, all_articles: List[Dict], 
                           limit: int = 3) -> List[Dict]:
        """Get related articles based on category and tags"""
        try:
            related = []
            article_id = article.get('id')
            article_category = article.get('category')
            article_tags = set(article.get('tags', []))
            
            for other_article in all_articles:
                if other_article.get('id') == article_id:
                    continue
                
                score = 0
                
                # Same category adds points
                if other_article.get('category') == article_category:
                    score += 3
                
                # Common tags add points
                other_tags = set(other_article.get('tags', []))
                common_tags = article_tags.intersection(other_tags)
                score += len(common_tags)
                
                if score > 0:
                    related.append((other_article, score))
            
            # Sort by score and return top articles
            related.sort(key=lambda x: x[1], reverse=True)
            return [article for article, score in related[:limit]]
        
        except Exception as e:
            return []
    
    def validate_article_data(self, title: str, content: str, category: str = None) -> Dict:
        """Validate article data before creation/update"""
        try:
            errors = []
            warnings = []
            
            # Validate title
            if not title or len(title.strip()) < 3:
                errors.append("Title must be at least 3 characters long")
            elif len(title) > 100:
                warnings.append("Title is longer than 100 characters")
            
            # Validate content
            if not content or len(content.strip()) < 50:
                errors.append("Content must be at least 50 characters long")
            elif len(content) > 10000:
                warnings.append("Content is longer than 10,000 characters")
            
            # Validate category
            if category and category not in self.article_categories:
                warnings.append(f"Category '{category}' is not in the standard list")
            
            # Check for duplicate content (simple check)
            if content and len(set(content.split())) / len(content.split()) < 0.3:
                warnings.append("Content appears to have many repeated words")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings
            }
        
        except Exception as e:
            return {
                'valid': False,
                'errors': [f'Validation error: {str(e)}'],
                'warnings': []
            }
    
    def export_articles(self, articles: List[Dict], format: str = 'json') -> str:
        """Export articles in specified format"""
        try:
            if format == 'json':
                import json
                return json.dumps(articles, indent=2, default=str)
            elif format == 'csv':
                import csv
                import io
                
                output = io.StringIO()
                if articles:
                    fieldnames = ['id', 'title', 'category', 'author', 'created_at', 'word_count', 'reading_time']
                    writer = csv.DictWriter(output, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for article in articles:
                        row = {field: article.get(field, '') for field in fieldnames}
                        writer.writerow(row)
                
                return output.getvalue()
            else:
                return f"Unsupported format: {format}"
        
        except Exception as e:
            return f"Export error: {str(e)}"
