# BPO Acceptor Lead Service - Brevo Webhook Integration

A FastAPI service for handling BPO lead submissions with email notifications and webhook automation via Brevo SMTP.

## Features

- 📧 **Email Notifications** via Brevo SMTP
- 🔗 **Webhook Integration** for real-time email event tracking
- 🚀 **Async Email Sending** for better performance
- ✅ **Lead Data Validation** with Pydantic
- 📝 **Interactive API Documentation** (Swagger UI)
- 🎯 **Simple `/bpo-acceptor-lead` Endpoint**
- 🔔 **Automated Event Handling** (delivered, opened, clicked, bounced, etc.)
- ☁️ **Ready for Render Deployment**

## Quick Start

### 1. Activate Virtual Environment

```bash
cd c:\Users\DELL\Desktop\Projects\BPO-Acceptor-new1\Brevo-SMTP
.venv\Scripts\activate
```

### 2. Configure Environment

Edit `.env` file with your Brevo credentials:

```env
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USERNAME=your-brevo-login-email@example.com
SMTP_PASSWORD=your-brevo-smtp-key
SMTP_FROM_EMAIL=your-sender-email@example.com
SMTP_FROM_NAME=BPO Acceptor
RECIPIENT_EMAIL=where-to-receive-leads@example.com
```

### 3. Run the Application

```bash
uvicorn main:app --reload
```

Server starts at `http://localhost:8000`

## API Endpoints

### Submit Lead

**POST** `/bpo-acceptor-lead`

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "company": "Acme Corp",
  "message": "Interested in BPO services"
}
```

### Webhook Endpoint

**POST** `/webhook/brevo`

Receives real-time events from Brevo:

- `delivered` - Email successfully delivered
- `opened` - Recipient opened the email
- `click` - Recipient clicked a link
- `soft_bounce` - Temporary delivery failure
- `hard_bounce` - Permanent delivery failure
- `spam` - Marked as spam
- `unsubscribed` - Recipient unsubscribed
- `error` - Processing error

### Other Endpoints

- **GET** `/health` - Health check
- **GET** `/docs` - Interactive API documentation
- **GET** `/` - API information

## Brevo Webhook Setup

### 1. Deploy Your Application

**Local Testing (with ngrok):**

```bash
ngrok http 8000
```

**Production (Render):**
Deploy to Render and get your production URL.

### 2. Configure in Brevo Dashboard

1. Log into Brevo
2. Go to **Settings** → **Webhooks**
3. Click **Add a new webhook**
4. Enter webhook URL: `https://your-domain.com/webhook/brevo`
5. Select events to track (delivered, opened, click, etc.)
6. Save webhook

### 3. Test the Integration

Submit a test lead and monitor the logs for webhook events.

## How It Works

```
Lead Submitted → Email Sent via SMTP → Brevo Delivers Email
                                              ↓
                                    Email Events Occur
                                              ↓
                              Brevo Sends Webhook to Your API
                                              ↓
                                  Your API Processes Event
                                              ↓
                              Triggers Automated Actions
```

## Event Automation

The webhook handler automatically processes events:

- **Delivered**: Logs successful delivery
- **Opened**: Tracks engagement metrics
- **Clicked**: High engagement indicator, can notify sales team
- **Hard Bounce**: Marks email as invalid
- **Spam**: Unsubscribes immediately
- **Unsubscribed**: Removes from mailing list

Customize automation logic in `app/webhook_handler.py`.

## Project Structure

```
Brevo-SMTP/
├── .venv/                    # Virtual environment
├── app/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models
│   ├── email_service.py     # Email sending logic
│   ├── webhook_handler.py   # Webhook event processing
│   └── routes.py            # API routes
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── .env                     # Your credentials (not in git)
├── .env.example             # Environment template
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## Environment Variables

| Variable          | Description            | Example                |
| ----------------- | ---------------------- | ---------------------- |
| `SMTP_HOST`       | Brevo SMTP server      | smtp-relay.brevo.com   |
| `SMTP_PORT`       | SMTP port              | 587                    |
| `SMTP_USERNAME`   | Brevo login email      | your-email@example.com |
| `SMTP_PASSWORD`   | Brevo SMTP key         | your-smtp-key          |
| `SMTP_FROM_EMAIL` | Sender email           | sender@example.com     |
| `SMTP_FROM_NAME`  | Sender name            | BPO Acceptor           |
| `RECIPIENT_EMAIL` | Lead recipient         | recipient@example.com  |
| `WEBHOOK_SECRET`  | Webhook security token | optional               |
| `DEBUG`           | Debug mode             | True/False             |

## Deploying to Render

1. **Push to GitHub** (ensure `.env` is in `.gitignore`)
2. **Create Web Service** on Render
3. **Configure Build**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Add Environment Variables** in Render dashboard
5. **Deploy!**
6. **Configure Webhook** in Brevo with your Render URL

## Testing

### Test Lead Submission

```bash
curl -X POST "http://localhost:8000/bpo-acceptor-lead" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Test Lead\",\"email\":\"test@example.com\",\"phone\":\"+1234567890\",\"company\":\"Test Co\",\"message\":\"Testing\"}"
```

### Monitor Webhook Events

Check application logs to see webhook events being processed:

```
INFO: Received webhook event: delivered for test@example.com
INFO: ✅ Email delivered to test@example.com
INFO: Processing webhook event: delivered for test@example.com
```

## Customization

Edit `app/webhook_handler.py` to customize automation logic:

```python
async def _handle_click(self, event: BrevoWebhookEvent):
    # Add your custom logic here
    # - Notify sales team
    # - Update CRM
    # - Trigger follow-up email
    # - Add to high-priority list
    pass
```

## Troubleshooting

**SMTP Authentication Failed**

- Verify SMTP credentials in `.env`
- Ensure you're using Brevo SMTP key, not API key

**Webhook Not Receiving Events**

- Check webhook URL in Brevo dashboard
- Verify app is running and accessible
- Check Brevo webhook logs for errors

**Module Not Found**

- Activate virtual environment: `.venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

## Documentation

- Interactive API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- [Brevo Webhook Docs](https://developers.brevo.com/docs/webhooks)
- [Brevo SMTP Guide](https://help.brevo.com/hc/en-us/articles/209467485)

## License

Open source and available for personal and commercial use.
