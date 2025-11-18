# User Authentication System

A complete user authentication system with email verification using Tkinter and Supabase.

## 📁 Project Structure

```
project/
├── __init__.py                 # Package initializer (can be empty)
├── config.py                   # Configuration settings
├── database.py                 # Database manager
├── email_service.py            # Email service
├── verification_window.py      # Email verification window
├── auth_windows.py             # Login, Register, Forgot Password
├── dashboard.py                # Main dashboard
├── main.py                     # Application entry point
├── check_setup.py              # Setup verification script
└── requirements.txt            # Python dependencies
```

## 🚀 Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install supabase
```

### Step 2: Verify Setup

Run the setup verification script:
```bash
python check_setup.py
```

This will check:
- ✓ All required files are present
- ✓ All dependencies are installed

### Step 3: Configure Email (Optional)

Edit `config.py` and update:
```python
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
```

**Note:** For Gmail, you need to create an App Password:
1. Go to Google Account settings
2. Security → 2-Step Verification
3. App passwords → Generate new password

### Step 4: Run the Application

```bash
python main.py
```

## 🔧 Troubleshooting

### Issue: ModuleNotFoundError

**Solution 1:** Make sure all files are in the same directory
```bash
# Check your directory structure
ls -la
# or on Windows
dir
```

**Solution 2:** Create an empty `__init__.py` file
```bash
# On Linux/Mac
touch __init__.py

# On Windows
type nul > __init__.py
```

**Solution 3:** Run from the correct directory
```bash
cd C:\Users\singc\Downloads\cleaned
python main.py
```

### Issue: Supabase connection error

Check your `config.py`:
- Verify `SUPABASE_URL` is correct
- Verify `SUPABASE_KEY` is correct

### Issue: Email not sending

The app will still work - verification codes are printed to the console for testing:
```
==================================================
VERIFICATION CODE FOR user@example.com: 123456
==================================================
```

## 📝 Features

- ✅ User Registration with email verification
- ✅ Secure login
- ✅ Password reset with email verification
- ✅ Profile editing
- ✅ Password change
- ✅ User dashboard with hover profile card

## 🔐 Security Notes

- Passwords are hashed using SHA256
- Email verification required for sensitive operations
- Session management included

## 📞 Support

If you encounter any issues:
1. Run `python check_setup.py` first
2. Check that all files are in the same directory
3. Verify dependencies are installed
4. Check console output for error messages