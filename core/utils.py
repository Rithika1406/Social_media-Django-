import re
from django.urls import reverse
from .models import Notification
from collections import Counter

def parse_tags_and_mentions(content):
    # Convert #hashtag into clickable links
    content = re.sub(r'#(\w+)', r'<a href="/hashtag/\1/">#\1</a>', content)
    # Convert @username into profile links
    content = re.sub(r'@(\w+)', r'<a href="/profile/\1/">@\1</a>', content)
    return content


def create_notification(recipient, message, link=""):
    if recipient != None and recipient != message:
        Notification.objects.create(
            recipient=recipient,
            message=message,
            link=link
        )



def extract_hashtags_from_text(text):
    return re.findall(r"#(\w+)", text)

def get_trending_hashtags():
    from .models import Post
    all_posts = Post.objects.all()
    hashtags = []
    for post in all_posts:
        hashtags.extend(extract_hashtags_from_text(post.content))
    count = Counter(hashtags)
    return count.most_common(10)