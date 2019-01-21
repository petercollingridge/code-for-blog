from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def fetch_results(search_term):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text


def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)


def get_results_count(html):
    result_stats = html.find(id="resultStats")
    result_stats_string = result_stats.string
    
    result_count = re.search('[\d,]+', result_stats.string)
    if result_count:
        result_count = result_count.group(0)
    else:
        return 0

    result_count = int(result_count.replace(',', ''))
    return result_count


def parse_search_results(raw_html):
    html = BeautifulSoup(raw_html, 'html.parser')
    results_count = get_results_count(html)
    print(results_count)

    print(html.prettify())
    results_group = html.find_all("div", class_="srg")
    print(results_group)



if __name__ == '__main__':
    search_term = '"the a word"'
    escaped_search_term = search_term.replace(' ', '+')
    url = 'https://www.google.com/search?q={}'.format(search_term)

    raw_html = simple_get(url)
    parse_search_results(raw_html)


