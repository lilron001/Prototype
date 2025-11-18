# auth_windows.py
"""Authentication windows: Login, Register, Forgot Password"""

import tkinter as tk
from tkinter import messagebox
from config import COLORS
from database import DatabaseManager
from email_service import EmailService
from verification_window import VerificationWindow
from dashboard import Dashboard


class LoginWindow:
    """Login window class"""

    def __init__(self):
        self.db = DatabaseManager()
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry("600x420")
        self.window.configure(bg=COLORS['white'])
        self.setup_ui()

    def setup_ui(self):
        """Setup login UI"""
        tk.Label(
            self.window,
            text="Login to Your Account",
            font=("Arial", 20, "bold"),
            bg=COLORS['white']
        ).pack(pady=30)

        tk.Label(
            self.window,
            text="Username:",
            bg=COLORS['white'],
            fg="black",
            font=("Arial", 11)
        ).pack(pady=5)
        self.entry_username = tk.Entry(self.window, width=30, font=("Arial", 11))
        self.entry_username.pack()

        tk.Label(
            self.window,
            text="Password:",
            bg=COLORS['white'],
            fg="black",
            font=("Arial", 11)
        ).pack(pady=5)
        self.entry_password = tk.Entry(self.window, width=30, show="*", font=("Arial", 11))
        self.entry_password.pack()

        tk.Button(
            self.window,
            text="Login",
            command=self.login,
            bg=COLORS['primary'],
            fg=COLORS['white'],
            font=("Arial", 12, "bold"),
            width=20,
            height=2
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="Create Account",
            command=self.open_register,
            bg=COLORS['info'],
            fg=COLORS['white'],
            font=("Arial", 10),
            width=20
        ).pack(pady=5)

        tk.Button(
            self.window,
            text="Forgot Password",
            command=self.open_forgot,
            bg=COLORS['white'],
            fg=COLORS['info'],
            font=("Arial", 9, "underline"),
            relief="flat"
        ).pack()

    def login(self):
        """Handle login"""
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            user = self.db.get_user_by_username(username)

            if user:
                if user['password'] == self.db.hash_password(password):
                    messagebox.showinfo("Login", "Login successful!")
                    self.window.destroy()
                    Dashboard(user)
                else:
                    messagebox.showerror("Login", "Invalid password")
            else:
                messagebox.showerror("Login", "Username not found")
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")

    def open_register(self):
        """Open registration window"""
        self.window.destroy()
        RegisterWindow()

    def open_forgot(self):
        """Open forgot password window"""
        self.window.destroy()
        ForgotPasswordWindow()

    def run(self):
        """Run the window"""
        self.window.mainloop()


class RegisterWindow:
    """Registration window class"""

    def __init__(self):
        self.db = DatabaseManager()
        self.email_service = EmailService()
        self.window = tk.Tk()
        self.window.title("Register")
        self.window.geometry("600x500")
        self.window.configure(bg=COLORS['white'])
        self.setup_ui()
        self.window.mainloop()

    def setup_ui(self):
        """Setup registration UI"""
        tk.Label(
            self.window,
            text="Create New Account",
            font=("Arial", 20, "bold"),
            bg=COLORS['white']
        ).pack(pady=30)

        tk.Label(self.window, text="Username:", bg=COLORS['white'], fg="black", font=("Arial", 11)).pack(pady=5)
        self.entry_username = tk.Entry(self.window, width=30, font=("Arial", 11))
        self.entry_username.pack()

        tk.Label(self.window, text="Email:", bg=COLORS['white'], fg="black", font=("Arial", 11)).pack(pady=5)
        self.entry_email = tk.Entry(self.window, width=30, font=("Arial", 11))
        self.entry_email.pack()

        tk.Label(self.window, text="Password:", bg=COLORS['white'], fg="black", font=("Arial", 11)).pack(pady=5)
        self.entry_password = tk.Entry(self.window, width=30, show="*", font=("Arial", 11))
        self.entry_password.pack()

        tk.Label(self.window, text="Confirm Password:", bg=COLORS['white'], fg="black", font=("Arial", 11)).pack(pady=5)
        self.entry_confirm = tk.Entry(self.window, width=30, show="*", font=("Arial", 11))
        self.entry_confirm.pack()

        tk.Button(
            self.window,
            text="Register",
            command=self.verify_and_register,
            bg=COLORS['success'],
            fg=COLORS['white'],
            font=("Arial", 12, "bold"),
            width=20,
            height=2
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="Back to Login",
            command=self.back_to_login,
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            font=("Arial", 10),
            width=20
        ).pack()

    def verify_and_register(self):
        """Verify and start registration process"""
        username = self.entry_username.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get()
        confirm_pass = self.entry_confirm.get()

        if not username or not email or not password or not confirm_pass:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if password != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if '@' not in email or '.' not in email:
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        try:
            if self.db.check_username_exists(username):
                messagebox.showerror("Error", "Username already exists")
                return

            if self.db.check_email_exists(email):
                messagebox.showerror("Error", "Email already registered")
                return

            # Show confirmation window
            self.show_confirmation(username, email, password)
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")

    def show_confirmation(self, username, email, password):
        """Show confirmation dialog"""
        confirm_window = tk.Toplevel(self.window)
        confirm_window.title("Confirm Account Creation")
        confirm_window.geometry("450x350")
        confirm_window.configure(bg=COLORS['white'])
        confirm_window.grab_set()

        tk.Label(
            confirm_window,
            text="Confirm Account Details",
            font=("Arial", 18, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        ).pack(pady=20)

        tk.Label(
            confirm_window,
            text="Please confirm your account details before\nwe send a verification code to your email.",
            font=("Arial", 10),
            bg=COLORS['white'],
            fg=COLORS['dark_gray']
        ).pack(pady=10)

        details_frame = tk.Frame(confirm_window, bg=COLORS['white'])
        details_frame.pack(pady=20, padx=30)

        details = [
            ("Username:", username),
            ("Email:", email),
            ("Password:", "*" * len(password))
        ]

        for label, value in details:
            row = tk.Frame(details_frame, bg=COLORS['white'])
            row.pack(fill="x", pady=5)
            tk.Label(row, text=label, font=("Arial", 11, "bold"), bg=COLORS['white'], width=12, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=("Arial", 11), bg=COLORS['white'], anchor="w").pack(side="left")

        tk.Label(
            confirm_window,
            text="⚠️ Make sure your email is correct!",
            font=("Arial", 9),
            bg=COLORS['white'],
            fg=COLORS['warning']
        ).pack(pady=10)

        def proceed():
            code = self.email_service.generate_verification_code()
            self.email_service.store_verification(email, code, username, password)

            messagebox.showinfo("Sending...", "Please wait while we send the verification code to your email...")

            if self.email_service.send_verification_email(email, code):
                confirm_window.destroy()
                VerificationWindow(
                    self.window,
                    email,
                    self.email_service,
                    lambda: self.complete_registration(username, email, password)
                )
            else:
                messagebox.showerror("Error", "Failed to send verification email. Please try again.")

        btn_frame = tk.Frame(confirm_window, bg=COLORS['white'])
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="Confirm & Send Code",
            command=proceed,
            bg=COLORS['success'],
            fg=COLORS['white'],
            font=("Arial", 11, "bold"),
            width=18,
            height=2
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=confirm_window.destroy,
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            font=("Arial", 10),
            width=10,
            height=2
        ).pack(side="left", padx=5)

    def complete_registration(self, username, email, password):
        """Complete user registration"""
        try:
            self.db.create_user(username, email, password)
            messagebox.showinfo("Success", "✓ Account created successfully! You can now login.")
            self.window.destroy()
            LoginWindow().run()
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")

    def back_to_login(self):
        """Return to login window"""
        self.window.destroy()
        LoginWindow().run()


