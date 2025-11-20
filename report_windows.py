# report_windows.py
"""Report-related UI windows"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
from config import COLORS
from report_manager import ReportManager
from email_service import EmailService


class CreateReportWindow:
    """Window for creating a new accident report"""

    def __init__(self, parent, user_data, callback=None):
        self.parent = parent
        self.user_data = user_data
        self.callback = callback
        self.report_manager = ReportManager()
        self.email_service = EmailService()
        self.evidence_file = None

        self.window = tk.Toplevel(parent)
        self.window.title("Create Accident Report")
        self.window.geometry("600x700")
        self.window.configure(bg=COLORS['white'])
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        """Setup create report UI"""
        # Header
        header = tk.Frame(self.window, bg=COLORS['danger'], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🚨 Create Accident Report",
            font=("Arial", 20, "bold"),
            bg=COLORS['danger'],
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

        # Reporter info (read-only)
        tk.Label(
            scrollable_frame,
            text="Reporter Information",
            font=("Arial", 12, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        ).pack(pady=(10, 5), anchor="w")

        tk.Label(
            scrollable_frame,
            text=f"Your Username: {self.user_data['username']}",
            font=("Arial", 10),
            bg=COLORS['white'],
            fg=COLORS['dark_gray']
        ).pack(anchor="w", padx=20)

        # Reported username
        tk.Label(
            scrollable_frame,
            text="Username Being Reported *",
            font=("Arial", 11, "bold"),
            bg=COLORS['white']
        ).pack(pady=(15, 5), anchor="w")

        self.entry_reported = tk.Entry(scrollable_frame, width=50, font=("Arial", 11))
        self.entry_reported.pack(anchor="w", padx=20)

        # Category
        tk.Label(
            scrollable_frame,
            text="Report Category *",
            font=("Arial", 11, "bold"),
            bg=COLORS['white']
        ).pack(pady=(15, 5), anchor="w")

        categories = [
            "Traffic Accident",
            "Road Hazard",
            "Reckless Driving",
            "Hit and Run",
            "Vehicle Malfunction",
            "Road Rage Incident",
            "Parking Violation",
            "Other Road-Related Issue"
        ]

        self.category_var = tk.StringVar(value=categories[0])
        category_menu = ttk.Combobox(
            scrollable_frame,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            width=47,
            font=("Arial", 11)
        )
        category_menu.pack(anchor="w", padx=20)

        # Description
        tk.Label(
            scrollable_frame,
            text="Incident Description *",
            font=("Arial", 11, "bold"),
            bg=COLORS['white']
        ).pack(pady=(15, 5), anchor="w")

        tk.Label(
            scrollable_frame,
            text="Please provide detailed information about the incident",
            font=("Arial", 9),
            bg=COLORS['white'],
            fg=COLORS['dark_gray']
        ).pack(anchor="w", padx=20)

        self.text_description = tk.Text(
            scrollable_frame,
            width=50,
            height=8,
            font=("Arial", 10),
            wrap="word"
        )
        self.text_description.pack(anchor="w", padx=20, pady=5)

        # Evidence text
        tk.Label(
            scrollable_frame,
            text="Additional Evidence Details",
            font=("Arial", 11, "bold"),
            bg=COLORS['white']
        ).pack(pady=(15, 5), anchor="w")

        tk.Label(
            scrollable_frame,
            text="Any additional details, witness information, or circumstances",
            font=("Arial", 9),
            bg=COLORS['white'],
            fg=COLORS['dark_gray']
        ).pack(anchor="w", padx=20)

        self.text_evidence = tk.Text(
            scrollable_frame,
            width=50,
            height=5,
            font=("Arial", 10),
            wrap="word"
        )
        self.text_evidence.pack(anchor="w", padx=20, pady=5)

        # File upload
        tk.Label(
            scrollable_frame,
            text="Upload Evidence File (Optional)",
            font=("Arial", 11, "bold"),
            bg=COLORS['white']
        ).pack(pady=(15, 5), anchor="w")

        file_frame = tk.Frame(scrollable_frame, bg=COLORS['white'])
        file_frame.pack(anchor="w", padx=20, fill="x")

        tk.Button(
            file_frame,
            text="📎 Choose File",
            command=self.choose_file,
            bg=COLORS['info'],
            fg=COLORS['white'],
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=(0, 10))

        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            font=("Arial", 9),
            bg=COLORS['white'],
            fg=COLORS['dark_gray']
        )
        self.file_label.pack(side="left")

        # Buttons
        btn_frame = tk.Frame(scrollable_frame, bg=COLORS['white'])
        btn_frame.pack(pady=30, fill="x")

        tk.Button(
            btn_frame,
            text="Submit Report",
            command=self.submit_report,
            bg=COLORS['danger'],
            fg=COLORS['white'],
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            cursor="hand2"
        ).pack(side="left", padx=20)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=self.window.destroy,
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            font=("Arial", 10),
            width=15,
            cursor="hand2"
        ).pack(side="left")

    def choose_file(self):
        """Open file dialog to choose evidence file"""
        file_path = filedialog.askopenfilename(
            title="Select Evidence File",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Document files", "*.pdf *.doc *.docx *.txt"),
                ("Video files", "*.mp4 *.avi *.mov"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.evidence_file = file_path
            filename = file_path.split('/')[-1]
            self.file_label.config(text=f"✓ {filename}", fg=COLORS['success'])

    def submit_report(self):
        """Submit the accident report"""
        reported = self.entry_reported.get().strip()
        category = self.category_var.get()
        description = self.text_description.get("1.0", tk.END).strip()
        evidence_text = self.text_evidence.get("1.0", tk.END).strip()

        if not reported:
            messagebox.showerror("Error", "Please enter the username being reported")
            return

        if not description:
            messagebox.showerror("Error", "Please provide an incident description")
            return

        try:
            # Create report
            report_id = self.report_manager.create_report(
                self.user_data['id'],
                self.user_data['username'],
                reported,
                category,
                description,
                evidence_text
            )

            if not report_id:
                messagebox.showerror("Error", "Failed to create report")
                return

            # Save evidence file if provided
            if self.evidence_file:
                saved_path = self.report_manager.save_evidence_file(self.evidence_file, report_id)
                if saved_path:
                    # Update report with file path
                    query = "UPDATE accident_reports SET evidence_file_path = %s WHERE id = %s"
                    self.report_manager.db.execute_query(query, (saved_path, report_id))

            # Send email notification to admins
            self.notify_admins(report_id, category, reported)

            messagebox.showinfo(
                "Success",
                f"Report #{report_id} submitted successfully!\n\n"
                "Your report has been sent to administrators for review.\n"
                "You can track the status in 'My Reports'."
            )

            self.window.destroy()

            if self.callback:
                self.callback()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit report: {str(e)}")

    def notify_admins(self, report_id, category, reported_user):
        """Send email notification to admin users"""
        try:
            # Get all admin emails
            query = "SELECT email FROM users WHERE is_admin = TRUE AND email IS NOT NULL"
            admins = self.report_manager.db.execute_query(query, fetch=True)

            for admin in admins:
                admin_email = admin.get('email')
                if admin_email:
                    subject = f"New Accident Report #{report_id} - {category}"
                    body = f"""
