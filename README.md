## Features

### Invitation Management
- Create invitations with unique UUID-based IDs
- Generate unique links and QR codes for each event
- Support for sub-events within invitations
- Automatic chat group creation for each invitation

### Chat System
- MongoDB-based chat groups for each invitation
- Real-time messaging capabilities with WebSocket support
- Group management with member addition
- Message history retrieval
- Live message broadcasting to connected clients

## API Endpoints

### Invitations
- `POST /service/invitation/` - Create/update invitation (automatically creates chat group)
- `GET /service/invitation/` - Get all invitations
- `GET /service/invitation/{id}` - Get invitation by ID

### Chat
- `GET /chat/group/{invitation_id}` - Get chat group for invitation
- `POST /chat/group/{chat_group_id}/message` - Send message to chat group
- `GET /chat/group/{chat_group_id}/messages` - Get messages from chat group
- `GET /chat/user/{user_id}/groups` - Get all chat groups for user
- `WebSocket /chat/ws/{chat_group_id}` - Real-time chat WebSocket endpoint

## WebSocket Chat Usage

Connect to the WebSocket endpoint at `ws://localhost:8000/chat/ws/{chat_group_id}` to receive real-time messages.

### Client Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/chat/ws/your_chat_group_id');

// Join the chat group
ws.onopen = function(event) {
    ws.send(JSON.stringify({
        "type": "join"
    }));
};

// Listen for messages
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'new_message') {
        console.log('New message:', data.data);
    }
};
```

### Message Types
- `new_message`: Broadcast when a new message is sent to the group
- `joined`: Confirmation when client successfully joins the group
- `message_received`: Acknowledgment when a message is sent via HTTP endpoint

Messages sent via the HTTP `POST /chat/group/{chat_group_id}/message` endpoint are automatically broadcast to all connected WebSocket clients in real-time.

## Testing WebSocket Functionality

Run the test script to verify WebSocket connections:

```bash
python test_websocket.py
```

This will connect to a chat group and listen for real-time messages.

## Setup (local)

Create and activate a virtualenv (Linux/macOS):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment:

```bash
cp .env.example .env
```

### Database Setup

Start PostgreSQL and MongoDB:

```bash
docker-compose up -d
```

Run database migrations:

```bash
cd app/api
alembic upgrade head
```

Run API:

```bash
uvicorn app.main:app --reload
```

## Common issue: `ModuleNotFoundError: No module named 'fastapi'`

This means you started `uvicorn` outside the virtualenv. Re-run with the venv activated:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```