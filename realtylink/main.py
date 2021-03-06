import smtplib
import datetime
import os
import time
import schedule
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from realtylink.scraper import Scraper
from realtylink import config
from random import randint


def get_host():
    index = randint(0, 1)
    if index == 0:
        host = "us" + str(randint(1, 1706)) + ".nordvpn.com"
    else:
        host = "ca" + str(randint(1, 291)) + ".nordvpn.com"
    return host


def send_mail(send_from, send_to, subject, text, file, email_server):
    """
    Sends a mail to send_to with file attached.

    :param send_from: str
    :param send_to: str
    :param subject: str
    :param text: str
    :param file: str
    :param email_server: str
    :return: None
    """
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    if file != "":
        attachment = open(file, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % file[6:])  # if path changes: change file[4:]
        msg.attach(part)

    server = smtplib.SMTP(email_server, 587)
    server.starttls()
    server.login(config.EMAIL_EMAIL, config.EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(send_from, send_to, text)
    server.quit()


def build_subject(changes):
    singular = ["listing", "change"]
    plural = ["listings", "changes"]
    subject_0 = ""
    subject_1 = ""
    subject_2 = ""
    if changes[0] > 0:
        if changes[0] == 1:
            a = singular[1]
        else:
            a = plural[1]
        subject_0 = "{} price {}. ".format(str(changes[0]), a)

    if changes[1] > 0:
        if changes[1] == 1:
            a = singular[0]
        else:
            a = plural[0]
        subject_1 = "{} new {}. ".format(str(changes[1]), a)
    if changes[2] > 0:
        if changes[2] == 1:
            a = singular[0]
        else:
            a = plural[0]
        subject_2 = "{} removed {}. ".format(str(changes[2]), a)

    subject = subject_0 + subject_1 + subject_2
    return subject[:-1]


def main():
    i = 20
    while i > 0:
        try:
            today_file = "files/" + str(datetime.date.today()) + ".csv"
            yesterday_file = "files/" + str(datetime.date.today() - datetime.timedelta(1)) + ".csv"
            if config.PROXY_SUPPORT:
                host = get_host()
                print("Running with " + host + "...")
                proxies = {'http': 'http://' + config.USERNAME +
                                   ':' + config.PASSWORD +
                                   '@' + host +
                                   ':' + config.PORT}
            else:
                proxies = {}
            exist = os.path.isfile(today_file)
            scraper = Scraper(yesterday_file, "cities.csv")
            scraper.set_proxies(proxies)
            pages = scraper.get_pages()
            houses = scraper.parse_realtylink_pages(pages)
            changes = scraper.update_houses(today_file, houses)
            if (changes[0] > 0 or changes[1] > 0 or changes[2] > 0) and (not exist):
                subject = build_subject(changes)
                send_mail(config.EMAIL_EMAIL, config.EMAIL_LIST, subject, "", today_file, config.EMAIL_SMTP)
        except Exception as e:
            print("Failed. Trying again...")
            subject = "Please check code, script failed."
            send_mail(config.EMAIL_EMAIL, [config.EMAIL_EMAIL], subject, str(e), "", config.EMAIL_SMTP)
            i -= 1
            continue
        break


if __name__ == "__main__":
    if config.RUN_DAILY:
        schedule.every().day.at(config.START_TIME).do(main)
        while 1:
            schedule.run_pending()
            time.sleep(1)
    else:
        main()