New Accident Report Submitted

Report ID: #{report_id}
Category: {category}
Reporter: {self.user_data['username']}
Reported User: {reported_user}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please log in to the admin dashboard to review this report.
                    """
                    self.email_service.send_email(admin_email, subject, body)
        except Exception as e:
            print(f"Error notifying admins: {e}")


class MyReportsWindow:
    """Window for viewing user's own reports"""

    def __init__(self, parent, user_data):
        self.parent = parent
        self.user_data = user_data
        self.report_manager = ReportManager()

        self.window = tk.Toplevel(parent)
        self.window.title("My Reports")
        self.window.geometry("900x600")
        self.window.configure(bg=COLORS['white'])
        self.window.grab_set()

        self.setup_ui()
        self.load_reports()

    def setup_ui(self):
        """Setup my reports UI"""
        # Header
        header = tk.Frame(self.window, bg=COLORS['info'], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📋 My Submitted Reports",
            font=("Arial", 18, "bold"),
            bg=COLORS['info'],
            fg=COLORS['white']
        ).pack(pady=15)

        # Toolbar
        toolbar = tk.Frame(self.window, bg=COLORS['light_gray'], height=50)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        tk.Button(
            toolbar,
            text="🔄 Refresh",
            command=self.load_reports,
            bg=COLORS['success'],
            fg=COLORS['white'],
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=10, pady=10)

        tk.Button(
            toolbar,
            text="✏️ Edit Selected",
            command=self.edit_report,
            bg=COLORS['warning'],
            fg=COLORS['white'],
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=5, pady=10)

        tk.Button(
            toolbar,
            text="🗑️ Delete Selected",
            command=self.delete_report,
            bg=COLORS['danger'],
            fg=COLORS['white'],
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=5, pady=10)

        # Reports list with treeview
        list_frame = tk.Frame(self.window, bg=COLORS['white'])
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create treeview
        columns = ("ID", "Reported User", "Category", "Status", "Date")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        # Define headings
        self.tree.heading("ID", text="Report #")
        self.tree.heading("Reported User", text="Reported User")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Date", text="Date Submitted")

        # Define column widths
        self.tree.column("ID", width=80)
        self.tree.column("Reported User", width=150)
        self.tree.column("Category", width=200)
        self.tree.column("Status", width=120)
        self.tree.column("Date", width=180)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind double-click to view details
        self.tree.bind("<Double-1>", lambda e: self.view_report_details())

        # Status bar
        self.status_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 9),
            bg=COLORS['light_gray'],
            fg=COLORS['dark_gray'],
            anchor="w"
        )
        self.status_label.pack(fill="x", side="bottom")

    def load_reports(self):
        """Load user's reports"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        reports = self.report_manager.get_user_reports(self.user_data['id'])

        for report in reports:
            status_color = {
                'pending': 'yellow',
                'reviewed': 'blue',
                'resolved': 'green'
            }.get(report['status'], 'gray')

            self.tree.insert("", "end", values=(
                f"#{report['id']}",
                report['reported_username'],
                report['report_category'],
                report['status'].upper(),
                report['created_at'].strftime('%Y-%m-%d %H:%M') if report['created_at'] else 'N/A'
            ), tags=(status_color,))

        # Configure tags
        self.tree.tag_configure('yellow', background='#fff9e6')
        self.tree.tag_configure('blue', background='#e6f2ff')
        self.tree.tag_configure('green', background='#e6ffe6')

        self.status_label.config(text=f"Total reports: {len(reports)}")

    def view_report_details(self):
        """View detailed report information"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report to view")
            return

        item = self.tree.item(selection[0])
        report_id = int(item['values'][0].replace('#', ''))

        report = self.report_manager.get_report_by_id(report_id)
        if report:
            ViewReportDetailsWindow(self.window, report)

    def edit_report(self):
        """Edit selected report"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report to edit")
            return

        item = self.tree.item(selection[0])
        report_id = int(item['values'][0].replace('#', ''))

        report = self.report_manager.get_report_by_id(report_id)
        if report:
            if report['status'] != 'pending':
                messagebox.showwarning("Warning", "Only pending reports can be edited")
                return

            EditReportWindow(self.window, report, self.load_reports)

    def delete_report(self):
        """Delete selected report"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a report to delete")
            return

        item = self.tree.item(selection[0])
        report_id = int(item['values'][0].replace('#', ''))

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this report?"):
            if self.report_manager.delete_report(report_id, self.user_data['id']):
                messagebox.showinfo("Success", "Report deleted successfully")
                self.load_reports()
            else:
                messagebox.showerror("Error", "Failed to delete report")


