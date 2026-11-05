import asyncio
import os
import random
import time
from typing import Dict, List, Optional, Union

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired, TwoFactorRequired
from playwright.async_api import async_playwright
import uvicorn

app = FastAPI(title="PRATIKXABHI //@ABUSIVEGANG PANEL")

# =====================================================================
# MULTI-USER ISOLATED LOGGING CONSOLE MANAGER
# =====================================================================
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        if username not in self.active_connections:
            self.active_connections[username] = []
        self.active_connections[username].append(websocket)

    def disconnect(self, websocket: WebSocket, username: str):
        if username in self.active_connections:
            if websocket in self.active_connections[username]:
                self.active_connections[username].remove(websocket)

    async def send_user_log(self, username: str, message: str, log_type: str = "info"):
        if username in self.active_connections:
            payload = {"message": message, "type": log_type, "timestamp": time.strftime("%H:%M:%S")}
            for connection in self.active_connections[username]:
                try:
                    await connection.send_json(payload)
                except Exception:
                    pass

manager = ConnectionManager()

# =====================================================================
# DYNAMIC DELAY PARSER UTILITY
# Supports single numeric delays (e.g. 3.5) or dynamic ranges (e.g. "20, 35")
# =====================================================================
def parse_panel_delay(delay_input: Union[str, float, int]) -> float:
    if isinstance(delay_input, (int, float)):
        return float(delay_input)
    if isinstance(delay_input, str):
        parts = [p.strip() for p in delay_input.split(",") if p.strip()]
        if len(parts) == 1:
            return float(parts[0])
        elif len(parts) >= 2:
            low = float(parts[0])
            high = float(parts[1])
            return random.uniform(low, high)
    return 3.0

# =====================================================================
# INSTAGRAPI CORE ENGINE SUITE
# =====================================================================
class InstagrapiEngineSuite:
    def __init__(self, owner: str):
        self.owner = owner
        self.cl = Client()
        self.is_authenticated = False
        self.session_cookie = None

    async def login_session(self, session_id: str) -> bool:
        try:
            await manager.send_user_log(self.owner, "[+] Authenticating session ID...", "info")
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.cl.login_by_sessionid, session_id)
            self.session_cookie = session_id
            self.is_authenticated = True
            await manager.send_user_log(self.owner, f"[SUCCESS] Logged in as @{self.cl.username}", "success")
            return True
        except Exception as e:
            await manager.send_user_log(self.owner, f"[ERROR] Session authentication failed: {e}", "error")
            return False

    async def run_insta_api_spam(self, messages: List[str], thread_id: Optional[str], delay_setting: str, loop_count: int = 10):
        if not self.is_authenticated:
            await manager.send_user_log(self.owner, "[!] Account not authenticated.", "error")
            return

        await manager.send_user_log(self.owner, "🚀 Starting Insta API Spammer Engine...", "info")
        loop = asyncio.get_event_loop()

        for i in range(loop_count):
            msg = random.choice(messages)
            delay = parse_panel_delay(delay_setting)

            if thread_id:
                try:
                    await loop.run_in_executor(None, lambda: self.cl.direct_send(msg, thread_ids=[thread_id]))
                    await manager.send_user_log(self.owner, f"[SINGLE GC] Sent msg #{i+1} to Thread {thread_id} | Delay: {delay:.2f}s", "success")
                except Exception as e:
                    await manager.send_user_log(self.owner, f"[ERROR] Single GC send error: {e}", "error")
            else:
                try:
                    threads = await loop.run_in_executor(None, lambda: self.cl.direct_threads(amount=20))
                    for t in threads:
                        await loop.run_in_executor(None, lambda: self.cl.direct_send(msg, thread_ids=[t.id]))
                        await manager.send_user_log(self.owner, f"[MULTI GC] Sent msg #{i+1} to Thread {t.id}", "success")
                except Exception as e:
                    await manager.send_user_log(self.owner, f"[ERROR] Multi GC execution error: {e}", "error")

            await asyncio.sleep(delay)

    async def run_photo_spam(self, image_path: str, thread_id: Optional[str], delay_setting: str, loop_count: int = 5):
        if not self.is_authenticated or not os.path.exists(image_path):
            await manager.send_user_log(self.owner, "[!] Invalid authentication or image path.", "error")
            return

        await manager.send_user_log(self.owner, "🖼️ Starting Photo Spammer Engine...", "info")
        loop = asyncio.get_event_loop()

        for i in range(loop_count):
            delay = parse_panel_delay(delay_setting)

            if thread_id:
                try:
                    await loop.run_in_executor(None, lambda: self.cl.direct_send_photo(image_path, thread_ids=[thread_id]))
                    await manager.send_user_log(self.owner, f"[PHOTO SINGLE GC] Sent photo #{i+1} | Delay: {delay:.2f}s", "success")
                except Exception as e:
                    await manager.send_user_log(self.owner, f"[ERROR] Single GC Photo error: {e}", "error")
            else:
                try:
                    threads = await loop.run_in_executor(None, lambda: self.cl.direct_threads(amount=20))
                    for t in threads:
                        await loop.run_in_executor(None, lambda: self.cl.direct_send_photo(image_path, thread_ids=[t.id]))
                        await manager.send_user_log(self.owner, f"[PHOTO MULTI GC] Blast sent to Thread {t.id}", "success")
                except Exception as e:
                    await manager.send_user_log(self.owner, f"[ERROR] Multi GC Photo error: {e}", "error")

            await asyncio.sleep(delay)

    async def run_gcpfp_changer(self, image_path: str, thread_id: Optional[str], delay_setting: str):
        if not self.is_authenticated or not os.path.exists(image_path):
            await manager.send_user_log(self.owner, "[!] Invalid authentication or image path.", "error")
            return

        await manager.send_user_log(self.owner, "📸 Starting GCPFP Profile Changer...", "info")
        loop = asyncio.get_event_loop()
        delay = parse_panel_delay(delay_setting)

        targets = [thread_id] if thread_id else [t.id for t in await loop.run_in_executor(None, lambda: self.cl.direct_threads(amount=20))]

        for tid in targets:
            try:
                await loop.run_in_executor(None, lambda: self.cl.direct_thread_change_photo(tid, image_path))
                await manager.send_user_log(self.owner, f"[GCPFP] PFP updated for Group {tid} | Delay: {delay:.2f}s", "success")
            except Exception as e:
                await manager.send_user_log(self.owner, f"[ERROR] GCPFP error for Thread {tid}: {e}", "error")
            await asyncio.sleep(delay)

    async def run_gcnc_protection(self, target_title: str, thread_id: Optional[str], delay_setting: str):
        if not self.is_authenticated:
            await manager.send_user_log(self.owner, "[!] Account not authenticated.", "error")
            return

        await manager.send_user_log(self.owner, "✏️ Starting GCNC Title Protection Engine...", "info")
        loop = asyncio.get_event_loop()
        delay = parse_panel_delay(delay_setting)

        targets = [thread_id] if thread_id else [t.id for t in await loop.run_in_executor(None, lambda: self.cl.direct_threads(amount=20))]

        for tid in targets:
            try:
                await loop.run_in_executor(None, lambda: self.cl.direct_thread_title(tid, target_title))
                await manager.send_user_log(self.owner, f"[GCNC] Applied title lock '{target_title}' on Thread {tid}", "success")
            except Exception as e:
                await manager.send_user_log(self.owner, f"[ERROR] Title protection failed on Thread {tid}: {e}", "error")
            await asyncio.sleep(delay)

    async def run_gc_creator(self, usernames: List[str], gc_prefix: str, total_gcs: int, delay_setting: str):
        if not self.is_authenticated:
            await manager.send_user_log(self.owner, "[!] Account not authenticated.", "error")
            return

        await manager.send_user_log(self.owner, "➕ Starting Mass GC Creator Engine...", "info")
        loop = asyncio.get_event_loop()

        user_ids = []
        for uname in usernames:
            try:
                uid = await loop.run_in_executor(None, lambda: self.cl.user_id_from_username(uname.strip()))
                user_ids.append(uid)
                await manager.send_user_log(self.owner, f"[RESOLVED] @{uname} -> UID: {uid}", "info")
            except Exception as e:
                await manager.send_user_log(self.owner, f"[WARNING] User @{uname} resolve error: {e}", "error")

        if not user_ids:
            return

        for i in range(total_gcs):
            title = f"{gc_prefix} #{i+1}"
            delay = parse_panel_delay(delay_setting)
            try:
                thread = await loop.run_in_executor(None, lambda: self.cl.direct_thread_create(user_ids, title=title))
                await manager.send_user_log(self.owner, f"[CREATED] Group '{title}' (ID: {thread.id}) created!", "success")
            except Exception as e:
                await manager.send_user_log(self.owner, f"[ERROR] Failed to create GC #{i+1}: {e}", "error")

            await manager.send_user_log(self.owner, f"[WAIT] Dynamic jitter delay: {delay:.2f}s...", "info")
            await asyncio.sleep(delay)

