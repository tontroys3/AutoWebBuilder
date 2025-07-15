from datetime import datetime
from typing import Dict, List, Optional
import re

class PageGenerator:
    def __init__(self):
        self.page_templates = {
            'about': self._get_about_template(),
            'contact': self._get_contact_template(),
            'privacy': self._get_privacy_template(),
            'disclaimer': self._get_disclaimer_template(),
            'terms': self._get_terms_template()
        }
    
    def generate_about_page(self, site_data: Dict) -> str:
        """Generate About page content"""
        try:
            title = site_data.get('title', 'Our Company')
            description = site_data.get('description', 'Learn more about us')
            category = site_data.get('category', 'Business')
            
            # Extract content from domain data if available
            domain_content = ""
            if 'domain_data' in site_data and site_data['domain_data'].get('content'):
                domain_content = site_data['domain_data']['content'].get('main_text', '')
            
            # Generate about content based on category
            about_content = self._generate_about_content(title, description, category, domain_content)
            
            return self._format_page_content('About Us', about_content)
        
        except Exception as e:
            return f"<h1>About Us</h1><p>Error generating about page: {str(e)}</p>"
    
    def generate_contact_page(self, site_data: Dict) -> str:
        """Generate Contact page content"""
        try:
            title = site_data.get('title', 'Contact Us')
            domain = site_data.get('domain', 'example.com')
            
            contact_content = f"""
            <h1>Contact Us</h1>
            <p>We'd love to hear from you! Get in touch with us using the information below.</p>
            
            <div class="contact-info">
                <h3>Get In Touch</h3>
                <p><strong>Email:</strong> info@{domain}</p>
                <p><strong>Phone:</strong> +1 (555) 123-4567</p>
                <p><strong>Address:</strong> 123 Business Street, City, State 12345</p>
            </div>
            
            <div class="contact-form">
                <h3>Send us a Message</h3>
                <form>
                    <div class="form-group">
                        <label for="name">Name:</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email:</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    <div class="form-group">
                        <label for="subject">Subject:</label>
                        <input type="text" id="subject" name="subject" required>
                    </div>
                    <div class="form-group">
                        <label for="message">Message:</label>
                        <textarea id="message" name="message" rows="5" required></textarea>
                    </div>
                    <button type="submit">Send Message</button>
                </form>
            </div>
            
            <div class="business-hours">
                <h3>Business Hours</h3>
                <p><strong>Monday - Friday:</strong> 9:00 AM - 6:00 PM</p>
                <p><strong>Saturday:</strong> 10:00 AM - 4:00 PM</p>
                <p><strong>Sunday:</strong> Closed</p>
            </div>
            """
            
            return self._format_page_content('Contact Us', contact_content)
        
        except Exception as e:
            return f"<h1>Contact Us</h1><p>Error generating contact page: {str(e)}</p>"
    
    def generate_privacy_policy(self, site_data: Dict) -> str:
        """Generate Privacy Policy page"""
        try:
            title = site_data.get('title', 'Our Website')
            domain = site_data.get('domain', 'example.com')
            
            privacy_content = f"""
            <h1>Privacy Policy</h1>
            <p><strong>Effective Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
            
            <p>This Privacy Policy describes how {title} ("we," "us," or "our") collects, uses, and protects your personal information when you visit our website at {domain}.</p>
            
            <h2>Information We Collect</h2>
            <p>We may collect the following types of information:</p>
            <ul>
                <li><strong>Personal Information:</strong> Name, email address, phone number, and other contact details when you provide them voluntarily.</li>
                <li><strong>Usage Information:</strong> Information about how you use our website, including pages visited, time spent, and browser type.</li>
                <li><strong>Cookies:</strong> Small files stored on your device to improve your browsing experience.</li>
            </ul>
            
            <h2>How We Use Your Information</h2>
            <p>We use the collected information to:</p>
            <ul>
                <li>Provide and maintain our services</li>
                <li>Respond to your inquiries and requests</li>
                <li>Improve our website and user experience</li>
                <li>Send you updates and promotional materials (with your consent)</li>
                <li>Comply with legal obligations</li>
            </ul>
            
            <h2>Information Sharing</h2>
            <p>We do not sell, trade, or otherwise transfer your personal information to third parties without your consent, except as described in this policy or as required by law.</p>
            
            <h2>Data Security</h2>
            <p>We implement appropriate technical and organizational measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.</p>
            
            <h2>Your Rights</h2>
            <p>You have the right to:</p>
            <ul>
                <li>Access your personal information</li>
                <li>Correct inaccurate information</li>
                <li>Request deletion of your information</li>
                <li>Object to processing of your information</li>
                <li>Data portability</li>
            </ul>
            
            <h2>Cookies</h2>
            <p>Our website uses cookies to enhance your experience. You can disable cookies in your browser settings, but this may affect website functionality.</p>
            
            <h2>Changes to This Policy</h2>
            <p>We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new policy on this page.</p>
            
            <h2>Contact Us</h2>
            <p>If you have any questions about this Privacy Policy, please contact us at info@{domain}.</p>
            """
            
            return self._format_page_content('Privacy Policy', privacy_content)
        
        except Exception as e:
            return f"<h1>Privacy Policy</h1><p>Error generating privacy policy: {str(e)}</p>"
    
    def generate_disclaimer(self, site_data: Dict) -> str:
        """Generate Disclaimer page"""
        try:
            title = site_data.get('title', 'Our Website')
            domain = site_data.get('domain', 'example.com')
            
            disclaimer_content = f"""
            <h1>Disclaimer</h1>
            <p><strong>Last Updated:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
            
            <h2>Website Disclaimer</h2>
            <p>The information on this website ({domain}) is provided on an "as is" basis. To the fullest extent permitted by law, {title} excludes all representations, warranties, obligations, and liabilities arising out of or in connection with the use of this website.</p>
            
            <h2>Information Accuracy</h2>
            <p>While we strive to provide accurate and up-to-date information, we make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or availability of the information, products, services, or related graphics contained on this website.</p>
            
            <h2>Professional Advice</h2>
            <p>The information on this website is not intended as professional advice. You should not rely on this information as a substitute for professional advice tailored to your specific circumstances.</p>
            
            <h2>External Links</h2>
            <p>Our website may contain links to external websites that are not provided or maintained by {title}. We do not guarantee the accuracy, relevance, timeliness, or completeness of any information on these external websites.</p>
            
            <h2>Limitation of Liability</h2>
            <p>In no event will {title} be liable for any loss or damage including, without limitation, indirect or consequential loss or damage, or any loss or damage whatsoever arising from the use of this website.</p>
            
            <h2>Indemnification</h2>
            <p>You agree to indemnify and hold {title} harmless from any claim, demand, or damages arising out of your use of this website.</p>
            
            <h2>Changes to Disclaimer</h2>
            <p>We reserve the right to modify this disclaimer at any time. Changes will be effective immediately upon posting on this website.</p>
            
            <h2>Contact Information</h2>
            <p>If you have any questions about this disclaimer, please contact us at info@{domain}.</p>
            """
            
            return self._format_page_content('Disclaimer', disclaimer_content)
        
        except Exception as e:
            return f"<h1>Disclaimer</h1><p>Error generating disclaimer: {str(e)}</p>"
    
    def generate_terms_of_service(self, site_data: Dict) -> str:
        """Generate Terms of Service page"""
        try:
            title = site_data.get('title', 'Our Website')
            domain = site_data.get('domain', 'example.com')
            
            terms_content = f"""
            <h1>Terms of Service</h1>
            <p><strong>Effective Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
            
            <p>Welcome to {title}. These Terms of Service ("Terms") govern your use of our website located at {domain} (the "Service") operated by {title}.</p>
            
            <h2>Acceptance of Terms</h2>
            <p>By accessing and using this website, you accept and agree to be bound by the terms and provision of this agreement.</p>
            
            <h2>Use License</h2>
            <p>Permission is granted to temporarily download one copy of the materials on {title}'s website for personal, non-commercial transitory viewing only.</p>
            
            <h2>Disclaimer</h2>
            <p>The materials on {title}'s website are provided on an 'as is' basis. {title} makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.</p>
            
            <h2>Limitations</h2>
            <p>In no event shall {title} or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on {title}'s website, even if {title} or a {title} authorized representative has been notified orally or in writing of the possibility of such damage.</p>
            
            <h2>Accuracy of Materials</h2>
            <p>The materials appearing on {title}'s website could include technical, typographical, or photographic errors. {title} does not warrant that any of the materials on its website are accurate, complete, or current.</p>
            
            <h2>Links</h2>
            <p>{title} has not reviewed all of the sites linked to our website and is not responsible for the contents of any such linked site. The inclusion of any link does not imply endorsement by {title} of the site.</p>
            
            <h2>Modifications</h2>
            <p>{title} may revise these terms of service for its website at any time without notice. By using this website, you are agreeing to be bound by the then current version of these terms of service.</p>
            
            <h2>Governing Law</h2>
            <p>These terms and conditions are governed by and construed in accordance with the laws and you irrevocably submit to the exclusive jurisdiction of the courts in that state or location.</p>
            """
            
            return self._format_page_content('Terms of Service', terms_content)
        
        except Exception as e:
            return f"<h1>Terms of Service</h1><p>Error generating terms of service: {str(e)}</p>"
    
    def _generate_about_content(self, title: str, description: str, category: str, domain_content: str) -> str:
        """Generate customized about content based on site data"""
        try:
            # Base about content
            about_content = f"""
            <h1>About {title}</h1>
            <p>{description}</p>
            """
            
            # Add category-specific content
            if category.lower() == 'business':
                about_content += """
                <h2>Our Mission</h2>
                <p>We are dedicated to providing exceptional services and solutions that help our clients achieve their goals. Our team of professionals brings years of experience and expertise to every project.</p>
                
                <h2>What We Do</h2>
                <p>We specialize in delivering high-quality services tailored to meet the unique needs of each client. Our approach combines industry best practices with innovative solutions to deliver outstanding results.</p>
                
                <h2>Why Choose Us</h2>
                <ul>
                    <li>Experienced and professional team</li>
                    <li>Commitment to quality and excellence</li>
                    <li>Customer-focused approach</li>
                    <li>Proven track record of success</li>
                    <li>Competitive pricing and value</li>
                </ul>
                """
            elif category.lower() == 'blog':
                about_content += """
                <h2>Welcome to Our Blog</h2>
                <p>This blog is dedicated to sharing insights, tips, and stories that matter to our community. We cover a wide range of topics and strive to provide valuable content that informs and inspires.</p>
                
                <h2>Our Content</h2>
                <p>We publish regular articles on various topics, ensuring that our readers always have fresh, relevant content to explore. Our writers are passionate about their subjects and committed to delivering quality content.</p>
                
                <h2>Join Our Community</h2>
                <p>We encourage our readers to engage with our content, share their thoughts, and be part of our growing community. Your feedback and participation help us improve and create better content.</p>
                """
            elif category.lower() == 'portfolio':
                about_content += """
                <h2>About My Work</h2>
                <p>This portfolio showcases my skills, experience, and projects. I'm passionate about creating high-quality work that meets client needs and exceeds expectations.</p>
                
                <h2>My Approach</h2>
                <p>I believe in combining creativity with functionality to deliver solutions that not only look great but also perform exceptionally well. Every project is an opportunity to learn and grow.</p>
                
                <h2>Let's Work Together</h2>
                <p>I'm always interested in new opportunities and collaborations. If you have a project in mind or would like to discuss potential partnerships, please don't hesitate to get in touch.</p>
                """
            
            # Add domain-specific content if available
            if domain_content and len(domain_content) > 100:
                about_content += f"""
                <h2>More About Us</h2>
                <p>{domain_content[:300]}...</p>
                """
            
            return about_content
        
        except Exception as e:
            return f"<h1>About Us</h1><p>Error generating about content: {str(e)}</p>"
    
    def _format_page_content(self, title: str, content: str) -> str:
        """Format page content with consistent styling"""
        try:
            formatted_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    h1 {{
                        color: #2c3e50;
                        border-bottom: 2px solid #3498db;
                        padding-bottom: 10px;
                    }}
                    h2 {{
                        color: #34495e;
                        margin-top: 30px;
                    }}
                    h3 {{
                        color: #5a6c7d;
                    }}
                    ul {{
                        padding-left: 20px;
                    }}
                    li {{
                        margin-bottom: 5px;
                    }}
                    .contact-info, .contact-form, .business-hours {{
                        background-color: #f8f9fa;
                        padding: 20px;
                        margin: 20px 0;
                        border-radius: 5px;
                    }}
                    .form-group {{
                        margin-bottom: 15px;
                    }}
                    label {{
                        display: block;
                        margin-bottom: 5px;
                        font-weight: bold;
                    }}
                    input, textarea {{
                        width: 100%;
                        padding: 8px;
                        border: 1px solid #ddd;
                        border-radius: 3px;
                        font-size: 14px;
                    }}
                    button {{
                        background-color: #3498db;
                        color: white;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 3px;
                        cursor: pointer;
                        font-size: 16px;
                    }}
                    button:hover {{
                        background-color: #2980b9;
                    }}
                </style>
            </head>
            <body>
                {content}
            </body>
            </html>
            """
            
            return formatted_content
        
        except Exception as e:
            return f"<html><body><h1>{title}</h1><p>Error formatting page: {str(e)}</p></body></html>"
    
    def _get_about_template(self) -> str:
        """Get about page template"""
        return """
        <h1>About {{ title }}</h1>
        <p>{{ description }}</p>
        
        <h2>Our Story</h2>
        <p>{{ story_content }}</p>
        
        <h2>What We Do</h2>
        <p>{{ services_content }}</p>
        
        <h2>Why Choose Us</h2>
        <ul>
            {% for feature in features %}
            <li>{{ feature }}</li>
            {% endfor %}
        </ul>
        """
    
    def _get_contact_template(self) -> str:
        """Get contact page template"""
        return """
        <h1>Contact {{ title }}</h1>
        <p>We'd love to hear from you!</p>
        
        <div class="contact-info">
            <h3>Get In Touch</h3>
            <p><strong>Email:</strong> {{ email }}</p>
            <p><strong>Phone:</strong> {{ phone }}</p>
            <p><strong>Address:</strong> {{ address }}</p>
        </div>
        """
    
    def _get_privacy_template(self) -> str:
        """Get privacy policy template"""
        return """
        <h1>Privacy Policy</h1>
        <p><strong>Effective Date:</strong> {{ effective_date }}</p>
        
        <h2>Information We Collect</h2>
        <p>{{ information_collected }}</p>
        
        <h2>How We Use Your Information</h2>
        <p>{{ information_usage }}</p>
        """
    
    def _get_disclaimer_template(self) -> str:
        """Get disclaimer template"""
        return """
        <h1>Disclaimer</h1>
        <p><strong>Last Updated:</strong> {{ last_updated }}</p>
        
        <h2>Website Disclaimer</h2>
        <p>{{ disclaimer_content }}</p>
        """
    
    def _get_terms_template(self) -> str:
        """Get terms of service template"""
        return """
        <h1>Terms of Service</h1>
        <p><strong>Effective Date:</strong> {{ effective_date }}</p>
        
        <h2>Acceptance of Terms</h2>
        <p>{{ acceptance_terms }}</p>
        """
    
    def generate_custom_page(self, page_name: str, content: str, site_data: Dict) -> str:
        """Generate a custom page with given content"""
        try:
            page_title = page_name.replace('_', ' ').title()
            
            custom_content = f"""
            <h1>{page_title}</h1>
            {content}
            """
            
            return self._format_page_content(page_title, custom_content)
        
        except Exception as e:
            return f"<h1>{page_name}</h1><p>Error generating custom page: {str(e)}</p>"
    
    def get_page_list(self) -> List[str]:
        """Get list of available page types"""
        return list(self.page_templates.keys())
    
    def validate_page_content(self, content: str) -> Dict:
        """Validate page content"""
        try:
            errors = []
            warnings = []
            
            if not content or len(content.strip()) < 10:
                errors.append("Page content must be at least 10 characters long")
            
            if len(content) > 50000:
                warnings.append("Page content is very long (over 50,000 characters)")
            
            # Check for potential HTML issues
            if '<script>' in content.lower():
                warnings.append("Page contains script tags - ensure content is safe")
            
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
