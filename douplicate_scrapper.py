from crawlbase import CrawlingAPI
import json
from bs4 import BeautifulSoup

# Initialize crawlbase API with JS token
crawling_api = CrawlingAPI({'token' : 'N_--sCFBiDzqX2c_O-qD0Q&url=https%3A%2F%2Fgithub.com%2Fcrawlbase%3Ftab%3Drepositories' })


# Function to extract the book title, rating and reviews from the page
def extract_book_details(html):
    soup = BeautifulSoup(html,'html.parser')
    title = soup.select_one('h1.H1Title a[data-testid = "title"]').text.strip() #text_value
    rating = soup.select_one('div.RatingStatistics span.RatingStars')['aria-label']  #number value

    reviews = []
    for review_div in soup.select('div.ReviewList article.ReviewCard'):
        user = review_div.select_one('div[data-testid = "name"]').text.strip()
        review_text = review_div.select_one('section.ReviewText span.Formatted').text.strip()
        reviews.append({'user' : user, 'review' : review_text})
    
    return {'title' : title, 'rating' : rating, 'reviews' : reviews}


#function to fetch and process Goodreads book details and reviews
def scrape_goodreads_review(base_url):
    page_data = []

    #Fetch initial page and reviews
    response = crawling_api.get(base_url, {
        'ajax_wait' : 'true',
        'page_wait' : '5000',
        'css_click_selector' : 'button:has(span[data-testid="loadMore"])'
    })

    if response['headers']['pc_status'] == '200' : 
        html_content = response['body'].decode('utf-8')
        page_data = extract_book_details(html_content)

    return page_data



#function to save scraped reviews to a JSON file
def save_reviews_to_json(data, filename = 'goodreads_reviews.json'):
    with open(filename,'w', encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii = False, indent = 4)

#example usage
book_reviews = scrape_goodreads_review('https://www.goodreads.com/book/show/4671.The_Great_Gatsby/reviews')
save_reviews_to_json(book_reviews)



#token : N_--sCFBiDzqX2c_O-qD0Q&url=https%3A%2F%2Fgithub.com%2Fcrawlbase%3Ftab%3Drepositories