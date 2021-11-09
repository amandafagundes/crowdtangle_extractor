from dotenv import dotenv_values
from posts.search_posts import search_posts
from util import save, interval_to_dates, get_file_name
import datetime, os, sys, time

config = dotenv_values('.env')

search_queries = ['"vírus chinês"', '"virus chinês"', '"vírus chines"',
                  '"vírus da china"', '"virus da china"', '"variante indiana"', 
                  '"doença de velho"', 'abortista']
limit = 100      

mode = 'EXTRACTION' # VALIDATION if terms are being validated
                    # EXTRACTION if the terms in search_queries have already been validated
                            

def crowdtangle_search(query, start_date, end_date, next_page):
    posts = []
    while len(posts) < limit:
        count = limit - len(posts)
        try:
            response = search_posts(query, str(start_date), str(end_date), 
                                    next_page, count=str(count), min_interactions='10')
            time.sleep(10)
            if len(response['result']['posts']) > 0:
                print('Yay!', len(response['result']['posts']), ' posts was found!')
                if 'nextPage' in response['result']['pagination']:
                    next_page = response['result']['pagination']['nextPage']
                    print('******1)', next_page)
                    response['result']['posts'][-1]['nextPageQuery'] = ''.join(next_page.split('&',2)[1:])
                    posts.extend(response['result']['posts'])
                    last_id = response['result']['posts'][-1]['platformId']
                else:
                    print('No more pages!')
                    break
            else:
                print('No posts found :(')
                break

        except Exception as e:
            print('Oops.. something went wrong: \n', e)
            break
    return posts, next_page

def main():

    # loop over search items,
    # creating a new file for each
    for query in search_queries:
        print(f'**** {query} ****')
        # authorize and load the twitter API
        start_date, end_date = interval_to_dates(1, 365)
        json_file = get_file_name(query, start_date, end_date)

        start = datetime.datetime.now()
        end = start + datetime.timedelta(hours=2)
        count, exitcount = 0, 0
        next_page = None

        while datetime.datetime.now() < end:
            
            posts, next_page = crowdtangle_search(query, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), next_page)
            # write posts to file in JSON format
            if posts:
                save(posts, json_file, 'EXTRACTION')
                exitcount = 0
            else:
                exitcount += 1
                if exitcount == 3:
                    if query == search_queries[-1]:
                        sys.exit(
                            'Maximum number of empty post strings reached - exiting')
                    else:
                        print(
                            'Maximum number of empty post strings reached - breaking')
                        break
            count += 1


if __name__ == "__main__":
    main()
