# report_manager.py
"""Report management functions for accident reports"""

import os
import shutil
from datetime import datetime
from database import DatabaseManager


class ReportManager:
    """Manages accident reports in the database"""

    def __init__(self):
        self.db = DatabaseManager()
        self.reports_dir = "reports_evidence"
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def create_report(self, reporter_id, reporter_username, reported_username,
                      category, description, evidence_text, evidence_file_path=None):
        """Create a new accident report"""
        try:
            query = """
                INSERT INTO accident_reports 
                (reporter_id, reporter_username, reported_username, report_category, 
                 description, evidence_text, evidence_file_path, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
                RETURNING id
            """
            result = self.db.execute_query(
                query,
                (reporter_id, reporter_username, reported_username, category,
                 description, evidence_text, evidence_file_path),
                fetch=True
            )

            if result:
                return result[0]['id']
            return None
        except Exception as e:
            print(f"Error creating report: {e}")
            return None

    def save_evidence_file(self, file_path, report_id):
        """Save evidence file to reports directory"""
        try:
            if not file_path or not os.path.exists(file_path):
                return None

            # Create unique filename
            filename = f"report_{report_id}_{os.path.basename(file_path)}"
            destination = os.path.join(self.reports_dir, filename)

            # Copy file
            shutil.copy2(file_path, destination)
            return destination
        except Exception as e:
            print(f"Error saving evidence file: {e}")
            return None

    def get_user_reports(self, user_id):
        """Get all reports submitted by a user"""
        try:
            query = """
                SELECT * FROM accident_reports 
                WHERE reporter_id = %s 
                ORDER BY created_at DESC
            """
            return self.db.execute_query(query, (user_id,), fetch=True)
        except Exception as e:
            print(f"Error fetching user reports: {e}")
            return []

    def get_all_reports(self):
        """Get all reports (for admin)"""
        try:
            query = """
                SELECT * FROM accident_reports 
                ORDER BY created_at DESC
            """
            return self.db.execute_query(query, fetch=True)
        except Exception as e:
            print(f"Error fetching all reports: {e}")
            return []

    def get_pending_reports_count(self):
        """Get count of pending reports"""
        try:
            query = """
                SELECT COUNT(*) as count FROM accident_reports 
                WHERE status = 'pending'
            """
            result = self.db.execute_query(query, fetch=True)
            return result[0]['count'] if result else 0
        except Exception as e:
            print(f"Error counting pending reports: {e}")
            return 0

    def update_report(self, report_id, category, description, evidence_text):
        """Update an existing report"""
        try:
            query = """
                UPDATE accident_reports 
                SET report_category = %s, description = %s, evidence_text = %s
                WHERE id = %s
            """
            self.db.execute_query(query, (category, description, evidence_text, report_id))
            return True
        except Exception as e:
            print(f"Error updating report: {e}")
            return False

    def delete_report(self, report_id, reporter_id):
        """Delete a report (only by reporter)"""
        try:
            # First get the evidence file path
            query = "SELECT evidence_file_path FROM accident_reports WHERE id = %s AND reporter_id = %s"
            result = self.db.execute_query(query, (report_id, reporter_id), fetch=True)

            if result and result[0].get('evidence_file_path'):
                # Delete the evidence file
                file_path = result[0]['evidence_file_path']
                if os.path.exists(file_path):
                    os.remove(file_path)

            # Delete the report
            query = "DELETE FROM accident_reports WHERE id = %s AND reporter_id = %s"
            self.db.execute_query(query, (report_id, reporter_id))
            return True
        except Exception as e:
            print(f"Error deleting report: {e}")
            return False

    def update_report_status(self, report_id, status, admin_id, admin_notes=None):
        """Update report status (admin only)"""
        try:
            query = """
                UPDATE accident_reports 
                SET status = %s, reviewed_by = %s, reviewed_at = CURRENT_TIMESTAMP, 
                    admin_notes = %s
                WHERE id = %s
            """
            self.db.execute_query(query, (status, admin_id, admin_notes, report_id))
            return True
        except Exception as e:
            print(f"Error updating report status: {e}")
            return False

    def is_user_admin(self, user_id):
        """Check if user is an admin"""
        try:
            query = "SELECT is_admin FROM users WHERE id = %s"
            result = self.db.execute_query(query, (user_id,), fetch=True)
            return result[0]['is_admin'] if result else False
        except Exception as e:
            print(f"Error checking admin status: {e}")
            return False

    def get_report_by_id(self, report_id):
        """Get a specific report by ID"""
        try:
            query = "SELECT * FROM accident_reports WHERE id = %s"
            result = self.db.execute_query(query, (report_id,), fetch=True)
            return result[0] if result else None
        except Exception as e:
            print(f"Error fetching report: {e}")
            return None