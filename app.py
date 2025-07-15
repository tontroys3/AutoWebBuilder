import streamlit as st
import os
from datetime import datetime
from components.site_builder import SiteBuilder
from components.article_manager import ArticleManager
from components.page_generator import PageGenerator
from utils.domain_analyzer import DomainAnalyzer
from utils.cloudflare_api import CloudflareAPI
from utils.seo_optimizer import SEOOptimizer
from utils.feed_generator import FeedGenerator
from utils.gemini_ai import GeminiAI
from utils.bing_image_scraper import BingImageScraper
from utils.bing_image_search import BingImageSearch
from utils.auto_content_manager import AutoContentManager
from utils.multi_domain_manager import MultiDomainManager
from utils.api_manager import APIManager
from utils.keyword_generator import KeywordGenerator
from utils.pixel_api import PixelAPI
from utils.domain_config_manager import DomainConfigManager
from utils.log_manager import LogManager
from utils.article_formatter import ArticleFormatter
from utils.template_engine import TemplateEngine
from utils.adsense_manager import AdSenseManager
from auth import AuthManager

# Initialize session state
if 'sites' not in st.session_state:
    st.session_state.sites = {}
if 'current_site' not in st.session_state:
    st.session_state.current_site = None
if 'articles' not in st.session_state:
    st.session_state.articles = {}