class ForgotPasswordWindow:
    """Forgot password window class"""

    def __init__(self):
        self.db = DatabaseManager()
        self.email_service = EmailService()
        self.window = tk.Tk()
        self.window.title("Forgot Password")
        self.window.geometry("600x500")
        self.window.configure(bg=COLORS['white'])
        self.setup_ui()
        self.window.mainloop()

    def setup_ui(self):
        """Setup forgot password UI"""
        tk.Label(
            self.window,
            text="Reset Password",
            font=("Arial", 20, "bold"),
            bg=COLORS['white']
        ).pack(pady=30)

        tk.Label(self.window, text="Username:", bg=COLORS['white'], fg="black", font=("Arial", 11)).pack(pady=5)
        self.entry_username = tk.Entry(self.window, width=30, font=("Arial", 11))
        self.entry_username.pack()

        tk.Label(self.window, text="Email:", bg=COLORS['white'], fg="black", font=("Arial", 11)).pack(pady=5)
        self.entry_email = tk.Entry(self.window, width=30, font=("Arial", 11))
        self.entry_email.pack()

        tk.Label(self.window, text="New Password:", bg=COLORS['white'], fg="black", font=("Arial", 11)).pack(pady=5)
        self.entry_newpass = tk.Entry(self.window, width=30, show="*", font=("Arial", 11))
        self.entry_newpass.pack()

        tk.Label(self.window, text="Confirm Password:", bg=COLORS['white'], fg="black", font=("Arial", 11)).pack(pady=5)
        self.entry_confirm = tk.Entry(self.window, width=30, show="*", font=("Arial", 11))
        self.entry_confirm.pack()

        tk.Button(
            self.window,
            text="Reset Password",
            command=self.verify_and_reset,
            bg=COLORS['danger'],
            fg=COLORS['white'],
            font=("Arial", 12, "bold"),
            width=20,
            height=2
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="Back to Login",
            command=self.back_to_login,
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            font=("Arial", 10),
            width=20
        ).pack()

    def verify_and_reset(self):
        """Verify and reset password"""
        username = self.entry_username.get()
        email = self.entry_email.get().strip()
        new_pass = self.entry_newpass.get()
        confirm_pass = self.entry_confirm.get()

        if not all([username, email, new_pass, confirm_pass]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            user = self.db.get_user_by_username(username)
            if not user:
                messagebox.showerror("Error", "Username not found")
                return

            if user.get('email') != email:
                messagebox.showerror("Error", "Email does not match the account")
                return

            code = self.email_service.generate_verification_code()
            self.email_service.store_verification(email, code)

            if self.email_service.send_verification_email(email, code):
                VerificationWindow(
                    self.window,
                    email,
                    self.email_service,
                    lambda: self.complete_reset(username, new_pass),
                    "Verify Email to Reset Password"
                )
            else:
                messagebox.showerror("Error", "Failed to send verification email.")
        except Exception as e:
            messagebox.showerror("Error", f"Password reset failed: {str(e)}")

    def complete_reset(self, username, new_pass):
        """Complete password reset"""
        try:
            user = self.db.get_user_by_username(username)
            self.db.update_user_password(user['id'], new_pass)
            messagebox.showinfo("Success", "Password reset successfully!")
            self.window.destroy()
            LoginWindow().run()
        except Exception as e:
            messagebox.showerror("Error", f"Password reset failed: {str(e)}")

    def back_to_login(self):
        """Return to login window"""
        self.window.destroy()
        LoginWindow().run()