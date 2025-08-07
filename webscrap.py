import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def scrape_bbc_headlines():
    """
    Scrapes top headlines from BBC News homepage
    Returns a list of headlines
    """
    # BBC News URL
    url = "https://www.bbc.com/news"
    
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print("Fetching BBC News homepage...")
        # Send GET request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for bad status codes
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        headlines = []
        
        # Find headlines - BBC uses various selectors for headlines
        # Looking for common headline patterns
        selectors = [
            'h2[data-testid="card-headline"]',  # Main story cards
            'h3[data-testid="card-headline"]',  # Secondary story cards  
            'h2.sc-4fedabc7-3',                # Alternative BBC selector
            'h3.gs-c-promo-heading__title',    # BBC promo headlines
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                headline_text = element.get_text(strip=True)
                if headline_text and len(headline_text) > 10:  # Filter out very short text
                    headlines.append(headline_text)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_headlines = []
        for headline in headlines:
            if headline not in seen:
                seen.add(headline)
                unique_headlines.append(headline)
        
        return unique_headlines[:15]  # Return top 15 headlines
        
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []
    except Exception as e:
        print(f"Error parsing the webpage: {e}")
        return []

def save_headlines_to_file(headlines, filename="news_headlines.txt"):
    """
    Saves headlines to a text file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            # Write header with timestamp
            file.write(f"BBC News Headlines - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("=" * 60 + "\n\n")
            
            # Write headlines
            for i, headline in enumerate(headlines, 1):
                file.write(f"{i}. {headline}\n\n")
            
            file.write(f"\nTotal headlines scraped: {len(headlines)}")
        
        print(f"Headlines saved to {filename}")
        return True
        
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False

def main():
    """
    Main function to run the news scraper
    """
    print("BBC News Headlines Scraper")
    print("-" * 30)
    
    # Scrape headlines
    headlines = scrape_bbc_headlines()
    
    if headlines:
        print(f"\nFound {len(headlines)} headlines:")
        print("-" * 40)
        
        # Display headlines
        for i, headline in enumerate(headlines, 1):
            print(f"{i}. {headline}")
        
        # Save to file
        print("\n" + "-" * 40)
        save_headlines_to_file(headlines)
        
    else:
        print("No headlines found. Please check your internet connection or try again later.")

# Alternative function for different news sources
def scrape_generic_news(url, headline_selectors):
    """
    Generic function to scrape headlines from any news website
    
    Args:
        url (str): The news website URL
        headline_selectors (list): List of CSS selectors to find headlines
    
    Returns:
        list: List of scraped headlines
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = []
        
        for selector in headline_selectors:
            elements = soup.select(selector)
            for element in elements:
                headline_text = element.get_text(strip=True)
                if headline_text and len(headline_text) > 5:
                    headlines.append(headline_text)
        
        # Remove duplicates
        return list(dict.fromkeys(headlines))
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

if __name__ == "__main__":
    main()
    
    # Example of using the generic scraper for other sites
    print("\n" + "="*50)
    print("You can also try other news sources:")
    print("Example selectors for different sites:")
    print("- CNN: ['h3.cd__headline', 'span.cd__headline-text']")
    print("- Reuters: ['h3[data-testid=\"Heading\"]', 'a[data-testid=\"Heading\"]']")
    print("- The Guardian: ['h3 > a', '.fc-item__title']")