class ViewReportDetailsWindow:
    """Window for viewing report details"""

    def __init__(self, parent, report):
        self.parent = parent
        self.report = report

        self.window = tk.Toplevel(parent)
        self.window.title(f"Report #{report['id']} Details")
        self.window.geometry("600x650")
        self.window.configure(bg=COLORS['white'])
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        """Setup view details UI"""
        # Header with status color
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

        # Report details
        details = [
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
            row = tk.Frame(scrollable_frame, bg=COLORS['white'])
            row.pack(fill="x", padx=20, pady=5)

            tk.Label(
                row,
                text=label,
                font=("Arial", 11, "bold"),
                bg=COLORS['white'],
                width=15,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                row,
                text=str(value),
                font=("Arial", 11),
                bg=COLORS['white'],
                anchor="w"
            ).pack(side="left")

        # Description
        tk.Label(
            scrollable_frame,
            text="Incident Description:",
            font=("Arial", 11, "bold"),
            bg=COLORS['white']
        ).pack(pady=(20, 5), anchor="w", padx=20)

        desc_text = tk.Text(
            scrollable_frame,
            width=60,
            height=6,
            font=("Arial", 10),
            wrap="word",
            bg=COLORS['light_gray']
        )
        desc_text.pack(padx=20, pady=5)
        desc_text.insert("1.0", self.report['description'])
        desc_text.config(state="disabled")

        # Evidence text
        if self.report.get('evidence_text'):
            tk.Label(
                scrollable_frame,
                text="Evidence Details:",
                font=("Arial", 11, "bold"),
                bg=COLORS['white']
            ).pack(pady=(20, 5), anchor="w", padx=20)

            evidence_text = tk.Text(
                scrollable_frame,
                width=60,
                height=4,
                font=("Arial", 10),
                wrap="word",
                bg=COLORS['light_gray']
            )
            evidence_text.pack(padx=20, pady=5)
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
            ).pack(pady=10, anchor="w", padx=20)

        # Admin notes
        if self.report.get('admin_notes'):
            tk.Label(
                scrollable_frame,
                text="Admin Notes:",
                font=("Arial", 11, "bold"),
                bg=COLORS['white'],
                fg=COLORS['danger']
            ).pack(pady=(20, 5), anchor="w", padx=20)

            admin_text = tk.Text(
                scrollable_frame,
                width=60,
                height=4,
                font=("Arial", 10),
                wrap="word",
                bg="#ffe6e6"
            )
            admin_text.pack(padx=20, pady=5)
            admin_text.insert("1.0", self.report['admin_notes'])
            admin_text.config(state="disabled")

        # Close button
        tk.Button(
            scrollable_frame,
            text="Close",
            command=self.window.destroy,
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            font=("Arial", 10),
            width=20,
            cursor="hand2"
        ).pack(pady=30)


