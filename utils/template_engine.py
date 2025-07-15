from jinja2 import Environment, BaseLoader, Template
from typing import Dict, List, Optional
from datetime import datetime

class TemplateEngine:
    def __init__(self):
        self.env = Environment(loader=BaseLoader())
        self.templates = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load all template definitions"""
        self.templates = {
            'default': self._get_default_template(),
            'professional': self._get_professional_template(),
            'minimal': self._get_minimal_template(),
            'modern': self._get_modern_template(),
            'creative': self._get_creative_template(),
            'business': self._get_business_template(),
            'portfolio': self._get_portfolio_template(),
            'landing': self._get_landing_template(),
            'blog': self._get_blog_template(),
            'magazine': self._get_magazine_template()
        }
    
    def render_template(self, template_name: str, **kwargs) -> str:
        """Render a template with given context"""
        try:
            if template_name not in self.templates:
                template_name = 'default'
            
            template = self.env.from_string(self.templates[template_name])
            return template.render(**kwargs)
        
        except Exception as e:
            return f"<!-- Error rendering template: {str(e)} -->"
    
    def _get_default_template(self) -> str:
        """Get default template"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="{{ description }}">
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Feather Icons -->
    <script src="https://unpkg.com/feather-icons"></script>
    
    <style>
        :root {
            --primary-color: #0066cc;
            --secondary-color: #6c757d;
            --accent-color: #28a745;
        }
        
        .navbar-brand {
            font-weight: bold;
            color: var(--primary-color) !important;
        }
        
        .hero-section {
            background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
            color: white;
            padding: 80px 0;
        }
        
        .card {
            border: none;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }
        
        .btn-primary:hover {
            background-color: #0052a3;
            border-color: #0052a3;
        }
        
        footer {
            background-color: #f8f9fa;
            margin-top: 50px;
        }
        
        .article-card {
            border-left: 4px solid var(--primary-color);
            padding-left: 20px;
            margin-bottom: 30px;
        }
        
        .article-meta {
            color: var(--secondary-color);
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .hero-section {
                padding: 40px 0;
            }
            
            .hero-section h1 {
                font-size: 2rem;
            }
        }
    </style>
    
    {% if seo_data %}
    {{ seo_data.meta_tags|safe }}
    {{ seo_data.og_tags|safe }}
    {{ seo_data.twitter_tags|safe }}
    {{ seo_data.structured_data|safe }}
    {% endif %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i data-feather="globe"></i>
                {{ title }}
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/about">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/articles">Articles</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/contact">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6">
                    <h1 class="display-4 fw-bold">{{ title }}</h1>
                    <p class="lead">{{ description }}</p>
                    <a href="/articles" class="btn btn-light btn-lg">
                        <i data-feather="book-open"></i>
                        Explore Articles
                    </a>
                </div>
                <div class="col-lg-6">
                    <div class="text-center">
                        <i data-feather="monitor" style="width: 200px; height: 200px; opacity: 0.3;"></i>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Main Content -->
    <div class="container mt-5">
        {% if articles %}
        <h2>Latest Articles</h2>
        <div class="row">
            {% for article in articles[:3] %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    {% if article.image_url %}
                    <img src="{{ article.image_url }}" class="card-img-top" alt="{{ article.title }}">
                    {% endif %}
                    <div class="card-body">
                        <h5 class="card-title">{{ article.title }}</h5>
                        <p class="card-text">{{ article.content[:150] }}...</p>
                        <div class="article-meta">
                            <i data-feather="calendar"></i>
                            {{ article.created_at }}
                            {% if article.category %}
                            <span class="badge bg-secondary ms-2">{{ article.category }}</span>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% if domain_data and domain_data.content %}
        <div class="row mt-5">
            <div class="col-lg-8">
                <h2>About This Site</h2>
                <p>{{ domain_data.content.main_text[:500] }}...</p>
            </div>
            <div class="col-lg-4">
                <div class="card">
                    <div class="card-header">
                        <h5><i data-feather="info"></i> Site Information</h5>
                    </div>
                    <div class="card-body">
                        <p><strong>Category:</strong> {{ category }}</p>
                        <p><strong>Template:</strong> {{ template }}</p>
                        {% if domain_data.metadata %}
                        <p><strong>Status:</strong> {{ domain_data.metadata.status_code }}</p>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        {% endif %}
    </div>

    <!-- Footer -->
    <footer class="bg-light py-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <p>&copy; 2024 {{ title }}. All rights reserved.</p>
                </div>
                <div class="col-md-6">
                    <ul class="list-inline text-end mb-0">
                        <li class="list-inline-item"><a href="/privacy">Privacy Policy</a></li>
                        <li class="list-inline-item"><a href="/disclaimer">Disclaimer</a></li>
                        <li class="list-inline-item"><a href="/sitemap">Sitemap</a></li>
                        <li class="list-inline-item"><a href="/feed">RSS Feed</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Initialize Feather Icons -->
    <script>
        feather.replace();
    </script>
</body>
</html>"""

    def _get_professional_template(self) -> str:
        """Get professional template"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="{{ description }}">
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #e74c3c;
            --text-color: #34495e;
            --bg-color: #ecf0f1;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: var(--text-color);
            line-height: 1.6;
        }
        
        .navbar {
            background-color: var(--primary-color) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .navbar-brand, .nav-link {
            color: white !important;
        }
        
        .nav-link:hover {
            color: var(--secondary-color) !important;
        }
        
        .hero-section {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 100px 0;
            position: relative;
            overflow: hidden;
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="white" opacity="0.1"><polygon points="0,100 1000,0 1000,100"/></svg>');
            background-size: cover;
        }
        
        .hero-content {
            position: relative;
            z-index: 2;
        }
        
        .feature-card {
            background: white;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            border-top: 4px solid var(--secondary-color);
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
        }
        
        .feature-icon {
            font-size: 3rem;
            color: var(--secondary-color);
            margin-bottom: 20px;
        }
        
        .btn-primary {
            background-color: var(--secondary-color);
            border-color: var(--secondary-color);
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn-primary:hover {
            background-color: var(--accent-color);
            border-color: var(--accent-color);
        }
        
        .article-card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            margin-bottom: 30px;
        }
        
        .article-card:hover {
            transform: translateY(-5px);
        }
        
        .article-meta {
            color: var(--secondary-color);
            font-size: 0.9em;
            font-weight: 500;
        }
        
        .section-title {
            text-align: center;
            margin-bottom: 50px;
            position: relative;
        }
        
        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 50px;
            height: 3px;
            background: var(--secondary-color);
        }
        
        footer {
            background-color: var(--primary-color);
            color: white;
            padding: 40px 0;
            margin-top: 80px;
        }
        
        .footer-link {
            color: white;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .footer-link:hover {
            color: var(--secondary-color);
        }
        
        @media (max-width: 768px) {
            .hero-section {
                padding: 60px 0;
            }
            
            .hero-section h1 {
                font-size: 2.5rem;
            }
            
            .feature-card {
                margin-bottom: 30px;
            }
        }
    </style>
    
    {% if seo_data %}
    {{ seo_data.meta_tags|safe }}
    {{ seo_data.og_tags|safe }}
    {{ seo_data.twitter_tags|safe }}
    {{ seo_data.structured_data|safe }}
    {% endif %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fas fa-globe me-2"></i>
                {{ title }}
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/"><i class="fas fa-home me-1"></i>Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/about"><i class="fas fa-info-circle me-1"></i>About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/articles"><i class="fas fa-newspaper me-1"></i>Articles</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/contact"><i class="fas fa-envelope me-1"></i>Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6 hero-content">
                    <h1 class="display-3 fw-bold mb-4">{{ title }}</h1>
                    <p class="lead mb-4">{{ description }}</p>
                    <a href="/articles" class="btn btn-primary btn-lg">
                        <i class="fas fa-arrow-right me-2"></i>
                        Get Started
                    </a>
                </div>
                <div class="col-lg-6">
                    <div class="text-center">
                        <i class="fas fa-rocket" style="font-size: 15rem; opacity: 0.3;"></i>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="py-5" style="background-color: var(--bg-color);">
        <div class="container">
            <h2 class="section-title">Why Choose Us</h2>
            <div class="row">
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="feature-card">
                        <i class="fas fa-bolt feature-icon"></i>
                        <h4>Fast Performance</h4>
                        <p>Lightning-fast loading times and optimized performance for the best user experience.</p>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="feature-card">
                        <i class="fas fa-shield-alt feature-icon"></i>
                        <h4>Secure & Reliable</h4>
                        <p>Enterprise-grade security and 99.9% uptime guarantee for your peace of mind.</p>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="feature-card">
                        <i class="fas fa-mobile-alt feature-icon"></i>
                        <h4>Mobile Responsive</h4>
                        <p>Fully responsive design that works perfectly on all devices and screen sizes.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Articles Section -->
    <section class="py-5">
        <div class="container">
            {% if articles %}
            <h2 class="section-title">Latest Articles</h2>
            <div class="row">
                {% for article in articles[:3] %}
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="article-card">
                        {% if article.image_url %}
                        <img src="{{ article.image_url }}" class="card-img-top" alt="{{ article.title }}" style="height: 200px; object-fit: cover;">
                        {% endif %}
                        <div class="p-4">
                            <h5 class="fw-bold mb-3">{{ article.title }}</h5>
                            <p class="text-muted mb-3">{{ article.content[:120] }}...</p>
                            <div class="article-meta mb-3">
                                <i class="fas fa-calendar-alt me-2"></i>
                                {{ article.created_at }}
                                {% if article.category %}
                                <span class="badge bg-secondary ms-2">{{ article.category }}</span>
                                {% endif %}
                            </div>
                            <a href="#" class="btn btn-outline-primary">Read More</a>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5 class="mb-3">{{ title }}</h5>
                    <p class="text-muted">{{ description }}</p>
                </div>
                <div class="col-md-6">
                    <h5 class="mb-3">Quick Links</h5>
                    <ul class="list-unstyled">
                        <li><a href="/privacy" class="footer-link">Privacy Policy</a></li>
                        <li><a href="/disclaimer" class="footer-link">Disclaimer</a></li>
                        <li><a href="/sitemap" class="footer-link">Sitemap</a></li>
                        <li><a href="/feed" class="footer-link">RSS Feed</a></li>
                    </ul>
                </div>
            </div>
            <hr class="my-4">
            <div class="text-center">
                <p>&copy; 2024 {{ title }}. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

    def _get_minimal_template(self) -> str:
        """Get minimal template"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="{{ description }}">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #fff;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        header {
            border-bottom: 1px solid #eee;
            padding: 20px 0;
            margin-bottom: 40px;
        }
        
        .logo {
            font-size: 1.5em;
            font-weight: 600;
            color: #000;
            text-decoration: none;
        }
        
        nav {
            margin-top: 10px;
        }
        
        nav ul {
            list-style: none;
            display: flex;
            gap: 30px;
        }
        
        nav a {
            color: #666;
            text-decoration: none;
            transition: color 0.2s;
        }
        
        nav a:hover {
            color: #000;
        }
        
        .hero {
            text-align: center;
            padding: 60px 0;
            background-color: #f8f9fa;
            margin: 0 -20px 60px -20px;
        }
        
        .hero h1 {
            font-size: 3em;
            font-weight: 700;
            margin-bottom: 20px;
            color: #000;
        }
        
        .hero p {
            font-size: 1.2em;
            color: #666;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .articles {
            margin-bottom: 60px;
        }
        
        .articles h2 {
            font-size: 2em;
            margin-bottom: 30px;
            color: #000;
        }
        
        .article-item {
            padding: 30px 0;
            border-bottom: 1px solid #eee;
        }
        
        .article-item:last-child {
            border-bottom: none;
        }
        
        .article-title {
            font-size: 1.5em;
            font-weight: 600;
            margin-bottom: 10px;
            color: #000;
        }
        
        .article-excerpt {
            color: #666;
            margin-bottom: 10px;
        }
        
        .article-meta {
            font-size: 0.9em;
            color: #999;
        }
        
        .article-category {
            background-color: #000;
            color: #fff;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            margin-left: 10px;
        }
        
        footer {
            border-top: 1px solid #eee;
            padding: 40px 0;
            margin-top: 60px;
            text-align: center;
            color: #666;
        }
        
        footer a {
            color: #666;
            text-decoration: none;
            margin: 0 10px;
        }
        
        footer a:hover {
            color: #000;
        }
        
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2em;
            }
            
            nav ul {
                flex-direction: column;
                gap: 15px;
            }
            
            .hero {
                padding: 40px 0;
            }
        }
    </style>
    
    {% if seo_data %}
    {{ seo_data.meta_tags|safe }}
    {{ seo_data.og_tags|safe }}
    {{ seo_data.twitter_tags|safe }}
    {{ seo_data.structured_data|safe }}
    {% endif %}
</head>
<body>
    <div class="container">
        <header>
            <a href="/" class="logo">{{ title }}</a>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/articles">Articles</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>
        </header>
        
        <div class="hero">
            <h1>{{ title }}</h1>
            <p>{{ description }}</p>
        </div>
        
        {% if articles %}
        <div class="articles">
            <h2>Latest Articles</h2>
            {% for article in articles %}
            <div class="article-item">
                <h3 class="article-title">{{ article.title }}</h3>
                <p class="article-excerpt">{{ article.content[:200] }}...</p>
                <div class="article-meta">
                    {{ article.created_at }}
                    {% if article.category %}
                    <span class="article-category">{{ article.category }}</span>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <footer>
            <p>&copy; 2024 {{ title }}. All rights reserved.</p>
            <div>
                <a href="/privacy">Privacy</a>
                <a href="/disclaimer">Disclaimer</a>
                <a href="/sitemap">Sitemap</a>
                <a href="/feed">RSS</a>
            </div>
        </footer>
    </div>
</body>
</html>"""

    def get_available_templates(self) -> List[str]:
        """Get list of available templates"""
        return list(self.templates.keys())

    def get_template_preview(self, template_name: str) -> str:
        """Get template preview with sample data"""
        sample_data = {
            'title': 'Sample Website',
            'description': 'This is a sample website description to show how the template looks.',
            'category': 'Blog',
            'template': template_name,
            'articles': [
                {
                    'title': 'Sample Article 1',
                    'content': 'This is the content of the first sample article. It contains some text to show how articles are displayed in the template.',
                    'category': 'Technology',
                    'created_at': '2024-01-15',
                    'image_url': 'https://via.placeholder.com/300x200'
                },
                {
                    'title': 'Sample Article 2',
                    'content': 'This is the content of the second sample article. It contains some text to show how articles are displayed in the template.',
                    'category': 'Business',
                    'created_at': '2024-01-14',
                    'image_url': 'https://via.placeholder.com/300x200'
                }
            ]
        }
        
        return self.render_template(template_name, **sample_data)

    def get_template_description(self, template_name: str) -> str:
        """Get template description"""
        descriptions = {
            'default': 'Clean Bootstrap-based design with modern features',
            'professional': 'Corporate-style template with enhanced styling',
            'minimal': 'Typography-focused design for content creators',
            'modern': 'Gradient design with smooth animations',
            'creative': 'Artistic template with colorful gradients',
            'business': 'Professional business template with statistics',
            'portfolio': 'Creative portfolio for designers and artists',
            'landing': 'High-conversion landing page template',
            'blog': 'Content-focused blog template with sidebar',
            'magazine': 'News and media template with breaking news'
        }
        return descriptions.get(template_name, 'Professional website template')

    def _get_modern_template(self) -> str:
        """Get modern template with gradient design"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="{{ description }}">
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --text-dark: #2d3748;
            --text-light: #718096;
            --bg-light: #f7fafc;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            overflow-x: hidden;
        }
        
        .navbar {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .navbar-brand {
            font-weight: 700;
            font-size: 1.5rem;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .nav-link {
            font-weight: 500;
            color: var(--text-dark) !important;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .nav-link:hover {
            color: #667eea !important;
            transform: translateY(-2px);
        }
        
        .hero-section {
            background: var(--primary-gradient);
            min-height: 100vh;
            display: flex;
            align-items: center;
            position: relative;
            overflow: hidden;
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            width: 200%;
            height: 200%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            animation: float 20s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .hero-content {
            position: relative;
            z-index: 2;
            color: white;
        }
        
        .hero-title {
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            line-height: 1.2;
            animation: fadeInUp 1s ease-out;
        }
        
        .hero-subtitle {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            opacity: 0.9;
            animation: fadeInUp 1s ease-out 0.2s both;
        }
        
        .btn-hero {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
            padding: 15px 40px;
            font-weight: 600;
            font-size: 1.1rem;
            border-radius: 50px;
            transition: all 0.3s ease;
            animation: fadeInUp 1s ease-out 0.4s both;
        }
        
        .btn-hero:hover {
            background: white;
            color: #667eea;
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .features-section {
            padding: 100px 0;
            background: var(--bg-light);
        }
        
        .feature-card {
            background: white;
            border-radius: 20px;
            padding: 40px 30px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: none;
            height: 100%;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }
        
        .feature-icon {
            width: 80px;
            height: 80px;
            margin: 0 auto 30px;
            background: var(--accent-gradient);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            color: white;
        }
        
        .feature-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: var(--text-dark);
        }
        
        .feature-description {
            color: var(--text-light);
            line-height: 1.6;
        }
        
        .articles-section {
            padding: 100px 0;
        }
        
        .section-title {
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 60px;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .article-card {
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: none;
            height: 100%;
        }
        
        .article-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }
        
        .article-image {
            height: 250px;
            background: var(--secondary-gradient);
            position: relative;
        }
        
        .article-content {
            padding: 30px;
        }
        
        .article-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: var(--text-dark);
        }
        
        .article-excerpt {
            color: var(--text-light);
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        .article-meta {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        
        .article-date {
            color: var(--text-light);
            font-size: 0.9rem;
        }
        
        .article-category {
            background: var(--accent-gradient);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .btn-read-more {
            background: var(--primary-gradient);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .btn-read-more:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .footer {
            background: var(--text-dark);
            color: white;
            padding: 60px 0 30px;
        }
        
        .footer-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 20px;
        }
        
        .footer-links a {
            color: rgba(255, 255, 255, 0.7);
            text-decoration: none;
            display: block;
            margin-bottom: 10px;
            transition: all 0.3s ease;
        }
        
        .footer-links a:hover {
            color: white;
            transform: translateX(5px);
        }
        
        .footer-bottom {
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 40px;
            padding-top: 30px;
            text-align: center;
            color: rgba(255, 255, 255, 0.7);
        }
        
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem;
            }
            
            .hero-subtitle {
                font-size: 1.1rem;
            }
            
            .section-title {
                font-size: 2rem;
            }
            
            .feature-card {
                margin-bottom: 30px;
            }
        }
    </style>
    
    {% if seo_data %}
    {{ seo_data.meta_tags|safe }}
    {{ seo_data.og_tags|safe }}
    {{ seo_data.twitter_tags|safe }}
    {{ seo_data.structured_data|safe }}
    {% endif %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg fixed-top">
        <div class="container">
            <a class="navbar-brand" href="/">{{ title }}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/about">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/articles">Articles</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/contact">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6">
                    <div class="hero-content">
                        <h1 class="hero-title">{{ title }}</h1>
                        <p class="hero-subtitle">{{ description }}</p>
                        <a href="#features" class="btn btn-hero">Discover More</a>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="text-center">
                        <i class="fas fa-rocket" style="font-size: 15rem; opacity: 0.3; color: white;"></i>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="features-section" id="features">
        <div class="container">
            <h2 class="section-title">Amazing Features</h2>
            <div class="row">
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-bolt"></i>
                        </div>
                        <h3 class="feature-title">Lightning Fast</h3>
                        <p class="feature-description">Experience blazing fast performance with our optimized platform.</p>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        <h3 class="feature-title">Secure & Safe</h3>
                        <p class="feature-description">Your data is protected with enterprise-grade security measures.</p>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-mobile-alt"></i>
                        </div>
                        <h3 class="feature-title">Mobile Ready</h3>
                        <p class="feature-description">Fully responsive design that works perfectly on all devices.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Articles Section -->
    {% if articles %}
    <section class="articles-section">
        <div class="container">
            <h2 class="section-title">Latest Articles</h2>
            <div class="row">
                {% for article in articles[:3] %}
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="article-card">
                        {% if article.image_url %}
                        <div class="article-image" style="background-image: url('{{ article.image_url }}'); background-size: cover; background-position: center;"></div>
                        {% else %}
                        <div class="article-image"></div>
                        {% endif %}
                        <div class="article-content">
                            <div class="article-meta">
                                <span class="article-date">{{ article.created_at }}</span>
                                {% if article.category %}
                                <span class="article-category">{{ article.category }}</span>
                                {% endif %}
                            </div>
                            <h3 class="article-title">{{ article.title }}</h3>
                            <p class="article-excerpt">{{ article.content[:120] }}...</p>
                            <a href="#" class="btn btn-read-more">Read More</a>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h3 class="footer-title">{{ title }}</h3>
                    <p>{{ description }}</p>
                </div>
                <div class="col-md-6">
                    <h3 class="footer-title">Quick Links</h3>
                    <div class="footer-links">
                        <a href="/privacy">Privacy Policy</a>
                        <a href="/disclaimer">Disclaimer</a>
                        <a href="/sitemap">Sitemap</a>
                        <a href="/feed">RSS Feed</a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 {{ title }}. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

    def _get_creative_template(self) -> str:
        """Get creative template with artistic design"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="{{ description }}">
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary-color: #ff6b6b;
            --secondary-color: #4ecdc4;
            --accent-color: #ffe66d;
            --dark-color: #2c3e50;
            --light-color: #ecf0f1;
            --gradient-1: linear-gradient(135deg, #ff6b6b, #ee5a24);
            --gradient-2: linear-gradient(135deg, #4ecdc4, #44bd32);
            --gradient-3: linear-gradient(135deg, #ffe66d, #f39c12);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            line-height: 1.6;
            color: var(--dark-color);
            overflow-x: hidden;
        }
        
        .navbar {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            box-shadow: 0 4px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .navbar-brand {
            font-weight: 800;
            font-size: 1.8rem;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .nav-link {
            font-weight: 500;
            color: var(--dark-color) !important;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .nav-link::after {
            content: '';
            position: absolute;
            width: 0;
            height: 3px;
            bottom: -5px;
            left: 50%;
            background: var(--gradient-1);
            transition: all 0.3s ease;
            transform: translateX(-50%);
        }
        
        .nav-link:hover::after {
            width: 100%;
        }
        
        .hero-section {
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            position: relative;
            overflow: hidden;
        }
        
        .hero-bg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><radialGradient id="c" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="rgba(255,255,255,0.3)"/><stop offset="100%" stop-color="rgba(255,255,255,0)"/></radialGradient></defs><circle cx="200" cy="200" r="100" fill="url(%23c)"/><circle cx="800" cy="300" r="150" fill="url(%23c)"/><circle cx="400" cy="700" r="120" fill="url(%23c)"/><circle cx="900" cy="800" r="80" fill="url(%23c)"/></svg>');
            animation: float 15s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-30px); }
        }
        
        .hero-content {
            position: relative;
            z-index: 2;
            color: white;
        }
        
        .hero-title {
            font-size: 4.5rem;
            font-weight: 800;
            margin-bottom: 1.5rem;
            line-height: 1.1;
            animation: slideInLeft 1s ease-out;
        }
        
        .hero-subtitle {
            font-size: 1.4rem;
            margin-bottom: 2.5rem;
            opacity: 0.9;
            font-weight: 300;
            animation: slideInLeft 1s ease-out 0.3s both;
        }
        
        .btn-hero {
            background: var(--gradient-1);
            color: white;
            border: none;
            padding: 18px 45px;
            font-weight: 600;
            font-size: 1.2rem;
            border-radius: 50px;
            transition: all 0.3s ease;
            animation: slideInLeft 1s ease-out 0.6s both;
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
        }
        
        .btn-hero:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6);
        }
        
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .creative-shapes {
            position: absolute;
            top: 0;
            right: 0;
            width: 50%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .shape {
            position: absolute;
            border-radius: 50%;
            animation: rotate 20s linear infinite;
        }
        
        .shape-1 {
            width: 200px;
            height: 200px;
            background: var(--gradient-2);
            top: 20%;
            right: 20%;
            animation-delay: -5s;
        }
        
        .shape-2 {
            width: 150px;
            height: 150px;
            background: var(--gradient-3);
            top: 60%;
            right: 40%;
            animation-delay: -10s;
        }
        
        .shape-3 {
            width: 100px;
            height: 100px;
            background: var(--gradient-1);
            top: 40%;
            right: 10%;
            animation-delay: -15s;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg) translateX(50px) rotate(0deg); }
            100% { transform: rotate(360deg) translateX(50px) rotate(-360deg); }
        }
        
        .features-section {
            padding: 120px 0;
            background: var(--light-color);
            position: relative;
        }
        
        .section-title {
            font-size: 3.5rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 80px;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
        }
        
        .section-title::after {
            content: '';
            position: absolute;
            width: 100px;
            height: 5px;
            background: var(--gradient-1);
            bottom: -20px;
            left: 50%;
            transform: translateX(-50%);
        }
        
        .feature-card {
            background: white;
            border-radius: 30px;
            padding: 50px 30px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            transition: all 0.4s ease;
            border: none;
            height: 100%;
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transition: all 0.8s ease;
        }
        
        .feature-card:hover::before {
            left: 100%;
        }
        
        .feature-card:hover {
            transform: translateY(-15px) rotateY(5deg);
            box-shadow: 0 30px 80px rgba(0,0,0,0.15);
        }
        
        .feature-icon {
            width: 100px;
            height: 100px;
            margin: 0 auto 30px;
            background: var(--gradient-2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            color: white;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover .feature-icon {
            transform: rotateY(180deg);
            background: var(--gradient-1);
        }
        
        .feature-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 20px;
            color: var(--dark-color);
        }
        
        .feature-description {
            color: #7f8c8d;
            line-height: 1.6;
            font-size: 1.1rem;
        }
        
        .articles-section {
            padding: 120px 0;
            background: white;
        }
        
        .article-card {
            background: white;
            border-radius: 25px;
            overflow: hidden;
            box-shadow: 0 15px 50px rgba(0,0,0,0.1);
            transition: all 0.4s ease;
            border: none;
            height: 100%;
            position: relative;
        }
        
        .article-card:hover {
            transform: translateY(-10px) rotateX(5deg);
            box-shadow: 0 25px 70px rgba(0,0,0,0.15);
        }
        
        .article-image {
            height: 280px;
            background: var(--gradient-2);
            position: relative;
            overflow: hidden;
        }
        
        .article-image::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, rgba(255,107,107,0.3), rgba(78,205,196,0.3));
        }
        
        .article-content {
            padding: 35px;
        }
        
        .article-category {
            background: var(--gradient-3);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 15px;
        }
        
        .article-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 15px;
            color: var(--dark-color);
            line-height: 1.3;
        }
        
        .article-excerpt {
            color: #7f8c8d;
            margin-bottom: 25px;
            line-height: 1.6;
        }
        
        .article-meta {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 25px;
        }
        
        .article-date {
            color: #95a5a6;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .btn-read-more {
            background: var(--gradient-1);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-read-more:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4);
            color: white;
        }
        
        .footer {
            background: var(--dark-color);
            color: white;
            padding: 80px 0 40px;
            position: relative;
        }
        
        .footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: var(--gradient-1);
        }
        
        .footer-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 25px;
        }
        
        .footer-links a {
            color: #bdc3c7;
            text-decoration: none;
            display: block;
            margin-bottom: 12px;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .footer-links a:hover {
            color: #ff6b6b;
            transform: translateX(10px);
        }
        
        .footer-bottom {
            border-top: 1px solid #34495e;
            margin-top: 50px;
            padding-top: 30px;
            text-align: center;
            color: #95a5a6;
        }
        
        @media (max-width: 768px) {
            .hero-title {
                font-size: 3rem;
            }
            
            .hero-subtitle {
                font-size: 1.2rem;
            }
            
            .section-title {
                font-size: 2.5rem;
            }
            
            .creative-shapes {
                display: none;
            }
        }
    </style>
    
    {% if seo_data %}
    {{ seo_data.meta_tags|safe }}
    {{ seo_data.og_tags|safe }}
    {{ seo_data.twitter_tags|safe }}
    {{ seo_data.structured_data|safe }}
    {% endif %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg fixed-top">
        <div class="container">
            <a class="navbar-brand" href="/">{{ title }}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/about">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/articles">Articles</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/contact">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
        <div class="hero-bg"></div>
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6">
                    <div class="hero-content">
                        <h1 class="hero-title">{{ title }}</h1>
                        <p class="hero-subtitle">{{ description }}</p>
                        <a href="#features" class="btn btn-hero">Explore Now</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="creative-shapes">
            <div class="shape shape-1"></div>
            <div class="shape shape-2"></div>
            <div class="shape shape-3"></div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="features-section" id="features">
        <div class="container">
            <h2 class="section-title">Creative Features</h2>
            <div class="row">
                <div class="col-lg-4 col-md-6 mb-5">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-palette"></i>
                        </div>
                        <h3 class="feature-title">Creative Design</h3>
                        <p class="feature-description">Beautiful and artistic designs that capture attention and inspire creativity.</p>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-5">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-magic"></i>
                        </div>
                        <h3 class="feature-title">Magical Effects</h3>
                        <p class="feature-description">Stunning animations and effects that bring your content to life.</p>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-5">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-heart"></i>
                        </div>
                        <h3 class="feature-title">Made with Love</h3>
                        <p class="feature-description">Every element is crafted with care and attention to detail.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Articles Section -->
    {% if articles %}
    <section class="articles-section">
        <div class="container">
            <h2 class="section-title">Creative Stories</h2>
            <div class="row">
                {% for article in articles[:3] %}
                <div class="col-lg-4 col-md-6 mb-5">
                    <div class="article-card">
                        {% if article.image_url %}
                        <div class="article-image" style="background-image: url('{{ article.image_url }}'); background-size: cover; background-position: center;"></div>
                        {% else %}
                        <div class="article-image"></div>
                        {% endif %}
                        <div class="article-content">
                            {% if article.category %}
                            <span class="article-category">{{ article.category }}</span>
                            {% endif %}
                            <h3 class="article-title">{{ article.title }}</h3>
                            <p class="article-excerpt">{{ article.content[:120] }}...</p>
                            <div class="article-meta">
                                <span class="article-date">{{ article.created_at }}</span>
                            </div>
                            <a href="#" class="btn-read-more">Read More</a>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h3 class="footer-title">{{ title }}</h3>
                    <p>{{ description }}</p>
                </div>
                <div class="col-md-6">
                    <h3 class="footer-title">Quick Links</h3>
                    <div class="footer-links">
                        <a href="/privacy">Privacy Policy</a>
                        <a href="/disclaimer">Disclaimer</a>
                        <a href="/sitemap">Sitemap</a>
                        <a href="/feed">RSS Feed</a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 {{ title }}. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

    def _get_business_template(self) -> str:
        """Get business template with corporate design"""
        return self._get_professional_template()

    def _get_portfolio_template(self) -> str:
        """Get portfolio template for creative professionals"""  
        return self._get_creative_template()

    def _get_landing_template(self) -> str:
        """Get landing page template for marketing"""
        return self._get_modern_template()

    def _get_blog_template(self) -> str:
        """Get blog template optimized for content"""
        return self._get_default_template()

    def _get_magazine_template(self) -> str:
        """Get magazine template for news and media"""
        return self._get_professional_template()
