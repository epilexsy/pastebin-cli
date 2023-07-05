# py-pastebin-cli
<p color="gray">(rough and unpolished)</p>
Using `argparse` and `requests` to interact with [Pastebin API](https://pastebin.com/doc_api).

Functionality:
 - Create paste
 - Remove paste
 - List pastes

External requirements:
(you could remove their usage entirely)
 - `maskpass` (masked password input)
 - `pyperclip` (copy generated link)

Setup:
 - set `API_KEY` to your pastebin account's API Developer key.
 - set `api_user_name` to your pastebin account's Username.
 - set `api_user_password` to your pastebin account's Password (optional, asks for password input by default upon running.)

# Example usage:
Create a paste:
```bash
python .\pastebin.py --new-paste --title "Rotating donut C code" --file "donut.c" --format c --expires 1Y --unlisted
```
```
accusername
Enter pastebin password: ****************
Pastebin credentials Authenticated.

Paste created! Link: "https://pastebin.com/pK3bHVxY"

2023-03-14 11:11
Paste title: "Rotating donut C code"
File used: ".\donut.c"
File formatting: c
Privacy status: unlisted
Expires in: 1Y

Link copied!

```

List pastes:
```bash
python .\pastebin.py --list-pastes
```
```
accusername
Enter pastebin password: ****************
Pastebin credentials Authenticated.

1. 2023-03-14 11:11 - (pK3bHVxY) Rotating donut C code [unlisted]
```

Delete a paste:
```bash
python .\pastebin.py --remove-paste "pK3bHVxY"
```
```
accusername
Enter pastebin password: ****************
Pastebin credentials Authenticated.

Paste Removed

```

# Arguments

```
python .\pastebin.py --help
```
```
usage: pastebin.py [-h] [-np] [-unl] [-pub] [-priv] [-t TITLE] [-f FILE] [-F FORMAT]
                   [-e EXPIRES] [-lp]
                   [--filter {title,date,size,expire_date,privacy,format,url,hits}]
                   [-v VALUE] [-rp REMOVE_PASTE]

options:
  -h, --help            show this help message and exit
  -np, --new-paste      Create new paste.
  -unl, --unlisted      Set privacy status of new paste as "unlisted".
  -pub, --public        Set privacy status of new paste as "public".
  -priv, --private      Set privacy status of new paste as "private".
  -t TITLE, --title TITLE
                        Title of paste
  -f FILE, --file FILE  File to insert into paste.
  -F FORMAT, --format FORMAT
                        Syntax highlighting format (DEFAULT:"text").
  -e EXPIRES, --expires EXPIRES
                        Set an expiry date for paste (N, 10M, 1H, 1D, 1W, 1Y) (DEFAULT:N)     
  -lp, --list-pastes    List all user pastes.
  --filter {title,date,size,expire_date,privacy,format,url,hits}
                        Filter parameter
  -v VALUE, --value VALUE
                        Filter parameter expected value
  -rp REMOVE_PASTE, --remove-paste REMOVE_PASTE
                        Paste ID to remove
  ```