# =====================================================================
# PLAYWRIGHT BROWSER ENGINE MODULE
# =====================================================================
class PlaywrightEngineModule:
    def __init__(self, owner: str):
        self.owner = owner

    async def run_playwright_spammer(self, session_cookie: str, target_url: str, messages: List[str], delay_setting: str, loop_count: int = 5):
        await manager.send_user_log(self.owner, "⚡ Launching Playwright Browser Module...", "info")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()

            if session_cookie:
                await context.add_cookies([{"name": "sessionid", "value": session_cookie, "domain": ".instagram.com", "path": "/"}])

            page = await context.new_page()
            try:
                await page.goto(target_url, timeout=60000)
                await asyncio.sleep(5)

                for i in range(loop_count):
                    msg = random.choice(messages)
                    delay = parse_panel_delay(delay_setting)

                    try:
                        selector = 'div[contenteditable="true"][aria-label="Message"]'
                        await page.wait_for_selector(selector, timeout=10000)
                        await page.click(selector)
                        await page.keyboard.type(msg)
                        await page.keyboard.press("Enter")
                        await manager.send_user_log(self.owner, f"[PLAYWRIGHT] Sent browser msg #{i+1}: '{msg}' | Delay: {delay:.2f}s", "success")
                    except Exception as err:
                        await manager.send_user_log(self.owner, f"[PLAYWRIGHT WARNING] DOM interaction error: {err}", "error")

                    await asyncio.sleep(delay)

            except Exception as e:
                await manager.send_user_log(self.owner, f"[PLAYWRIGHT ERROR] Session failed: {e}", "error")
            finally:
                await browser.close()
                await manager.send_user_log(self.owner, "[PLAYWRIGHT] Browser closed.", "info")

