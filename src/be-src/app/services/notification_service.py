from fastapi import WebSocket, WebSocketDisconnect

# Danh sách kết nối WebSocket của Admin
admin_connections = set()

async def websocket_endpoint(websocket: WebSocket):
    """WebSocket để Admin nhận thông báo."""
    await websocket.accept()
    admin_connections.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # Giữ kết nối mở
    except WebSocketDisconnect:
        admin_connections.remove(websocket)

async def send_notification(message: str):
    """Gửi thông báo đến tất cả Admin đang kết nối."""
    for connection in admin_connections:
        await connection.send_text(message)
