import feedparser  # For fetching RSS news feeds
from transformers import pipeline  # Hugging Face NLP model for summarization
import smtplib  # For sending emails
from email.mime.text import MIMEText  # Email formatting
from email.mime.multipart import MIMEMultipart  # Handling multi-part email messages


# Step 1: Fetch news from multiple RSS feeds
UK_RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/uk/rss.xml",
    "https://www.theguardian.com/uk/rss",
    "https://www.independent.co.uk/news/uk/rss",
    "https://www.telegraph.co.uk/news/rss.xml"
]

US_RSS_FEEDS = [
    "http://rss.cnn.com/rss/cnn_us.rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
]

def fetch_news_from_feeds(feed_urls):
    """Fetches news articles from multiple RSS feeds."""
    articles = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # Get the top 5 news articles
            articles.append({"title": entry.title, "link": entry.link, "summary": entry.summary})
    return articles

# Step 2: Summarize articles using Hugging Face NLP model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  # Load AI model

def summarize_text(text):
    """Summarizes the given text using the BART model."""
    input_length = len(text.split())
    max_len = max(10, min(50, input_length))  # Adjust max_length dynamically
    summary = summarizer(text, max_length=max_len, min_length=10, do_sample=False)  # Generate summary
    return summary[0]['summary_text']  # Extract summarized text

# Step 3: Send email with summarized news
def send_email(news_list):
    """Sends an email containing the summarized news."""
    sender_email = "stephaniesomade@gmail.com"  # Replace with sender email
    receiver_email = "stephaniesomadee@gmail.com"  # Replace with recipient email
    password = ""  # Use an app password for Gmail
    
    msg = MIMEMultipart()  # Create an email message object
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Your Daily UK and US News Summary"  # Email subject
    
    email_content = "<h2>Top News Summaries</h2>"  # Start building the email body
    for news in news_list:
        email_content += f"<h3>{news['title']}</h3>"  # Add news title
        email_content += f"<p>{news['summary']}</p>"  # Add summarized content
        email_content += f"<a href='{news['link']}'>Read More</a><br><br>"  # Add a 'Read More' link
    
    msg.attach(MIMEText(email_content, 'html'))  # Attach email content as HTML
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:  # Connect to Gmail's SMTP server securely
        server.login(sender_email, password)  # Log in to the email account
        server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email

# Running the pipeline
all_news_feeds = UK_RSS_FEEDS + US_RSS_FEEDS  # Combine UK and US feeds
news_articles = fetch_news_from_feeds(all_news_feeds)  # Fetch news articles

# Summarize each article
for article in news_articles:
    article['summary'] = summarize_text(article['summary'])

# Send summarized news via email
send_email(news_articles)

print("Email Sent!")  # Confirm successful email delivery
