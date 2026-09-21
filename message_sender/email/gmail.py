from __future__ import annotations

import smtplib
from email.message import EmailMessage
from typing import Final

from aiosmtplib import SMTP


class _GmailBase:
    _SMTP_SERVER: Final = "smtp.gmail.com"
    _SMTP_PORT: Final = 587

    def __init__(
        self,
        email_address: str,
        app_password: str,
    ) -> None:
        self.email_address = email_address
        self.app_password = app_password


class AsyncGmailClient(_GmailBase):
    """Async client for sending Gmail emails.

    Requires a Google App Password (not your regular account password), which can be
    generated from your Google Account settings once 2-Step Verification is enabled.

    Args:
        email_address: The Gmail address used to send the email
        app_password: The Google App Password generated for this account
    """

    def __init__(
        self,
        email_address: str,
        app_password: str,
    ) -> None:
        super().__init__(email_address=email_address, app_password=app_password)

    async def send_email(
        self,
        *,
        message: str,
        email_to: str,
        subject: str,
        html_content: str | None = None,
    ) -> None:
        """Send the email through Gmail.

        Args:
            message: The message body. If no html_content is provided or the receiving client does
                not support HTML this is used.
            email_to: The email address where the email should be sent
            subject: The subject of the email
            html_content: The message body with HTML markup. Defaults to None

        Examples:
            >>> from message_sender.email.gmail import AsyncGmailClient
            >>>
            >>> client = AsyncGmailClient(
            >>>     email_address="sender@gmail.com", app_password="your-app-password"
            >>> )
            >>> await client.send_email(
            >>>     message="Your message body",
            >>>     email_to="someone@email.com",
            >>>     subject="Example",
            >>>     html_content="<p>Your HTML message body</p>",
            >>> )
        """

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.email_address
        msg["To"] = email_to
        msg.set_content(message)

        if html_content:
            msg.add_alternative(html_content, subtype="html")

        async with SMTP(
            hostname=self._SMTP_SERVER,
            port=self._SMTP_PORT,
            username=self.email_address,
            password=self.app_password,
            start_tls=True,
        ) as smtp:
            await smtp.send_message(msg)


class GmailClient(_GmailBase):
    """Client for sending Gmail emails.

    Requires a Google App Password (not your regular account password), which can be
    generated from your Google Account settings once 2-Step Verification is enabled.

    Args:
        email_address: The Gmail address used to send the email
        app_password: The Google App Password generated for this account
    """

    def __init__(
        self,
        email_address: str,
        app_password: str,
    ) -> None:
        super().__init__(email_address=email_address, app_password=app_password)

    def send_email(
        self,
        *,
        message: str,
        email_to: str,
        subject: str,
        html_content: str | None = None,
    ) -> None:
        """Send the email through Gmail.

        Args:
            message: The message body. If no html_content is provided or the receiving client does
                not support HTML this is used.
            email_to: The email address where the email should be sent
            subject: The subject of the email
            html_content: The message body with HTML markup. Defaults to None

        Examples:
            >>> from message_sender.email.gmail import GmailClient
            >>>
            >>> client = GmailClient(
            >>>     email_address="sender@gmail.com", app_password="your-app-password"
            >>> )
            >>> client.send_email(
            >>>     message="Your message body",
            >>>     email_to="someone@email.com",
            >>>     subject="Example",
            >>>     html_content="<p>Your HTML message body</p>",
            >>> )
        """

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.email_address
        msg["To"] = email_to
        msg.set_content(message)

        if html_content:
            msg.add_alternative(html_content, subtype="html")

        with smtplib.SMTP(self._SMTP_SERVER, self._SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(self.email_address, self.app_password)
            smtp.send_message(msg)
