import streamlit as st
from newsapi import NewsApiClient
from textblob import TextBlob

# Set up News API key (replace with the actual key from https://www.newsapi.ai/)
newsapi_key = 'c17c7f4e-81c3-4246-94fc-83a2dfe5d817'
newsapi = NewsApiClient(api_key=newsapi_key)

# Streamlit app
def main():
    st.title("Stock News Sentiment Analysis")

    # User input for stock names
    stocks_input = st.text_input("Enter stock names separated by commas (e.g., TCS, Reliance):")
    stocks = [stock.strip() for stock in stocks_input.split(',')]

    if not stocks_input:
        st.warning("Please enter at least one stock name.")
        st.stop()

    # Fetch news articles for the specified stocks
    try:
        articles = fetch_news(stocks)
    except Exception as e:
        st.error(f"Error fetching news articles: {str(e)}")
        st.stop()

    if not articles:
        st.warning("No news articles found for the specified stocks.")
        st.stop()

    # Perform sentiment analysis
    sentiment_scores = analyze_sentiment(articles)

    # Display results in a table
    display_results(articles, sentiment_scores)

def fetch_news(stocks):
    articles = []
    for stock in stocks:
        try:
            # Fetch the latest 20 news articles for each stock
            news = newsapi.get_everything(q=stock, language='en', sort_by='publishedAt', page_size=20)
            articles.extend(news.get('articles', []))
        except Exception as e:
            st.error(f"Error fetching news for stock {stock}: {str(e)}")
    return articles

def analyze_sentiment(articles):
    sentiment_scores = []
    for article in articles:
        # Perform sentiment analysis using TextBlob
        analysis = TextBlob(article['title'])
        sentiment_scores.append(analysis.sentiment.polarity)
    return sentiment_scores

def display_results(articles, sentiment_scores):
    st.subheader("Results: Sentiment Analysis for Indian Business and Stocks")

    # Create a table to display results
    result_table = {'Stock': [], 'Article Title': [], 'Sentiment Score': []}
    for i in range(len(articles)):
        result_table['Stock'].append(stocks[i % len(stocks)])
        result_table['Article Title'].append(articles[i]['title'])
        result_table['Sentiment Score'].append(sentiment_scores[i])

    st.table(result_table)

if __name__ == '__main__':
    main()
