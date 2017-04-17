import os
import json
import fnmatch
import urllib.request
import logging
from bs4 import BeautifulSoup
import smtplib


logger = logging.getLogger(__name__)


def decode_text(string, character_decoding):
    """
    :param string: string to be decoded
    :param character_decoding: translation
    :return: string
    """

    return string.decode(character_decoding)


def get_tag_link(links, wildcard):
    """
    :param url_prefix: https prefix to be concatenated with tag link
    :param links: tuple of tag links from parsed html
    :param zip_wildcard: string of file type to be searched
    :return: url for downloading desired file
    """
    try:
        matching = fnmatch.filter(links, wildcard)
        return matching
    except:
        return []


def get_tag_list(url, parser, tag1, tag2, character_decoding):
    """
    :param url: website to inspect html
    :param parser: string of type of parser for inspecting website backend
    :param tag1: string of html tag
    :param tag2: string of html tag
    :param character_decoding: string of character translation
    :return: list of targetted tag links in tuple
    """
    #navigate to epa website
    data = urllib.request.urlopen(url)
    web_data = decode_text(data.read(), character_decoding)
    soup = BeautifulSoup(web_data, parser)

    #create list of href strings from epa website
    links = []
    for path in soup.find_all(tag1):
        links.append(str(path.get(tag2)))
    return links


def send_email_with_urls(urls, sent_from, to, subject, server, username, password):
    body = "\n\n".join(urls)
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL(server, 465)
        server.ehlo()
        server.login(username, password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print("Email sent!")
    except:
        print("Something went wrong...")


def get_desirable_urls():
    try:
        print("BEGIN PROCESS.")
        #set current working directory
        json_data = os.path.join(os.getcwd(), "config", "mmafighting.conf")
        with open(json_data) as json_file:
            parameters = json.load(json_file)
        p= parameters['website']

        #get list of href strings from epa website
        print("GET TAG LIST")
        tag_links = get_tag_list(p['url_main'], p['parser'],
                                   p['tag1'], p['tag2'], p['character_decoding2'])
        #get tscainv href link
        print("GET WEBSITE URLS")
        wildcard_url = get_tag_link(tag_links, p['wildcard'])
        if wildcard_url:
            urls = set(wildcard_url)
            print(urls)
            p = parameters['email']
            send_email_with_urls(urls, [p['email']], [p['email']], p['subject'], p['server'], p['email'], p['password'])

    except Exception as e:
        print(str(e))
        raise
    finally:
        print("PROCESS COMPLETE.")

get_desirable_urls()

