from dotenv import dotenv_values
from posts.search_posts import search_posts
from util import save, interval_to_dates, get_file_name
import datetime
import sys
import time

config = dotenv_values('.env')

# search_queries = ['"vírus chinês"', '"virus chinês"', '"vírus chines"',
#                   '"vírus da china"', '"virus da china"', '"variante indiana"',
#                   '"doença de velho"', 'abortista']

hashtags_queries = [f'%23blacklivematters', f'%23pretosnopoder', f'%23negrosnopoder', f'%23racistasnãopassarão', f'%23negritude', f'%23blackpower',
                  f'%23RacismoContraBrancos', f'%23GenocídioDosBrancos', f'%23GenocídioBranco', f'%23VidasBrancasImportam', f'%23todavidaimporta',
                  f'%23sororidade', f'%23feminismo', f'%23escutaasminas', f'%23forçameninas', f'%23mulheresunidas'
                  f'%23antifeminismo', f'%23conservadorismo', f'%23feminismonao',
                  f'%23lgbtqia', f'%23LGBT', f'%23orgulhogay', f'%23orgulholgbtqia', f'%23orgulhogay', f'%23lgbtbrasil', f'%23gaypride', f'%23queer',
                  f'%23orgulhohetero', f'%23ideologiadegeneronao', f'%23naoaideologiadegenero']

terms_queries = ['covid-19', 'coronavirus', '"variante delta"', 'B.1.1.529', 'omicron', '"virus chines"', 
                  '"virus da china"', '"variante indiana"', '"variante da india"', '"virus da india"', 
                  '"virus indiano"', '"variante da africa"', '"variante africana"', '"virus da africa"',
                  '"virus africano"', '"doença de velho"', 'aborto assassinato', 'abortista', 'aborto benção',
                  'aborteira', 'liberação aborto', '"liberação do aborto"', 'aborto saúde', 'aborto saúde pública',
                  'legalização aborto', '"legalização do aborto"', 'maconha legalização', 'maconha liberação', 
                  '"liberação da maconha"','"legalização das drogas"','"liberação das drogas"']  

limit = 100

mode = 'EXTRACTION'  # VALIDATION if terms are being validated
# EXTRACTION if the terms in search_queries have already been validated


def crowdtangle_search(query, start_date, end_date, next_page, json_file):
    posts = []
    while len(posts) < limit:
        count = limit - len(posts)
        try:
            response = search_posts(query, str(start_date), str(end_date),
                                    next_page, count=str(count), min_interactions='2')
            time.sleep(10)
            if len(response['result']['posts']) > 0:
                print('Yay!', len(response['result']
                      ['posts']), f'posts was found!')
                if f'nextPage' in response['result']['pagination']:
                    next_page = response['result']['pagination']['nextPage']
                    print('******1)', next_page)
                    response['result']['posts'][-1]['nextPageQuery'] = f''.join(
                        next_page.split('&', 2)[1:])
                    posts.extend(response['result']['posts'])
                    last_id = response['result']['posts'][-1]['platformId']
                else:
                    print('No more pages!')
                    break
            else:
                print('No posts found :(')
                break
            if posts:
                save(posts, json_file, f'EXTRACTION')

        except Exception as e:
            print('Oops.. something went wrong: \n', e)
            break
    return posts, next_page


def main(argv):
    
    data_type = argv[1]
    
    if data_type.upper() == 'HASHTAGS':
        search_queries = hashtags_queries
        custom_path = 'data/hashtags'
    else:
        search_queries = terms_queries
        custom_path = 'data/bias'
        
    # loop over search items,
    # creating a new file for each
    for query in search_queries:
        print(f'**** {query} ****')
        # authorize and load the twitter API
        start_date, end_date = interval_to_dates(1, 365)
        json_file = get_file_name(query, start_date, end_date, custom_path=custom_path)

        start = datetime.datetime.now()
        end = start + datetime.timedelta(hours=2)
        count, exitcount = 0, 0
        next_page = None

        while datetime.datetime.now() < end:

            posts, next_page = crowdtangle_search(query, start_date.strftime(
                f'%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), next_page, json_file)
            # write posts to file in JSON format
            if posts:
                exitcount = 0
            else:
                exitcount += 1
                if exitcount == 3:
                    if query == search_queries[-1]:
                        sys.exit(
                            f'Maximum number of empty post strings reached - exiting')
                    else:
                        print(
                            f'Maximum number of empty post strings reached - breaking')
                        break
            count += 1


if __name__ == "__main__":
    main(sys.argv)
