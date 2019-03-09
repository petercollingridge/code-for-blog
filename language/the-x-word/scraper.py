from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from string import ascii_lowercase

import re


def search_the_x_word(letter):
    url = 'https://www.google.com/search?q="the+{}+word"'.format(letter)
    return simple_get(url)


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


def write_html(filename, html):
    with open(filename, 'w') as f:
        f.write(html.prettify())


def parse_search_results(raw_html):
    html = BeautifulSoup(raw_html, 'html.parser')

    results = {
        'count': get_results_count(html),
        'pages': []
    }

    page_list = html.find("div", { 'id': "ires" }).find("ol")
    pages = page_list.find_all('h3')

    for page in pages:
        results['pages'].append({
            'text': " ".join(page.find('a').stripped_strings),
            'link': page.find('a').get('href')[7:]
        })

    return results


def write_page_results(filename, letter, results):
    with open(filename, 'a') as f:
        f.write(letter + '\n')

        for page in results['pages']:
            f.write("{}\n\t{}\n".format(page['text'], page['link']))


if __name__ == '__main__':
    for letter in ascii_lowercase:
        raw_html = search_the_x_word(letter)
        results = parse_search_results(raw_html)

        print("{}: {}".format(letter, "{0:.2f}".format(results['count'] * 1e-6)))
        # write_page_results('the-x-word-results.txt', letter, results)
