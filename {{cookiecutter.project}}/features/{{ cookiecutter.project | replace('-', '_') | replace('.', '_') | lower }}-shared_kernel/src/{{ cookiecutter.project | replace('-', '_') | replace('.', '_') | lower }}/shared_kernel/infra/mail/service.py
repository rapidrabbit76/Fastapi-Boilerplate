import smtplib
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

import aiosmtplib


class EmailService(ABC):
    @abstractmethod
    def send(self, receiver: str, subject: str, message: str, **kwargs): ...


class SMTPEmailService(EmailService):
    sender_email: str
    sender_password: str
    client: smtplib.SMTP

    def __init__(
        self,
        sender_email: str,
        sender_password: str,
        client: smtplib.SMTP,
        **kwargs,
    ):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.client = client
        self.client.starttls()
        self.client.login(sender_email, sender_password)

    async def send(self, receiver: str, subject: str, message: str):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = receiver
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))
        self.client.sendmail(self.sender_email, receiver, msg.as_string())


class AsyncSMTPEmailService(EmailService):
    sender_email: str
    sender_password: str
    client: aiosmtplib.SMTP
    is_connect: bool = False

    def __init__(
        self,
        sender_email: str,
        sender_password: str,
        client: aiosmtplib.SMTP,
        **kwargs,
    ):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.client = client
        self.is_connect = False

    async def login(self):
        await self.client.connect(username=self.sender_email, password=self.sender_password)
        self.is_connect = True

    async def send(self, receiver: str, subject: str, message: str):
        if self.is_connect is False:
            await self.login()

        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = receiver
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))
        await self.client.send_message(msg)


class SESEmailService(EmailService):
    charset = "UTF-8"
    client: Any
    sender_email: str

    def __init__(self, client, sender_email: str, **kwargs):
        self.client = client
        self.sender_email = sender_email

    def send(self, receiver: str, subject: str, message: str, type: str):
        self.client.send_email(
            Destination={"ToAddresses": [receiver]},
            Message={
                "Subject": {"Charset": self.charset, "Data": subject},
                "Body": {type: {"Charset": self.charset, "Data": message}},
            },
            Source=self.sender_email,
        )
