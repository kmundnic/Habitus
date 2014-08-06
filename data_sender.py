# File adapted from Rodrigo Coutinho's code to send emails with attachments
# through Python using Gmail. The original code may be found at:
# http://kutuma.blogspot.com/2007/08/sending-emails-via-gmail-with-python.html

import smtplib
import json
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders


class DataSender():

    def __init__(self):
        self.file = "send_info.json"
        self.info = self.load_email_account()  # Contains "from",
                                               # "password", "to"

    def load_email_account(self):
        """
        Load the email info from account.json in this directory. The JSON file
        should have the following structure:
        {
        "user": sender Gmail,
        "password": account password,
        "to": receiver email
        }
        :return: user, password, to
        """
        dictionary = {}
        try:
            json_file = open(self.file, 'r')
            print "Opened JSON file successfully"
            try:  # Load data if there is data in the file
                dictionary = json.load(json_file)
                json_file.close()
                print "Loaded JSON file successfully"
            except ValueError:  # If not, create a new dict
                print "Create and send_info.json file with" \
                      "{'from': email_sender," \
                      " 'password': password," \
                      " 'to': email_receiver}"
                raise

        except (IOError, OSError):
            # TODO: Replace for logger
            print "Unable to open send_info.json."
            raise

        print dictionary
        return dictionary

    def send_email(self, subject="", text="", attach=None):
        msg = MIMEMultipart()

        msg['From'] = self.info["from"]
        msg['To'] = self.info["to"]
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        if attach is not None:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attach, 'rb').read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % os.path.basename(attach))
            msg.attach(part)

        mail_server = smtplib.SMTP("smtp.gmail.com", 587)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(self.info["from"],
                          self.info["password"])
        mail_server.sendmail(self.info["from"],
                             self.info["to"],
                             msg.as_string())
        # Should be mail_server.quit(), but that crashes...
        mail_server.close()
