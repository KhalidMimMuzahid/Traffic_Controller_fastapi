# connection_manager.py
from fastapi import WebSocket
from typing import List

active_connections: List[WebSocket] = []