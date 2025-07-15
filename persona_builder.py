
import os
import nltk
from collections import Counter
from openai import OpenAI
import praw
import re

# Load env.txt manually
env_path = r"D:\07-SANKET\GEN AI\env.txt"
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            os.environ[key.strip()] = value.strip()

# Download NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Initialize clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent="reddit-persona-builder"
)

# Functions


def extract_username(url_or_username):
    # full URL or  username
    if "reddit.com/user/" in url_or_username:
        return url_or_username.rstrip('/').split("/")[-1]
    return url_or_username


def fetch_user_content(username, post_limit=20, comment_limit=20):
    redditor = reddit.redditor(username)
    posts = []
    comments = []

    for submission in redditor.submissions.new(limit=post_limit):
        posts.append({
            'title': submission.title,
            'body': submission.selftext
        })

    for comment in redditor.comments.new(limit=comment_limit):
        comments.append({
            'body': comment.body
        })

    return posts, comments


def simple_nlp_analysis(posts, comments):
    text = " ".join(
        [p['title'] + " " + p['body'] for p in posts] +
        [c['body'] for c in comments]
    )
    tokens = nltk.word_tokenize(text.lower())
    stopwords = set(nltk.corpus.stopwords.words('english'))
    keywords = [t for t in tokens if t.isalpha() and t not in stopwords]
    top_keywords = [kw for kw, count in Counter(keywords).most_common(10)]
    return top_keywords


def build_persona_with_llm(username, posts, comments, keywords):
    post_texts = "\n".join([f"- {p['title']} | {p['body']}" for p in posts])
    comment_texts = "\n".join([f"- {c['body']}" for c in comments])

    prompt = f"""
You are an analyst. Build a detailed user persona for Reddit user '{username}'.
For each characteristic (like interests, tone, activity, personality etc):
- Describe the trait.
- Add a citation: mention the post title or comment snippet you used to extract it.

Here are the user's recent posts:
{post_texts}

Here are the user's recent comments:
{comment_texts}

Top keywords: {keywords}

Return the persona as readable text with citations.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful analyst."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# Run
url = input("Enter Reddit profile URL or username: ").strip()
username = extract_username(url)
print(f"Fetching data for u/{username}...")

posts, comments = fetch_user_content(username)
print(f"Got {len(posts)} posts and {len(comments)} comments.")

keywords = simple_nlp_analysis(posts, comments)
print(f"Top keywords: {keywords}")

persona = build_persona_with_llm(username, posts, comments, keywords)

print("\n=== Generated User Persona ===\n")
print(persona)

# Save to text file
output_filename = f"{username}_persona.txt"
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(persona)

print(f"\n Persona saved to: {output_filename}")