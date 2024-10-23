from crawlbase import CrawlingAPI
import json
from bs4 import BeautifulSoup

# Initialize Crawlbase API with JS Token
crawling_api = CrawlingAPI({ 'token': 'N_--sCFBiDzqX2c_O-qD0Q&url=https%3A%2F%2Fgithub.com%2Fcrawlbase%3Ftab%3Drepositories' })

# Function to extract book details and reviews from the HTML content
def extract_book_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('h1.H1Title a[data-testid="title"]').text.strip()
    rating = soup.select_one('div.RatingStatistics span.RatingStars')['aria-label']

    reviews = []
    for review_div in soup.select('div.ReviewsList article.ReviewCard'):
        user = review_div.select_one('div[data-testid="name"]').text.strip()
        review_text = review_div.select_one('section.ReviewText span.Formatted').text.strip()
        reviews.append({'user': user, 'review': review_text})

    return {'title': title, 'rating': rating, 'reviews': reviews}

# Function to scrape Goodreads with pagination
def scrape_goodreads_reviews_with_pagination(base_url):
    page_data = []

    # Fetch initial page and reviews
    response = crawling_api.get(base_url, {
        'ajax_wait': 'true',
        'page_wait': '5000',
        'css_click_selector': 'button:has(span[data-testid="loadMore"])'
    })

    if response['headers']['pc_status'] == '200':
        html_content = response['body'].decode('utf-8')
        page_data = extract_book_details(html_content)

    return page_data

# Function to save the reviews in JSON format
def save_reviews_to_json(data, filename='goodreads_reviews.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Example usage
book_reviews = scrape_goodreads_reviews_with_pagination('https://www.goodreads.com/book/show/4671.The_Great_Gatsby/reviews')
save_reviews_to_json(book_reviews)