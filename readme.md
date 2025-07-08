
# 📲 Social Media Feed App (Django 5.2)

A simple but feature-rich social media platform built with Django 5.2. Users can sign up, post content (with text, images, or videos), like and comment on posts, follow other users, receive notifications, and explore trending hashtags.

---

## 🚀 Features

- 👤 **User Authentication** (Sign Up / Login / Logout)
- 📝 **Create Posts** with content, image, or video
- ❤️ **Like** and 💬 **Comment** on posts
- 🔍 **Search** users by username, first or last name
- 👥 **Follow / Unfollow** users
- 📲 **Notifications** for likes, comments, and mentions
- 🏷 **Hashtag Parsing** and hashtag-based feeds
- 📡 **Explore Feed** with trending hashtags
- 🧑‍💻 **Profile Pages** (both for users and guests)
- ⚙️ **Change Username** from profile settings

---

## 🛠️ Tech Stack

- **Backend**: Django 5.2
- **Frontend**: HTML + Bootstrap 5 (via `django-bootstrap5`)
- **Database**: SQLite (default)
- **Media Handling**: Image & Video upload
- **Authentication**: Django built-in auth system

---

## 📦 Dependencies

Install the following packages in your Python environment:

```bash
pip install -r requirements.txt
````

<details>
<summary>📄 <code>requirements.txt</code> (basic)</summary>

```txt
Django==5.2
django-bootstrap5
pillow
```

</details>

---

## 📁 Project Structure (Important Apps & Files)

```
social_media_feed/
│
├── core/                  # Main app
│   ├── models.py          # Models: Post, Comment, Like, Follow, Notification, Tag
|   ├── templates/         # HTML templates
│   ├── views.py           # All views for feed, post, follow, etc.
│   ├── forms.py           # Django forms for Post, Comment, Username change
│   ├── utils.py           # Tag/Mention parsing & notification helpers
│   └── urls.py            # Core app URL routing
│
├── media/                 # Uploaded images & videos (runtime)                
├── db.sqlite3             # SQLite DB
├── manage.py
└── social_media_feed/     # Project config
    └── settings.py
```

---

## 🖥️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Rithika1406/Social_media-Django-

cd social_media_feed
```

### 2️⃣ Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply migrations

```bash
python manage.py migrate
```

### 5️⃣ Run the development server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

---

## 🧪 Sample Test Users (Optional)

```txt
username: testuser1
password: testpass123
```

---

## 📌 TODO / Improvements

* Add unit tests
* Add support for notifications via email
* Improve video handling and compression
* Add private profiles & follow request system
* Add infinite scroll for feeds

---

## 🙌 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you would like to change.

