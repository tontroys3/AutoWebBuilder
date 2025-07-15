# Auto Website Builder

## Overview

This is a comprehensive web application built with Streamlit that enables users to create and manage professional websites with automated content generation, SEO optimization, and Cloudflare integration. The system analyzes domains, generates content, and provides a complete website building solution with multiple templates and management tools.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - Python-based web application framework
- **UI Components**: Custom components for site building, article management, and page generation
- **Navigation**: Sidebar-based menu system with multiple sections (Dashboard, Site Creation, Management, SEO Tools, etc.)
- **State Management**: Streamlit session state for managing sites, articles, and current selections

### Backend Architecture
- **Core Language**: Python
- **Component-Based Design**: Modular architecture with specialized classes for different functionalities
- **Template Engine**: Jinja2-based template rendering system
- **Content Processing**: Trafilatura for web scraping and content extraction

### Data Storage
- **Session Storage**: In-memory storage using Streamlit session state
- **File-Based Templates**: HTML templates stored as files and loaded dynamically
- **No Database**: Currently uses in-memory storage, suitable for adding database integration later

## Key Components

### Core Components
1. **SiteBuilder** (`components/site_builder.py`)
   - Creates new websites with domain analysis integration
   - Processes domain data and generates initial content
   - Manages site configuration and settings

2. **ArticleManager** (`components/article_manager.py`)
   - Handles article creation, editing, and management
   - Supports categories, tags, and metadata
   - Calculates reading time and generates excerpts

3. **PageGenerator** (`components/page_generator.py`)
   - Generates standard pages (About, Contact, Privacy, etc.)
   - Creates content based on site data and category
   - Provides template-based page generation

### Utility Components
1. **DomainAnalyzer** (`utils/domain_analyzer.py`)
   - Analyzes existing domains for content extraction
   - Uses trafilatura for web scraping
   - Extracts metadata and site structure

2. **CloudflareAPI** (`utils/cloudflare_api.py`)
   - Integrates with Cloudflare API for domain management
   - Handles API authentication and zone management
   - Provides connection testing capabilities

3. **SEOOptimizer** (`utils/seo_optimizer.py`)
   - Generates SEO metadata and structured data
   - Creates OpenGraph and Twitter Card tags
   - Extracts keywords and optimizes content

4. **FeedGenerator** (`utils/feed_generator.py`)
   - Creates RSS 2.0 feeds for websites
   - Generates XML feeds with proper namespaces
   - Supports article feeds and site syndication

5. **TemplateEngine** (`utils/template_engine.py`)
   - Jinja2-based template rendering
   - Supports multiple template types (default, professional, minimal)
   - Handles dynamic content insertion

### Template System
- **Default Template**: Bootstrap-based responsive design
- **Professional Template**: Corporate-style template with enhanced styling
- **Minimal Template**: Clean, typography-focused design
- **Extensible**: Easy to add new templates through the template engine

## Data Flow

1. **Site Creation Flow**:
   - User inputs domain, title, description
   - Domain analyzer extracts existing content (if applicable)
   - Site builder creates site structure with processed data
   - Template engine renders initial pages

2. **Content Generation Flow**:
   - Article manager creates articles with metadata
   - Page generator creates standard pages
   - SEO optimizer generates meta tags and structured data
   - Feed generator creates RSS feeds

3. **Domain Analysis Flow**:
   - Domain analyzer fetches and processes existing site content
   - Trafilatura extracts clean text and metadata
   - Content is processed and integrated into new site structure

## External Dependencies

### Python Libraries
- **streamlit**: Web application framework
- **jinja2**: Template engine
- **trafilatura**: Web scraping and content extraction
- **requests**: HTTP client for API calls
- **datetime**: Date/time handling
- **uuid**: Unique identifier generation
- **xml.etree.ElementTree**: XML processing for feeds
- **re**: Regular expressions for text processing
- **urllib.parse**: URL parsing utilities

### External Services
- **Cloudflare API**: Domain and DNS management
- **Bootstrap CDN**: CSS framework for responsive design
- **Feather Icons**: Icon library
- **Font Awesome**: Icon library for professional template

### Web Resources
- **Bootstrap 5.1.3**: Frontend framework
- **Feather Icons**: SVG icon library
- **Font Awesome 6.0**: Icon library

## Deployment Strategy

### Current Setup
- **Development**: Streamlit development server
- **Session-Based**: Uses Streamlit session state for data persistence
- **Single-User**: Designed for single-user sessions

### Recommended Enhancements
- **Database Integration**: Add persistent storage (PostgreSQL recommended)
- **Multi-User Support**: Implement user authentication and data isolation
- **File Storage**: Add file upload capabilities for images and assets
- **Production Deployment**: Deploy on cloud platforms with proper scaling
- **API Layer**: Consider adding REST API for external integrations

### Security Considerations
- **API Key Management**: Secure storage of Cloudflare API keys
- **Input Validation**: Sanitize user inputs for security
- **HTTPS**: Ensure secure connections for production deployment
- **Authentication**: Implement user authentication for production use

This architecture provides a solid foundation for a website building platform with room for enhancement and scaling as needed.

## Recent Updates (July 2025)

### Major System Enhancements

1. **Domain Configuration System** - Complete per-domain management
   - Individual TXT file configuration per domain in `PanelDomain` folder
   - Domain-specific keyword generation and storage
   - Article management with bullet point formatting
   - Comprehensive domain analytics and logging

2. **Query-Based Image Search** - No API required
   - Verified image sources with proper format validation
   - Support for JPG, PNG, WebP, and GIF formats
   - Automatic fallback system for broken images
   - High-quality Unsplash integration with format optimization

3. **Enhanced Auto Content Generation**
   - Per-domain content generation with bullet formatting
   - Keyword-based article creation with listing format
   - Domain-specific article storage and management
   - Integrated SEO optimization and meta generation

4. **SEO and Traffic Management**
   - Google Index API integration for auto-indexing
   - Manual URL import functionality
   - Sitemap generation per domain
   - Cloudflare API integration for traffic analysis

### Technical Architecture Updates

- **File-Based Storage**: All configurations stored as readable TXT files
- **Domain Isolation**: Complete separation of domain data and settings
- **Image Validation**: Comprehensive format checking and fallback system
- **Query-Based Systems**: Eliminated API dependencies where possible
- **Professional UI**: Simplified cPanel-style interface with functional tools

### Current System Features

- **Domain Management**: Individual panels with complete configuration
- **Content Generation**: Bullet-formatted articles with keyword optimization
- **Image System**: Verified sources with format validation
- **SEO Tools**: Auto-indexing and traffic analysis
- **Performance**: Optimized with proper caching and validation

### User Interface Improvements

- **Simplified Navigation**: Removed redundant menu items
- **Domain-Focused Design**: All functionality accessible within domain panels
- **Professional Styling**: Clean, functional cPanel-inspired interface
- **Real-Time Validation**: Immediate feedback on image and configuration validity

The system now provides a streamlined, professional website management platform with comprehensive per-domain functionality and robust image handling.