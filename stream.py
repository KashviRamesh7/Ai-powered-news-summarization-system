import streamlit as st
from textblob import TextBlob
from newspaper import Article
import dateutil.parser
import re

def summarize(url):
    if not url:
        return "Error: Please enter a valid URL.", "", "", "", ""
    
    article = Article(url)
    try:
        article.download()
        article.parse()
        article.nlp()
    except Exception as e:
        return f"Error: {str(e)}", "", "", "", ""

    # Extract and format the publication date
    pub_date = article.publish_date
    if not pub_date:
        meta_date = re.search(r'\d{4}-\d{2}-\d{2}', str(article.meta_data))
        if meta_date:
            pub_date = dateutil.parser.parse(meta_date.group()).date()
    formatted_date = pub_date.strftime('%B %d, %Y') if pub_date else "N/A"
    
    # Sentiment Analysis
    analysis = TextBlob(article.text)
    sentiment_result = f'Polarity: {analysis.polarity}, Sentiment: {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}'
    
    return article.title, ', '.join(article.authors) if article.authors else "N/A", formatted_date, article.text, sentiment_result

# Streamlit UI
st.title("News Summarizer")

url = st.text_input("Enter the news article URL")

if st.button("Summarize"):
    title, author, publication, summary, sentiment = summarize(url)
    
    if "Error" in title:
        st.error(title)
    else:
        st.subheader("Title")
        st.write(title)
        
        st.subheader("Author/Authors")
        st.write(author)
        
        st.subheader("Publishing Date")
        st.write(publication)
        
        st.subheader("Summary")
        st.write(summary)
        
        st.subheader("Sentiment Analysis")
        st.write(sentiment)
