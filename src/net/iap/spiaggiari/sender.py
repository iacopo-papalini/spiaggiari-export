from email import encoders
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.text import MIMEText
from os.path import dirname, join

from jinja2 import Environment, FileSystemLoader

__author__ = "Iacopo Papalini <iacopo.papalini@gmail.com>"
import smtplib

from net.iap.spiaggiari.doclist_parser import Document
from net.iap.spiaggiari.vote_parser import VoteList


class MailSender:
    def __init__(self, user, password, server, ssl_port, to, **_):
        self.user = user
        self.password = password
        self.server = server
        self.ssl_port = ssl_port
        self.to = to
        self.templates_directory = join(dirname(__file__), "templates")

    def send(self, parsed: VoteList):
        data = parsed.votes
        server = smtplib.SMTP_SSL(self.server, self.ssl_port)
        server.login(self.user, self.password)
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Voti {parsed.student}"
        message["From"] = self.user
        message["To"] = ",".join(self.to)
        environment = Environment(
            loader=FileSystemLoader(searchpath=self.templates_directory)
        )
        text_template = environment.get_template("votes.text.jinja2")
        html_template = environment.get_template("votes.html.jinja2")

        env = {"data": data}
        part1 = MIMEText(text_template.render(env), "plain")
        part2 = MIMEText(html_template.render(env), "html")

        message.attach(part1)
        message.attach(part2)

        server.sendmail(self.user, self.to, message.as_string())
        server.close()


class DocumentMailSender:
    def __init__(self, user, password, server, ssl_port, to, **_):
        self.user = user
        self.password = password
        self.server = server
        self.ssl_port = ssl_port
        self.to = to
        self.templates_directory = join(dirname(__file__), "templates")

    def send(self, document: Document):
        server = smtplib.SMTP_SSL(self.server, self.ssl_port)
        server.login(self.user, self.password)
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Nuovo documento '{document.title}'"
        message["From"] = self.user
        message["To"] = ",".join(self.to)
        environment = Environment(
            loader=FileSystemLoader(searchpath=self.templates_directory)
        )
        text_template = environment.get_template("document.text.jinja2")
        html_template = environment.get_template("document.html.jinja2")

        env = {"document": document}
        part1 = MIMEText(text_template.render(env), "plain")
        part2 = MIMEText(html_template.render(env), "html")

        message.attach(part1)
        message.attach(part2)

        for attachment in document.attachments:
            type_, subtype = attachment.content_type.split("/")
            mime = MIMENonMultipart(_maintype=type_, _subtype=subtype)
            mime.set_payload(attachment.bytes_)
            mime.add_header(
                "Content-Disposition", "attachment", filename=attachment.name
            )
            encoders.encode_base64(mime)
            message.attach(mime)

        server.sendmail(self.user, self.to, message.as_string())
        server.close()
