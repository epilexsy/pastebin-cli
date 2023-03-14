import requests
import re
import argparse
import pyperclip
from maskpass import askpass
from datetime import datetime

parser = argparse.ArgumentParser()

LOGIN_URL = 'https://pastebin.com/api/api_login.php'
POST_URL = 'https://pastebin.com/api/api_post.php'

API_KEY = "" # Your account API Development key
api_user_name = "" # Your account Username
api_user_key = None # Will be set when user is authenticated

def authenticate_obtain_user_key():
    data = {
        'api_dev_key':API_KEY,
        'api_user_name':api_user_name,
        'api_user_password':api_user_password,
    }
    
    response = requests.post(url = LOGIN_URL, data = data)
    print(f'[*] ({api_user_name})', end=' ')
    if response.status_code == 200:
        print('Pastebin credentials Authenticated.')
        api_user_key = response._content.decode()
        return api_user_key
    elif response.status_code == 401:
        print('Pastebin credentials Invalid.')
    elif response.status_code == 503:
        print('Pastebin server issue.')
    else:
        print('Unmanaged status code', response.status_code)
    return False



def get_paste_list():
    data = {
        'api_dev_key':API_KEY,
        'api_user_key':api_user_key,
        'api_option':'list',
        'api_results_limit':1000,
    }

    response = requests.post(url = POST_URL, data = data)._content.decode()
    pattern = r'<paste>\s*<paste_key>(.*?)</paste_key>\s*<paste_date>(.*?)</paste_date>\s*<paste_title>(.*?)</paste_title>\s*<paste_size>(.*?)</paste_size>\s*<paste_expire_date>(.*?)</paste_expire_date>\s*<paste_private>(.*?)</paste_private>\s*<paste_format_long>(.*?)</paste_format_long>\s*<paste_format_short>(.*?)</paste_format_short>\s*<paste_url>(.*?)</paste_url>\s*<paste_hits>(.*?)</paste_hits>\s*</paste>'
    regex = re.compile(pattern)
    matches = regex.findall(response)
    pastes = {}
    for match in matches:
        pastes[match[0]] = {
        'date': datetime.utcfromtimestamp(int(match[1])).strftime('%Y-%m-%d %H:%M'),
        'title': match[2] or 'Untitled',
        'size': match[3],
        'expire_date': datetime.utcfromtimestamp(int(match[4])).strftime('%Y-%m-%d %H:%M'),
        'private': match[5],
        'format': match[7],
        'url': match[8],
        'hits': match[9],
        }

    return pastes

def get_pastes(filter_param='title', filter_value=None):
    pastes = get_paste_list()
    filtered = {}
    for paste_id in pastes:
        if filter_param and filter_value and pastes[paste_id][filter_param] == filter_value:
            filtered[paste_id] = pastes[paste_id]
            continue
        elif filter_param and filter_value and pastes[paste_id][filter_param] != filter_value:
            continue
        filtered[paste_id] = pastes[paste_id]
    return filtered

def delete_paste(paste_id):
    data = {
        'api_dev_key':API_KEY,
        'api_user_key':api_user_key,
        'api_paste_key':paste_id,
        'api_option':'delete'
    }

    response = requests.post(url=POST_URL, data=data)
    return response._content.decode()

def create_paste(title, data, paste_format='text', privacy_status='public', expires='N'):
    privacy_status_codes = {'public':0, 'unlisted':1, 'private':2}
    privacy_status = privacy_status_codes[privacy_status]
    data_ = {
        'api_dev_key':API_KEY,
        'api_user_key':api_user_key,
        'api_option':'paste',
        'api_paste_name':title,
        'api_paste_code':data,
        'api_paste_format':paste_format,
        'api_paste_private':privacy_status,
        'api_paste_expire_date':expires,
        
    }
    response = requests.post(url=POST_URL, data=data_)
    return response._content.decode()

def create_paste_from_file(dir_, title, paste_format='text', privacy_status='public', expires='N'):
    with open(dir_, 'r') as f:
        data = f.read()
        f.close()
    return create_paste(title, data, paste_format, privacy_status, expires)

# ARGPARSE IT

# Create paste
parser.add_argument('-np', '--new-paste', help='Create new paste.', action='store_true', default=False)
parser.add_argument('-unl', '--unlisted', help='Set privacy status of new paste as "unlisted".', default=False, action='store_true')
parser.add_argument('-pub', '--public', help='Set privacy status of new paste as "public".', default=False, action='store_true')
parser.add_argument('-priv', '--private', help='Set privacy status of new paste as "private".', default=False, action='store_true')
parser.add_argument('-t', '--title', help='Title of paste', default=None)
parser.add_argument('-f', '--file', help='File to insert into paste.', default=None)
parser.add_argument('-F', '--format', help='Syntax highlighting format (DEFAULT:"text").', default='text')
parser.add_argument('-e', '--expires', help='Set an expiry date for paste (N, 10M, 1H, 1D, 1W, 1Y) (DEFAULT:N)', default='N')

# Get paste list
parser.add_argument('-lp', '--list-pastes', help='List all user pastes.', default=False, action='store_true')
parser.add_argument('--filter', help='Filter parameter', default='title')
parser.add_argument('-v', '--value', help='Filter parameter expected value', default=None)

# Remove paste
parser.add_argument('-rp', '--remove-paste', help='Paste ID to remove', default=None)
args = parser.parse_args()

api_user_password = askpass(prompt=f'{api_user_name}\nEnter pastebin password: ', mask='*')
api_user_key = authenticate_obtain_user_key()

if args.new_paste:
    if not args.unlisted and not args.public and not args.private:
        args.public = True
    if not args.file:
        print('[*] No file provided.')
        exit()
    elif not args.title:
        print('[*] No title for paste provided.')
        exit()

    privacy_status = None
    if args.unlisted:
        privacy_status = 'unlisted'
    elif args.public:
        privacy_status = 'public'
    else:
        privacy_status = 'private'

    
    paste_url = create_paste_from_file(args.file, args.title, args.format, privacy_status, args.expires)
    pyperclip.copy(paste_url)
    print(f'[*] New paste information:')
    print(f'[*]     -> Paste title: "{args.title}"')
    print(f'[*]     -> File used: "{args.file}"')
    print(f'[*]     -> File formatting: {args.format}')
    print(f'[*]     -> Privacy status: {privacy_status}')
    print(f'[*]     -> Expires in: {args.expires}')
    print(f'[*]     -> {datetime.now()}')
    print(f'[*] Paste created: "{paste_url}"')
    print(f'[*] Link copied!')

elif args.list_pastes:
    privacy_status = {'0':'public  ', '1':'unlisted', '2':'private '}
    paste_dump = get_pastes(args.filter, args.value)
    if args.filter != 'title' and args.value:
        print(f'    FILTERED BY ("{args.filter}" = {args.value})') 
    else:
        print()
    for n, paste_id in enumerate(paste_dump):
        print(f'[{n+1}] {paste_id} |{privacy_status[paste_dump[paste_id]["private"]]}| -> {paste_dump[paste_id]["date"]} -- "{paste_dump[paste_id]["title"]}"')
    print()

elif args.remove_paste:
    print('[*] '+delete_paste(args.remove_paste))