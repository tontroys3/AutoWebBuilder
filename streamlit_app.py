"""
Streamlit App Entry Point for Deployment
Auto Website Builder - Professional Website Management System
"""

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

# Import the main function directly
from app import main

# Run the main application
main()