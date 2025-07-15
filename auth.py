import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta

class AuthManager:
    def __init__(self):
        self.users_file = "users.json"
        self.session_timeout = 3600  # 1 hour
        self.default_users = {
            "user": {
                "password": self.hash_password("user@123"),
                "role": "admin",
                "created_at": datetime.now().isoformat(),
                "last_login": None
            }
        }
        self.ensure_users_file()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def ensure_users_file(self):
        """Create users file if it doesn't exist"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump(self.default_users, f, indent=2)
    
    def load_users(self) -> dict:
        """Load users from file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return self.default_users
    
    def save_users(self, users: dict):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user"""
        users = self.load_users()
        
        if username in users:
            stored_password = users[username]["password"]
            if self.hash_password(password) == stored_password:
                # Update last login
                users[username]["last_login"] = datetime.now().isoformat()
                self.save_users(users)
                return True
        return False
    
    def is_session_valid(self) -> bool:
        """Check if current session is valid"""
        if 'authenticated' not in st.session_state:
            return False
        
        if 'login_time' not in st.session_state:
            return False
        
        login_time = datetime.fromisoformat(st.session_state.login_time)
        if datetime.now() - login_time > timedelta(seconds=self.session_timeout):
            return False
        
        return st.session_state.authenticated
    
    def login(self, username: str, password: str) -> bool:
        """Login user"""
        if self.authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.login_time = datetime.now().isoformat()
            return True
        return False
    
    def logout(self):
        """Logout user"""
        st.session_state.authenticated = False
        if 'username' in st.session_state:
            del st.session_state.username
        if 'login_time' in st.session_state:
            del st.session_state.login_time
    
    def show_login_form(self):
        """Show login form"""
        # Center the entire page content
        st.markdown("""
        <style>
        .main > div {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .login-container {
            max-width: 450px;
            margin: 8vh auto;
            padding: 0;
            position: relative;
        }
        .login-card {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .login-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 30px 30px;
            text-align: center;
            color: white;
            position: relative;
        }
        .login-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.3;
        }
        .login-header > * {
            position: relative;
            z-index: 1;
        }
        .login-title {
            font-size: 2.2em;
            font-weight: 700;
            margin: 0 0 8px;
            letter-spacing: -0.5px;
        }
        .login-subtitle {
            font-size: 1em;
            opacity: 0.9;
            margin: 0;
            font-weight: 300;
        }
        .login-body {
            padding: 40px 30px;
            background: #fafafa;
        }
        .login-form {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }
        .stTextInput > div > div > input {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            padding: 16px 20px;
            font-size: 1em;
            transition: all 0.3s ease;
            color: #495057;
        }
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .stTextInput > label {
            font-weight: 600;
            color: #495057;
            margin-bottom: 8px;
        }
        .login-button {
            margin-top: 25px;
        }
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 16px 24px;
            font-size: 1.1em;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        .stButton > button:active {
            transform: translateY(0);
        }
        .login-footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .credentials-info {
            color: #6c757d;
            font-size: 0.9em;
            line-height: 1.5;
        }
        .credentials-info strong {
            color: #495057;
            background: #e9ecef;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
        }
        /* Hide Streamlit elements */
        .stDeployButton {display: none;}
        footer {display: none;}
        .stDecoration {display: none;}
        header {display: none;}
        </style>
        """, unsafe_allow_html=True)
        
        # Create centered container
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="login-container">
                <div class="login-card">
                    <div class="login-header">
                        <div class="login-title">⚡ Worker Panel</div>
                        <div class="login-subtitle">Website Management System</div>
                    </div>
                    <div class="login-body">
                        <div class="login-form">
            """, unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("👤 Username", placeholder="Enter your username", label_visibility="visible")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", label_visibility="visible")
                
                st.markdown('<div class="login-button">', unsafe_allow_html=True)
                login_button = st.form_submit_button("Sign In", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if login_button:
                    if username and password:
                        if self.login(username, password):
                            st.success("Welcome! Redirecting to dashboard...")
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please try again.")
                    else:
                        st.warning("Please fill in all fields.")
            
            st.markdown("""
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Default credentials info
            st.markdown("""
            <div class="login-footer">
                <div class="credentials-info">
                    Default Access:<br>
                    Username: <strong>user</strong><br>
                    Password: <strong>user@123</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def show_logout_button(self):
        """Show logout button in sidebar"""
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            self.logout()
            st.rerun()
    
    def get_current_user(self) -> str:
        """Get current logged in user"""
        return st.session_state.get('username', 'Unknown')
    
    def change_password(self, username: str, old_password: str, new_password: str) -> dict:
        """Change user password"""
        users = self.load_users()
        
        if username not in users:
            return {'success': False, 'error': 'User not found'}
        
        # Verify old password
        if self.hash_password(old_password) != users[username]["password"]:
            return {'success': False, 'error': 'Current password is incorrect'}
        
        # Validate new password
        if len(new_password) < 6:
            return {'success': False, 'error': 'New password must be at least 6 characters'}
        
        # Update password
        users[username]["password"] = self.hash_password(new_password)
        users[username]["password_changed_at"] = datetime.now().isoformat()
        
        self.save_users(users)
        return {'success': True, 'message': 'Password changed successfully'}
    
    def add_user(self, username: str, password: str, role: str = "user") -> dict:
        """Add new user"""
        users = self.load_users()
        
        # Validate input
        if not username or not password:
            return {'success': False, 'error': 'Username and password are required'}
        
        if len(username) < 3:
            return {'success': False, 'error': 'Username must be at least 3 characters'}
        
        if len(password) < 6:
            return {'success': False, 'error': 'Password must be at least 6 characters'}
        
        # Check if user already exists
        if username in users:
            return {'success': False, 'error': 'Username already exists'}
        
        # Add new user
        users[username] = {
            "password": self.hash_password(password),
            "role": role,
            "created_at": datetime.now().isoformat(),
            "created_by": self.get_current_user(),
            "last_login": None
        }
        
        self.save_users(users)
        return {'success': True, 'message': f'User {username} added successfully'}
    
    def delete_user(self, username: str) -> dict:
        """Delete user"""
        users = self.load_users()
        current_user = self.get_current_user()
        
        if username not in users:
            return {'success': False, 'error': 'User not found'}
        
        if username == current_user:
            return {'success': False, 'error': 'Cannot delete your own account'}
        
        if username == "user":  # Protect default admin
            return {'success': False, 'error': 'Cannot delete default admin user'}
        
        del users[username]
        self.save_users(users)
        return {'success': True, 'message': f'User {username} deleted successfully'}
    
    def get_all_users(self) -> dict:
        """Get all users with basic info"""
        users = self.load_users()
        user_info = {}
        
        for username, data in users.items():
            user_info[username] = {
                'role': data.get('role', 'user'),
                'created_at': data.get('created_at', 'Unknown'),
                'last_login': data.get('last_login', 'Never'),
                'created_by': data.get('created_by', 'System')
            }
        
        return user_info
    
    def show_user_management_panel(self):
        """Show user management panel in sidebar"""
        if not self.is_session_valid():
            return
        
        current_user = self.get_current_user()
        users = self.get_all_users()
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("👥 User Management")
        
        # Change Password Section
        with st.sidebar.expander("🔑 Change Password", expanded=False):
            with st.form("change_password_form"):
                old_password = st.text_input("Current Password", type="password", key="old_pass")
                new_password = st.text_input("New Password", type="password", key="new_pass")
                confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pass")
                
                if st.form_submit_button("Change Password"):
                    if not old_password or not new_password or not confirm_password:
                        st.error("All fields are required")
                    elif new_password != confirm_password:
                        st.error("New passwords do not match")
                    else:
                        result = self.change_password(current_user, old_password, new_password)
                        if result['success']:
                            st.success(result['message'])
                        else:
                            st.error(result['error'])
        
        # Add User Section (only for admin role)
        current_user_role = users.get(current_user, {}).get('role', 'user')
        if current_user_role == 'admin':
            with st.sidebar.expander("➕ Add New User", expanded=False):
                with st.form("add_user_form"):
                    new_username = st.text_input("Username", key="new_username")
                    new_user_password = st.text_input("Password", type="password", key="new_user_pass")
                    new_user_role = st.selectbox("Role", ["user", "admin"], key="new_user_role")
                    
                    if st.form_submit_button("Add User"):
                        if not new_username or not new_user_password:
                            st.error("Username and password are required")
                        else:
                            result = self.add_user(new_username, new_user_password, new_user_role)
                            if result['success']:
                                st.success(result['message'])
                                st.rerun()
                            else:
                                st.error(result['error'])
        
        # User List Section
        with st.sidebar.expander("📋 User List", expanded=False):
            for username, info in users.items():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    role_badge = "🔑" if info['role'] == 'admin' else "👤"
                    st.write(f"{role_badge} **{username}**")
                    if info['last_login'] != 'Never':
                        try:
                            last_login = datetime.fromisoformat(info['last_login']).strftime("%m/%d %H:%M")
                            st.caption(f"Last: {last_login}")
                        except:
                            st.caption("Last: Unknown")
                    else:
                        st.caption("Last: Never")
                
                with col2:
                    if current_user_role == 'admin' and username != current_user and username != "user":
                        if st.button("🗑️", key=f"del_{username}", help="Delete user"):
                            result = self.delete_user(username)
                            if result['success']:
                                st.success(result['message'])
                                st.rerun()
                            else:
                                st.error(result['error'])