from datetime import datetime
from typing import Dict, List
import xml.etree.ElementTree as ET
from xml.dom import minidom

class FeedGenerator:
    def __init__(self):
        self.namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'dc': 'http://purl.org/dc/elements/1.1/'
        }
    
    def generate_rss_feed(self, site_data: Dict, articles: List[Dict], domain: str) -> str:
        """Generate RSS 2.0 feed"""
        try:
            # Create RSS root
            rss = ET.Element('rss')
            rss.set('version', '2.0')
            rss.set('xmlns:content', self.namespaces['content'])
            rss.set('xmlns:dc', self.namespaces['dc'])
            
            # Create channel
            channel = ET.SubElement(rss, 'channel')
            
            # Add channel metadata
            title = ET.SubElement(channel, 'title')
            title.text = site_data.get('title', 'Website')
            
            link = ET.SubElement(channel, 'link')
            link.text = f"https://{domain}" if not domain.startswith('http') else domain
            
            description = ET.SubElement(channel, 'description')
            description.text = site_data.get('description', 'Website description')
            
            language = ET.SubElement(channel, 'language')
            language.text = 'en-US'
            
            last_build_date = ET.SubElement(channel, 'lastBuildDate')
            last_build_date.text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
            
            generator = ET.SubElement(channel, 'generator')
            generator.text = 'Auto Website Builder'
            
            # Add articles as items
            for article in articles:
                item = ET.SubElement(channel, 'item')
                
                item_title = ET.SubElement(item, 'title')
                item_title.text = article.get('title', 'Untitled')
                
                item_link = ET.SubElement(item, 'link')
                article_slug = self._generate_slug(article.get('title', ''))
                item_link.text = f"{link.text}/articles/{article_slug}"
                
                item_description = ET.SubElement(item, 'description')
                item_description.text = article.get('content', '')[:200] + '...'
                
                item_content = ET.SubElement(item, 'content:encoded')
                item_content.text = f"<![CDATA[{article.get('content', '')}]]>"
                
                item_pub_date = ET.SubElement(item, 'pubDate')
                pub_date = article.get('created_at', datetime.now().isoformat())
                if isinstance(pub_date, str):
                    try:
                        pub_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    except:
                        pub_date = datetime.now()
                item_pub_date.text = pub_date.strftime('%a, %d %b %Y %H:%M:%S %z')
                
                item_guid = ET.SubElement(item, 'guid')
                item_guid.text = f"{link.text}/articles/{article_slug}"
                item_guid.set('isPermaLink', 'true')
                
                # Add category
                if article.get('category'):
                    item_category = ET.SubElement(item, 'category')
                    item_category.text = article['category']
                
                # Add author
                item_author = ET.SubElement(item, 'dc:creator')
                item_author.text = 'Auto Website Builder'
            
            # Convert to string with pretty formatting
            rough_string = ET.tostring(rss, encoding='unicode')
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent='  ')
        
        except Exception as e:
            return f"<!-- Error generating RSS feed: {str(e)} -->"
    
    def generate_atom_feed(self, site_data: Dict, articles: List[Dict], domain: str) -> str:
        """Generate Atom 1.0 feed"""
        try:
            # Create Atom root
            feed = ET.Element('feed')
            feed.set('xmlns', self.namespaces['atom'])
            
            # Add feed metadata
            title = ET.SubElement(feed, 'title')
            title.text = site_data.get('title', 'Website')
            
            link_self = ET.SubElement(feed, 'link')
            link_self.set('href', f"https://{domain}/atom.xml" if not domain.startswith('http') else f"{domain}/atom.xml")
            link_self.set('rel', 'self')
            
            link_alternate = ET.SubElement(feed, 'link')
            link_alternate.set('href', f"https://{domain}" if not domain.startswith('http') else domain)
            link_alternate.set('rel', 'alternate')
            
            feed_id = ET.SubElement(feed, 'id')
            feed_id.text = f"https://{domain}/" if not domain.startswith('http') else f"{domain}/"
            
            updated = ET.SubElement(feed, 'updated')
            updated.text = datetime.now().isoformat() + 'Z'
            
            subtitle = ET.SubElement(feed, 'subtitle')
            subtitle.text = site_data.get('description', 'Website description')
            
            generator = ET.SubElement(feed, 'generator')
            generator.text = 'Auto Website Builder'
            
            # Add articles as entries
            for article in articles:
                entry = ET.SubElement(feed, 'entry')
                
                entry_title = ET.SubElement(entry, 'title')
                entry_title.text = article.get('title', 'Untitled')
                
                entry_link = ET.SubElement(entry, 'link')
                article_slug = self._generate_slug(article.get('title', ''))
                entry_link.set('href', f"{link_alternate.get('href')}/articles/{article_slug}")
                
                entry_id = ET.SubElement(entry, 'id')
                entry_id.text = f"{link_alternate.get('href')}/articles/{article_slug}"
                
                entry_updated = ET.SubElement(entry, 'updated')
                updated_date = article.get('created_at', datetime.now().isoformat())
                if isinstance(updated_date, str):
                    try:
                        updated_date = datetime.fromisoformat(updated_date.replace('Z', '+00:00'))
                    except:
                        updated_date = datetime.now()
                entry_updated.text = updated_date.isoformat() + 'Z'
                
                entry_summary = ET.SubElement(entry, 'summary')
                entry_summary.text = article.get('content', '')[:200] + '...'
                
                entry_content = ET.SubElement(entry, 'content')
                entry_content.set('type', 'html')
                entry_content.text = f"<![CDATA[{article.get('content', '')}]]>"
                
                entry_author = ET.SubElement(entry, 'author')
                author_name = ET.SubElement(entry_author, 'name')
                author_name.text = 'Auto Website Builder'
                
                # Add category
                if article.get('category'):
                    entry_category = ET.SubElement(entry, 'category')
                    entry_category.set('term', article['category'])
            
            # Convert to string with pretty formatting
            rough_string = ET.tostring(feed, encoding='unicode')
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent='  ')
        
        except Exception as e:
            return f"<!-- Error generating Atom feed: {str(e)} -->"
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title"""
        import re
        slug = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
        slug = re.sub(r'\s+', '-', slug.strip())
        return slug
    
    def generate_feed_index(self, site_data: Dict, domain: str) -> str:
        """Generate feed index page"""
        try:
            site_title = site_data.get('title', 'Website')
            base_url = f"https://{domain}" if not domain.startswith('http') else domain
            
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feeds - {site_title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .feed-item {{ background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 8px; }}
        .feed-link {{ color: #0066cc; text-decoration: none; font-weight: bold; }}
        .feed-link:hover {{ text-decoration: underline; }}
        .feed-description {{ color: #666; margin-top: 10px; }}
    </style>
</head>
<body>
    <h1>RSS and Atom Feeds</h1>
    <p>Subscribe to our feeds to get the latest updates from {site_title}.</p>
    
    <div class="feed-item">
        <h2>RSS Feed</h2>
        <a href="{base_url}/rss.xml" class="feed-link">Subscribe to RSS Feed</a>
        <p class="feed-description">RSS (Really Simple Syndication) feed for all our latest articles and updates.</p>
    </div>
    
    <div class="feed-item">
        <h2>Atom Feed</h2>
        <a href="{base_url}/atom.xml" class="feed-link">Subscribe to Atom Feed</a>
        <p class="feed-description">Atom feed for all our latest articles and updates.</p>
    </div>
    
    <div class="feed-item">
        <h2>How to Subscribe</h2>
        <p>You can subscribe to our feeds using any RSS reader such as:</p>
        <ul>
            <li>Feedly</li>
            <li>Inoreader</li>
            <li>NewsBlur</li>
            <li>Or any other RSS reader of your choice</li>
        </ul>
    </div>
</body>
</html>"""
            
            return html
        
        except Exception as e:
            return f"<!-- Error generating feed index: {str(e)} -->"
    
    def validate_feed(self, feed_content: str, feed_type: str) -> Dict:
        """Validate RSS or Atom feed"""
        try:
            # Parse XML
            root = ET.fromstring(feed_content)
            
            validation_result = {
                'valid': True,
                'errors': [],
                'warnings': [],
                'feed_type': feed_type
            }
            
            if feed_type == 'rss':
                # Validate RSS structure
                if root.tag != 'rss':
                    validation_result['valid'] = False
                    validation_result['errors'].append("Root element must be 'rss'")
                
                channel = root.find('channel')
                if channel is None:
                    validation_result['valid'] = False
                    validation_result['errors'].append("RSS feed must contain a 'channel' element")
                else:
                    # Check required channel elements
                    required_elements = ['title', 'link', 'description']
                    for element in required_elements:
                        if channel.find(element) is None:
                            validation_result['valid'] = False
                            validation_result['errors'].append(f"Channel must contain '{element}' element")
            
            elif feed_type == 'atom':
                # Validate Atom structure
                if root.tag != '{http://www.w3.org/2005/Atom}feed':
                    validation_result['valid'] = False
                    validation_result['errors'].append("Root element must be 'feed' with Atom namespace")
                
                # Check required feed elements
                required_elements = ['title', 'id', 'updated']
                for element in required_elements:
                    if root.find(f'{{{self.namespaces["atom"]}}}{element}') is None:
                        validation_result['valid'] = False
                        validation_result['errors'].append(f"Feed must contain '{element}' element")
            
            return validation_result
        
        except ET.ParseError as e:
            return {
                'valid': False,
                'errors': [f"XML parsing error: {str(e)}"],
                'warnings': [],
                'feed_type': feed_type
            }
        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': [],
                'feed_type': feed_type
            }
