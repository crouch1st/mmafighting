import fnmatch
import urllib.request
import logging
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self, config, image):
        self.config = config
        self.image = image
        self.web_content = self.config["website"]
        self.email_content = self.config["email"]
        self.tag_list = []

    def get_tag_list(self):
        """
        This method will capture all targeted html tag links
        by reading all html content of the page, targeting
        parent tags and filtering child tags into a list
        :return: list of tag links
        """
        data = urllib.request.urlopen(self.web_content["url_main"])
        web_data = data.read().decode(self.web_content["character_decoding2"])
        soup = BeautifulSoup(web_data, self.web_content["parser"])

        for path in soup.find_all(self.web_content["tag1"]):
            self.tag_list.append(str(path.get(self.web_content["tag2"])))

        logger.info(self.tag_list)
        return self.tag_list

    def send_email_with_urls(self, match_list):
        """
        This method will email recipient URL links of desirable content
        :param match_list: list of URLs
        :return:
        """

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_content["email"]
            msg['To'] = self.email_content["email"]
            msg['Subject'] = self.email_content["subject"]

            body = MIMEText('<p><img src="cid:{image}" /></p>'.format(image=self.image), _subtype='html')
            msg.attach(body)

            fp = open(self.image, 'rb')
            img = MIMEImage(fp.read(), 'png')
            fp.close()
            img.add_header('Content-Id', '<{image}>'.format(image=self.image))
            msg.attach(img)

            contents = "\n\n".join(match_list)
            msg.attach(MIMEText(contents, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_content["email"], self.email_content["password"])
            text = msg.as_string()
            server.sendmail(self.email_content["email"], self.email_content["email"], text)
            server.quit()
            logger.info("EMAIL SENT TO: {recipient}".format(recipient=self.email_content["email"]))

        except:
            logger.info("Something went wrong...")
            raise

    def send_desirable_content(self):
        """
        This method drives the scraping of the page and sending of the content to recipient
        :return:
        """
        try:
            logger.info("GET TAG LIST")
            self.get_tag_list()

            logger.info("GET WEBSITE URLS")
            match_list = set(fnmatch.filter(self.tag_list, self.web_content["wildcard"]))
            if match_list:
                logger.info("LIST OF URL LINKS: {}".format(match_list))
                self.send_email_with_urls(match_list)
            else:
                logger.info("NO DESIRABLE CONTENT SENT")
        except:
            raise
