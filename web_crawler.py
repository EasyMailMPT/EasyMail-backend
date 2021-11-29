# from settings import LOGGING
import logging, logging.config
import urllib, urllib.request, urllib.error, urllib.parse
import re
import traceback

# Logging
# logging.config.dictConfig(LOGGING)
logger = logging.getLogger("crawler_logger")

google_adurl_regex = re.compile('adurl=(.*?)"')
google_url_regex = re.compile('url\?q=(.*?)&amp;sa=')
email_regex = re.compile('([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})', re.IGNORECASE)
url_regex = re.compile('<a\s.*?href=[\'"](.*?)[\'"].*?>')


def find_emails_in_html(url):
    try:
        html = urllib.request.urlopen(url)
    except urllib.error.URLError or urllib.error.HTTPError as err:
        print("Exception at url: %s\n%s" % (url, err))
        return
    except Exception:
        print('Unexpected event happened')
        return
    text_data = str(html.read())

    if not text_data:
        return list()
    email_list = list()
    for email in email_regex.findall(text_data):
        email_list.append(email)
    return email_list


if __name__ == "__main__":
    import argparse
    import sys

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--url', required=True)
        args = parser.parse_args()
        url = args.url
        email_list = list(set(find_emails_in_html(url)))
        for email in email_list:
            print(email)
    except KeyboardInterrupt:
        logger.error("Stopping (KeyboardInterrupt)")
        sys.exit()
    except Exception as err:
        logger.error("EXCEPTION: %s " % err)
        traceback.print_exc()
