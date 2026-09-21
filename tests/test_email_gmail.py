from email.message import EmailMessage
from unittest.mock import AsyncMock, MagicMock, patch

from message_sender.email.gmail import AsyncGmailClient, GmailClient


def test_send_email_plain_text() -> None:
    mock_smtp = MagicMock()
    mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
    mock_smtp.__exit__ = MagicMock(return_value=False)

    with patch("message_sender.email.gmail.smtplib.SMTP", return_value=mock_smtp):
        client = GmailClient(email_address="sender@gmail.com", app_password="test-password")
        client.send_email(
            message="Hello, World!",
            email_to="recipient@example.com",
            subject="Test Subject",
        )

    mock_smtp.starttls.assert_called_once()
    mock_smtp.login.assert_called_once_with("sender@gmail.com", "test-password")
    mock_smtp.send_message.assert_called_once()

    sent_message: EmailMessage = mock_smtp.send_message.call_args[0][0]
    assert sent_message["Subject"] == "Test Subject"
    assert sent_message["From"] == "sender@gmail.com"
    assert sent_message["To"] == "recipient@example.com"
    assert sent_message.get_content().strip() == "Hello, World!"


def test_send_email_with_html() -> None:
    mock_smtp = MagicMock()
    mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
    mock_smtp.__exit__ = MagicMock(return_value=False)

    with patch("message_sender.email.gmail.smtplib.SMTP", return_value=mock_smtp):
        client = GmailClient(email_address="sender@gmail.com", app_password="test-password")
        client.send_email(
            message="Hello, World!",
            email_to="recipient@example.com",
            subject="Test Subject",
            html_content="<p>Hello, World!</p>",
        )

    mock_smtp.send_message.assert_called_once()

    sent_message: EmailMessage = mock_smtp.send_message.call_args[0][0]
    assert sent_message.is_multipart()


def test_smtp_connection_parameters() -> None:
    mock_smtp = MagicMock()
    mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
    mock_smtp.__exit__ = MagicMock(return_value=False)

    with patch(
        "message_sender.email.gmail.smtplib.SMTP", return_value=mock_smtp
    ) as mock_smtp_class:
        client = GmailClient(email_address="sender@gmail.com", app_password="test-password")
        client.send_email(
            message="Hello",
            email_to="recipient@example.com",
            subject="Test",
        )

    mock_smtp_class.assert_called_once_with("smtp.gmail.com", 587)


async def test_async_send_email_plain_text() -> None:
    mock_smtp = MagicMock()
    mock_smtp.__aenter__ = AsyncMock(return_value=mock_smtp)
    mock_smtp.__aexit__ = AsyncMock(return_value=False)
    mock_smtp.send_message = AsyncMock()

    with patch("message_sender.email.gmail.SMTP", return_value=mock_smtp):
        client = AsyncGmailClient(email_address="sender@gmail.com", app_password="test-password")
        await client.send_email(
            message="Hello, World!",
            email_to="recipient@example.com",
            subject="Test Subject",
        )

    mock_smtp.send_message.assert_called_once()

    sent_message: EmailMessage = mock_smtp.send_message.call_args[0][0]
    assert sent_message["Subject"] == "Test Subject"
    assert sent_message["From"] == "sender@gmail.com"
    assert sent_message["To"] == "recipient@example.com"
    assert sent_message.get_content().strip() == "Hello, World!"


async def test_async_send_email_with_html() -> None:
    mock_smtp = MagicMock()
    mock_smtp.__aenter__ = AsyncMock(return_value=mock_smtp)
    mock_smtp.__aexit__ = AsyncMock(return_value=False)
    mock_smtp.send_message = AsyncMock()

    with patch("message_sender.email.gmail.SMTP", return_value=mock_smtp):
        client = AsyncGmailClient(email_address="sender@gmail.com", app_password="test-password")
        await client.send_email(
            message="Hello, World!",
            email_to="recipient@example.com",
            subject="Test Subject",
            html_content="<p>Hello, World!</p>",
        )

    mock_smtp.send_message.assert_called_once()

    sent_message: EmailMessage = mock_smtp.send_message.call_args[0][0]
    assert sent_message.is_multipart()


async def test_aync_smtp_connection_parameters() -> None:
    mock_smtp = MagicMock()
    mock_smtp.__aenter__ = AsyncMock(return_value=mock_smtp)
    mock_smtp.__aexit__ = AsyncMock(return_value=False)
    mock_smtp.send_message = AsyncMock()

    with patch("message_sender.email.gmail.SMTP", return_value=mock_smtp) as mock_smtp_class:
        client = AsyncGmailClient(email_address="sender@gmail.com", app_password="test-password")
        await client.send_email(
            message="Hello",
            email_to="recipient@example.com",
            subject="Test",
        )

    mock_smtp_class.assert_called_once_with(
        hostname="smtp.gmail.com",
        port=587,
        username="sender@gmail.com",
        password="test-password",
        start_tls=True,
    )
