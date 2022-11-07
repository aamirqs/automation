import requests
import logging
import csv
from bs4 import BeautifulSoup
from lxml import etree
from bs4.element import Comment

HEADER = {
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
STATUS_SUCCESS = 'success'
STATUS_FAIL = 'fail'


def get_request(url):
    out = {'status': STATUS_FAIL, 'content': ''}
    print('Executing GET call on:', url)
    resp = requests.get(url, HEADER)
    if resp.status_code == 200:
        out['status'] = STATUS_SUCCESS
        out['content'] = resp.content
    return out


def read_csv(file_path, delimiter=','):
    content = []
    out = {'status': STATUS_FAIL, 'content': content}
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            for r in reader:
                content.append(r)
            out['status'] = STATUS_SUCCESS
    except Exception as ex:
        logging.error(ex)
    return out


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def write_csv(file_path, data):
    with open(file_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def get_bs4_obj(content, parser='html.parser'):
    soup = BeautifulSoup(content, parser)
    return soup
