import datetime
import os
import json

def date_to_str(date):
    return '{0}-{1:0>2}-{2:0>2}'.format(date.year, date.month, date.day)

def interval_to_dates(interval_begin, interval_end):
    start_date = datetime.datetime.now() - datetime.timedelta(days=interval_end)
    end_date = datetime.datetime.now() - datetime.timedelta(days=interval_begin-1)
    return start_date, end_date

def format_post(nested_json):
    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

def get_file_name(query, start_date, end_date, custom_path='data/hashtags'):
    query = query.replace(' ', '_').replace(f'%23', '#')
    json_path = f'{custom_path}/{query}/{query}'
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    day = start_date.strftime('%Y-%m-%d') + '_to_' + end_date.strftime('%Y-%m-%d')

    return f'{json_path}_{day}.json'

def save(posts, filename, mode):
    isFile = False
    # remove the brackets ] at the end of file
    if os.path.isfile(filename):
        isFile = True
        lines = open(filename, 'r').readlines()
        last_line = lines[-1]
        last_line = ''.join(last_line.rsplit(']', 1))
        lines[-1] = last_line
        open(filename, 'w').writelines(lines)
        
    with open(filename, 'a') as f:
        if not isFile:
            f.write('[')
        for post in posts:
            if mode == 'VALIDATION':
                print(post['message'])
                resp = input('Is that a valid post? (Y/N)')
                if resp.lower() == 'y':
                    json.dump(format_post(post), f)
            else:
                json.dump(format_post(post), f)
            f.write(',\n')
        f.write(']')
