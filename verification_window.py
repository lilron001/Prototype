# verification_window.py
"""Email verification window"""

import tkinter as tk
from tkinter import messagebox
from config import COLORS


class VerificationWindow:
    """Email verification window class"""
    
    def __init__(self, parent, email, email_service, callback, title="Email Verification"):
        self.parent = parent
        self.email = email
        self.email_service = email_service
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("450x380")
        self.window.configure(bg=COLORS['white'])
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup verification UI"""
        tk.Label(
            self.window,
            text="📧 Email Verification",
            font=("Arial", 18, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        ).pack(pady=20)
        
        tk.Label(
            self.window,
            text="A 6-digit verification code has been sent to:",
            font=("Arial", 10),
            bg=COLORS['white'],
            fg=COLORS['dark_gray']
        ).pack(pady=5)
        
        tk.Label(
            self.window,
            text=self.email,
            font=("Arial", 11, "bold"),
            bg=COLORS['white'],
            fg=COLORS['primary']
        ).pack(pady=5)
        
        tk.Label(
            self.window,
            text="Please check your inbox and enter the code below.",
            font=("Arial", 9),
            bg=COLORS['white'],
            fg=COLORS['dark_gray']
        ).pack(pady=10)
        
        tk.Label(
            self.window,
            text="Enter Verification Code:",
            bg=COLORS['white'],
            font=("Arial", 11, "bold")
        ).pack(pady=10)
        
        self.entry_code = tk.Entry(self.window, width=15, font=("Arial", 18, "bold"), justify="center")
        self.entry_code.pack(pady=5)
        self.entry_code.focus()
        
        tk.Label(
            self.window,
            text="(6-digit code)",
            font=("Arial", 8),
            bg=COLORS['white'],
            fg=COLORS['secondary']
        ).pack()
        
        # Bind Enter key to verify
        self.entry_code.bind('<Return>', lambda e: self.verify_code())
        
        tk.Button(
            self.window,
            text="Verify Code",
            command=self.verify_code,
            bg=COLORS['success'],
            fg=COLORS['white'],
            font=("Arial", 12, "bold"),
            width=18,
            height=2
        ).pack(pady=15)
        
        tk.Button(
            self.window,
            text="Resend Code",
            command=self.resend_code,
            bg=COLORS['info'],
            fg=COLORS['white'],
            font=("Arial", 10),
            width=18
        ).pack(pady=5)
        
        tk.Button(
            self.window,
            text="Cancel",
            command=self.cancel,
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            font=("Arial", 9),
            width=18
        ).pack(pady=5)
    
    def verify_code(self):
        """Verify the entered code"""
        entered_code = self.entry_code.get().strip()
        
        if not entered_code:
            messagebox.showerror("Error", "Please enter the verification code.")
            return
        
        if self.email_service.verify_code(self.email, entered_code):
            messagebox.showinfo("Success", "✓ Email verified successfully!")
            self.email_service.remove_verification(self.email)
            self.window.destroy()
            self.callback()
        else:
            messagebox.showerror("Error", "❌ Invalid verification code. Please check and try again.")
            self.entry_code.delete(0, tk.END)
    
    def resend_code(self):
        """Resend verification code"""
        pending_data = self.email_service.get_pending_data(self.email)
        
        if pending_data:
            new_code = self.email_service.generate_verification_code()
            pending_data['code'] = new_code
            
            if self.email_service.send_verification_email(self.email, new_code):
                messagebox.showinfo("Success", "📧 New verification code sent! Please check your email.")
                self.entry_code.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to resend code. Please try again.")
        else:
            messagebox.showerror("Error", "Verification session expired. Please start over.")
            self.window.destroy()
    
    def cancel(self):
        """Cancel verification"""
        self.email_service.remove_verification(self.email)
        self.window.destroy()