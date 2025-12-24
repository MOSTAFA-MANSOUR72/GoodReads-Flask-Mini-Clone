# Book App
Here is the live and hosted website to check out.
<br>
Give it a try:
https://mostafamansour.pythonanywhere.com
## Overview

Book App is a web-based application built with Flask, designed for book enthusiasts to manage their reading lists, track reading progress, and connect with other users. Users can add books, mark them as currently reading or completed, follow other users, and view friends' reading activities. The application features a user-friendly interface with Bootstrap styling and supports image uploads for book covers and user profiles.

## Features

- **User Authentication**: Register, log in, and log out with secure password hashing.
- **Book Management**: Add, edit, and delete books with details like title, author, description, page count, and cover image.
- **Reading Progress**: Track currently reading books, update page progress, and mark books as completed.
- **Social Features**: Follow/unfollow users, view friends' activities (e.g., adding books, updating progress).
- **Profile**: View user stats, including the number of books currently reading, completed, and owned.
- **Explore**: Browse all books and users, with options to add books to your reading list or follow users.

## Project Structure

```
book-app/
├── web/
│   ├── static/                # Static files (CSS, JS, uploaded images)
│   ├── templates/             # HTML templates
│   │   ├── add-book.html      # Form to add a new book
│   │   ├── base.html          # Base template with footer
│   │   ├── container.html     # Template for displaying book lists (My Books, Completed Books)
│   │   ├── current_reading_books.html # Home page with currently reading books and friends' activities
│   │   ├── edit-book.html     # Form to edit book details
│   │   ├── explore.html       # Page to browse books and users
│   │   ├── home.html          # Main layout with navigation bar
│   │   ├── login.html         # Login form
│   │   ├── profile.html       # User profile page
│   │   ├── register.html      # Registration form
│   ├── __init__.py            # Flask app initialization
│   ├── auth.py                # Authentication routes (login, register, logout)
│   ├── models.py              # Database models (User, Book, Activity, relationships)
│   ├── views.py               # Application routes (home, book management, social features)
├── main.py                    # Entry point to run the Flask app
├── site.db                    # SQLite database (created on first run)
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- A modern web browser

## Installation


1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```


2. **Run the Application**:
   ```bash
   python main.py
   ```
   The app will start in debug mode at `http://127.0.0.1:5000`.

## Configuration

- **Secret Key**: The `SECRET_KEY` in `web/__init__.py` is set to `'your_secret_key'`. Replace it with a secure, random string in production:
  ```python
  app.config['SECRET_KEY'] = 'your-secure-random-string'
  ```
- **Upload Folder**: The `UPLOAD_FOLDER` is set to `web/static/`. Ensure this directory is writable.
- **Database**: The app uses SQLite (`site.db`). The database is automatically created on the first run.

----------

### 🎨 **Design Improvements:**

- **Modern UI**: Replaced Bootstrap 3 with Tailwind CSS
- **Consistent Color Scheme**: Primary blue theme with accent colors
- **Card-based Layout**: Clean, modern card designs throughout
- **Responsive Design**: Mobile-first approach with proper breakpoints
- **Visual Hierarchy**: Better typography and spacing


### 🚀 **Enhanced Features:**

- **Interactive Navigation**: Dropdown menus and mobile-responsive nav
- **Progress Tracking**: Visual progress bars for reading status
- **Improved Forms**: Better file uploads and form validation
- **Social Features**: Enhanced friend activities and user interactions
- **Status Indicators**: Clear visual feedback for book states


### 📱 **User Experience:**

- **Mobile Responsive**: Works perfectly on all device sizes
- **Accessibility**: Proper labels, focus states, and semantic HTML
- **Smooth Animations**: Hover effects and transitions
- **Intuitive Icons**: Font Awesome 6 icons throughout
- **Loading States**: Better visual feedback


### 🔧 **Technical Upgrades:**

- **Alpine.js**: For interactive components (dropdowns, mobile menu)
- **Modern CSS**: Flexbox and Grid layouts
- **Performance**: Optimized loading and rendering
- **Maintainable**: Clean, organized code structure
