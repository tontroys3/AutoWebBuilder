import re
from typing import Dict, List

class ArticleFormatter:
    def __init__(self):
        self.bullet_patterns = [
            r'^\d+\.\s+',  # Numbered lists
            r'^\-\s+',     # Dash bullets
            r'^\*\s+',     # Asterisk bullets
            r'^\•\s+',     # Bullet points
        ]
    
    def format_article_content(self, content: str, format_type: str = "html") -> str:
        """Format article content with proper bullet points and columns"""
        if format_type == "html":
            return self.format_html_content(content)
        elif format_type == "markdown":
            return self.format_markdown_content(content)
        else:
            return content
    
    def format_html_content(self, content: str) -> str:
        """Format content as HTML with bullet points and columns"""
        # Split content into paragraphs
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            if self.is_list_paragraph(paragraph):
                formatted_paragraphs.append(self.format_list_html(paragraph))
            elif self.should_be_columns(paragraph):
                formatted_paragraphs.append(self.format_columns_html(paragraph))
            else:
                formatted_paragraphs.append(f"<p>{paragraph}</p>")
        
        return '\n\n'.join(formatted_paragraphs)
    
    def format_markdown_content(self, content: str) -> str:
        """Format content as Markdown with proper bullet points"""
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            if self.is_list_paragraph(paragraph):
                formatted_paragraphs.append(self.format_list_markdown(paragraph))
            else:
                formatted_paragraphs.append(paragraph)
        
        return '\n\n'.join(formatted_paragraphs)
    
    def is_list_paragraph(self, paragraph: str) -> bool:
        """Check if paragraph should be formatted as a list"""
        lines = paragraph.split('\n')
        list_lines = 0
        
        for line in lines:
            line = line.strip()
            if any(re.match(pattern, line) for pattern in self.bullet_patterns):
                list_lines += 1
        
        return list_lines > 1  # At least 2 lines should be list items
    
    def should_be_columns(self, paragraph: str) -> bool:
        """Check if paragraph should be formatted in columns"""
        # Check for comparison content, benefits/drawbacks, etc.
        keywords = ['vs', 'compared to', 'advantages', 'disadvantages', 'pros', 'cons', 'benefits', 'drawbacks']
        return any(keyword in paragraph.lower() for keyword in keywords)
    
    def format_list_html(self, paragraph: str) -> str:
        """Format paragraph as HTML list"""
        lines = paragraph.split('\n')
        list_items = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Remove bullet patterns and add as list item
                cleaned_line = line
                for pattern in self.bullet_patterns:
                    cleaned_line = re.sub(pattern, '', cleaned_line)
                
                if cleaned_line:
                    list_items.append(f"<li>{cleaned_line}</li>")
        
        if list_items:
            return f"<ul class='formatted-list'>\n{''.join(list_items)}\n</ul>"
        else:
            return f"<p>{paragraph}</p>"
    
    def format_list_markdown(self, paragraph: str) -> str:
        """Format paragraph as Markdown list"""
        lines = paragraph.split('\n')
        list_items = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Ensure consistent bullet formatting
                cleaned_line = line
                for pattern in self.bullet_patterns:
                    cleaned_line = re.sub(pattern, '', cleaned_line)
                
                if cleaned_line:
                    list_items.append(f"- {cleaned_line}")
        
        return '\n'.join(list_items)
    
    def format_columns_html(self, paragraph: str) -> str:
        """Format paragraph content in columns"""
        # Split content that can be displayed in columns
        sentences = paragraph.split('. ')
        
        if len(sentences) >= 4:
            mid_point = len(sentences) // 2
            col1 = '. '.join(sentences[:mid_point])
            col2 = '. '.join(sentences[mid_point:])
            
            return f"""
            <div class='two-column-layout'>
                <div class='column-left'>
                    <p>{col1}</p>
                </div>
                <div class='column-right'>
                    <p>{col2}</p>
                </div>
            </div>
            """
        else:
            return f"<p>{paragraph}</p>"
    
    def add_article_styles(self) -> str:
        """Return CSS styles for formatted articles"""
        return """
        <style>
        .formatted-list {
            margin: 20px 0;
            padding-left: 20px;
        }
        
        .formatted-list li {
            margin: 8px 0;
            line-height: 1.6;
            padding: 5px 0;
            border-left: 3px solid #007bff;
            padding-left: 15px;
            margin-left: 10px;
        }
        
        .two-column-layout {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 20px 0;
        }
        
        .column-left, .column-right {
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }
        
        .article-content {
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.7;
            font-size: 16px;
        }
        
        .article-content h1, .article-content h2, .article-content h3 {
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        
        .article-content p {
            margin-bottom: 15px;
            text-align: justify;
        }
        
        @media (max-width: 768px) {
            .two-column-layout {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """
    
    def generate_article_structure(self, title: str, content: str, category: str) -> Dict:
        """Generate structured article with proper formatting"""
        # Split content into sections
        sections = self.split_into_sections(content)
        
        # Format each section
        formatted_sections = []
        for section in sections:
            formatted_section = {
                'heading': section.get('heading', ''),
                'content': self.format_article_content(section.get('content', '')),
                'type': section.get('type', 'text')
            }
            formatted_sections.append(formatted_section)
        
        return {
            'title': title,
            'category': category,
            'sections': formatted_sections,
            'formatted_html': self.compile_full_article(title, formatted_sections),
            'word_count': len(content.split()),
            'reading_time': self.calculate_reading_time(content)
        }
    
    def split_into_sections(self, content: str) -> List[Dict]:
        """Split content into logical sections"""
        # Simple section splitting based on headings
        sections = []
        current_section = {'heading': '', 'content': '', 'type': 'text'}
        
        paragraphs = content.split('\n\n')
        
        for paragraph in paragraphs:
            # Check if paragraph is a heading
            if self.is_heading(paragraph):
                if current_section['content']:
                    sections.append(current_section)
                current_section = {
                    'heading': paragraph,
                    'content': '',
                    'type': 'text'
                }
            else:
                current_section['content'] += paragraph + '\n\n'
        
        # Add final section
        if current_section['content']:
            sections.append(current_section)
        
        return sections
    
    def is_heading(self, paragraph: str) -> bool:
        """Check if paragraph is a heading"""
        # Simple heuristic: short lines that don't end with period
        return (len(paragraph) < 100 and 
                not paragraph.endswith('.') and 
                not paragraph.endswith('!') and 
                not paragraph.endswith('?') and
                len(paragraph.split()) < 10)
    
    def compile_full_article(self, title: str, sections: List[Dict]) -> str:
        """Compile full article HTML"""
        html = f"""
        <div class='article-content'>
            <h1>{title}</h1>
        """
        
        for section in sections:
            if section['heading']:
                html += f"<h2>{section['heading']}</h2>\n"
            html += section['content'] + "\n"
        
        html += "</div>"
        return html
    
    def calculate_reading_time(self, content: str) -> int:
        """Calculate reading time in minutes"""
        word_count = len(content.split())
        # Average reading speed: 200 words per minute
        return max(1, round(word_count / 200))