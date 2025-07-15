import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class LogManager:
    def __init__(self):
        self.log_dir = "PanelDomain/logs"
        self.ensure_log_directory()
    
    def ensure_log_directory(self):
        """Create log directory if it doesn't exist"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def get_log_file_path(self, domain: str) -> str:
        """Get log file path for domain"""
        safe_domain = domain.replace(".", "_").replace("/", "_")
        return os.path.join(self.log_dir, f"{safe_domain}_log.txt")
    
    def add_log_entry(self, domain: str, log_type: str, message: str, level: str = "info") -> Dict:
        """Add log entry for domain"""
        try:
            log_path = self.get_log_file_path(domain)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            log_entry = f"[{timestamp}] [{level.upper()}] [{log_type}] {message}\n"
            
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            return {
                'success': True,
                'message': f'Log entry added for {domain}',
                'timestamp': timestamp,
                'level': level
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def load_domain_logs(self, domain: str) -> List[Dict]:
        """Load logs for domain"""
        try:
            log_path = self.get_log_file_path(domain)
            
            if not os.path.exists(log_path):
                return []
            
            logs = []
            with open(log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        # Parse log entry
                        # Format: [timestamp] [level] [type] message
                        parts = line.split('] ', 3)
                        if len(parts) >= 4:
                            timestamp = parts[0].replace('[', '')
                            level = parts[1].replace('[', '')
                            log_type = parts[2].replace('[', '')
                            message = parts[3]
                            
                            logs.append({
                                'timestamp': timestamp,
                                'level': level,
                                'type': log_type,
                                'message': message
                            })
            
            return logs
        except Exception as e:
            return []
    
    def get_domain_status(self, domain: str) -> Dict:
        """Get domain status based on logs"""
        try:
            logs = self.load_domain_logs(domain)
            
            if not logs:
                return {
                    'domain': domain,
                    'status': 'unknown',
                    'last_activity': 'Never',
                    'error_count': 0,
                    'warning_count': 0
                }
            
            # Count errors and warnings
            error_count = len([log for log in logs if log['level'] == 'ERROR'])
            warning_count = len([log for log in logs if log['level'] == 'WARNING'])
            
            # Get last activity
            last_log = logs[-1] if logs else None
            last_activity = last_log['timestamp'] if last_log else 'Never'
            
            # Determine status
            if error_count > 0:
                status = 'error'
            elif warning_count > 0:
                status = 'warning'
            else:
                status = 'healthy'
            
            return {
                'domain': domain,
                'status': status,
                'last_activity': last_activity,
                'error_count': error_count,
                'warning_count': warning_count,
                'total_logs': len(logs)
            }
        except Exception as e:
            return {
                'domain': domain,
                'status': 'error',
                'error': str(e)
            }
    
    def get_recent_logs(self, logs: List[Dict], hours: int = 24) -> List[Dict]:
        """Get logs from last N hours"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_logs = []
            
            for log in logs:
                try:
                    log_time = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S')
                    if log_time >= cutoff_time:
                        recent_logs.append(log)
                except:
                    continue
            
            return recent_logs
        except Exception as e:
            return []
    
    def clean_old_logs(self, domain: str, hours: int = 24) -> Dict:
        """Clean logs older than N hours"""
        try:
            logs = self.load_domain_logs(domain)
            recent_logs = self.get_recent_logs(logs, hours)
            
            # Rewrite log file with only recent logs
            log_path = self.get_log_file_path(domain)
            
            with open(log_path, 'w', encoding='utf-8') as f:
                for log in recent_logs:
                    log_entry = f"[{log['timestamp']}] [{log['level']}] [{log['type']}] {log['message']}\n"
                    f.write(log_entry)
            
            cleaned_count = len(logs) - len(recent_logs)
            
            return {
                'success': True,
                'domain': domain,
                'cleaned_count': cleaned_count,
                'remaining_count': len(recent_logs)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'domain': domain
            }
    
    def auto_clean_all_logs(self, hours: int = 24) -> Dict:
        """Auto clean logs for all domains"""
        try:
            cleaned_domains = []
            
            # Get all log files
            if os.path.exists(self.log_dir):
                for filename in os.listdir(self.log_dir):
                    if filename.endswith('_log.txt'):
                        domain = filename.replace('_log.txt', '').replace('_', '.')
                        result = self.clean_old_logs(domain, hours)
                        if result.get('success'):
                            cleaned_domains.append(domain)
            
            return {
                'success': True,
                'cleaned_domains': cleaned_domains,
                'total_cleaned': len(cleaned_domains)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_all_domain_status(self) -> Dict:
        """Get status for all domains"""
        try:
            domain_statuses = {}
            
            if os.path.exists(self.log_dir):
                for filename in os.listdir(self.log_dir):
                    if filename.endswith('_log.txt'):
                        domain = filename.replace('_log.txt', '').replace('_', '.')
                        status = self.get_domain_status(domain)
                        domain_statuses[domain] = status
            
            return domain_statuses
        except Exception as e:
            return {}
    
    def log_deploy_success(self, domain: str, message: str = "Deploy successful"):
        """Log successful deployment"""
        return self.add_log_entry(domain, "DEPLOY", message, "info")
    
    def log_deploy_error(self, domain: str, error: str):
        """Log deployment error"""
        return self.add_log_entry(domain, "DEPLOY", f"Deploy failed: {error}", "error")
    
    def log_content_generation(self, domain: str, message: str):
        """Log content generation"""
        return self.add_log_entry(domain, "CONTENT", message, "info")
    
    def log_seo_update(self, domain: str, message: str):
        """Log SEO update"""
        return self.add_log_entry(domain, "SEO", message, "info")
    
    def log_error(self, domain: str, error: str):
        """Log general error"""
        return self.add_log_entry(domain, "ERROR", error, "error")
    
    def log_warning(self, domain: str, warning: str):
        """Log warning"""
        return self.add_log_entry(domain, "WARNING", warning, "warning")
    
    def log_info(self, domain: str, message: str):
        """Log info message"""
        return self.add_log_entry(domain, "INFO", message, "info")
    
    def get_domain_log_summary(self, domain: str) -> Dict:
        """Get summary of domain logs"""
        try:
            logs = self.load_domain_logs(domain)
            
            if not logs:
                return {
                    'domain': domain,
                    'total_logs': 0,
                    'error_count': 0,
                    'warning_count': 0,
                    'info_count': 0,
                    'deploy_count': 0,
                    'content_count': 0,
                    'seo_count': 0
                }
            
            # Count by type
            type_counts = {}
            level_counts = {}
            
            for log in logs:
                log_type = log.get('type', 'UNKNOWN')
                log_level = log.get('level', 'INFO')
                
                type_counts[log_type] = type_counts.get(log_type, 0) + 1
                level_counts[log_level] = level_counts.get(log_level, 0) + 1
            
            return {
                'domain': domain,
                'total_logs': len(logs),
                'error_count': level_counts.get('ERROR', 0),
                'warning_count': level_counts.get('WARNING', 0),
                'info_count': level_counts.get('INFO', 0),
                'deploy_count': type_counts.get('DEPLOY', 0),
                'content_count': type_counts.get('CONTENT', 0),
                'seo_count': type_counts.get('SEO', 0),
                'last_activity': logs[-1]['timestamp'] if logs else 'Never'
            }
        except Exception as e:
            return {
                'domain': domain,
                'error': str(e)
            }
    
    def export_domain_logs(self, domain: str, format: str = 'txt') -> Dict:
        """Export domain logs in specified format"""
        try:
            logs = self.load_domain_logs(domain)
            
            if format == 'json':
                import json
                export_content = json.dumps(logs, indent=2)
            else:  # txt format
                export_content = f"# Logs for {domain}\n"
                export_content += f"# Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                
                for log in logs:
                    export_content += f"[{log['timestamp']}] [{log['level']}] [{log['type']}] {log['message']}\n"
            
            return {
                'success': True,
                'domain': domain,
                'format': format,
                'content': export_content,
                'log_count': len(logs)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'domain': domain
            }