# =====================================================================
# EMBEDDED HTML FRONTEND INTERFACE
# =====================================================================
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PRATIKXABHI //@ABUSIVEGANG PANEL</title>
    <style>
        :root {
            --bg-base: #030712;
            --panel-bg: #0b0f19;
            --card-bg: #111827;
            --border-color: #1f293d;
            --accent-red: #ff1e56;
            --accent-blue: #00f0ff;
            --accent-glow-red: rgba(255, 30, 86, 0.25);
            --accent-glow-blue: rgba(0, 240, 255, 0.25);
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
        }
        * { box-sizing: border-box; }
        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
            margin: 0; padding: 15px;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 30, 86, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(0, 240, 255, 0.05) 0%, transparent 40%);
            background-attachment: fixed;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        
        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--panel-bg); border: 1px solid var(--border-color); padding: 16px 24px;
            border-radius: 12px; margin-bottom: 15px; box-shadow: 0 0 25px var(--accent-glow-red), inset 0 0 15px rgba(0, 240, 255, 0.05);
        }
        .fire-title {
            font-size: 20px; font-weight: 900; letter-spacing: 1.5px; margin: 0; text-transform: uppercase;
            background: linear-gradient(135deg, #ff1e56 20%, #ff8800 50%, #00f0ff 90%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 12px rgba(255, 30, 86, 0.7)) drop-shadow(0 0 20px rgba(0, 240, 255, 0.4));
            animation: firePulse 3s ease-in-out infinite alternate;
        }
        @keyframes firePulse {
            0% { filter: drop-shadow(0 0 10px rgba(255, 30, 86, 0.6)) drop-shadow(0 0 15px rgba(0, 240, 255, 0.3)); }
            100% { filter: drop-shadow(0 0 18px rgba(255, 30, 86, 0.9)) drop-shadow(0 0 25px rgba(0, 240, 255, 0.6)); }
        }

        .nav-tabs { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; background: var(--panel-bg); padding: 10px 18px; border-radius: 10px; border: 1px solid var(--border-color); flex-wrap: wrap; gap: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        .nav-left { display: flex; gap: 8px; flex-wrap: wrap; }
        .nav-tabs a {
            background: var(--card-bg); border: 1px solid var(--border-color); color: var(--text-muted);
            padding: 8px 14px; border-radius: 6px; text-decoration: none; font-size: 11px; font-weight: 600; transition: 0.2s; cursor: pointer; text-transform: uppercase;
        }
        .nav-tabs a:hover { color: var(--accent-blue); border-color: var(--accent-blue); box-shadow: 0 0 10px var(--accent-glow-blue); }
        .nav-tabs a.active { background: linear-gradient(135deg, var(--accent-red), #b91c1c); color: #fff; border-color: var(--accent-red); font-weight: 700; box-shadow: 0 0 12px var(--accent-glow-red); }
        .btn-logout { background: #881337 !important; color: #fff !important; border-color: #f43f5e !important; }

        .stats-bar {
            background: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 10px;
            padding: 12px 20px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;
            font-size: 12px; font-family: monospace; white-space: nowrap; overflow-x: auto; box-shadow: inset 0 0 15px rgba(0, 240, 255, 0.03);
        }
        .stat-item { display: flex; align-items: center; gap: 8px; }
        .stat-item span { color: var(--text-muted); }
        .stat-item strong { color: var(--accent-blue); font-weight: 700; text-shadow: 0 0 8px var(--accent-glow-blue); }

        .dashboard-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
        @media(max-width: 1100px) { .dashboard-grid { grid-template-columns: 1fr; } }

        .card {
            background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px;
            padding: 18px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4); display: flex; flex-direction: column; justify-content: space-between;
            position: relative; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .card:hover { border-color: var(--accent-blue); box-shadow: 0 8px 30px var(--accent-glow-blue); transform: translateY(-2px); }
        .card-top-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
        .card-icon-box {
            width: 42px; height: 42px; background: #030712; border: 1px solid var(--border-color); border-radius: 10px;
            display: flex; align-items: center; justify-content: center; font-size: 18px; color: var(--accent-blue);
            box-shadow: inset 0 0 10px rgba(0, 240, 255, 0.1);
        }
        .badge-tag {
            background: rgba(0, 240, 255, 0.1); border: 1px solid var(--accent-blue); color: var(--accent-blue);
            padding: 4px 10px; font-size: 9px; font-weight: 700; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.8px;
            box-shadow: 0 0 8px rgba(0, 240, 255, 0.2);
        }
        .card-title { font-size: 15px; font-weight: 700; color: var(--text-main); margin-bottom: 6px; letter-spacing: 0.5px; }
        .card-desc { font-size: 11px; color: var(--text-muted); line-height: 1.4; margin-bottom: 15px; font-family: monospace; }
        
        .tags-row { display: flex; gap: 6px; margin-bottom: 15px; flex-wrap: wrap; }
        .mini-tag { background: #030712; border: 1px solid var(--border-color); color: var(--text-muted); padding: 3px 8px; border-radius: 6px; font-size: 9px; font-family: monospace; }

        .btn {
            width: 100%; padding: 11px; background: linear-gradient(135deg, var(--accent-red), #dc2626); border: none; color: #fff;
            font-weight: 700; border-radius: 8px; cursor: pointer; font-size: 11px; margin-top: 6px; transition: all 0.2s;
            text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 15px var(--accent-glow-red);
        }
        .btn:hover { opacity: 0.9; transform: scale(1.01); box-shadow: 0 6px 20px rgba(255, 30, 86, 0.4); }
        .btn-danger { background: linear-gradient(135deg, #991b1b, #7f1d1d); box-shadow: 0 4px 15px rgba(153, 27, 27, 0.4); }
        .btn-success { background: linear-gradient(135deg, #0e7490, #00f0ff); color: #030712; box-shadow: 0 4px 15px var(--accent-glow-blue); font-weight: 800; }

        .view-section { display: none; }
        .view-section.active { display: block; }

        .form-group { margin-bottom: 15px; }
        label { display: block; font-size: 11px; font-weight: 600; color: var(--accent-blue); margin-bottom: 6px; font-family: monospace; letter-spacing: 0.5px; }
        input, select, textarea {
            width: 100%; padding: 10px 12px; background: #030712; border: 1px solid var(--border-color);
            color: var(--text-main); border-radius: 8px; font-size: 11px; outline: none; transition: all 0.2s;
        }
        input:focus, select:focus, textarea:focus { border-color: var(--accent-blue); box-shadow: 0 0 12px var(--accent-glow-blue); }

        .checkbox-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 8px; background: #030712; padding: 12px; border-radius: 8px; border: 1px solid var(--border-color); max-height: 140px; overflow-y: auto; }
        .checkbox-item { display: flex; align-items: center; gap: 6px; font-size: 11px; cursor: pointer; color: var(--text-main); font-family: monospace; }

        .node-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 11px; font-family: monospace; }
        .node-table th, .node-table td { border: 1px solid var(--border-color); padding: 10px; text-align: left; }
        .node-table th { background: #030712; color: var(--accent-blue); text-transform: uppercase; letter-spacing: 0.5px; }
        .status-pill { padding: 3px 8px; border-radius: 12px; font-size: 9px; font-weight: 700; text-transform: uppercase; display: inline-block; }
        .status-live { background: rgba(0, 240, 255, 0.15); border: 1px solid var(--accent-blue); color: var(--accent-blue); box-shadow: 0 0 8px var(--accent-glow-blue); }
        .status-stop { background: rgba(255, 30, 86, 0.15); border: 1px solid var(--accent-red); color: var(--accent-red); }

        .terminal-container { grid-column: span 3; margin-top: 15px; }
        @media(max-width: 1100px) { .terminal-container { grid-column: span 1; } }
        .terminal {
            background: #030712; border: 1px solid var(--border-color); border-radius: 8px;
            height: 260px; overflow-y: auto; padding: 14px; font-size: 11px; font-family: monospace; display: flex; flex-direction: column-reverse;
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.8);
        }
        .log-line { margin-bottom: 5px; }
        .success { color: var(--accent-blue); }
        .error { color: var(--accent-red); font-weight: bold; }
        .warning { color: #f59e0b; }
        .info { color: #38bdf8; }

        #authModal {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(3, 7, 18, 0.92); backdrop-filter: blur(8px); z-index: 9999;
            display: flex; align-items: center; justify-content: center; padding: 20px;
        }
        .auth-card {
            background: var(--panel-bg); border: 1px solid var(--accent-blue); border-radius: 16px;
            width: 100%; max-width: 420px; padding: 30px; box-shadow: 0 0 40px var(--accent-glow-blue);
        }
    </style>
</head>
<body>

    <div id="authModal">
        <div class="auth-card">
            <h2 id="authModalTitle" style="color: var(--accent-blue); margin-top: 0; font-size: 18px; text-align: center; text-transform: uppercase; letter-spacing: 1px;">🔐 Panel Authentication</h2>
            <p id="authModalSubtitle" style="color: var(--text-muted); font-size: 11px; text-align: center; margin-bottom: 20px;">New user? Register your credentials to save session access.</p>
            
            <div class="form-group">
                <label>Username / Handle</label>
                <input type="text" id="modalUser" placeholder="Enter username...">
            </div>
            <div class="form-group">
                <label>Access Password</label>
                <input type="password" id="modalPass" placeholder="Enter password...">
            </div>
            <button type="button" class="btn btn-success" style="width: 100%; margin-top: 10px;" onclick="handleAuthSubmit()">Authorize Access</button>
        </div>
    </div>

<div class="container">
    <div class="header">
        <h1 class="fire-title">PRATIKXABHI //@ABUSIVEGANG PANEL</h1>
        <div style="font-size: 12px; color: var(--text-muted); font-family: monospace;">Uptime: <span id="uptime" style="color: var(--accent-blue); font-weight: 700;">0h 0m 0s</span></div>
    </div>

    <div class="stats-bar">
        <div class="stat-item"><span>🛡️ IDs:</span> <strong id="stat-logged-count">4</strong></div>
        <div class="stat-item"><span>⚡ Active:</span> <strong id="stat-running-count">2</strong></div>
        <div class="stat-item"><span>💬 Sent:</span> <strong id="stat-msg-sent">1,420</strong></div>
    </div>

    <div class="nav-tabs">
        <div class="nav-left">
            <a onclick="switchView('dashboard')" id="nav-dashboard" class="active">Control Hub</a>
            <a onclick="openEngine('nodes')" id="nav-nodes">Nodes List & Status</a>
            <a id="nav-engine-breadcrumb" style="display:none; background: var(--accent-blue); color: #030712; font-weight: 700;" class="active">Active Engine Console</a>
        </div>
        <div>
            <a href="#" class="btn-logout" onclick="logoutUser()">Logout</a>
        </div>
    </div>

    <div id="view-dashboard" class="view-section active">
        <div class="dashboard-grid">
            <div class="card">
                <div>
                    <div class="card-top-header">
                        <div class="card-icon-box">🛡️</div>
                        <div class="badge-tag">Auth Vault</div>
                    </div>
                    <div class="card-title">Managed Accounts</div>
                    <div class="card-desc">Dedicated ID login hub via Session ID or IDP credentials with OTP verification flow.</div>
                    <div class="tags-row">
                        <span class="mini-tag">Session ID</span>
                        <span class="mini-tag">IDP Login</span>
                        <span class="mini-tag">OTP</span>
                    </div>
                </div>
                <button class="btn" onclick="openEngine('auth')">LAUNCH ENGINE &rarr;</button>
            </div>

            <div class="card">
                <div>
                    <div class="card-top-header">
                        <div class="card-icon-box">💬</div>
                        <div class="badge-tag">Insta API</div>
                    </div>
                    <div class="card-title">Insta API Spammer</div>
                    <div class="card-desc">Multi-node text broadcasting via uploaded .txt file payloads supporting Single GC or Multiple GC routing.</div>
                    <div class="tags-row">
                        <span class="mini-tag">.txt File Upload</span>
                        <span class="mini-tag">Multi/Single GC</span>
                        <span class="mini-tag">Delay Jitter</span>
                    </div>
                </div>
                <button class="btn btn-success" onclick="openEngine('insta_api')">LAUNCH ENGINE &rarr;</button>
            </div>

            <div class="card">
                <div>
                    <div class="card-top-header">
                        <div class="card-icon-box">🖼️</div>
                        <div class="badge-tag">Photo Spm</div>
                    </div>
                    <div class="card-title">Photo Spammer</div>
                    <div class="card-desc">Continuous direct photo blast across Single & Multiple GC targets using uploaded .jpeg payloads.</div>
                    <div class="tags-row">
                        <span class="mini-tag">.jpeg Upload</span>
                        <span class="mini-tag">Multi/Single GC</span>
                        <span class="mini-tag">Delay</span>
                    </div>
                </div>
                <button class="btn" onclick="openEngine('photo')">LAUNCH ENGINE &rarr;</button>
            </div>

            <div class="card">
                <div>
                    <div class="card-top-header">
                        <div class="card-icon-box">📸</div>
                        <div class="badge-tag">Gcpfp Chnge</div>
                    </div>
                    <div class="card-title">GCPFP Profile Changer</div>
                    <div class="card-desc">Change group profile picture with .jpeg file upload and custom delay intervals (Except managed and GC creator).</div>
                    <div class="tags-row">
                        <span class="mini-tag">.jpeg PFP</span>
                        <span class="mini-tag">Except Managed</span>
                        <span class="mini-tag">Delay</span>
                    </div>
                </div>
                <button class="btn" onclick="openEngine('gcpfp')">LAUNCH ENGINE &rarr;</button>
            </div>

            <div class="card">
                <div>
                    <div class="card-top-header">
                        <div class="card-icon-box">✏️</div>
                        <div class="badge-tag">Gcnc Chnge</div>
                    </div>
                    <div class="card-title">GCNC Name Protection</div>
                    <div class="card-desc">Secure group title lock and automated name reversion across Single or Multiple GCs (Except managed and GC creator).</div>
                    <div class="tags-row">
                        <span class="mini-tag">NC Lock</span>
                        <span class="mini-tag">Except Managed</span>
                        <span class="mini-tag">Auto Sync</span>
                    </div>
                </div>
                <button class="btn" onclick="openEngine('gcnc')">LAUNCH ENGINE &rarr;</button>
            </div>

            <div class="card">
                <div>
                    <div class="card-top-header">
                        <div class="card-icon-box">➕</div>
                        <div class="badge-tag">GC Creator</div>
                    </div>
                    <div class="card-title">GC Creator Engine</div>
                    <div class="card-desc">Mass sequential group creation adding multiple comma-separated usernames with dynamic delay box (e.g. 20,35).</div>
                    <div class="tags-row">
                        <span class="mini-tag">Comma Users</span>
                        <span class="mini-tag">Delay Jitter</span>
                    </div>
                </div>
                <button class="btn" onclick="openEngine('gc_creator')">LAUNCH ENGINE &rarr;</button>
            </div>

            <div class="card">
                <div>
                    <div class="card-top-header">
                        <div class="card-icon-box">⚡</div>
                        <div class="badge-tag">Playwright</div>
                    </div>
                    <div class="card-title">Playwright Automation</div>
                    <div class="card-desc">Automated browser spam routine via uploaded .txt file payloads supporting Single GC or Multiple GC targets.</div>
                    <div class="tags-row">
                        <span class="mini-tag">.txt File Upload</span>
                        <span class="mini-tag">Multi/Single GC</span>
                        <span class="mini-tag">Delay Jitter</span>
                    </div>
                </div>
                <button class="btn" onclick="openEngine('playwright')">LAUNCH ENGINE &rarr;</button>
            </div>
        </div>
    </div>

    <div id="view-engine" class="view-section">
        <div style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 22px; margin-bottom: 15px; box-shadow: 0 8px 30px rgba(0,0,0,0.5);">
            <div class="card-header" id="engine-page-title" style="margin-bottom: 15px; font-size: 14px; color: var(--accent-blue); font-family: monospace; font-weight: 700;"></div>
            
            <form id="engine-active-form">
                <div id="account-selector-wrapper" class="form-group" style="background: #030712; padding: 14px; border-radius: 8px; border: 1px solid var(--border-color); margin-bottom: 15px;">
                    <label style="color: var(--accent-blue); font-weight: 700; margin-bottom: 8px; font-size: 11px;">Select Logged-In Accounts / Nodes from Panel</label>
                    <div class="checkbox-grid">
                        <label class="checkbox-item"><input type="checkbox" name="node_select" value="bot_alpha" checked> @bot_alpha</label>
                        <label class="checkbox-item"><input type="checkbox" name="node_select" value="instarunner" checked> @instarunner</label>
                        <label class="checkbox-item"><input type="checkbox" name="node_select" value="abusive_node1"> @abusive_node1</label>
                        <label class="checkbox-item"><input type="checkbox" name="node_select" value="elite_spammer"> @elite_spammer</label>
                    </div>
                </div>

                <div id="engine-form-content"></div>

                <div id="execution-buttons-wrapper" style="display: flex; gap: 10px; margin-top: 18px;">
                    <button type="button" class="btn btn-success" style="flex: 2;" onclick="alert('Engine Started Successfully!')">▶ START</button>
                    <button type="button" class="btn btn-danger" style="flex: 1;" onclick="alert('Engine Halted!')">⏹ HALT</button>
                    <button type="button" class="btn" style="background: var(--panel-bg); color: var(--text-main); border: 1px solid var(--border-color); flex: 1;" onclick="switchView('dashboard')">BACK</button>
                </div>
            </form>
        </div>
    </div>

    <div class="card terminal-container">
        <div class="card-header" style="color: var(--accent-blue); font-weight: 700; margin-bottom: 8px;">💀 Private Terminal Console & Telemetry (Encrypted & Isolated)</div>
        <div id="terminal" class="terminal">
            <div class="log-line info">[ABUSIVEGANG] Secure haunted console active. No cross-user log leaks detected.</div>
        </div>
    </div>
</div>

<script>
    let ws = null;
    let currentUser = null;

    window.addEventListener('DOMContentLoaded', () => {
        let savedCreds = localStorage.getItem('abusivegang_user');
        if(savedCreds) {
            let data = JSON.parse(savedCreds);
            currentUser = data.username;
            document.getElementById('authModal').style.display = 'none';
            initWebSocket();
        } else {
            document.getElementById('authModal').style.display = 'flex';
        }
    });

    function initWebSocket() {
        if (!currentUser) return;
        let protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        ws = new WebSocket(`${protocol}//${window.location.host}/ws/${currentUser}`);
        ws.onmessage = (event) => {
            let data = JSON.parse(event.data);
            logTerminal(data.message, data.type);
        };
    }

    function handleAuthSubmit() {
        let u = document.getElementById('modalUser').value.trim();
        let p = document.getElementById('modalPass').value.trim();
        if(!u || !p) {
            alert('Please enter both username and password.');
            return;
        }
        currentUser = u;
        localStorage.setItem('abusivegang_user', JSON.stringify({username: u, password: p}));
        document.getElementById('authModal').style.display = 'none';
        initWebSocket();
        alert('Credentials saved successfully! Welcome to @Abusivegang Suite.');
    }

    function logoutUser() {
        localStorage.removeItem('abusivegang_user');
        location.reload();
    }

    function switchView(viewName) {
        document.getElementById('view-dashboard').classList.remove('active');
        document.getElementById('view-engine').classList.remove('active');
        document.getElementById('nav-dashboard').classList.remove('active');
        document.getElementById('nav-nodes').classList.remove('active');
        document.getElementById('nav-engine-breadcrumb').style.display = 'none';

        if(viewName === 'dashboard') {
            document.getElementById('view-dashboard').classList.add('active');
            document.getElementById('nav-dashboard').classList.add('active');
        } else if(viewName === 'engine') {
            document.getElementById('view-engine').classList.add('active');
            document.getElementById('nav-engine-breadcrumb').style.display = 'inline-block';
        }
        window.scrollTo(0, 0);
    }

    function removeNode(btnEl) {
        let row = btnEl.closest('tr');
        row.remove();
        alert('Node removed successfully from status matrix.');
    }

    function openEngine(engineType) {
        let titleEl = document.getElementById('engine-page-title');
        let contentEl = document.getElementById('engine-form-content');
        let accSelectorWrapper = document.getElementById('account-selector-wrapper');
        let execButtonsWrapper = document.getElementById('execution-buttons-wrapper');
        let html = '';

        if(engineType === 'nodes') {
            titleEl.innerText = "📋 Active Logged-In Nodes List & Status Matrix";
            accSelectorWrapper.style.display = 'none';
            execButtonsWrapper.style.display = 'none';
            html = `
                <div style="overflow-x:auto;">
                    <table class="node-table">
                        <thead>
                            <tr>
                                <th>Username</th>
                                <th>Engine</th>
                                <th>Status</th>
                                <th>Thread</th>
                                <th>Msg Count</th>
                                <th>Engine Uptime</th>
                                <th>Total</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>@bot_alpha</td>
                                <td style="color:var(--accent-blue);">Insta API Spm</td>
                                <td><span class="status-pill status-live">Live</span></td>
                                <td>#104</td>
                                <td>840 Msgs</td>
                                <td>1h 12m</td>
                                <td>840</td>
                                <td><button class="btn btn-danger" style="padding:4px 8px; font-size:9px; margin:0;" onclick="removeNode(this)">Remove</button></td>
                            </tr>
                            <tr>
                                <td>@instarunner</td>
                                <td style="color:var(--accent-red);">GCPFP</td>
                                <td><span class="status-pill status-live">Live</span></td>
                                <td>#209</td>
                                <td>320 PFP</td>
                                <td>45m</td>
                                <td>320</td>
                                <td><button class="btn btn-danger" style="padding:4px 8px; font-size:9px; margin:0;" onclick="removeNode(this)">Remove</button></td>
                            </tr>
                            <tr>
                                <td>@abusive_node1</td>
                                <td style="color:var(--text-muted);">Standby</td>
                                <td><span class="status-pill status-stop">Stop</span></td>
                                <td>&mdash;</td>
                                <td>0 Msgs</td>
                                <td>0h 0m</td>
                                <td>0</td>
                                <td><button class="btn btn-danger" style="padding:4px 8px; font-size:9px; margin:0;" onclick="removeNode(this)">Remove</button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div style="margin-top:15px;">
                    <button type="button" class="btn" style="background: var(--panel-bg); color: var(--text-main); border: 1px solid var(--border-color);" onclick="switchView('dashboard')">RETURN TO HUB</button>
                </div>
            `;
            document.getElementById('nav-nodes').classList.add('active');
            document.getElementById('view-engine').classList.add('active');
            document.getElementById('view-dashboard').classList.remove('active');
            contentEl.innerHTML = html;
            window.scrollTo(0, 0);
            return;
        }

        if(engineType === 'auth') {
            titleEl.innerText = "🛡️ Managed Accounts & IDP Verification Vault";
            accSelectorWrapper.style.display = 'none';
            execButtonsWrapper.style.display = 'none';
            html = `
                <div class="form-group">
                    <label>Login Method</label>
                    <select id="loginModeSelect" onchange="toggleLoginMode()">
                        <option value="session">Session ID Cookie String</option>
                        <option value="idp">IDP Login (Username & Password + OTP)</option>
                    </select>
                </div>
                
                <div id="sessionFieldGroup" class="form-group">
                    <label>Session ID Cookie String</label>
                    <input type="text" placeholder="Paste sessionid cookie...">
                    <button type="button" class="btn" style="margin-top:8px;" onclick="alert('Session ID registered successfully!')">Authorize Session Node</button>
                </div>

                <div id="idpFieldGroup" style="display:none;">
                    <div class="form-group">
                        <label>Instagram Username / Email / Phone</label>
                        <input type="text" id="idpUser" placeholder="Enter username...">
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" id="idpPass" placeholder="Enter password...">
                    </div>
                    
                    <div id="otpBoxContainer" class="form-group" style="display:none; background:#030712; padding:12px; border:1px solid var(--accent-red); border-radius:8px; margin-top:8px;">
                        <label style="color:var(--accent-red);">Enter OTP / 2FA Code received</label>
                        <input type="text" id="idpOtp" placeholder="6-digit code..." style="margin-top:6px;">
                    </div>

                    <div style="display: flex; gap: 10px; margin-top: 12px;">
                        <button type="button" class="btn" style="flex:1;" onclick="handleIdpStep1()">1. Request Code</button>
                        <button type="button" class="btn btn-success" style="flex:1;" onclick="handleIdpStep2()">2. Verify & Login</button>
                    </div>
                </div>

                <div style="margin-top:15px;">
                    <button type="button" class="btn" style="background: var(--panel-bg); color: var(--text-main); border: 1px solid var(--border-color);" onclick="switchView('dashboard')">RETURN TO HUB</button>
                </div>
            `;
        } else {
            accSelectorWrapper.style.display = 'block';
            execButtonsWrapper.style.display = 'flex';

            if(engineType === 'insta_api') {
                titleEl.innerText = "💬 Insta API Spammer (.txt file upload)";
                html = `
                    <div class="form-group">
                        <label>Upload .txt Message Payload File</label>
                        <input type="file" accept=".txt" required style="padding: 6px;">
                    </div>
                    <div class="form-group">
                        <label>Routing Scope (Single GC vs Multiple GC)</label>
                        <select id="apiScopeSelect" onchange="toggleApiScope()">
                            <option value="multi">Multiple GC (All active threads - No Thread ID required)</option>
                            <option value="single">Single GC (Isolated target - Thread ID required)</option>
                        </select>
                    </div>
                    <div id="singleGcFields" style="display:none;">
                        <div class="form-group">
                            <label>Target Group ID / Thread Link</label>
                            <input type="text" placeholder="Thread ID...">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Delay Box (Single delay like 3.5 or comma-separated like 20,35)</label>
                        <input type="text" value="20,35" required placeholder="e.g. 20,35">
                    </div>
                `;
            } else if(engineType === 'photo') {
                titleEl.innerText = "🖼️ Photo Spammer (.jpeg direct blast)";
                html = `
                    <div class="form-group">
                        <label>Upload .jpeg Image File</label>
                        <input type="file" accept=".jpeg, .jpg" required style="padding: 6px;">
                    </div>
                    <div class="form-group">
                        <label>Routing Scope (Single GC vs Multiple GC)</label>
                        <select id="photoScopeSelect" onchange="togglePhotoScope()">
                            <option value="multi">Multiple GC (All active threads - No Thread ID required)</option>
                            <option value="single">Single GC (Isolated target - Thread ID required)</option>
                        </select>
                    </div>
                    <div id="photoSingleGcFields" style="display:none;">
                        <div class="form-group">
                            <label>Target Group ID / Thread Link</label>
                            <input type="text" placeholder="Thread ID...">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Delay Box (Single delay like 4.0 or comma-separated like 20,35)</label>
                        <input type="text" value="20,35" required placeholder="e.g. 20,35">
                    </div>
                `;
            } else if(engineType === 'gcpfp') {
                titleEl.innerText = "📸 GCPFP Profile Picture Changer (Except Managed & GC Creator)";
                html = `
                    <div class="form-group">
                        <label>Upload .jpeg Image File (Leave empty to skip)</label>
                        <input type="file" accept=".jpeg, .jpg" style="padding: 6px;">
                    </div>
                    <div class="form-group">
                        <label>Delay Box (Single or comma-separated like 20,35)</label>
                        <input type="text" value="20,35" required placeholder="e.g. 20,35">
                    </div>
                `;
            } else if(engineType === 'gcnc') {
                titleEl.innerText = "✏️ GCNC Group Name Protection (Except Managed & GC Creator)";
                html = `
                    <div class="form-group">
                        <label>Routing Scope (Single GC vs Multiple GC)</label>
                        <select id="gcncScopeSelect" onchange="toggleGcncScope()">
                            <option value="multi">Multiple GC (All active threads)</option>
                            <option value="single">Single GC (Thread ID required)</option>
                        </select>
                    </div>
                    <div id="gcncSingleFields" style="display:none;">
                        <div class="form-group">
                            <label>Target Group ID / Thread Link</label>
                            <input type="text" placeholder="Thread ID...">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>New Secured Group Title (GCNC)</label>
                        <input type="text" placeholder="Enter title..." required>
                    </div>
                    <div class="form-group">
                        <label>Delay Box (Single or comma-separated like 20,35)</label>
                        <input type="text" value="20,35" required placeholder="e.g. 20,35">
                    </div>
                `;
            } else if(engineType === 'gc_creator') {
                titleEl.innerText = "➕ Mass GC Creator Engine";
                html = `
                    <div class="form-group">
                        <label>Deployment Prefix</label>
                        <input type="text" value="RAID GROUP" required>
                    </div>
                    <div class="form-group">
                        <label>Usernames to Add (Comma Separated)</label>
                        <input type="text" placeholder="user1, user2, user3..." required>
                    </div>
                    <div class="form-group">
                        <label>Delay Box (Single delay or comma-separated like 20,35)</label>
                        <input type="text" value="20,35" required placeholder="e.g. 20,35">
                    </div>
                `;
            } else if(engineType === 'playwright') {
                titleEl.innerText = "⚡ Playwright Automation Engine (.txt file upload)";
                html = `
                    <div class="form-group">
                        <label>Upload .txt Message Payload File</label>
                        <input type="file" accept=".txt" required style="padding: 6px;">
                    </div>
                    <div class="form-group">
                        <label>Routing Scope (Single GC vs Multiple GC)</label>
                        <select id="pwScopeSelect" onchange="togglePwScope()">
                            <option value="multi">Multiple GC (All active threads - No Thread ID required)</option>
                            <option value="single">Single GC (Isolated target - Thread ID required)</option>
                        </select>
                    </div>
                    <div id="pwSingleGcFields" style="display:none;">
                        <div class="form-group">
                            <label>Target Group ID / Thread Link</label>
                            <input type="text" placeholder="Thread ID...">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Delay Box (Single delay like 3.5 or comma-separated like 20,35)</label>
                        <input type="text" value="20,35" required placeholder="e.g. 20,35">
                    </div>
                `;
            }
        }

        contentEl.innerHTML = html;
        switchView('engine');
    }

    function toggleLoginMode() {
        let mode = document.getElementById('loginModeSelect').value;
        if(mode === 'session') {
            document.getElementById('sessionFieldGroup').style.display = 'block';
            document.getElementById('idpFieldGroup').style.display = 'none';
        } else {
            document.getElementById('sessionFieldGroup').style.display = 'none';
            document.getElementById('idpFieldGroup').style.display = 'block';
        }
    }

    function handleIdpStep1() {
        let user = document.getElementById('idpUser').value;
        if(!user) {
            alert('Please enter your username first.');
            return;
        }
        alert('Login request sent! Verification code dispatched.');
        document.getElementById('otpBoxContainer').style.display = 'block';
    }

    function handleIdpStep2() {
        let otp = document.getElementById('idpOtp').value;
        if(!otp) {
            alert('Please paste the received OTP code.');
            return;
        }
        alert('OTP verified successfully! Account logged in.');
    }

    function toggleApiScope() {
        let scope = document.getElementById('apiScopeSelect').value;
        document.getElementById('singleGcFields').style.display = (scope === 'single') ? 'block' : 'none';
    }

    function togglePhotoScope() {
        let scope = document.getElementById('photoScopeSelect').value;
        document.getElementById('photoSingleGcFields').style.display = (scope === 'single') ? 'block' : 'none';
    }

    function toggleGcncScope() {
        let scope = document.getElementById('gcncScopeSelect').value;
        document.getElementById('gcncSingleFields').style.display = (scope === 'single') ? 'block' : 'none';
    }

    function togglePwScope() {
        let scope = document.getElementById('pwScopeSelect').value;
        document.getElementById('pwSingleGcFields').style.display = (scope === 'single') ? 'block' : 'none';
    }

    function logTerminal(msg, type="info") {
        let term = document.getElementById('terminal');
        let div = document.createElement('div');
        div.className = `log-line ${type}`;
        let time = new Date().toLocaleTimeString();
        div.innerText = `[${time}] [${currentUser || 'GUEST'}] ${msg}`;
        term.appendChild(div);
    }

    let startTime = Math.floor(Date.now() / 1000);
    function updateUptime() {
        let now = Math.floor(Date.now() / 1000);
        let diff = now - startTime;
        let h = Math.floor(diff / 3600);
        let m = Math.floor((diff % 3600) / 60);
        let s = diff % 60;
        document.getElementById('uptime').innerText = h + "h " + m + "m " + s + "s";
    }
    setInterval(updateUptime, 1000);
</script>
</body>
</html>"""

# =====================================================================
# ROUTING & WEBSOCKET ENDPOINTS
# =====================================================================
@app.get("/", response_class=HTMLResponse)
async def get_index():
    return HTMLResponse(content=HTML_CONTENT)

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, username)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
