import imaplib
import os
import email
import random
import config


class Sender:

    def __init__(self):
        CONFIG_KEYS = ('email_user', 'email_pass', 'email_server')

        self.config = dict()

        for var in CONFIG_KEYS:
            self.config[var] = os.environ.get(var.upper())

        self.config['email_user'] = config.email_user
        self.config['email_pass'] = config.email_pass
        self.config['email_server'] = config.email_server

    def check(self):
        print('Checking...')
        output = list()
        mail = imaplib.IMAP4(self.config['email_server'])
        mail.starttls()
        mail.login(self.config['email_user'], self.config['email_pass'])
        mail.select('INBOX')

        # Getting all Email-IDs and store it in data
        #type, data = mail.search(None, 'ALL')
        type, data = mail.search(None, 'UNSEEN')
        mail_ids = data[0]
        id_list = mail_ids.split()

        if len(data[0].split()) > 0:
            print('New Mails')
        else:
            print('No Mails')
            return
        counter = 0
        for num in data[0].split():

            typ, data = mail.fetch(num, '(RFC822)')
            # converts byte literal to string removing b''
            raw_email = data[0][1]

            raw_email_string = ''

            try:
                raw_email_string = raw_email.decode('utf-8')
            except:
                raw_email_string = raw_email.decode('latin-1')

            email_message = email.message_from_string(raw_email_string)
            counter += 1

            mail_subject = str(email_message.get_all('subject')[0])
            mail_body = None
            if "Druckanfrage" not in mail_subject:
                continue
            try:
                mail_body = str(email_message.get_payload()
                                [0].get_payload()).strip()
                mail_body = mail_body[mail_body.find("\n")+1:]

            except:

                mail_body = str(email_message.get_payload()).strip()
                mail_body = mail_body[mail_body.find("\n")+1:]

            if isinstance(mail_body, list) or "email.message.Message" in mail_body:
                continue

            printName = None
            for part in email_message.walk():

                fileName = part.get_filename()
                if fileName is None:
                    continue
                fileEnding = str(fileName[fileName.find("."):])

                if bool(fileName):

                    printName = fileName
                    filePath = os.path.join(printName)
                    if not os.path.isfile(filePath):
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
            item = dict()
            lines = mail_body.split('\n')
            for line in lines:
                infos = line.split(" ")
                item[infos[0].strip()] = infos[1].strip()
            if printName is not None:
                item['file'] = printName

            output.append(item)

        return output