def main():
    st.set_page_config(
        page_title="Worker Login Panel Manager",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize authentication
    auth_manager = AuthManager()
    
    # Check authentication
    if not auth_manager.is_session_valid():
        auth_manager.show_login_form()
        return
    
    # Initialize managers
    api_manager = APIManager()
    domain_config_manager = DomainConfigManager()
    log_manager = LogManager()
    article_formatter = ArticleFormatter()
    
    # Auto-clean logs every 24 hours
    log_manager.auto_clean_all_logs(24)
    
    # Initialize components with API manager
    site_builder = SiteBuilder()
    article_manager = ArticleManager()
    page_generator = PageGenerator()
    domain_analyzer = DomainAnalyzer()
    cloudflare_api = CloudflareAPI()
    seo_optimizer = SEOOptimizer()
    feed_generator = FeedGenerator()
    gemini_ai = GeminiAI(api_manager)
    bing_image_scraper = BingImageScraper(api_manager)
    bing_image_search = BingImageSearch()
    auto_content_manager = AutoContentManager(api_manager)
    multi_domain_manager = MultiDomainManager(api_manager)
    keyword_generator = KeywordGenerator(api_manager)
    pixel_api = PixelAPI(api_manager)
    adsense_manager = AdSenseManager()
    
    # Professional sidebar navigation with list style
    with st.sidebar:
        st.markdown("""
        <style>
        .nav-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .nav-item {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 12px 16px;
            margin: 8px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .nav-item:hover {
            background: #e9ecef;
            border-color: #6c757d;
        }
        .nav-item.active {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            border-color: #28a745;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # User info section
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;">
            <h4>👤 {auth_manager.get_current_user()}</h4>
            <p>Worker Login Panel Manager</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            auth_manager.logout()
            st.rerun()
        
        st.markdown("---")
        
        # Navigation menu items (Worker Panel-style simplified)
        nav_items = [
            ("🏠 Dashboard", "Dashboard"),
            ("🔐 API Settings", "API Settings"),
            ("➕ Add Site", "Add New Site")
        ]
        
        # Initialize menu selection
        if 'selected_menu' not in st.session_state:
            st.session_state.selected_menu = "Dashboard"
        
        # Create navigation buttons
        for display_name, menu_value in nav_items:
            if st.button(display_name, key=f"nav_{menu_value}", use_container_width=True):
                st.session_state.selected_menu = menu_value
                st.rerun()
        
        # System status overview
        st.markdown("---")
        st.subheader("🔧 System Status")
        
        # Get domain status overview
        domain_status = log_manager.get_all_domain_status()
        
        if domain_status:
            healthy_count = sum(1 for status in domain_status.values() if status['status'] == 'healthy')
            warning_count = sum(1 for status in domain_status.values() if status['status'] == 'warning')
            error_count = sum(1 for status in domain_status.values() if status['status'] == 'error')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("✅", healthy_count)
            with col2:
                st.metric("⚠️", warning_count)
            with col3:
                st.metric("❌", error_count)
            
            # Show problematic domains
            if error_count > 0:
                st.error(f"🚨 {error_count} domain(s) have errors")
                if st.button("🔍 View Error Logs"):
                    st.session_state.show_error_logs = True
            elif warning_count > 0:
                st.warning(f"⚠️ {warning_count} domain(s) have warnings")
            else:
                st.success("✅ All systems operational")
        else:
            st.info("No domains to monitor")
        
        # Add user management panel
        auth_manager.show_user_management_panel()
        
        menu_option = st.session_state.selected_menu
    
    # Main content area
    if menu_option == "Dashboard":
        show_worker_dashboard(multi_domain_manager, keyword_generator, pixel_api, log_manager, domain_config_manager, auto_content_manager, gemini_ai, bing_image_scraper, article_formatter)
    elif menu_option == "API Settings":
        show_api_settings(api_manager, pixel_api)
    elif menu_option == "Add New Site":
        show_add_site(site_builder, domain_analyzer, seo_optimizer, multi_domain_manager, domain_config_manager)

def show_worker_dashboard(multi_domain_manager, keyword_generator, pixel_api, log_manager, domain_config_manager, auto_content_manager, gemini_ai, bing_image_scraper, article_formatter):
    """Minimalistic Worker Panel dashboard with 9x6 grid layout"""
    
    # Minimalistic dashboard styling
    st.markdown("""
    <style>
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 10px;
        margin: 20px 0;
        max-width: 100%;
    }
    .mini-domain-card {
        background: white;
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
        position: relative;
        min-height: 120px;
        cursor: pointer;
    }
    .mini-domain-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .mini-domain-card.status-error {
        border-left: 4px solid #dc3545;
        background: #fff5f5;
    }
    .mini-domain-card.status-warning {
        border-left: 4px solid #ffc107;
        background: #fffbf0;
    }
    .mini-domain-card.status-healthy {
        border-left: 4px solid #28a745;
        background: #f8fff8;
    }
    .domain-name {
        font-size: 0.9em;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 8px;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
    }
    .domain-status {
        font-size: 0.7em;
        padding: 2px 6px;
        border-radius: 12px;
        position: absolute;
        top: 8px;
        right: 8px;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 4px;
    }
    .status-dot.healthy { background: #28a745; }
    .status-dot.warning { background: #ffc107; }
    .status-dot.error { background: #dc3545; }
    .status-dot.inactive { background: #6c757d; }
    .domain-info {
        font-size: 0.75em;
        color: #6c757d;
        margin: 4px 0;
    }
    .add-domain-mini {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        border: 2px dashed rgba(255,255,255,0.3);
        color: white;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 120px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .add-domain-mini:hover {
        transform: scale(1.05);
        border-color: rgba(255,255,255,0.6);
    }
    .action-buttons {
        display: flex;
        gap: 4px;
        margin-top: 8px;
    }
    .mini-btn {
        flex: 1;
        padding: 4px 8px;
        font-size: 0.7em;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .btn-manage { background: #007bff; color: white; }
    .btn-view { background: #28a745; color: white; }
    .btn-delete { background: #dc3545; color: white; }
    </style>
    """, unsafe_allow_html=True)
    
    # Simplified header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h2>🌐 Domain Control Panel</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Get domain data and status
    domains = multi_domain_manager.get_domain_grid_view()
    domain_status = log_manager.get_all_domain_status()
    
    # Quick stats - simplified
    col1, col2 = st.columns(2)
    
    total_domains = len(domains) if domains and 'error' not in domains[0] else 0
    active_domains = sum(1 for d in domains if d.get('status') == 'active') if domains and 'error' not in domains[0] else 0
    
    with col1:
        st.metric("Total Domains", total_domains)
    with col2:
        st.metric("Active Domains", active_domains)
    
    # Domain grid display (9x6 layout)
    st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
    
    # Calculate pages for pagination
    domains_per_page = 54  # 9 rows × 6 columns
    page = st.session_state.get('dashboard_page', 0)
    
    if domains and 'error' not in domains[0]:
        # Paginate domains
        start_idx = page * domains_per_page
        end_idx = start_idx + domains_per_page
        page_domains = domains[start_idx:end_idx]
        
        # Display domains in grid
        for i, domain_data in enumerate(page_domains):
            domain_name = domain_data['domain']
            status = domain_status.get(domain_name, {'status': 'unknown'})
            
            card_html = f"""
            <div class="mini-domain-card status-{status['status']}" onclick="selectDomain('{domain_name}')">
                <div class="domain-name" title="{domain_name}">{domain_name}</div>
                <div class="domain-info">
                    <div class="status-dot {status['status']}"></div>
                    {status['status'].title()}
                </div>
                <div class="domain-info">
                    Articles: {domain_data.get('article_count', 0)}
                </div>
                <div class="domain-info">
                    Template: {domain_data.get('template', 'default')}
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Action buttons below each card
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("⚙️", key=f"manage_{domain_name}_{i}", help="Manage", use_container_width=True):
                    st.session_state.selected_menu = "Domain Management"
                    st.session_state.selected_domain = domain_name
                    st.rerun()
            
            with col2:
                if st.button("📊", key=f"view_{domain_name}_{i}", help="View Analytics", use_container_width=True):
                    st.session_state.selected_menu = "Domain Management"
                    st.session_state.analytics_domain = domain_name
                    st.rerun()
            
            with col3:
                if st.button("❌", key=f"delete_{domain_name}_{i}", help="Delete", use_container_width=True):
                    if st.session_state.get('confirm_delete') == domain_name:
                        multi_domain_manager.delete_domain(domain_name)
                        del st.session_state.confirm_delete
                        st.success(f"Domain {domain_name} deleted!")
                        st.rerun()
                    else:
                        st.session_state.confirm_delete = domain_name
                        st.warning(f"Click again to confirm deletion of {domain_name}")
        
        # Add empty slots up to grid size
        remaining_slots = domains_per_page - len(page_domains)
        if remaining_slots > 0:
            for i in range(min(remaining_slots, 1)):  # Show only one "add" button
                st.markdown("""
                <div class="add-domain-mini">
                    <div style="font-size: 1.5em; margin-bottom: 5px;">➕</div>
                    <div style="font-size: 0.8em;">Add Domain</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🚀 Add New Domain", key=f"add_domain_{i}", use_container_width=True):
                    st.session_state.selected_menu = "Add New Site"
                    st.rerun()
                break
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Pagination controls
    if domains and len(domains) > domains_per_page:
        total_pages = (len(domains) + domains_per_page - 1) // domains_per_page
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if page > 0:
                if st.button("⬅️ Previous"):
                    st.session_state.dashboard_page = page - 1
                    st.rerun()
        
        with col2:
            st.write(f"Page {page + 1} of {total_pages}")
        
        with col3:
            if page < total_pages - 1:
                if st.button("Next ➡️"):
                    st.session_state.dashboard_page = page + 1
                    st.rerun()
    
    # Show error/warning domains if any
    if domain_status:
        error_domains = [d for d, s in domain_status.items() if s['status'] == 'error']
        warning_domains = [d for d, s in domain_status.items() if s['status'] == 'warning']
        
        if error_domains:
            st.error(f"⚠️ Domains with errors: {', '.join(error_domains)}")
        
        if warning_domains:
            st.warning(f"⚠️ Domains with warnings: {', '.join(warning_domains)}")
    
    # Initialize dashboard page
    if 'dashboard_page' not in st.session_state:
        st.session_state.dashboard_page = 0

def show_add_site(site_builder, domain_analyzer, seo_optimizer, multi_domain_manager, domain_config_manager):
    st.header("➕ Add New Domain")
    
    # Template preview section
    st.subheader("🎨 Template Preview")
    
    # Template selection with previews - All available templates
    template_engine = TemplateEngine()
    available_templates = template_engine.get_available_templates()
    
    template_options = {
        "default": {
            "name": "Default Template",
            "description": "Clean, responsive design with modern styling",
            "preview": "https://via.placeholder.com/300x200/007bff/ffffff?text=Default"
        },
        "professional": {
            "name": "Professional Template", 
            "description": "Corporate-style with enhanced features",
            "preview": "https://via.placeholder.com/300x200/28a745/ffffff?text=Professional"
        },
        "minimal": {
            "name": "Minimal Template",
            "description": "Typography-focused clean design",
            "preview": "https://via.placeholder.com/300x200/6c757d/ffffff?text=Minimal"
        },
        "modern": {
            "name": "Modern Template",
            "description": "Gradient design with smooth animations",
            "preview": "https://via.placeholder.com/300x200/667eea/ffffff?text=Modern"
        },
        "creative": {
            "name": "Creative Template",
            "description": "Artistic design with colorful gradients",
            "preview": "https://via.placeholder.com/300x200/ff6b6b/ffffff?text=Creative"
        },
        "business": {
            "name": "Business Template",
            "description": "Professional business template with statistics",
            "preview": "https://via.placeholder.com/300x200/1e3a8a/ffffff?text=Business"
        },
        "portfolio": {
            "name": "Portfolio Template",
            "description": "Creative portfolio for designers and artists",
            "preview": "https://via.placeholder.com/300x200/2c2c2c/ffffff?text=Portfolio"
        },
        "landing": {
            "name": "Landing Template",
            "description": "High-conversion landing page template",
            "preview": "https://via.placeholder.com/300x200/ff4757/ffffff?text=Landing"
        },
        "blog": {
            "name": "Blog Template",
            "description": "Content-focused blog template with sidebar",
            "preview": "https://via.placeholder.com/300x200/2c5aa0/ffffff?text=Blog"
        },
        "magazine": {
            "name": "Magazine Template",
            "description": "News and media template with breaking news",
            "preview": "https://via.placeholder.com/300x200/1a1a1a/ffffff?text=Magazine"
        }
    }
    
    # Show all templates in a grid layout
    st.markdown("### Available Templates")
    
    # Display templates in rows of 3
    template_keys = list(template_options.keys())
    selected_template = None
    
    for i in range(0, len(template_keys), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(template_keys):
                template_key = template_keys[i + j]
                template_info = template_options[template_key]
                
                with col:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 15px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 15px;">
                        <img src="{template_info['preview']}" style="width: 100%; border-radius: 4px; height: 150px; object-fit: cover;">
                        <h4 style="margin: 10px 0 5px 0; font-size: 1.1em;">{template_info['name']}</h4>
                        <p style="font-size: 0.8em; color: #666; margin: 0;">{template_info['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Select {template_info['name']}", key=f"select_{template_key}", use_container_width=True):
                        selected_template = template_key
                        st.session_state.selected_template = template_key
                        st.success(f"✅ {template_info['name']} selected!")
    
    # Show currently selected template
    if hasattr(st.session_state, 'selected_template'):
        selected_name = template_options[st.session_state.selected_template]['name']
        st.info(f"🎨 Currently selected: **{selected_name}**")
    
    # Store selected template
    if selected_template:
        st.session_state.selected_template = selected_template
    
    # Domain configuration form
    st.subheader("⚙️ Domain Configuration")
    
    with st.form("create_site_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            domain = st.text_input("Target Domain", placeholder="example.com")
            site_title = st.text_input("Site Title", placeholder="My Awesome Website")
            site_description = st.text_area("Site Description", placeholder="Brief description of your website")
        
        with col2:
            template_list = list(template_options.keys())
            default_index = 0
            if hasattr(st.session_state, 'selected_template') and st.session_state.selected_template in template_list:
                default_index = template_list.index(st.session_state.selected_template)
            
            template = st.selectbox("Template", template_list, 
                                  index=default_index,
                                  format_func=lambda x: template_options[x]['name'])
            category = st.selectbox("Site Category", ["Blog", "Business", "Portfolio", "E-commerce", "News", "Educational"])
            auto_generate = st.checkbox("Auto-generate content based on domain analysis", value=True)
        
        submitted = st.form_submit_button("🚀 Create Domain")
        
        if submitted and domain and site_title:
            with st.spinner("Creating domain..."):
                # Analyze domain if auto-generate is enabled
                domain_data = {}
                if auto_generate:
                    domain_data = domain_analyzer.analyze_domain(domain)
                
                # Create site
                site_data = site_builder.create_site(
                    domain=domain,
                    title=site_title,
                    description=site_description,
                    template=template,
                    category=category,
                    domain_data=domain_data
                )
                
                # Create domain configuration
                domain_config = {
                    'title': site_title,
                    'description': site_description,
                    'template': template,
                    'category': category,
                    'status': 'active',
                    'auto_posting': {
                        'enabled': False,
                        'interval_hours': 6,
                        'max_posts_per_day': 4,
                        'article_length': 1000,
                        'images_per_article': 3,
                        'seo_optimization': True,
                        'manual_keywords': [],
                        'manual_titles': []
                    },
                    'feed_enabled': True,
                    'sitemap_enabled': True,
                    'seo_settings': {
                        'auto_meta_generation': True,
                        'schema_markup': True,
                        'sitemap_auto_update': True,
                        'robots_txt': True,
                        'keyword_optimization': True
                    },
                    'performance': {
                        'cache_enabled': True,
                        'lazy_loading': True,
                        'image_optimization': True,
                        'minification': True
                    }
                }
                
                # Save domain configuration
                config_result = domain_config_manager.save_domain_config(domain, domain_config)
                
                # Create domain panel
                result = multi_domain_manager.create_domain_panel(domain, domain_config)
                
                if result.get('success') and config_result.get('success'):
                    st.session_state.sites[domain] = site_data
                    st.session_state.current_site = domain
                    
                    # Generate SEO data
                    seo_data = seo_optimizer.generate_seo_data(site_title, site_description, category)
                    st.session_state.sites[domain]['seo'] = seo_data
                    
                    st.success(f"Domain '{site_title}' created successfully!")
                    st.info(f"Configuration saved to: {domain_config_manager.get_config_file_path(domain)}")
                    st.session_state.selected_menu = "Dashboard"
                    st.rerun()
                else:
                    st.error(f"Failed to create domain: {result.get('error', 'Unknown error')}")

def show_manage_sites(site_builder):
    st.header("🛠️ Manage Sites")
    
    if not st.session_state.sites:
        st.info("No sites to manage. Create a site first!")
        return
    
    selected_domain = st.selectbox("Select Site", list(st.session_state.sites.keys()))
    
    if selected_domain:
        site_data = st.session_state.sites[selected_domain]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Site Information")
            st.write(f"**Domain:** {selected_domain}")
            st.write(f"**Title:** {site_data.get('title', 'N/A')}")
            st.write(f"**Template:** {site_data.get('template', 'default')}")
            st.write(f"**Category:** {site_data.get('category', 'N/A')}")
            st.write(f"**Status:** {site_data.get('status', 'inactive')}")
        
        with col2:
            st.subheader("Actions")
            if st.button("Generate Essential Pages"):
                pages = site_builder.generate_essential_pages(selected_domain, site_data)
                st.session_state.sites[selected_domain]['pages'] = pages
                st.success("Essential pages generated!")
                st.rerun()
            
            if st.button("Preview Site"):
                preview_html = site_builder.generate_preview(selected_domain, site_data)
                st.components.v1.html(preview_html, height=600, scrolling=True)
            
            if st.button("Toggle Status"):
                current_status = site_data.get('status', 'inactive')
                new_status = 'active' if current_status == 'inactive' else 'inactive'
                st.session_state.sites[selected_domain]['status'] = new_status
                st.success(f"Site status changed to {new_status}")
                st.rerun()
        
        # Show generated pages
        if 'pages' in site_data:
            st.subheader("Generated Pages")
            for page_name, page_content in site_data['pages'].items():
                with st.expander(f"📄 {page_name.title()}"):
                    st.code(page_content[:500] + "..." if len(page_content) > 500 else page_content)

def show_articles(article_manager):
    st.header("📝 Article Management")
    
    if not st.session_state.sites:
        st.info("Create a site first to manage articles!")
        return
    
    selected_domain = st.selectbox("Select Site", list(st.session_state.sites.keys()))
    
    if selected_domain:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Create New Article")
            with st.form("article_form"):
                article_title = st.text_input("Article Title")
                article_content = st.text_area("Article Content", height=200)
                article_category = st.selectbox("Category", ["General", "Technology", "Business", "Lifestyle", "News"])
                article_tags = st.text_input("Tags (comma separated)")
                image_url = st.text_input("Featured Image URL (optional)")
                
                if st.form_submit_button("Create Article"):
                    if article_title and article_content:
                        article_data = article_manager.create_article(
                            title=article_title,
                            content=article_content,
                            category=article_category,
                            tags=article_tags.split(",") if article_tags else [],
                            image_url=image_url
                        )
                        
                        if selected_domain not in st.session_state.articles:
                            st.session_state.articles[selected_domain] = []
                        
                        st.session_state.articles[selected_domain].append(article_data)
                        st.success("Article created successfully!")
                        st.rerun()
        
        with col2:
            st.subheader("Article Statistics")
            if selected_domain in st.session_state.articles:
                articles = st.session_state.articles[selected_domain]
                st.metric("Total Articles", len(articles))
                
                if articles:
                    categories = [article.get('category', 'General') for article in articles]
                    category_counts = {cat: categories.count(cat) for cat in set(categories)}
                    
                    st.subheader("Categories")
                    for cat, count in category_counts.items():
                        st.write(f"**{cat}:** {count}")
        
        # Show existing articles
        if selected_domain in st.session_state.articles and st.session_state.articles[selected_domain]:
            st.subheader("Existing Articles")
            for i, article in enumerate(st.session_state.articles[selected_domain]):
                with st.expander(f"📄 {article['title']}"):
                    st.write(f"**Category:** {article.get('category', 'General')}")
                    st.write(f"**Created:** {article.get('created_at', 'Unknown')}")
                    st.write(f"**Tags:** {', '.join(article.get('tags', []))}")
                    st.write(f"**Content:** {article['content'][:200]}...")
                    if article.get('image_url'):
                        st.image(article['image_url'], width=200)

def show_seo_tools(seo_optimizer):
    st.header("🔍 SEO Tools")
    
    tab1, tab2 = st.tabs(["SEO Analysis", "Meta Tag Generator"])
    
    with tab1:
        st.subheader("SEO Analysis")
        if st.session_state.sites:
            selected_domain = st.selectbox("Select Site for Analysis", list(st.session_state.sites.keys()))
            
            if selected_domain and st.button("Analyze SEO"):
                site_data = st.session_state.sites[selected_domain]
                seo_analysis = seo_optimizer.analyze_site_seo(site_data)
                
                st.subheader("SEO Score")
                st.metric("Overall Score", f"{seo_analysis.get('score', 0)}/100")
                
                st.subheader("Recommendations")
                for recommendation in seo_analysis.get('recommendations', []):
                    st.write(f"• {recommendation}")
    
    with tab2:
        st.subheader("Meta Tag Generator")
        with st.form("meta_form"):
            meta_title = st.text_input("Page Title")
            meta_description = st.text_area("Meta Description")
            meta_keywords = st.text_input("Keywords (comma separated)")
            
            if st.form_submit_button("Generate Meta Tags"):
                if meta_title:
                    meta_tags = seo_optimizer.generate_meta_tags(meta_title, meta_description, meta_keywords)
                    st.code(meta_tags, language="html")

def show_feed_management(feed_generator):
    st.header("📡 Feed Management")
    
    if not st.session_state.sites:
        st.info("Create a site first to manage feeds!")
        return
    
    selected_domain = st.selectbox("Select Site", list(st.session_state.sites.keys()))
    
    if selected_domain:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Generate RSS Feed")
            if st.button("Generate RSS Feed"):
                if selected_domain in st.session_state.articles:
                    articles = st.session_state.articles[selected_domain]
                    site_data = st.session_state.sites[selected_domain]
                    
                    rss_feed = feed_generator.generate_rss_feed(
                        site_data=site_data,
                        articles=articles,
                        domain=selected_domain
                    )
                    
                    st.code(rss_feed, language="xml")
                    st.download_button(
                        label="Download RSS Feed",
                        data=rss_feed,
                        file_name=f"{selected_domain}_feed.xml",
                        mime="application/rss+xml"
                    )
                else:
                    st.warning("No articles found for this site!")
        
        with col2:
            st.subheader("Generate Atom Feed")
            if st.button("Generate Atom Feed"):
                if selected_domain in st.session_state.articles:
                    articles = st.session_state.articles[selected_domain]
                    site_data = st.session_state.sites[selected_domain]
                    
                    atom_feed = feed_generator.generate_atom_feed(
                        site_data=site_data,
                        articles=articles,
                        domain=selected_domain
                    )
                    
                    st.code(atom_feed, language="xml")
                    st.download_button(
                        label="Download Atom Feed",
                        data=atom_feed,
                        file_name=f"{selected_domain}_atom.xml",
                        mime="application/atom+xml"
                    )
                else:
                    st.warning("No articles found for this site!")

def show_cloudflare_settings(cloudflare_api):
    st.header("☁️ Cloudflare Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("API Configuration")
        api_key = st.text_input("Cloudflare API Key", type="password", value=os.getenv("CLOUDFLARE_API_KEY", ""))
        zone_id = st.text_input("Zone ID", value=os.getenv("CLOUDFLARE_ZONE_ID", ""))
        
        if st.button("Test Connection"):
            if api_key and zone_id:
                result = cloudflare_api.test_connection(api_key, zone_id)
                if result['success']:
                    st.success("Connection successful!")
                else:
                    st.error(f"Connection failed: {result['error']}")
            else:
                st.warning("Please provide both API key and Zone ID")
    
    with col2:
        st.subheader("Domain Management")
        if st.session_state.sites:
            selected_domain = st.selectbox("Select Domain", list(st.session_state.sites.keys()))
            
            if selected_domain:
                if st.button("Deploy to Cloudflare"):
                    site_data = st.session_state.sites[selected_domain]
                    result = cloudflare_api.deploy_site(api_key, zone_id, selected_domain, site_data)
                    
                    if result['success']:
                        st.success("Site deployed successfully!")
                        st.session_state.sites[selected_domain]['cloudflare_deployed'] = True
                    else:
                        st.error(f"Deployment failed: {result['error']}")
                
                if st.button("Check DNS Records"):
                    dns_records = cloudflare_api.get_dns_records(api_key, zone_id, selected_domain)
                    if dns_records:
                        st.subheader("DNS Records")
                        for record in dns_records:
                            st.write(f"**{record['type']}:** {record['name']} -> {record['content']}")

def show_domain_management(multi_domain_manager, auto_content_manager, gemini_ai, bing_image_search, keyword_generator, pixel_api):
    """Domain management panel with per-domain settings"""
    st.header("🌐 Domain Management Panel")
    
    # Check if specific domain is selected
    selected_domain = st.session_state.get('selected_domain')
    analytics_domain = st.session_state.get('analytics_domain')
    
    if selected_domain:
        show_domain_panel(selected_domain, multi_domain_manager, auto_content_manager, gemini_ai, bing_image_search, keyword_generator, pixel_api)
    elif analytics_domain:
        show_domain_analytics(analytics_domain, multi_domain_manager)
    else:
        # Show main domain management interface
        domains = multi_domain_manager.get_all_domains()
        
        if not domains:
            st.info("No domains found. Create your first domain from the dashboard!")
            if st.button("🚀 Create New Domain"):
                st.session_state.selected_menu = "Add New Site"
                st.rerun()
            return
        
        # Domain selection
        domain_options = [d['domain'] for d in domains]
        selected = st.selectbox("Select Domain to Manage", domain_options)
        
        if selected:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("⚙️ Manage Domain Settings", use_container_width=True):
                    st.session_state.selected_domain = selected
                    st.rerun()
            
            with col2:
                if st.button("📊 View Analytics", use_container_width=True):
                    st.session_state.analytics_domain = selected
                    st.rerun()

def show_domain_panel(domain, multi_domain_manager, auto_content_manager, gemini_ai, bing_image_search, keyword_generator, pixel_api, adsense_manager):
    """Show individual domain management panel"""
    
    # Header with back button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back to Dashboard"):
            del st.session_state.selected_domain
            st.session_state.selected_menu = "Dashboard"
            st.rerun()
    
    with col2:
        st.subheader(f"🌐 Managing: {domain}")
    
    # Get domain settings
    domain_panel = multi_domain_manager.get_domain_panel(domain)
    
    if 'error' in domain_panel:
        st.error(f"Error loading domain: {domain_panel['error']}")
        return
    
    # Domain configuration tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["⚙️ General", "🤖 Auto Content", "🔍 SEO", "📡 Feeds", "☁️ Cloudflare", "💰 AdSense", "📊 Analytics"])
    
    with tab1:
        show_domain_general_settings(domain, domain_panel, multi_domain_manager)
    
    with tab2:
        show_domain_auto_content(domain, domain_panel, auto_content_manager, gemini_ai, bing_image_search, keyword_generator, pixel_api)
    
    with tab3:
        show_domain_seo_settings(domain, domain_panel, multi_domain_manager)
    
    with tab4:
        show_domain_feed_settings(domain, domain_panel, multi_domain_manager)
    
    with tab5:
        show_domain_cloudflare_settings(domain, domain_panel, multi_domain_manager)
    
    with tab6:
        show_domain_adsense_settings(domain, domain_panel, adsense_manager)
    
    with tab7:
        show_domain_analytics(domain, multi_domain_manager)

def show_domain_general_settings(domain, domain_panel, multi_domain_manager):
    """Show general domain settings"""
    st.subheader("⚙️ General Settings")
    
    settings = domain_panel['settings']
    
    with st.form("general_settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Site Title", value=settings.get('title', ''))
            description = st.text_area("Site Description", value=settings.get('description', ''))
            template = st.selectbox("Template", ["default", "professional", "minimal"], 
                                  index=["default", "professional", "minimal"].index(settings.get('template', 'default')))
        
        with col2:
            category = st.selectbox("Category", ["Blog", "Business", "Portfolio", "E-commerce", "News", "Educational"],
                                  index=["Blog", "Business", "Portfolio", "E-commerce", "News", "Educational"].index(settings.get('category', 'Blog')))
            status = st.selectbox("Status", ["active", "inactive"], 
                                index=["active", "inactive"].index(settings.get('status', 'active')))
            
        # Performance settings
        st.subheader("🚀 Performance Settings")
        col1, col2 = st.columns(2)
        
        with col1:
            cache_enabled = st.checkbox("Enable Caching", value=settings.get('performance', {}).get('cache_enabled', True))
            lazy_loading = st.checkbox("Lazy Loading", value=settings.get('performance', {}).get('lazy_loading', True))
        
        with col2:
            image_optimization = st.checkbox("Image Optimization", value=settings.get('performance', {}).get('image_optimization', True))
            minification = st.checkbox("CSS/JS Minification", value=settings.get('performance', {}).get('minification', True))
        
        if st.form_submit_button("💾 Save Settings"):
            updates = {
                'title': title,
                'description': description,
                'template': template,
                'category': category,
                'status': status,
                'performance': {
                    'cache_enabled': cache_enabled,
                    'lazy_loading': lazy_loading,
                    'image_optimization': image_optimization,
                    'minification': minification
                }
            }
            
            result = multi_domain_manager.update_domain_settings(domain, updates)
            if result.get('success'):
                st.success("Settings updated successfully!")
                st.rerun()
            else:
                st.error(f"Failed to update settings: {result.get('error')}")

def show_domain_auto_content(domain, domain_panel, auto_content_manager, gemini_ai, bing_image_search, keyword_generator, pixel_api):
    """Show auto content settings for domain"""
    st.subheader("🤖 Auto Content Generation")
    
    settings = domain_panel['settings']
    auto_posting = settings.get('auto_posting', {})
    
    # Auto posting configuration
    with st.form("auto_content_settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            enabled = st.checkbox("Enable Auto Posting", value=auto_posting.get('enabled', False))
            interval_hours = st.slider("Posting Interval (hours)", 1, 24, value=auto_posting.get('interval_hours', 6))
            max_posts_per_day = st.slider("Max Posts per Day", 1, 10, value=auto_posting.get('max_posts_per_day', 4))
        
        with col2:
            article_length = st.slider("Article Length (words)", 500, 3000, value=auto_posting.get('article_length', 1000))
            images_per_article = st.slider("Images per Article", 1, 10, value=auto_posting.get('images_per_article', 3))
            seo_optimization = st.checkbox("SEO Optimization", value=auto_posting.get('seo_optimization', True))
        
        # Manual keyword input
        st.subheader("📝 Manual Keywords & Titles")
        manual_keywords = st.text_area("Manual Keywords (one per line)", 
                                     value="\n".join(auto_posting.get('manual_keywords', [])),
                                     help="Enter keywords manually, one per line")
        
        manual_titles = st.text_area("Manual Titles (one per line)", 
                                   value="\n".join(auto_posting.get('manual_titles', [])),
                                   help="Enter article titles manually, one per line")
        
        if st.form_submit_button("💾 Save Auto Content Settings"):
            updates = {
                'auto_posting': {
                    'enabled': enabled,
                    'interval_hours': interval_hours,
                    'max_posts_per_day': max_posts_per_day,
                    'article_length': article_length,
                    'images_per_article': images_per_article,
                    'seo_optimization': seo_optimization,
                    'manual_keywords': [k.strip() for k in manual_keywords.split('\n') if k.strip()],
                    'manual_titles': [t.strip() for t in manual_titles.split('\n') if t.strip()]
                }
            }
            
            result = multi_domain_manager.update_domain_settings(domain, updates)
            if result.get('success'):
                st.success("Auto content settings updated!")
                
                # Start or stop auto posting based on settings
                if enabled:
                    auto_result = auto_content_manager.start_auto_posting(domain, updates['auto_posting'])
                    if auto_result.get('success'):
                        st.success("Auto posting started!")
                    else:
                        st.error(f"Failed to start auto posting: {auto_result.get('error')}")
                else:
                    auto_content_manager.stop_auto_posting(domain)
                    st.info("Auto posting stopped.")
                
                st.rerun()
            else:
                st.error(f"Failed to update settings: {result.get('error')}")
    
    # Keyword generation tools
    st.markdown("---")
    st.subheader("🔍 Keyword Generation Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Generate Keywords**")
        category = st.selectbox("Category for Keywords", ["Technology", "Health", "Business", "Lifestyle", "Education", "Finance"])
        keyword_count = st.slider("Number of Keywords", 5, 50, 20)
        
        if st.button("🔍 Generate Keywords"):
            with st.spinner("Generating keywords..."):
                keywords = keyword_generator.generate_trending_keywords(category, keyword_count)
                st.session_state.generated_keywords = keywords
                st.success(f"Generated {len(keywords)} keywords!")
    
    with col2:
        st.write("**Generate Titles**")
        main_keyword = st.text_input("Main Keyword for Titles")
        title_count = st.slider("Number of Titles", 5, 20, 10)
        
        if st.button("📝 Generate Titles") and main_keyword:
            with st.spinner("Generating titles..."):
                titles = keyword_generator.generate_title_suggestions(main_keyword, title_count)
                st.session_state.generated_titles = titles
                st.success(f"Generated {len(titles)} titles!")
    
    # Display generated keywords and titles
    if 'generated_keywords' in st.session_state:
        st.subheader("Generated Keywords:")
        st.write(", ".join(st.session_state.generated_keywords))
        
        if st.button("📋 Copy Keywords to Manual Input"):
            st.session_state.copy_keywords = True
            st.success("Keywords copied! Refresh to see them in manual input.")
    
    if 'generated_titles' in st.session_state:
        st.subheader("Generated Titles:")
        for i, title in enumerate(st.session_state.generated_titles, 1):
            st.write(f"{i}. {title}")
        
        if st.button("📋 Copy Titles to Manual Input"):
            st.session_state.copy_titles = True
            st.success("Titles copied! Refresh to see them in manual input.")

def show_domain_seo_settings(domain, domain_panel, multi_domain_manager):
    """Show SEO settings for domain"""
    st.subheader("🔍 SEO Settings")
    
    settings = domain_panel['settings']
    seo_settings = settings.get('seo_settings', {})
    
    with st.form("seo_settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            auto_meta = st.checkbox("Auto Meta Generation", value=seo_settings.get('auto_meta_generation', True))
            schema_markup = st.checkbox("Schema Markup", value=seo_settings.get('schema_markup', True))
            keyword_optimization = st.checkbox("Keyword Optimization", value=seo_settings.get('keyword_optimization', True))
        
        with col2:
            sitemap_auto = st.checkbox("Auto Sitemap Update", value=seo_settings.get('sitemap_auto_update', True))
            robots_txt = st.checkbox("Generate Robots.txt", value=seo_settings.get('robots_txt', True))
            
        if st.form_submit_button("💾 Save SEO Settings"):
            updates = {
                'seo_settings': {
                    'auto_meta_generation': auto_meta,
                    'schema_markup': schema_markup,
                    'sitemap_auto_update': sitemap_auto,
                    'robots_txt': robots_txt,
                    'keyword_optimization': keyword_optimization
                }
            }
            
            result = multi_domain_manager.update_domain_settings(domain, updates)
            if result.get('success'):
                st.success("SEO settings updated successfully!")
                st.rerun()
            else:
                st.error(f"Failed to update settings: {result.get('error')}")

def show_domain_feed_settings(domain, domain_panel, multi_domain_manager):
    """Show feed settings for domain"""
    st.subheader("📡 Feed Management")
    
    settings = domain_panel['settings']
    
    with st.form("feed_settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            feed_enabled = st.checkbox("Enable RSS Feed", value=settings.get('feed_enabled', True))
            auto_feed_update = st.checkbox("Auto Feed Update", value=settings.get('auto_feed_update', True))
        
        with col2:
            feed_format = st.selectbox("Feed Format", ["RSS 2.0", "Atom 1.0"], 
                                     index=0 if settings.get('feed_format', 'RSS 2.0') == 'RSS 2.0' else 1)
            max_feed_items = st.slider("Max Feed Items", 10, 100, value=settings.get('max_feed_items', 50))
        
        if st.form_submit_button("💾 Save Feed Settings"):
            updates = {
                'feed_enabled': feed_enabled,
                'auto_feed_update': auto_feed_update,
                'feed_format': feed_format,
                'max_feed_items': max_feed_items
            }
            
            result = multi_domain_manager.update_domain_settings(domain, updates)
            if result.get('success'):
                st.success("Feed settings updated successfully!")
                st.rerun()
            else:
                st.error(f"Failed to update settings: {result.get('error')}")

def show_domain_cloudflare_settings(domain, domain_panel, multi_domain_manager):
    """Show Cloudflare settings for domain"""
    st.subheader("☁️ Cloudflare Integration")
    
    settings = domain_panel['settings']
    cloudflare_settings = settings.get('cloudflare', {})
    
    with st.form("cloudflare_settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            enabled = st.checkbox("Enable Cloudflare Integration", value=cloudflare_settings.get('enabled', False))
            api_key = st.text_input("Cloudflare API Key", value=cloudflare_settings.get('api_key', ''), type="password")
        
        with col2:
            zone_id = st.text_input("Zone ID", value=cloudflare_settings.get('zone_id', ''))
            auto_deploy = st.checkbox("Auto Deploy", value=cloudflare_settings.get('auto_deploy', False))
        
        if st.form_submit_button("💾 Save Cloudflare Settings"):
            updates = {
                'cloudflare': {
                    'enabled': enabled,
                    'api_key': api_key,
                    'zone_id': zone_id,
                    'auto_deploy': auto_deploy
                }
            }
            
            result = multi_domain_manager.update_domain_settings(domain, updates)
            if result.get('success'):
                st.success("Cloudflare settings updated successfully!")
                st.rerun()
            else:
                st.error(f"Failed to update settings: {result.get('error')}")

def show_domain_adsense_settings(domain, domain_panel, adsense_manager):
    """Show AdSense settings for domain with widget management"""
    st.subheader("💰 AdSense Widget Management")
    
    # Get current AdSense configuration
    adsense_config = adsense_manager.get_domain_adsense_config(domain)
    
    # AdSense general settings
    st.markdown("### 🔧 General AdSense Settings")
    
    with st.form("adsense_general_settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            adsense_enabled = st.checkbox("Enable AdSense", value=adsense_config.get('adsense_enabled', False))
            publisher_id = st.text_input("Publisher ID (ca-pub-xxxxxxxxx)", 
                                       value=adsense_config.get('publisher_id', ''),
                                       placeholder="ca-pub-1234567890123456")
        
        with col2:
            auto_ads_enabled = st.checkbox("Enable Auto Ads", value=adsense_config.get('auto_ads', {}).get('enabled', False))
            if auto_ads_enabled:
                auto_ads_code = st.text_area("Auto Ads Code (Optional)", 
                                           value=adsense_config.get('auto_ads', {}).get('code', ''),
                                           placeholder="Custom Auto Ads code...")
            else:
                auto_ads_code = ""
        
        if st.form_submit_button("💾 Save General Settings", use_container_width=True):
            adsense_config['adsense_enabled'] = adsense_enabled
            adsense_config['publisher_id'] = publisher_id
            adsense_config['auto_ads'] = {
                'enabled': auto_ads_enabled,
                'code': auto_ads_code
            }
            
            result = adsense_manager.save_domain_adsense_config(domain, adsense_config)
            if result.get('success'):
                st.success("✅ General AdSense settings saved!")
                st.rerun()
            else:
                st.error(f"❌ {result.get('error')}")
    
    # Widget management section
    st.markdown("### 🎯 Ad Widget Configuration")
    
    # Get available widget positions
    widget_positions = adsense_manager.get_widget_positions()
    
    # Show widget configuration in tabs
    widget_tabs = st.tabs([pos['name'] for pos in widget_positions])
    
    for i, (tab, widget_pos) in enumerate(zip(widget_tabs, widget_positions)):
        with tab:
            widget_id = widget_pos['id']
            widget_config = adsense_config['widgets'].get(widget_id, {})
            
            st.markdown(f"**{widget_pos['description']}**")
            st.markdown(f"*Recommended size: {widget_pos['recommended_size']}*")
            
            with st.form(f"widget_{widget_id}_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    widget_enabled = st.checkbox("Enable Widget", 
                                                value=widget_config.get('enabled', False),
                                                key=f"enable_{widget_id}")
                    
                    if widget_enabled:
                        ad_unit_id = st.text_input("Ad Unit ID", 
                                                 value=widget_config.get('ad_unit_id', ''),
                                                 key=f"unit_{widget_id}",
                                                 placeholder="1234567890")
                        
                        size = st.selectbox("Ad Size", 
                                          widget_pos['sizes'],
                                          index=widget_pos['sizes'].index(widget_config.get('size', widget_pos['recommended_size'])) 
                                          if widget_config.get('size') in widget_pos['sizes'] else 0,
                                          key=f"size_{widget_id}")
                    else:
                        ad_unit_id = ""
                        size = widget_pos['recommended_size']
                
                with col2:
                    if widget_enabled:
                        st.markdown("**Custom Ad Code (Optional):**")
                        custom_code = st.text_area("Custom Code", 
                                                 value=widget_config.get('code', ''),
                                                 key=f"code_{widget_id}",
                                                 height=100,
                                                 placeholder="Paste your custom AdSense code here...")
                        
                        # Show preview of generated code if using standard settings
                        if ad_unit_id and not custom_code:
                            st.markdown("**Generated Code Preview:**")
                            preview_code = adsense_manager.generate_ad_code(widget_id, ad_unit_id, size)
                            st.code(preview_code[:200] + "..." if len(preview_code) > 200 else preview_code, language="html")
                    else:
                        custom_code = ""
                        st.info("Enable widget to configure ad settings")
                
                if st.form_submit_button(f"💾 Save {widget_pos['name']}", use_container_width=True):
                    # Update widget configuration
                    adsense_config['widgets'][widget_id] = {
                        'enabled': widget_enabled,
                        'ad_unit_id': ad_unit_id,
                        'size': size,
                        'code': custom_code
                    }
                    
                    result = adsense_manager.save_domain_adsense_config(domain, adsense_config)
                    if result.get('success'):
                        st.success(f"✅ {widget_pos['name']} settings saved!")
                        st.rerun()
                    else:
                        st.error(f"❌ {result.get('error')}")
    
    # Ads.txt management
    st.markdown("### 📄 Ads.txt Management")
    
    with st.form("ads_txt_form"):
        st.markdown("**Add ads.txt entries for this domain:**")
        
        current_entries = '\n'.join(adsense_config.get('ads_txt_entries', []))
        ads_txt_entries = st.text_area("Ads.txt Entries", 
                                     value=current_entries,
                                     height=120,
                                     placeholder="google.com, pub-1234567890123456, DIRECT, f08c47fec0942fa0")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("💾 Save Ads.txt", use_container_width=True):
                entries_list = [entry.strip() for entry in ads_txt_entries.split('\n') if entry.strip()]
                adsense_config['ads_txt_entries'] = entries_list
                
                result = adsense_manager.save_domain_adsense_config(domain, adsense_config)
                if result.get('success'):
                    st.success("✅ Ads.txt entries saved!")
                    st.rerun()
                else:
                    st.error(f"❌ {result.get('error')}")
        
        with col2:
            if st.form_submit_button("🔄 Update Global Ads.txt", use_container_width=True):
                result = adsense_manager.update_global_ads_txt()
                if result.get('success'):
                    st.success(f"✅ Global ads.txt updated with {result.get('entries_count', 0)} entries!")
                else:
                    st.error(f"❌ {result.get('error')}")
    
    # AdSense statistics and export
    st.markdown("### 📊 AdSense Overview")
    
    stats = adsense_manager.get_adsense_stats(domain)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Widgets", stats['total_widgets'])
    with col2:
        st.metric("Enabled Widgets", stats['enabled_widgets'])
    with col3:
        status = "✅ Enabled" if stats['adsense_enabled'] else "❌ Disabled"
        st.metric("AdSense Status", status)
    with col4:
        auto_status = "✅ On" if stats['auto_ads_enabled'] else "❌ Off"
        st.metric("Auto Ads", auto_status)
    
    # Export functionality
    st.markdown("### 🚀 Export Ad Codes")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Export All Ad Codes", use_container_width=True):
            all_codes = adsense_manager.export_domain_ads(domain)
            st.code(all_codes, language="html")
    
    with col2:
        if st.button("📊 View AdSense Stats", use_container_width=True):
            st.json(stats)

def show_domain_analytics(domain, multi_domain_manager):
    """Show domain analytics"""
    st.subheader(f"📊 Analytics for {domain}")
    
    # Get analytics data
    analytics = multi_domain_manager.get_domain_analytics(domain)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Page Views", analytics.get('page_views', 0))
    with col2:
        st.metric("Unique Visitors", analytics.get('unique_visitors', 0))
    with col3:
        st.metric("Bounce Rate", f"{analytics.get('bounce_rate', 0):.1f}%")
    with col4:
        st.metric("Avg Session Duration", f"{analytics.get('avg_session_duration', 0):.1f}min")
    
    # SEO Performance
    st.subheader("🔍 SEO Performance")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("SEO Score", f"{analytics.get('seo_score', 0)}/100")
    with col2:
        st.metric("Indexed Pages", analytics.get('indexed_pages', 0))
    with col3:
        st.metric("Backlinks", analytics.get('backlinks', 0))
    
    # Traffic Sources
    st.subheader("📈 Traffic Sources")
    traffic_sources = analytics.get('traffic_sources', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Organic Search:** ", traffic_sources.get('organic', 0))
        st.write("**Direct:** ", traffic_sources.get('direct', 0))
    
    with col2:
        st.write("**Social Media:** ", traffic_sources.get('social', 0))
        st.write("**Referral:** ", traffic_sources.get('referral', 0))
    
    # Article Performance
    st.subheader("📝 Article Performance")
    articles = analytics.get('top_articles', [])
    
    if articles:
        for i, article in enumerate(articles[:5], 1):
            st.write(f"{i}. **{article.get('title', 'Unknown')}** - {article.get('views', 0)} views")
    else:
        st.info("No article data available yet.")

def show_multi_domain_manager(multi_domain_manager):
    st.header("🌐 Multi-Domain Manager")
    
    # Professional cPanel-like CSS
    st.markdown("""
    <style>
    .domain-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .domain-card:hover {
        transform: translateY(-2px);
    }
    .domain-title {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .domain-stats {
        display: flex;
        justify-content: space-between;
        margin: 10px 0;
    }
    .stat-item {
        text-align: center;
        flex: 1;
    }
    .stat-value {
        font-size: 1.5em;
        font-weight: bold;
        color: #fff;
    }
    .stat-label {
        font-size: 0.8em;
        opacity: 0.9;
    }
    .action-buttons {
        display: flex;
        gap: 10px;
        margin-top: 15px;
    }
    .cpanel-header {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with cPanel-like styling
    st.markdown("""
    <div class="cpanel-header">
        <h2>🌐 Multi-Domain Control Panel</h2>
        <p>Manage all your domains from one professional interface</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get all domains in grid view
    domains = multi_domain_manager.get_domain_grid_view()
    
    if not domains or (len(domains) == 1 and 'error' in domains[0]):
        st.info("No domains managed yet. Create a domain panel to get started!")
        
        # Create new domain panel with professional styling
        st.subheader("🚀 Create New Domain Panel")
        
        with st.form("create_domain_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_domain = st.text_input("Domain Name", placeholder="example.com")
                domain_title = st.text_input("Site Title", placeholder="My Awesome Website")
                template = st.selectbox("Template", ["default", "professional", "minimal"])
            
            with col2:
                category = st.selectbox("Category", ["Blog", "Business", "Portfolio", "News", "Technology", "Health"])
                description = st.text_area("Description", placeholder="Brief description of your website")
                auto_posting = st.checkbox("Enable Auto Posting", value=False)
            
            submit_button = st.form_submit_button("🚀 Create Domain Panel", use_container_width=True)
            
            if submit_button:
                if new_domain and domain_title:
                    result = multi_domain_manager.create_domain_panel(new_domain, {
                        'title': domain_title,
                        'template': template,
                        'category': category,
                        'description': description,
                        'auto_posting': {'enabled': auto_posting}
                    })
                    
                    if result.get('success'):
                        st.success(f"✅ Domain panel created for {new_domain}")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to create domain panel: {result.get('error', 'Unknown error')}")
                else:
                    st.warning("Please enter domain name and title")
        
        return
    
    # Show domains in professional grid
    st.subheader("📊 Domain Overview")
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    total_domains = len(domains)
    active_domains = sum(1 for d in domains if d.get('status') == 'active')
    auto_posting_domains = sum(1 for d in domains if d.get('auto_posting', False))
    avg_seo_score = sum(d.get('seo_score', 0) for d in domains) / total_domains if total_domains > 0 else 0
    
    with col1:
        st.metric("Total Domains", total_domains)
    with col2:
        st.metric("Active Domains", active_domains)
    with col3:
        st.metric("Auto Posting", auto_posting_domains)
    with col4:
        st.metric("Avg SEO Score", f"{avg_seo_score:.1f}/100")
    
    # Display domains in professional grid
    st.subheader("🎛️ Domain Control Panel")
    
    # Create grid layout
    cols = st.columns(2)
    
    for i, domain_data in enumerate(domains):
        if 'error' in domain_data:
            continue
            
        col = cols[i % 2]
        
        with col:
            # Professional domain card
            st.markdown(f"""
            <div class="domain-card">
                <div class="domain-title">{domain_data['domain']}</div>
                <div style="margin-bottom: 15px;">
                    <strong>Title:</strong> {domain_data['title']}<br>
                    <strong>Template:</strong> {domain_data['template']}<br>
                    <strong>Status:</strong> {'🟢 Active' if domain_data['status'] == 'active' else '🔴 Inactive'}
                </div>
                
                <div class="domain-stats">
                    <div class="stat-item">
                        <div class="stat-value">{domain_data['seo_score']}</div>
                        <div class="stat-label">SEO Score</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{domain_data['performance_score']}</div>
                        <div class="stat-label">Performance</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{domain_data['article_count']}</div>
                        <div class="stat-label">Articles</div>
                    </div>
                </div>
                
                <div style="margin-top: 10px;">
                    <strong>Auto Posting:</strong> {'✅ Enabled' if domain_data['auto_posting'] else '❌ Disabled'}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⚙️ Settings", key=f"settings_{domain_data['domain']}", use_container_width=True):
                    st.session_state.selected_domain = domain_data['domain']
                    st.rerun()
            
            with col2:
                if st.button("📊 Analytics", key=f"analytics_{domain_data['domain']}", use_container_width=True):
                    st.session_state.analytics_domain = domain_data['domain']
                    st.rerun()
            
            with col3:
                if st.button("🚀 Manage", key=f"manage_{domain_data['domain']}", use_container_width=True):
                    st.session_state.manage_domain = domain_data['domain']
                    st.rerun()
    
    # Add new domain button
    st.markdown("---")
    if st.button("➕ Add New Domain", use_container_width=True, type="primary"):
        st.session_state.show_add_domain = True
        st.rerun()
    
    # Show domain settings modal if selected
    if hasattr(st.session_state, 'selected_domain') and st.session_state.selected_domain:
        show_domain_settings_modal(multi_domain_manager, st.session_state.selected_domain)
    
    # Show analytics modal if selected
    if hasattr(st.session_state, 'analytics_domain') and st.session_state.analytics_domain:
        show_domain_analytics_modal(multi_domain_manager, st.session_state.analytics_domain)
    
def show_domain_settings_modal(multi_domain_manager, domain):
    st.subheader(f"⚙️ Settings for {domain}")
    
    # Get current settings
    panel_data = multi_domain_manager.get_domain_panel(domain)
    
    if 'error' in panel_data:
        st.error(f"Error loading settings: {panel_data['error']}")
        return
    
    settings = panel_data['settings']
    
    # Professional settings form
    with st.form("domain_settings_form"):
        st.write("### Auto Posting Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            auto_posting_enabled = st.checkbox(
                "Enable Auto Posting", 
                value=settings.get('auto_posting', {}).get('enabled', False)
            )
            
            interval_hours = st.slider(
                "Posting Interval (hours)", 
                min_value=1, 
                max_value=24, 
                value=settings.get('auto_posting', {}).get('interval_hours', 6)
            )
        
        with col2:
            max_posts_per_day = st.slider(
                "Max Posts per Day", 
                min_value=1, 
                max_value=20, 
                value=settings.get('auto_posting', {}).get('max_posts_per_day', 4)
            )
            
            article_length = st.slider(
                "Article Length (words)", 
                min_value=500, 
                max_value=3000, 
                value=settings.get('auto_posting', {}).get('article_length', 1000)
            )
        
        st.write("### Performance & SEO Settings")
        col1, col2 = st.columns(2)
        
        with col1:
            cache_enabled = st.checkbox(
                "Enable Caching", 
                value=settings.get('performance', {}).get('cache_enabled', True)
            )
            
            lazy_loading = st.checkbox(
                "Enable Lazy Loading", 
                value=settings.get('performance', {}).get('lazy_loading', True)
            )
        
        with col2:
            image_optimization = st.checkbox(
                "Enable Image Optimization", 
                value=settings.get('performance', {}).get('image_optimization', True)
            )
            
            minification = st.checkbox(
                "Enable Minification", 
                value=settings.get('performance', {}).get('minification', True)
            )
        
        # Submit button
        if st.form_submit_button("💾 Save Settings", use_container_width=True):
            updates = {
                'auto_posting': {
                    'enabled': auto_posting_enabled,
                    'interval_hours': interval_hours,
                    'max_posts_per_day': max_posts_per_day,
                    'article_length': article_length,
                    'images_per_article': 3,
                    'seo_optimization': True
                },
                'performance': {
                    'cache_enabled': cache_enabled,
                    'lazy_loading': lazy_loading,
                    'image_optimization': image_optimization,
                    'minification': minification
                }
            }
            
            result = multi_domain_manager.update_domain_settings(domain, updates)
            
            if result.get('success'):
                st.success("✅ Settings updated successfully!")
                st.session_state.selected_domain = None
                st.rerun()
            else:
                st.error(f"❌ Failed to update settings: {result.get('error', 'Unknown error')}")
    
    # Additional actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤖 Generate Robots.txt"):
            robots_content = multi_domain_manager.generate_domain_robots_txt(domain)
            st.text_area("robots.txt Content", robots_content, height=200)
    
    with col2:
        if st.button("🔄 Optimize Performance"):
            result = multi_domain_manager.optimize_domain_performance(domain)
            if result.get('success'):
                st.success("✅ Performance optimized!")
                st.write("**Optimizations Applied:**")
                for opt in result.get('optimizations', []):
                    st.write(f"- {opt}")
            else:
                st.error(f"❌ {result.get('error', 'Unknown error')}")
    
    # Close button
    if st.button("❌ Close Settings"):
        st.session_state.selected_domain = None
        st.rerun()

def show_domain_analytics_modal(multi_domain_manager, domain):
    st.subheader(f"📊 Analytics for {domain}")
    
    analytics_data = multi_domain_manager.get_domain_analytics(domain)
    
    if 'error' in analytics_data:
        st.error(f"Error loading analytics: {analytics_data['error']}")
        return
    
    analytics = analytics_data.get('analytics', {})
    
    # Display metrics in professional cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Page Views", analytics.get('page_views', 0))
    
    with col2:
        st.metric("Unique Visitors", analytics.get('unique_visitors', 0))
    
    with col3:
        st.metric("Bounce Rate", f"{analytics.get('bounce_rate', 0)}%")
    
    with col4:
        st.metric("Avg Session Duration", f"{analytics.get('average_session_duration', 0)}s")
    
    # Performance metrics
    performance_metrics = multi_domain_manager.get_performance_metrics(domain)
    
    if 'error' not in performance_metrics:
        st.subheader("Performance Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Page Load Time", f"{performance_metrics.get('page_load_time', 0)}s")
        
        with col2:
            st.metric("Cache Hit Ratio", f"{performance_metrics.get('cache_hit_ratio', 0)*100:.1f}%")
        
        with col3:
            st.metric("SEO Score", f"{performance_metrics.get('seo_score', 0)}/100")
    
    # Close button
    if st.button("❌ Close Analytics"):
        st.session_state.analytics_domain = None
        st.rerun()

def show_api_settings(api_manager, pixel_api):
    """Enhanced API settings with Pixel API support"""
    st.header("🔐 API Settings")
    
    # Custom CSS for cPanel-like appearance
    st.markdown("""
    <style>
    .api-status-card {
        background: #f0f2f6;
        border: 1px solid #e1e5e9;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .api-key-input {
        background: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 8px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get API status
    api_status = api_manager.get_api_status()
    
    # API Status Overview
    st.subheader("📊 API Status Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Keys", api_status['total_keys'])
    
    with col2:
        st.metric("Active Keys", len(api_status['available_keys']))
    
    with col3:
        gemini_status = "✅ Connected" if api_status['gemini']['success'] else "❌ Disconnected"
        st.metric("Gemini Status", gemini_status)
    
    # Gemini API Configuration
    st.subheader("🤖 Gemini AI Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        current_gemini_key = api_manager.get_api_key('GEMINI_API_KEY') or ''
        new_gemini_key = st.text_input(
            "Gemini API Key",
            value=current_gemini_key[:20] + "..." if len(current_gemini_key) > 20 else current_gemini_key,
            type="password",
            help="Get your API key from Google AI Studio"
        )
        
        if st.button("Update Gemini API Key"):
            if new_gemini_key and not new_gemini_key.endswith("..."):
                if api_manager.update_api_key('GEMINI_API_KEY', new_gemini_key):
                    st.success("✅ Gemini API key updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update Gemini API key")
            else:
                st.warning("Please enter a valid API key")
    
    with col2:
        if st.button("Test Gemini API"):
            test_result = api_manager.test_gemini_api()
            if test_result['success']:
                st.success("✅ Gemini API working!")
            else:
                st.error(f"❌ {test_result['error']}")
    
    # Bing API Configuration
    st.subheader("🖼️ Bing Image Search Configuration")
    
    bing_keys = api_manager.get_bing_api_keys()
    
    for i in range(1, 4):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            current_key = api_manager.get_api_key(f'BING_API_KEY_{i}') or ''
            new_key = st.text_input(
                f"Bing API Key {i}",
                value=current_key[:20] + "..." if len(current_key) > 20 else current_key,
                type="password",
                help="Get your API key from Microsoft Azure Cognitive Services"
            )
            
            if st.button(f"Update Bing API Key {i}"):
                if new_key and not new_key.endswith("..."):
                    if api_manager.update_api_key(f'BING_API_KEY_{i}', new_key):
                        st.success(f"✅ Bing API key {i} updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to update Bing API key {i}")
                else:
                    st.warning("Please enter a valid API key")
        
        with col2:
            if st.button(f"Test Bing API {i}"):
                test_result = api_manager.test_bing_api()
                if test_result['success']:
                    st.success("✅ Bing API working!")
                else:
                    st.error(f"❌ {test_result['error']}")
    
    # API Usage Guidelines
    st.subheader("📋 API Usage Guidelines")
    
    st.markdown("""
    **Gemini API:**
    - Free tier: 15 requests per minute
    - Used for: Article generation, keyword research, SEO optimization
    - Get your key: [Google AI Studio](https://ai.google.dev/)
    
    **Bing Image Search API:**
    - Free tier: 1,000 transactions per month
    - Used for: Image search and optimization
    - Get your key: [Microsoft Azure Portal](https://portal.azure.com/)
    
    **API Key Security:**
    - Keys are stored locally in `apikey.txt`
    - Never share your API keys publicly
    - Rotate keys regularly for security
    """)
    
    # Load API keys from file
    if st.button("🔄 Reload API Keys from File"):
        api_manager.load_api_keys()
        st.success("✅ API keys reloaded from apikey.txt")
        st.rerun()
    
    # Show current API file content
    with st.expander("View apikey.txt Content"):
        try:
            with open("apikey.txt", "r") as f:
                content = f.read()
                st.code(content, language="text")
        except FileNotFoundError:
            st.warning("apikey.txt file not found. It will be created automatically.")
        except Exception as e:
            st.error(f"Error reading apikey.txt: {str(e)}")

def show_auto_content_manager(auto_content_manager, gemini_ai, bing_image_scraper, keyword_generator, article_formatter, domain_config_manager):
    """Enhanced auto content manager with domain-specific configuration"""
    st.header("🤖 Auto Content Manager")
    
    # Domain selection
    st.subheader("📂 Domain Selection")
    available_domains = domain_config_manager.get_all_domain_configs()
    
    if not available_domains:
        st.warning("No domains configured. Please add a domain first.")
        return
    
    selected_domain = st.selectbox("Select Domain", available_domains)
    
    if selected_domain:
        # Load domain configuration
        domain_config = domain_config_manager.load_domain_config(selected_domain)
        domain_keywords = domain_config_manager.load_domain_keywords(selected_domain)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Domain:** {selected_domain}")
            st.info(f"**Category:** {domain_config.get('category', 'General')}")
            st.info(f"**Keywords:** {len(domain_keywords)} available")
        
        with col2:
            st.info(f"**Template:** {domain_config.get('template', 'default')}")
            st.info(f"**Auto Posting:** {'✅ Enabled' if domain_config.get('auto_posting', {}).get('enabled', False) else '❌ Disabled'}")
            st.info(f"**Status:** {domain_config.get('status', 'active')}")
        
        # Keyword management
        st.subheader("🔑 Keyword Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Generate Keywords for Domain"):
                with st.spinner("Generating keywords..."):
                    result = keyword_generator.generate_keywords_for_domain(
                        selected_domain, 
                        domain_config.get('category', 'Business'), 
                        20
                    )
                    
                    if result.get('success'):
                        st.success(f"Generated {result['count']} keywords for {selected_domain}")
                        st.info(f"Keywords saved to: {result['file_path']}")
                        
                        # Show generated keywords
                        st.write("Generated Keywords:")
                        for keyword in result['keywords']:
                            st.write(f"• {keyword}")
                        
                        st.rerun()
                    else:
                        st.error(f"Failed to generate keywords: {result.get('error', 'Unknown error')}")
        
        with col2:
            # Manual keyword addition
            manual_keywords = st.text_area("Add Manual Keywords (one per line)", height=100)
            if st.button("➕ Add Manual Keywords"):
                if manual_keywords:
                    keywords_list = [k.strip() for k in manual_keywords.split('\n') if k.strip()]
                    result = keyword_generator.add_manual_keywords(selected_domain, keywords_list)
                    
                    if result.get('success'):
                        st.success(f"Added {len(result['added_keywords'])} keywords to {selected_domain}")
                        st.rerun()
                    else:
                        st.error(f"Failed to add keywords: {result.get('error', 'Unknown error')}")
        
        # Show existing keywords
        if domain_keywords:
            with st.expander(f"📋 Current Keywords ({len(domain_keywords)})"):
                for i, keyword in enumerate(domain_keywords, 1):
                    st.write(f"{i}. {keyword}")
        
        # Article generation
        st.subheader("📄 Article Generation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Use existing keywords or manual input
            use_existing_keywords = st.checkbox("Use Domain Keywords", value=True)
            
            if use_existing_keywords and domain_keywords:
                selected_keyword = st.selectbox("Select Keyword", domain_keywords)
                topic = selected_keyword
            else:
                topic = st.text_input("Custom Topic/Keyword")
                
            article_length = st.slider("Article Length (words)", 500, 3000, 1000)
            
        with col2:
            include_images = st.checkbox("Include Images", value=True)
            image_count = st.slider("Images per Article", 1, 5, 3)
            seo_optimized = st.checkbox("SEO Optimized", value=True)
            bullet_formatting = st.checkbox("Bullet Point Formatting", value=True)
        
        if st.button("🚀 Generate Article"):
            if topic:
                with st.spinner("Generating article with bullet formatting..."):
                    # Generate article content with bullet formatting
                    article_content = f"""
                    {topic}
                    
                    Comprehensive Guide to {topic}:
                    
                    Key Benefits:
                    • Enhanced productivity and efficiency
                    • Improved results and outcomes
                    • Better user experience
                    • Cost-effective solutions
                    • Scalable implementation
                    
                    Implementation Steps:
                    1. Research and planning phase
                    2. Resource gathering and preparation
                    3. Step-by-step execution
                    4. Testing and optimization
                    5. Monitoring and maintenance
                    
                    Best Practices:
                    - Follow industry standards
                    - Use proven methodologies
                    - Focus on user needs
                    - Maintain quality standards
                    - Continuously improve
                    
                    Advanced Techniques:
                    • Leverage automation tools
                    • Use data-driven insights
                    • Implement best practices
                    • Stay updated with trends
                    • Optimize for performance
                    
                    Common Challenges:
                    - Resource limitations
                    - Technical complexity
                    - Time constraints
                    - Budget considerations
                    - Skill requirements
                    
                    Solutions and Tips:
                    1. Start with basics and build up
                    2. Use available tools and resources
                    3. Seek expert guidance when needed
                    4. Plan for scalability
                    5. Monitor progress regularly
                    
                    This comprehensive approach to {topic} will help you achieve better results and maintain competitive advantage.
                    """
                    
                    # Format with bullet points
                    formatted_content = article_formatter.format_article_content(article_content, "html")
                    
                    # Create article data
                    article_data = {
                        'title': topic,
                        'content': formatted_content,
                        'category': domain_config.get('category', 'General'),
                        'keywords': [topic] + (domain_keywords[:4] if domain_keywords else []),
                        'word_count': len(article_content.split()),
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'domain': selected_domain,
                        'formatted': True
                    }
                    
                    # Save article to domain
                    existing_articles = domain_config_manager.load_domain_articles(selected_domain)
                    existing_articles.append(article_data)
                    save_result = domain_config_manager.save_domain_articles(selected_domain, existing_articles)
                    
                    if save_result.get('success'):
                        st.success(f"Article generated and saved for {selected_domain}!")
                        st.info(f"Article saved to: {save_result['file_path']}")
                        
                        # Display generated content
                        st.subheader("📄 Generated Article")
                        st.markdown(article_formatter.add_article_styles(), unsafe_allow_html=True)
                        st.markdown(formatted_content, unsafe_allow_html=True)
                        
                        # Show article stats
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Word Count", article_data['word_count'])
                        with col2:
                            st.metric("Keywords", len(article_data['keywords']))
                        with col3:
                            st.metric("Reading Time", f"{article_data['word_count'] // 200} min")
                    else:
                        st.error(f"Failed to save article: {save_result.get('error', 'Unknown error')}")
            else:
                st.warning("Please enter a topic/keyword")
        
        # Domain articles overview
        st.subheader("📚 Domain Articles")
        
        existing_articles = domain_config_manager.load_domain_articles(selected_domain)
        
        if existing_articles:
            st.write(f"Total articles for {selected_domain}: {len(existing_articles)}")
            
            for i, article in enumerate(existing_articles[-5:], 1):  # Show last 5 articles
                with st.expander(f"Article {i}: {article.get('title', 'Untitled')}"):
                    st.write(f"**Category:** {article.get('category', 'General')}")
                    st.write(f"**Keywords:** {', '.join(article.get('keywords', []))}")
                    st.write(f"**Word Count:** {article.get('word_count', 0)}")
                    st.write(f"**Created:** {article.get('created_at', 'Unknown')}")
                    
                    if article.get('formatted'):
                        st.markdown(article_formatter.add_article_styles(), unsafe_allow_html=True)
                        st.markdown(article.get('content', ''), unsafe_allow_html=True)
                    else:
                        st.write(article.get('content', ''))
        else:
            st.info("No articles generated yet for this domain")
        
        # Bulk generation
        st.subheader("🔄 Bulk Article Generation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            num_articles = st.number_input("Number of Articles", min_value=1, max_value=10, value=3)
            
        with col2:
            use_all_keywords = st.checkbox("Use All Domain Keywords", value=True)
        
        if st.button("🚀 Generate Bulk Articles"):
            if domain_keywords or not use_all_keywords:
                with st.spinner(f"Generating {num_articles} articles..."):
                    keywords_to_use = domain_keywords if use_all_keywords else [keyword_generator.generate_trending_keyword(domain_config.get('category', 'Business')) for _ in range(num_articles)]
                    
                    generated_articles = []
                    
                    for i in range(min(num_articles, len(keywords_to_use))):
                        keyword = keywords_to_use[i]
                        
                        # Generate article content
                        article_content = f"""
                        {keyword}
                        
                        Essential Guide to {keyword}:
                        
                        Key Benefits:
                        • Improved efficiency
                        • Better results
                        • Enhanced productivity
                        • Cost-effective approach
                        
                        Implementation Steps:
                        1. Planning and preparation
                        2. Execution phase
                        3. Monitoring and optimization
                        4. Continuous improvement
                        
                        This guide covers all aspects of {keyword} to help you achieve your goals.
                        """
                        
                        formatted_content = article_formatter.format_article_content(article_content, "html")
                        
                        article_data = {
                            'title': keyword,
                            'content': formatted_content,
                            'category': domain_config.get('category', 'General'),
                            'keywords': [keyword],
                            'word_count': len(article_content.split()),
                            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'domain': selected_domain,
                            'formatted': True
                        }
                        
                        generated_articles.append(article_data)
                    
                    # Save all articles
                    existing_articles = domain_config_manager.load_domain_articles(selected_domain)
                    all_articles = existing_articles + generated_articles
                    save_result = domain_config_manager.save_domain_articles(selected_domain, all_articles)
                    
                    if save_result.get('success'):
                        st.success(f"Generated {len(generated_articles)} articles for {selected_domain}!")
                        st.info(f"Articles saved to: {save_result['file_path']}")
                        st.rerun()
                    else:
                        st.error(f"Failed to save articles: {save_result.get('error', 'Unknown error')}")
            else:
                st.warning("No keywords available. Please generate keywords first.")

if __name__ == "__main__":
    main()
