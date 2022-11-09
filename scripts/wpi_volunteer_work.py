import datetime

from lib.lib import *
from dateutil import parser
import re

archived = "needs to be archived"
no_change = "up to date"
foise_reference = 'needs to be archived, Foisie reference'
cred_req_msg = "WPI credential required to view this page"
date_xpath = ['/html/body/div[3]/div/main/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/span',
              '/html/body/div[3]/div/main/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div/span',
              '/html/body/div[3]/div/main/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[4]/div/div/div/div/div/span',
              '/html/body/div[3]/div/main/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div/div/span',
              '/html/body/div[3]/div/main/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div/div/span',
              '/html/body/div[3]/div/main/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div[3]/div/div/div/div/div/span',
              '/html/body/div[3]/div/main/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[3]/div/div/div/div/div/span',
              '/html/body/div[3]/div/main/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div[4]/div/div/div/div/div/span',
              '/html/body/div[3]/div/main/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/div/div/span']


def get_date_field(page_content):
    soup = get_bs4_obj(page_content)
    dom = etree.HTML(str(soup))
    date_field = ''
    for path in date_xpath:
        path_found = dom.xpath(path)
        if path_found and path_found[0].text is not None:
            date_field = path_found[0].text.strip()
            break
    if not date_field:
        print("Check no date Field found")
    return date_field


def check_credentials_required(text):
    match = re.search(' credentials\srequired\sto\sview', text, re.I)
    if match:
        print("Creds required to view")
        return True
    else:
        return False


def process_csv_file():
    expiry_date = datetime.date(2021, 8, 30)
    read_file = '/home/aamir/Downloads/wpi_url_list.csv'
    write_file = '/home/aamir/Downloads/wpi_url_updated.csv'
    resp = read_csv(read_file)
    # resp = read_csv('/home/aamir/Downloads/amsterdam2.csv')

    out = resp['content']
    for i in out:
        if not i["Comments"]:
            url_resp = get_request(i['URL'])
            if url_resp['status'] == STATUS_SUCCESS:

                date_field = get_date_field(url_resp['content']).strip()
                page_content = text_from_html(url_resp['content'])

                if check_credentials_required(page_content):
                    i['Comments'] = cred_req_msg
                elif re.search('Foisie\sBusiness\sSchool', page_content, re.I):
                    i['Comments'] = foise_reference
                elif not date_field.strip():
                    i['Comments'] = "No Update Date Present"
                elif date_field:
                    page_date = parser.parse(date_field)
                    if page_date.date() < expiry_date:
                        i['Comments'] = archived
                    else:
                        i['Comments'] = no_change
                else:
                    i['Comments'] = no_change
                # check page older than aug 2021

    for i in out:
        print(i)
    write_csv(write_file, out)


process_csv_file()
