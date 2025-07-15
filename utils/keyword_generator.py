import os
import random
from datetime import datetime
from typing import List, Dict, Optional
from utils.domain_config_manager import DomainConfigManager

class KeywordGenerator:
    def __init__(self, api_manager=None):
        self.api_manager = api_manager
        self.domain_config_manager = DomainConfigManager()
        
        # Category-based keyword templates
        self.category_keywords = {
            'Technology': [
                'artificial intelligence', 'machine learning', 'blockchain', 'cybersecurity',
                'cloud computing', 'data science', 'web development', 'mobile apps',
                'IoT devices', 'automation', 'digital transformation', 'tech trends'
            ],
            'Business': [
                'entrepreneurship', 'digital marketing', 'business strategy', 'leadership',
                'management', 'finance', 'startup', 'investment', 'e-commerce',
                'business growth', 'productivity', 'innovation'
            ],
            'Health': [
                'nutrition', 'fitness', 'mental health', 'wellness', 'medicine',
                'healthcare', 'exercise', 'healthy lifestyle', 'diet', 'medical research',
                'preventive care', 'health technology'
            ],
            'Education': [
                'online learning', 'education technology', 'skill development', 'training',
                'certification', 'academic research', 'teaching methods', 'student success',
                'educational tools', 'learning platforms', 'knowledge management'
            ],
            'Lifestyle': [
                'travel', 'fashion', 'home decor', 'cooking', 'entertainment',
                'hobbies', 'personal development', 'relationships', 'family',
                'leisure activities', 'cultural trends', 'lifestyle tips'
            ],
            'Finance': [
                'personal finance', 'investing', 'cryptocurrency', 'banking',
                'insurance', 'retirement planning', 'budgeting', 'financial advice',
                'market analysis', 'economic trends', 'wealth building'
            ]
        }
        
        # Trending keyword modifiers
        self.trending_modifiers = [
            '2024', '2025', 'guide', 'tips', 'best practices', 'ultimate',
            'complete', 'advanced', 'beginner', 'expert', 'how to',
            'step by step', 'essential', 'proven', 'effective'
        ]
    
    def generate_keywords_for_domain(self, domain: str, category: str = None, count: int = 20) -> Dict:
        """Generate keywords specifically for a domain and save to file"""
        try:
            # Load domain config to get category if not provided
            if not category:
                domain_config = self.domain_config_manager.load_domain_config(domain)
                category = domain_config.get('category', 'Blog')
            
            # Generate base keywords
            base_keywords = self.category_keywords.get(category, self.category_keywords['Business'])
            
            # Generate domain-specific keywords
            domain_keywords = []
            
            # Add category-specific keywords
            for keyword in base_keywords[:count//2]:
                domain_keywords.append(keyword)
            
            # Add trending combinations
            for _ in range(count//2):
                base_keyword = random.choice(base_keywords)
                modifier = random.choice(self.trending_modifiers)
                combined_keyword = f"{base_keyword} {modifier}"
                domain_keywords.append(combined_keyword)
            
            # Add domain-specific long-tail keywords
            domain_name = domain.replace('.com', '').replace('.', ' ')
            for i in range(min(5, count//4)):
                base_keyword = random.choice(base_keywords)
                domain_specific = f"{base_keyword} for {domain_name}"
                domain_keywords.append(domain_specific)
            
            # Remove duplicates and limit to count
            domain_keywords = list(set(domain_keywords))[:count]
            
            # Save keywords to domain file
            save_result = self.domain_config_manager.save_domain_keywords(domain, domain_keywords)
            
            return {
                'success': True,
                'domain': domain,
                'category': category,
                'keywords': domain_keywords,
                'count': len(domain_keywords),
                'file_path': save_result.get('file_path', ''),
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'domain': domain
            }
    
    def generate_trending_keyword(self, category: str = 'Business') -> str:
        """Generate a single trending keyword for category"""
        try:
            base_keywords = self.category_keywords.get(category, self.category_keywords['Business'])
            base_keyword = random.choice(base_keywords)
            modifier = random.choice(self.trending_modifiers)
            
            return f"{base_keyword} {modifier}"
        except Exception as e:
            return f"{category} guide"
    
    def generate_keyword_variations(self, base_keyword: str, count: int = 10) -> List[str]:
        """Generate variations of a base keyword"""
        variations = []
        
        # Add modifiers
        for modifier in self.trending_modifiers[:count//2]:
            variations.append(f"{base_keyword} {modifier}")
            variations.append(f"{modifier} {base_keyword}")
        
        # Add question formats
        question_formats = [
            f"what is {base_keyword}",
            f"how to {base_keyword}",
            f"why {base_keyword}",
            f"best {base_keyword}",
            f"{base_keyword} benefits"
        ]
        
        variations.extend(question_formats[:count//2])
        
        return variations[:count]
    
    def get_domain_keywords(self, domain: str) -> List[str]:
        """Get saved keywords for domain"""
        return self.domain_config_manager.load_domain_keywords(domain)
    
    def add_manual_keywords(self, domain: str, keywords: List[str]) -> Dict:
        """Add manual keywords to domain"""
        try:
            existing_keywords = self.domain_config_manager.load_domain_keywords(domain)
            
            # Combine and remove duplicates
            all_keywords = list(set(existing_keywords + keywords))
            
            # Save updated keywords
            save_result = self.domain_config_manager.save_domain_keywords(domain, all_keywords)
            
            return {
                'success': True,
                'domain': domain,
                'added_keywords': keywords,
                'total_keywords': len(all_keywords),
                'file_path': save_result.get('file_path', '')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'domain': domain
            }
    
    def generate_seo_keywords(self, domain: str, target_keyword: str) -> Dict:
        """Generate SEO-optimized keywords for specific target"""
        try:
            seo_keywords = []
            
            # Long-tail variations
            long_tail_templates = [
                f"best {target_keyword}",
                f"how to {target_keyword}",
                f"{target_keyword} guide",
                f"{target_keyword} tips",
                f"{target_keyword} benefits",
                f"{target_keyword} for beginners",
                f"advanced {target_keyword}",
                f"{target_keyword} strategies",
                f"{target_keyword} techniques",
                f"{target_keyword} solutions"
            ]
            
            seo_keywords.extend(long_tail_templates)
            
            # Location-based if applicable
            locations = ['online', 'local', 'business', 'professional', 'expert']
            for location in locations:
                seo_keywords.append(f"{target_keyword} {location}")
            
            # Year-based
            current_year = datetime.now().year
            seo_keywords.extend([
                f"{target_keyword} {current_year}",
                f"{target_keyword} {current_year + 1}",
                f"latest {target_keyword}"
            ])
            
            # Save SEO keywords
            existing_keywords = self.domain_config_manager.load_domain_keywords(domain)
            all_keywords = list(set(existing_keywords + seo_keywords))
            
            save_result = self.domain_config_manager.save_domain_keywords(domain, all_keywords)
            
            return {
                'success': True,
                'domain': domain,
                'target_keyword': target_keyword,
                'seo_keywords': seo_keywords,
                'total_keywords': len(all_keywords),
                'file_path': save_result.get('file_path', '')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'domain': domain
            }
    
    def analyze_keyword_performance(self, domain: str) -> Dict:
        """Analyze keyword performance for domain"""
        try:
            keywords = self.domain_config_manager.load_domain_keywords(domain)
            articles = self.domain_config_manager.load_domain_articles(domain)
            
            # Simple analysis
            keyword_usage = {}
            for keyword in keywords:
                usage_count = 0
                for article in articles:
                    if keyword.lower() in article.get('content', '').lower():
                        usage_count += 1
                keyword_usage[keyword] = usage_count
            
            # Sort by usage
            sorted_keywords = sorted(keyword_usage.items(), key=lambda x: x[1], reverse=True)
            
            return {
                'success': True,
                'domain': domain,
                'total_keywords': len(keywords),
                'total_articles': len(articles),
                'keyword_usage': dict(sorted_keywords),
                'most_used': sorted_keywords[:5] if sorted_keywords else [],
                'least_used': sorted_keywords[-5:] if sorted_keywords else [],
                'unused_keywords': [k for k, v in sorted_keywords if v == 0]
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'domain': domain
            }
    
    def generate_bulk_keywords_for_domains(self, domains: List[str]) -> Dict:
        """Generate keywords for multiple domains"""
        results = {}
        
        for domain in domains:
            try:
                # Get domain config to determine category
                domain_config = self.domain_config_manager.load_domain_config(domain)
                category = domain_config.get('category', 'Business')
                
                # Generate keywords for this domain
                result = self.generate_keywords_for_domain(domain, category, 20)
                results[domain] = result
                
            except Exception as e:
                results[domain] = {
                    'success': False,
                    'error': str(e),
                    'domain': domain
                }
        
        return {
            'success': True,
            'processed_domains': len(domains),
            'results': results,
            'successful': len([r for r in results.values() if r.get('success')]),
            'failed': len([r for r in results.values() if not r.get('success')])
        }
    
    def export_domain_keywords(self, domain: str, format: str = 'csv') -> Dict:
        """Export domain keywords in specified format"""
        try:
            keywords = self.domain_config_manager.load_domain_keywords(domain)
            
            if format == 'csv':
                export_content = "Keyword,Category,Generated\n"
                for keyword in keywords:
                    export_content += f'"{keyword}","{domain}","{datetime.now().strftime("%Y-%m-%d")}"\n'
            
            elif format == 'json':
                import json
                export_data = {
                    'domain': domain,
                    'keywords': keywords,
                    'exported_at': datetime.now().isoformat(),
                    'count': len(keywords)
                }
                export_content = json.dumps(export_data, indent=2)
            
            else:  # txt format
                export_content = f"Keywords for {domain}\n"
                export_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                for i, keyword in enumerate(keywords, 1):
                    export_content += f"{i}. {keyword}\n"
            
            return {
                'success': True,
                'domain': domain,
                'format': format,
                'content': export_content,
                'keyword_count': len(keywords)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'domain': domain
            }