class EditReportWindow:
    """Window for editing a report"""

    def __init__(self, parent, report, callback):
        self.parent = parent
        self.report = report
        self.callback = callback
        self.report_manager = ReportManager()

        self.window = tk.Toplevel(parent)
        self.window.title(f"Edit Report #{report['id']}")
        self.window.geometry("600x600")
        self.window.configure(bg=COLORS['white'])
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        """Setup edit report UI"""
        # Header
        tk.Label(
            self.window,
            text=f"Edit Report #{self.report['id']}",
            font=("Arial", 18, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        ).pack(pady=20)

        # Category
        tk.Label(
            self.window,
            text="Report Category",
            font=("Arial", 11, "bold"),
            bg=COLORS['white']
        ).pack(pady=(10, 5), anchor="w", padx=20)

        categories = [
            "Traffic Accident",
            "Road Hazard",
            "Reckless Driving",
            "Hit and Run",
            "Vehicle Malfunction",
            "Road Rage Incident",
            "Parking Violation",
            "Other Road-Related Issue"
        ]

        self.category_var = tk.StringVar(value=self.report['report_category'])
        category_menu = ttk.Combobox(
            self.window,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            width=47,
            font=("Arial", 11)
        )
        category_menu.pack(anchor="w", padx=20)

        # Description
        tk.Label(
            self.window,
            text="Incident Description",
            font=("Arial", 11, "bold"),
            bg=COLORS['white']
        ).pack(pady=(15, 5), anchor="w", padx=20)

        self.text_description = tk.Text(
            self.window,
            width=60,
            height=8,
            font=("Arial", 10),
            wrap="word"
        )
        self.text_description.pack(anchor="w", padx=20, pady=5)
        self.text_description.insert("1.0", self.report['description'])

        # Evidence text
        tk.Label(
            self.window,
            text="Additional Evidence Details",
            font=("Arial", 11, "bold"),
            bg=COLORS['white']
        ).pack(pady=(15, 5), anchor="w", padx=20)

        self.text_evidence = tk.Text(
            self.window,
            width=60,
            height=5,
            font=("Arial", 10),
            wrap="word"
        )
        self.text_evidence.pack(anchor="w", padx=20, pady=5)
        if self.report.get('evidence_text'):
            self.text_evidence.insert("1.0", self.report['evidence_text'])

        # Buttons
        btn_frame = tk.Frame(self.window, bg=COLORS['white'])
        btn_frame.pack(pady=30)

        tk.Button(
            btn_frame,
            text="Save Changes",
            command=self.save_changes,
            bg=COLORS['success'],
            fg=COLORS['white'],
            font=("Arial", 12, "bold"),
            width=15,
            cursor="hand2"
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=self.window.destroy,
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            font=("Arial", 10),
            width=15,
            cursor="hand2"
        ).pack(side="left")

    def save_changes(self):
        """Save report changes"""
        category = self.category_var.get()
        description = self.text_description.get("1.0", tk.END).strip()
        evidence_text = self.text_evidence.get("1.0", tk.END).strip()

        if not description:
            messagebox.showerror("Error", "Description cannot be empty")
            return

        if self.report_manager.update_report(self.report['id'], category, description, evidence_text):
            messagebox.showinfo("Success", "Report updated successfully")
            self.window.destroy()
            if self.callback:
                self.callback()
        else:
            messagebox.showerror("Error", "Failed to update report")