# Message Sender

Sends messages with different services such as email and Google Chat.

## Installation

```sh
pip install message-sender
```

## Usage

### Google Chat

Send messages to Google Chat via webhooks. To set this up, create a "space" in Google Chat, then go
to Apps & integrations and create a new webhook.

#### Sync Client

```py
from message_sender.google_chat import GoogleChatClient

with GoogleChatClient("https://your-webhook-url.com") as client:
    client.send_message("Some test message")
```

#### Async Client

```py
from message_sender.google_chat import AsyncGoogleChatClient

async with AsyncGoogleChatClient("https://your-webhook-url.com") as client:
    await client.send_message("Some test message")
```

### Proton Email

Send emails through Proton Mail's SMTP service. For setup instructions see
[https://proton.me/support/smtp-submission](https://proton.me/support/smtp-submission)

#### Sync Client

```py
from message_sender.email.proton import ProtonEmailClient

client = ProtonEmailClient(
    email_address="smtp_setup_email@proton.me", smtp_token="your-token"
)
client.send_email(
    message="Your message body",
    email_to="someone@email.com",
    subject="Example",
    html_content="<p>Your HTML message body</p>",  # optional
)
```

#### Async Client

```py
from message_sender.email.proton import AsyncProtonEmailClient

client = AsyncProtonEmailClient(
    email_address="smtp_setup_email@proton.me", smtp_token="your-token"
)
await client.send_email(
    message="Your message body",
    email_to="someone@email.com",
    subject="Example",
    html_content="<p>Your HTML message body</p>",  # optional
)
```
