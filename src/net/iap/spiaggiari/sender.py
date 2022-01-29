from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import dirname, join

from jinja2 import Environment, FileSystemLoader

__author__ = 'Iacopo Papalini <iacopo.papalini@gmail.com>'
import smtplib

from net.iap.spiaggiari.parser import VoteList


class MailSender:
    def __init__(self, user, password, server, ssl_port, to, **_):
        self.user = user
        self.password = password
        self.server = server
        self.ssl_port = ssl_port
        self.to = to
        self.templates_directory = join(dirname(__file__), 'templates')

    def send(self, parsed:VoteList):
        data = parsed.votes
        server = smtplib.SMTP_SSL(self.server, self.ssl_port)
        server.login(self.user, self.password)
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Voti {parsed.student}"
        message["From"] = self.user
        message["To"] = ','.join(self.to)
        environment = Environment(loader=FileSystemLoader(searchpath=self.templates_directory))
        text_template = environment.get_template('votes.text.jinja2')
        html_template = environment.get_template('votes.html.jinja2')

        env = {'data': data}
        part1 = MIMEText(text_template.render(env), "plain")
        part2 = MIMEText(html_template.render(env), "html")

        message.attach(part1)
        message.attach(part2)

        server.sendmail(self.user, self.to, message.as_string())
        server.close()
