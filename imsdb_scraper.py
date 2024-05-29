import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_movie_links():
    url = 'https://imsdb.com/all-scripts.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = ['https://imsdb.com' + a['href'] for a in soup.select('p a[href^="/Movie Scripts/"]')]
    return links

def scrape_movie_page(movie_url):
    response = requests.get(movie_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find_all('h1')[1].get_text(strip=True)
    title = title[:-7]

    writers = []
    movie_writers_div = soup.find('b', text='Writers')
    if movie_writers_div:
        for sibling in movie_writers_div.find_next_siblings():
            if sibling.name == 'a':
                writers.append(sibling.get_text(strip=True))
            elif sibling.name == 'br':
                continue
            else:
                break

    genres = []
    movie_genres_div = soup.find('b', text='Genres')
    if movie_genres_div:
        consecutive_br_count = 0
        for sibling in movie_genres_div.find_next_siblings():
            if sibling.name == 'a':
                genres.append(sibling.get_text(strip=True))
                consecutive_br_count = 0
            elif sibling.name == 'br':
                consecutive_br_count += 1
                if consecutive_br_count == 2:
                    break
            else:
                consecutive_br_count = 0

    script_date = 'N/A'
    script_date_div = soup.find('b', text='Script Date')
    if script_date_div:
        script_date_text = script_date_div.next_sibling
        if script_date_text and isinstance(script_date_text, str):
            script_date = script_date_text.strip().strip(' : ')
            script_date = script_date.split(' ', 1)[1]
    
    movie_date = 'N/A'
    movie_date_div = soup.find('b', text='Movie Release Date')
    if movie_date_div:
        movie_date_text = movie_date_div.next_sibling
        if movie_date_text and isinstance(movie_date_text, str):
            movie_date = movie_date_text.strip().strip(' : ')
            movie_date = movie_date.split(' ', 1)[1]
    

    script_text = ''
    script_link = soup.find('a', string=lambda text: text and 'Read' in text and 'Script' in text)
    if script_link:
        script_url = 'https://imsdb.com' + script_link['href']
        script_response = requests.get(script_url)
        script_soup = BeautifulSoup(script_response.content, 'html.parser')
        script_pre = script_soup.find('pre')
        if script_pre:
            script_text = script_pre.get_text()

    return {
        'Title': title,
        'Writers': ', '.join(writers),
        'Genres': ', '.join(genres),
        'Script Date': script_date,
        'Movie Release Date': movie_date,
        'Script': script_text
    }

def main():
    movie_links = get_movie_links()
    movies_data = []

    for movie_link in movie_links:
        try:
            movie_data = scrape_movie_page(movie_link)
            movies_data.append(movie_data)
            print(f'Successfully scraped: {movie_data["Title"]}')
            time.sleep(0.5)
        except Exception as e:
            print(f'Failed to scrape {movie_link}: {e}')

    df = pd.DataFrame(movies_data)
    df.to_csv('imsdb_movie_scripts.csv', index=False, encoding='utf-8')
    print("Data has been scraped and saved to imsdb_movie_scripts.csv")

if __name__ == '__main__':
    main()
