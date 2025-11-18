# dashboard.py
"""Main dashboard window with camera integration"""

import tkinter as tk
from tkinter import messagebox
from config import COLORS
from database import DatabaseManager
from email_service import EmailService
from verification_window import VerificationWindow

try:
    import cv2
    from PIL import Image, ImageTk

    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False
    print("Warning: OpenCV or PIL not installed. Camera feature will be disabled.")


class Dashboard:
    """Main dashboard class"""

    def __init__(self, user_data):
        self.user_data = user_data
        self.db = DatabaseManager()
        self.email_service = EmailService()

        self.window = tk.Tk()
        self.window.title("Dashboard")
        self.window.geometry("800x600")
        self.window.configure(bg=COLORS['light_gray'])

        # Camera variables
        self.camera_active = False
        self.cap = None
        self.camera_frame = None
        self.camera_label = None
        self.content_frame = None

        self.setup_ui()
        self.window.mainloop()

    def setup_ui(self):
        """Setup dashboard UI"""
        # Top bar
        self.create_top_bar()

        # Main content
        self.create_main_content()

    def create_top_bar(self):
        """Create top navigation bar"""
        top_frame = tk.Frame(self.window, bg=COLORS['primary'], height=60)
        top_frame.pack(fill="x", side="top")
        top_frame.pack_propagate(False)

        # User info section
        user_info_frame = tk.Frame(top_frame, bg=COLORS['primary'])
        user_info_frame.pack(side="left", padx=20, pady=10)

        profile_btn = tk.Label(
            user_info_frame,
            text="👤",
            bg=COLORS['primary'],
            fg=COLORS['white'],
            font=("Arial", 14, "bold"),
            cursor="hand2"
        )
        profile_btn.pack(side="left", padx=(0, 8))

        username_label = tk.Label(
            user_info_frame,
            text=self.user_data['username'],
            bg=COLORS['primary'],
            fg=COLORS['white'],
            font=("Arial", 12, "bold"),
            cursor="hand2"
        )
        username_label.pack(anchor="w")

        if self.user_data.get('full_name'):
            fullname_label = tk.Label(
                user_info_frame,
                text=self.user_data['full_name'],
                bg=COLORS['primary'],
                fg="#ecf0f1",
                font=("Arial", 9)
            )
            fullname_label.pack(anchor="w")

        # Create hover card
        self.create_hover_card(user_info_frame, profile_btn, username_label)

        # Logout button
        logout_btn = tk.Button(
            top_frame,
            text="Logout",
            command=self.logout,
            bg=COLORS['danger'],
            fg=COLORS['white'],
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        logout_btn.pack(side="right", padx=20)

    def create_hover_card(self, user_info_frame, profile_btn, username_label):
        """Create profile hover card"""
        hover_card = tk.Toplevel(self.window)
        hover_card.withdraw()
        hover_card.overrideredirect(True)
        hover_card.configure(bg=COLORS['white'])

        card_container = tk.Frame(hover_card, bg=COLORS['white'], relief="raised", borderwidth=2)
        card_container.pack(padx=2, pady=2)

        tk.Label(
            card_container,
            text="Account Information",
            font=("Arial", 12, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        ).pack(pady=10, padx=15)

        info_details = [
            ("Username:", self.user_data.get('username', 'N/A')),
            ("Full Name:", self.user_data.get('full_name', 'Not set')),
            ("Email:", self.user_data.get('email', 'Not set')),
            ("Phone:", self.user_data.get('phone', 'Not set')),
            ("Age:", self.user_data.get('age', 'Not set'))
        ]

        for label, value in info_details:
            row = tk.Frame(card_container, bg=COLORS['white'])
            row.pack(fill="x", padx=15, pady=3)
            tk.Label(
                row,
                text=label,
                font=("Arial", 9, "bold"),
                bg=COLORS['white'],
                width=12,
                anchor="w"
            ).pack(side="left")
            tk.Label(
                row,
                text=str(value),
                font=("Arial", 9),
                bg=COLORS['white'],
                anchor="w",
                wraplength=150
            ).pack(side="left")

        # Action buttons
        btn_frame = tk.Frame(card_container, bg=COLORS['white'])
        btn_frame.pack(pady=10, padx=15)

        tk.Button(
            btn_frame,
            text="Edit Profile",
            command=lambda: [hover_card.withdraw(), self.open_edit_profile()],
            bg=COLORS['info'],
            fg=COLORS['white'],
            font=("Arial", 9, "bold"),
            width=12,
            cursor="hand2"
        ).pack(side="left", padx=3)

        tk.Button(
            btn_frame,
            text="Change Password",
            command=lambda: [hover_card.withdraw(), self.open_change_password()],
            bg=COLORS['purple'],
            fg=COLORS['white'],
            font=("Arial", 9, "bold"),
            width=14,
            cursor="hand2"
        ).pack(side="left", padx=3)

        # Hover logic
        hide_timer = [None]
        is_pinned = [False]

        def toggle_pin(event):
            is_pinned[0] = not is_pinned[0]
            if is_pinned[0]:
                if hide_timer[0]:
                    self.window.after_cancel(hide_timer[0])
                    hide_timer[0] = None
                show_hover_card(event)
                profile_btn.config(text="📌")
            else:
                hover_card.withdraw()
                profile_btn.config(text="👤")

        def show_hover_card(event):
            if hide_timer[0]:
                self.window.after_cancel(hide_timer[0])
                hide_timer[0] = None
            x = user_info_frame.winfo_rootx()
            y = user_info_frame.winfo_rooty() + user_info_frame.winfo_height() + 5
            hover_card.geometry(f"+{x}+{y}")
            hover_card.deiconify()
            hover_card.lift()

        def schedule_hide(event):
            if not is_pinned[0]:
                hide_timer[0] = self.window.after(300, hover_card.withdraw)

        def cancel_hide(event):
            if hide_timer[0]:
                self.window.after_cancel(hide_timer[0])
                hide_timer[0] = None

        profile_btn.bind("<Button-1>", toggle_pin)
        user_info_frame.bind("<Enter>", show_hover_card)
        user_info_frame.bind("<Leave>", schedule_hide)
        username_label.bind("<Enter>", show_hover_card)
        username_label.bind("<Leave>", schedule_hide)
        hover_card.bind("<Enter>", cancel_hide)
        hover_card.bind("<Leave>", schedule_hide)
        card_container.bind("<Enter>", cancel_hide)
        card_container.bind("<Leave>", schedule_hide)

    def create_main_content(self):
        """Create main content area"""
        self.content_frame = tk.Frame(self.window, bg=COLORS['light_gray'])
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        welcome_label = tk.Label(
            self.content_frame,
            text=f"Welcome back, {self.user_data['username']}!",
            font=("Arial", 24, "bold"),
            bg=COLORS['light_gray'],
            fg=COLORS['primary']
        )
        welcome_label.pack(pady=30)

        info_label = tk.Label(
            self.content_frame,
            text="Hover over your profile in the top-left corner\nto view your account information",
            font=("Arial", 12),
            bg=COLORS['light_gray'],
            fg=COLORS['dark_gray']
        )
        info_label.pack(pady=20)

        # Camera button
        if CAMERA_AVAILABLE:
            self.camera_btn = tk.Button(
                self.content_frame,
                text="📷 Open Camera",
                command=self.toggle_camera,
                bg=COLORS['info'],
                fg=COLORS['white'],
                font=("Arial", 14, "bold"),
                width=20,
                height=2,
                cursor="hand2"
            )
            self.camera_btn.pack(pady=30)
        else:
            tk.Label(
                self.content_frame,
                text="⚠️ Camera unavailable\nInstall: pip install opencv-python pillow",
                font=("Arial", 11),
                bg=COLORS['light_gray'],
                fg=COLORS['danger']
            ).pack(pady=30)

    def toggle_camera(self):
        """Toggle camera on/off"""
        if self.camera_active:
            self.close_camera()
        else:
            self.open_camera()

    def open_camera(self):
        """Open camera in expanded dashboard"""
        if self.camera_active:
            return

        # Expand window
        self.window.geometry("800x900")

        # Update button
        self.camera_btn.config(text="❌ Close Camera", bg=COLORS['danger'])

        # Create camera frame
        self.camera_frame = tk.Frame(self.content_frame, bg=COLORS['dark_gray'], relief="solid", borderwidth=2)
        self.camera_frame.pack(pady=20, padx=10, fill="both", expand=True)

        # Title
        tk.Label(
            self.camera_frame,
            text="📷 Live Camera Feed",
            font=("Arial", 16, "bold"),
            bg=COLORS['dark_gray'],
            fg=COLORS['white']
        ).pack(pady=10)

        # Camera display label
        self.camera_label = tk.Label(self.camera_frame, bg=COLORS['dark_gray'])
        self.camera_label.pack(pady=10)

        # Status label
        self.status_label = tk.Label(
            self.camera_frame,
            text="Initializing camera...",
            font=("Arial", 11),
            bg=COLORS['dark_gray'],
            fg=COLORS['white']
        )
        self.status_label.pack(pady=10)

        # Start camera
        self.start_camera()

    def start_camera(self):
        """Start camera capture"""
        try:
            self.cap = cv2.VideoCapture(0)

            if not self.cap.isOpened():
                self.status_label.config(text="❌ Error: Could not open camera", fg=COLORS['danger'])
                messagebox.showerror("Camera Error", "Could not open camera. Please check if your camera is connected.")
                self.close_camera()
                return

            self.camera_active = True
            self.status_label.config(text="✅ Camera active", fg=COLORS['success'])
            self.update_camera_feed()

        except Exception as e:
            messagebox.showerror("Camera Error", f"Failed to start camera: {str(e)}")
            self.close_camera()

    def update_camera_feed(self):
        """Update camera feed continuously"""
        if self.camera_active and self.cap is not None:
            ret, frame = self.cap.read()

            if ret:
                # Convert frame from BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Resize frame to fit window
                frame = cv2.resize(frame, (640, 480))

                # Convert to PIL Image
                img = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(image=img)

                # Update label
                self.camera_label.config(image=img_tk)
                self.camera_label.image = img_tk

                # Schedule next update
                self.window.after(10, self.update_camera_feed)
            else:
                self.status_label.config(text="❌ Error: Failed to read frame", fg=COLORS['danger'])
                self.close_camera()

    def close_camera(self):
        """Close camera and restore window size"""
        self.camera_active = False

        if self.cap is not None:
            self.cap.release()
            self.cap = None

        if self.camera_frame is not None:
            self.camera_frame.destroy()
            self.camera_frame = None

        # Restore window size
        self.window.geometry("800x600")

        # Update button
        if hasattr(self, 'camera_btn'):
            self.camera_btn.config(text="📷 Open Camera", bg=COLORS['info'])

        print("Camera closed")

    def open_edit_profile(self):
        """Open edit profile window"""
        EditProfileWindow(self.window, self.user_data, self.db, self.email_service, self.refresh_dashboard)

    def open_change_password(self):
        """Open change password window"""
        ChangePasswordWindow(self.window, self.user_data, self.db, self.email_service)

    def refresh_dashboard(self):
        """Refresh dashboard with updated user data"""
        # Save camera state
        was_camera_active = self.camera_active

        # Close camera if open
        if self.camera_active:
            self.close_camera()

        # Get updated user data
        updated_user = self.db.get_user_by_id(self.user_data['id'])
        self.user_data = updated_user

        # Update all UI elements without destroying window
        self.refresh_ui()

        # Reopen camera if it was active
        if was_camera_active and CAMERA_AVAILABLE:
            self.window.after(100, self.open_camera)

    def refresh_ui(self):
        """Refresh UI elements with updated user data"""
        # Update window title if needed
        self.window.title("Dashboard")

        # No need to rebuild entire UI, user data is already updated
        # The hover card will show new data on next hover

    def logout(self):
        """Logout and return to login"""
        # Close camera if open
        if self.camera_active:
            self.close_camera()

        self.window.destroy()
        from auth_windows import LoginWindow
        LoginWindow().run()


class EditProfileWindow:
    """Edit profile window class"""

    def __init__(self, parent, user_data, db, email_service, refresh_callback):
        self.parent = parent
        self.user_data = user_data
        self.db = db
        self.email_service = email_service
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Edit Profile")
        self.window.geometry("500x500")
        self.window.configure(bg=COLORS['white'])
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        """Setup edit profile UI"""
        tk.Label(
            self.window,
            text="Edit Your Profile",
            font=("Arial", 18, "bold"),
            bg=COLORS['white']
        ).pack(pady=20)

        fields = [
            ("Full Name:", self.user_data.get('full_name', '')),
            ("Email:", self.user_data.get('email', '')),
            ("Phone:", self.user_data.get('phone', '')),
            ("Age:", self.user_data.get('age', ''))
        ]

        self.entries = {}

        for label, value in fields:
            tk.Label(
                self.window,
                text=label,
                bg=COLORS['white'],
                fg="black",
                font=("Arial", 11)
            ).pack(pady=5)
            entry = tk.Entry(self.window, width=35, font=("Arial", 11))
            entry.insert(0, str(value) if value else '')
            entry.pack()
            self.entries[label.replace(':', '').lower().replace(' ', '_')] = entry

        tk.Button(
            self.window,
            text="Save Changes",
            command=self.verify_and_save,
            bg=COLORS['success'],
            fg=COLORS['white'],
            font=("Arial", 12, "bold"),
            width=20,
            height=2
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="Cancel",
            command=self.window.destroy,
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            font=("Arial", 10),
            width=20
        ).pack()

    def verify_and_save(self):
        """Verify email if changed, then save"""
        email = self.entries['email'].get().strip()
        if not email:
            messagebox.showerror("Error", "Email is required")
            return

        if email != self.user_data.get('email'):
            code = self.email_service.generate_verification_code()
            self.email_service.store_verification(email, code)

            if self.email_service.send_verification_email(email, code):
                VerificationWindow(
                    self.window,
                    email,
                    self.email_service,
                    self.save_profile,
                    "Verify New Email"
                )
            else:
                messagebox.showerror("Error", "Failed to send verification email.")
        else:
            self.save_profile()

    def save_profile(self):
        """Save profile changes"""
        try:
            age_val = self.entries['age'].get()
            age = int(age_val) if age_val else None

            self.db.update_user_profile(
                self.user_data['id'],
                self.entries['full_name'].get(),
                self.entries['email'].get(),
                self.entries['phone'].get(),
                age
            )

            messagebox.showinfo("Success", "Profile updated successfully!")
            self.window.destroy()
            self.refresh_callback()
        except ValueError:
            messagebox.showerror("Error", "Age must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile: {str(e)}")


class ChangePasswordWindow:
    """Change password window class"""

    def __init__(self, parent, user_data, db, email_service):
        self.parent = parent
        self.user_data = user_data
        self.db = db
        self.email_service = email_service

        self.window = tk.Toplevel(parent)
        self.window.title("Change Password")
        self.window.geometry("450x450")
        self.window.configure(bg=COLORS['white'])
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        """Setup change password UI"""
        tk.Label(
            self.window,
            text="Change Password",
            font=("Arial", 18, "bold"),
            bg=COLORS['white']
        ).pack(pady=20)

        tk.Label(self.window, text="Current Password:", bg=COLORS['white'], font=("Arial", 11)).pack(pady=5)
        self.entry_current = tk.Entry(self.window, width=30, show="*", font=("Arial", 11))
        self.entry_current.pack()

        tk.Label(self.window, text="New Password:", bg=COLORS['white'], font=("Arial", 11)).pack(pady=5)
        self.entry_new = tk.Entry(self.window, width=30, show="*", font=("Arial", 11))
        self.entry_new.pack()

        tk.Label(self.window, text="Confirm New Password:", bg=COLORS['white'], font=("Arial", 11)).pack(pady=5)
        self.entry_confirm = tk.Entry(self.window, width=30, show="*", font=("Arial", 11))
        self.entry_confirm.pack()

        tk.Button(
            self.window,
            text="Change Password",
            command=self.verify_and_change,
            bg=COLORS['warning'],
            fg=COLORS['white'],
            font=("Arial", 12, "bold"),
            width=20,
            height=2
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="Cancel",
            command=self.window.destroy,
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            font=("Arial", 10),
            width=20
        ).pack()

    def verify_and_change(self):
        """Verify current password and change"""
        current_pass = self.entry_current.get()
        new_pass = self.entry_new.get()
        confirm_pass = self.entry_confirm.get()

        if not all([current_pass, new_pass, confirm_pass]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Error", "New passwords do not match")
            return

        try:
            if not self.db.verify_password(self.user_data['id'], current_pass):
                messagebox.showerror("Error", "Current password is incorrect")
                return

            email = self.user_data.get('email')
            if not email:
                messagebox.showerror("Error", "No email address found. Please add an email to your profile first.")
                return

            code = self.email_service.generate_verification_code()
            self.email_service.store_verification(email, code)

            if self.email_service.send_verification_email(email, code):
                VerificationWindow(
                    self.window,
                    email,
                    self.email_service,
                    lambda: self.change_password(new_pass),
                    "Verify Identity"
                )
            else:
                messagebox.showerror("Error", "Failed to send verification email.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change password: {str(e)}")

    def change_password(self, new_pass):
        """Complete password change"""
        try:
            self.db.update_user_password(self.user_data['id'], new_pass)
            messagebox.showinfo("Success", "Password changed successfully!")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change password: {str(e)}")