# admin_dashboard.py
"""Admin dashboard for managing accident reports"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from config import COLORS
from report_manager import ReportManager
from email_service import EmailService


class AdminReportsWindow:
    """Admin window for viewing and managing all reports"""

    def __init__(self, parent, user_data):
        self.parent = parent
        self.user_data = user_data
        self.report_manager = ReportManager()
        self.email_service = EmailService()

        # Check if user is admin
        if not self.report_manager.is_user_admin(user_data['id']):
            messagebox.showerror("Access Denied", "You do not have admin privileges")
            return

        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Admin - Accident Reports Management")
        self.window.geometry("1200x700")
        self.window.configure(bg=COLORS['white'])
        if parent:
            self.window.grab_set()

        self.setup_ui()
        self.load_reports()

    def setup_ui(self):
        """Setup admin reports UI"""
        # Header
        header = tk.Frame(self.window, bg=COLORS['danger'], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🛡️ Admin - Accident Reports Management",
            font=("Arial", 20, "bold"),
            bg=COLORS['danger'],
            fg=COLORS['white']
        ).pack(side="left", padx=20, pady=20)

        # Notification badge
        self.notification_badge = tk.Label(
            header,
            text="",
            font=("Arial", 12, "bold"),
            bg=COLORS['white'],
            fg=COLORS['danger'],
            relief="raised",
            borderwidth=2
        )
        self.notification_badge.pack(side="left", padx=10)

        # Toolbar
        toolbar = tk.Frame(self.window, bg=COLORS['light_gray'], height=60)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        # Filter frame
        filter_frame = tk.Frame(toolbar, bg=COLORS['light_gray'])
        filter_frame.pack(side="left", padx=20, pady=10)

        tk.Label(
            filter_frame,
            text="Filter by Status:",
            font=("Arial", 10, "bold"),
            bg=COLORS['light_gray']
        ).pack(side="left", padx=5)

        self.filter_var = tk.StringVar(value="all")
        filters = [("All", "all"), ("Pending", "pending"), ("Reviewed", "reviewed"), ("Resolved", "resolved")]

        for text, value in filters:
            tk.Radiobutton(
                filter_frame,
                text=text,
                variable=self.filter_var,
                value=value,
                command=self.load_reports,
                bg=COLORS['light_gray'],
                font=("Arial", 9)
            ).pack(side="left", padx=5)

        # Action buttons
        btn_frame = tk.Frame(toolbar, bg=COLORS['light_gray'])
        btn_frame.pack(side="right", padx=20, pady=10)

        tk.Button(
            btn_frame,
            text="🔄 Refresh",
            command=self.load_reports,
            bg=COLORS['success'],
            fg=COLORS['white'],
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="👁️ View Details",
            command=self.view_report,
            bg=COLORS['info'],
            fg=COLORS['white'],
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="✅ Mark Reviewed",
            command=self.mark_reviewed,
            bg=COLORS['primary'],
            fg=COLORS['white'],
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="✔️ Mark Resolved",
            command=self.mark_resolved,
            bg=COLORS['success'],
            fg=COLORS['white'],
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=5)

        # Reports table
        table_frame = tk.Frame(self.window, bg=COLORS['white'])
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create treeview with scrollbars
        columns = ("ID", "Reporter", "Reported User", "Category", "Status", "Date", "Reviewed")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        # Define headings
        self.tree.heading("ID", text="Report #")
        self.tree.heading("Reporter", text="Reporter")
        self.tree.heading("Reported User", text="Reported User")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Date", text="Date Submitted")
        self.tree.heading("Reviewed", text="Reviewed By")

        # Define column widths
        self.tree.column("ID", width=80)
        self.tree.column("Reporter", width=120)
        self.tree.column("Reported User", width=120)
        self.tree.column("Category", width=180)
        self.tree.column("Status", width=100)
        self.tree.column("Date", width=150)
        self.tree.column("Reviewed", width=120)

        # Scrollbars
        vsb = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = tk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Bind double-click
        self.tree.bind("<Double-1>", lambda e: self.view_report())

        # Status bar
        self.status_bar = tk.Label(
            self.window,
            text="",
            font=("Arial", 9),
            bg=COLORS['light_gray'],
            fg=COLORS['dark_gray'],
            anchor="w"
        )
        self.status_bar.pack(fill="x", side="bottom")

    def load_reports(self):
        """Load and display reports"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get filter
        filter_status = self.filter_var.get()

        # Load reports
        all_reports = self.report_manager.get_all_reports()

        # Filter reports
        if filter_status != "all":
            reports = [r for r in all_reports if r['status'] == filter_status]
        else:
            reports = all_reports

        # Count pending reports
        pending_count = sum(1 for r in all_reports if r['status'] == 'pending')

        # Update notification badge
        if pending_count > 0:
            self.notification_badge.config(text=f"🔔 {pending_count} Pending")
        else:
            self.notification_badge.config(text="✓ All Clear")

        # Populate table
        for report in reports:
            reviewed_by = "Not reviewed"
            if report.get('reviewed_by'):
                # Get reviewer username
                query = "SELECT username FROM users WHERE id = %s"
                result = self.report_manager.db.execute_query(query, (report['reviewed_by'],), fetch=True)
                if result:
                    reviewed_by = result[0]['username']

            status_color = {
                'pending': 'yellow',
                'reviewed': 'blue',
                'resolved': 'green'
            }.get(report['status'], 'gray')

            self.tree.insert("", "end", values=(
                f"#{report['id']}",
                report['reporter_username'],
                report['reported_username'],
                report['report_category'],
                report['status'].upper(),
                report['created_at'].strftime('%Y-%m-%d %H:%M') if report['created_at'] else 'N/A',
                reviewed_by
            ), tags=(status_color,))

        # Configure tags
        self.tree.tag_configure('yellow', background='#fff9e6')
        self.tree.tag_configure('blue', background='#e6f2ff')
        self.tree.tag_configure('green', background='#e6ffe6')

        # Update status bar
        self.status_bar.config(
            text=f"Total reports: {len(reports)} | "
                 f"Pending: {pending_count} | "
                 f"Reviewed: {sum(1 for r in all_reports if r['status'] == 'reviewed')} | "
                 f"Resolved: {sum(1 for r in all_reports if r['status'] == 'resolved')}"
        )

    def view_report(self):
        """View detailed report"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report to view")
            return

        item = self.tree.item(selection[0])
        report_id = int(item['values'][0].replace('#', ''))

        report = self.report_manager.get_report_by_id(report_id)
        if report:
            AdminReportDetailWindow(self.window, report, self.user_data, self.load_reports)

    def mark_reviewed(self):
        """Mark report as reviewed"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report")
            return

        item = self.tree.item(selection[0])
        report_id = int(item['values'][0].replace('#', ''))

        if messagebox.askyesno("Confirm", "Mark this report as reviewed?"):
            if self.report_manager.update_report_status(report_id, 'reviewed', self.user_data['id']):
                messagebox.showinfo("Success", "Report marked as reviewed")
                self.load_reports()
            else:
                messagebox.showerror("Error", "Failed to update report status")

    def mark_resolved(self):
        """Mark report as resolved"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report")
            return

        item = self.tree.item(selection[0])
        report_id = int(item['values'][0].replace('#', ''))

        if messagebox.askyesno("Confirm", "Mark this report as resolved?"):
            if self.report_manager.update_report_status(report_id, 'resolved', self.user_data['id']):
                messagebox.showinfo("Success", "Report marked as resolved")
                self.load_reports()
            else:
                messagebox.showerror("Error", "Failed to update report status")


class AdminReportDetailWindow:
    """Admin window for viewing and managing a specific report"""

    def __init__(self, parent, report, admin_data, callback):
        self.parent = parent
        self.report = report
        self.admin_data = admin_data
        self.callback = callback
        self.report_manager = ReportManager()

        self.window = tk.Toplevel(parent)
        self.window.title(f"Admin - Report #{report['id']}")
        self.window.geometry("700x800")
        self.window.configure(bg=COLORS['white'])
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        """Setup detail view UI"""
        # Header
        status_colors = {
            'pending': COLORS['warning'],
            'reviewed': COLORS['info'],
            'resolved': COLORS['success']
        }
        header_color = status_colors.get(self.report['status'], COLORS['secondary'])

        header = tk.Frame(self.window, bg=header_color, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"Report #{self.report['id']} - {self.report['status'].upper()}",
            font=("Arial", 18, "bold"),
            bg=header_color,
            fg=COLORS['white']
        ).pack(pady=20)

        # Scrollable content
        canvas = tk.Canvas(self.window, bg=COLORS['white'])
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['white'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        # Report information
        info_frame = tk.Frame(scrollable_frame, bg=COLORS['light_gray'], relief="raised", borderwidth=1)
        info_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            info_frame,
            text="Report Information",
            font=("Arial", 14, "bold"),
            bg=COLORS['light_gray'],
            fg=COLORS['primary']
        ).pack(pady=10)

        details = [
            ("Report ID:", f"#{self.report['id']}"),
            ("Reporter:", self.report['reporter_username']),
            ("Reported User:", self.report['reported_username']),
            ("Category:", self.report['report_category']),
            ("Status:", self.report['status'].upper()),
            ("Date Submitted:",
             self.report['created_at'].strftime('%Y-%m-%d %H:%M:%S') if self.report['created_at'] else 'N/A'),
        ]

        if self.report.get('reviewed_at'):
            details.append(("Reviewed At:", self.report['reviewed_at'].strftime('%Y-%m-%d %H:%M:%S')))

        for label, value in details:
            row = tk.Frame(info_frame, bg=COLORS['light_gray'])
            row.pack(fill="x", padx=20, pady=3)

            tk.Label(
                row,
                text=label,
                font=("Arial", 10, "bold"),
                bg=COLORS['light_gray'],
                width=15,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                row,
                text=str(value),
                font=("Arial", 10),
                bg=COLORS['light_gray'],
                anchor="w"
            ).pack(side="left")

        # Description
        tk.Label(
            scrollable_frame,
            text="Incident Description:",
            font=("Arial", 12, "bold"),
            bg=COLORS['white']
        ).pack(pady=(20, 5), anchor="w", padx=10)

        desc_text = tk.Text(
            scrollable_frame,
            width=70,
            height=8,
            font=("Arial", 10),
            wrap="word",
            bg=COLORS['light_gray']
        )
        desc_text.pack(padx=10, pady=5)
        desc_text.insert("1.0", self.report['description'])
        desc_text.config(state="disabled")

        # Evidence
        if self.report.get('evidence_text'):
            tk.Label(
                scrollable_frame,
                text="Evidence Details:",
                font=("Arial", 12, "bold"),
                bg=COLORS['white']
            ).pack(pady=(20, 5), anchor="w", padx=10)

            evidence_text = tk.Text(
                scrollable_frame,
                width=70,
                height=5,
                font=("Arial", 10),
                wrap="word",
                bg=COLORS['light_gray']
            )
            evidence_text.pack(padx=10, pady=5)
            evidence_text.insert("1.0", self.report['evidence_text'])
            evidence_text.config(state="disabled")

        # Evidence file
        if self.report.get('evidence_file_path'):
            tk.Label(
                scrollable_frame,
                text=f"📎 Evidence File: {self.report['evidence_file_path'].split('/')[-1]}",
                font=("Arial", 10),
                bg=COLORS['white'],
                fg=COLORS['info']
            ).pack(pady=10, anchor="w", padx=10)

        # Admin notes section
        tk.Label(
            scrollable_frame,
            text="Admin Notes:",
            font=("Arial", 12, "bold"),
            bg=COLORS['white'],
            fg=COLORS['danger']
        ).pack(pady=(20, 5), anchor="w", padx=10)

        self.admin_notes_text = tk.Text(
            scrollable_frame,
            width=70,
            height=5,
            font=("Arial", 10),
            wrap="word"
        )
        self.admin_notes_text.pack(padx=10, pady=5)
        if self.report.get('admin_notes'):
            self.admin_notes_text.insert("1.0", self.report['admin_notes'])

        # Action buttons
        btn_frame = tk.Frame(scrollable_frame, bg=COLORS['white'])
        btn_frame.pack(pady=30)

        tk.Button(
            btn_frame,
            text="✅ Mark Reviewed",
            command=lambda: self.update_status('reviewed'),
            bg=COLORS['info'],
            fg=COLORS['white'],
            font=("Arial", 10, "bold"),
            width=15,
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="✔️ Mark Resolved",
            command=lambda: self.update_status('resolved'),
            bg=COLORS['success'],
            fg=COLORS['white'],
            font=("Arial", 10, "bold"),
            width=15,
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="💾 Save Notes",
            command=self.save_notes,
            bg=COLORS['warning'],
            fg=COLORS['white'],
            font=("Arial", 10, "bold"),
            width=15,
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Close",
            command=self.window.destroy,
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            font=("Arial", 10),
            width=15,
            cursor="hand2"
        ).pack(side="left", padx=5)

    def update_status(self, new_status):
        """Update report status"""
        admin_notes = self.admin_notes_text.get("1.0", tk.END).strip()

        if self.report_manager.update_report_status(
                self.report['id'],
                new_status,
                self.admin_data['id'],
                admin_notes if admin_notes else None
        ):
            messagebox.showinfo("Success", f"Report marked as {new_status}")
            self.window.destroy()
            if self.callback:
                self.callback()
        else:
            messagebox.showerror("Error", "Failed to update report status")

    def save_notes(self):
        """Save admin notes"""
        admin_notes = self.admin_notes_text.get("1.0", tk.END).strip()

        query = "UPDATE accident_reports SET admin_notes = %s WHERE id = %s"
        try:
            self.report_manager.db.execute_query(query, (admin_notes, self.report['id']))
            messagebox.showinfo("Success", "Admin notes saved")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save notes: {str(e)}")


# Add this to your main dashboard to show admin button if user is admin
def add_admin_button_to_dashboard(dashboard_instance):
    """Add admin button to dashboard if user is admin"""
    if dashboard_instance.report_manager.is_user_admin(dashboard_instance.user_data['id']):
        admin_btn = tk.Button(
            dashboard_instance.content_frame,
            text="🛡️ Admin Panel",
            command=lambda: AdminReportsWindow(dashboard_instance.window, dashboard_instance.user_data),
            bg=COLORS['purple'],
            fg=COLORS['white'],
            font=("Arial", 12, "bold"),
            width=20,
            cursor="hand2"
        )
        admin_btn.pack(pady=10)