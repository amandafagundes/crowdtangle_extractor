from dotenv import dotenv_values
import requests

config = dotenv_values('.env')
BASE_URL = config['BASE_URL']
API_TOKEN = config['API_TOKEN']

def search_posts(query, start_date, end_date, next_page, count='10', language='pt', history='false',
                 summary='true', min_interactions=5, platforms='facebook'):
    print('*', next_page)
    if next_page:
        request_url = next_page
    else:
        request_url = f'{BASE_URL}/posts/search?token={API_TOKEN}'
        request_url += '&searchTerm=' + query + '&startDate=' + start_date + \
                   '&endDate=' + end_date + '&language=' + language + \
                   '&includeHistory=' + history + '&includeSummary=' + summary + \
                   '&minInteractions=' + min_interactions + '&platforms=' + platforms + \
                   '&count=' + count + "&searchField=text_fields_only"
    print('*', request_url)

    r = requests.get(request_url)
    print('2')
    if r.status_code > 300:
        raise Exception(r.text)
    return r.json()

def search_post_by_id(id, history='false'):
    request_url = f'{BASE_URL}/posts?token={API_TOKEN}'
    request_url += '&id=' + id + '&includeHistory=' + history

    r = requests.get(request_url)

    if r.status_code > 300:
        raise Exception(r.text)
    
    return r.text