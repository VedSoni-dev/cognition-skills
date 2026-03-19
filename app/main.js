const { app, BrowserWindow, screen, ipcMain, Tray, Menu, nativeImage } = require('electron');
const { WebSocketServer } = require('ws');
const path = require('path');

let win = null;
let wss = null;
let isBubble = false; // start expanded so you can see it

const WS_PORT = 3210;
const BUBBLE_SIZE = 80;
const PANEL_W = 500;
const PANEL_H = 760;

function getPosition(w, h) {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;
  return { x: width - w - 20, y: height - h - 20 };
}

function createWindow() {
  const pos = getPosition(PANEL_W, PANEL_H);
  win = new BrowserWindow({
    width: PANEL_W,
    height: PANEL_H,
    x: pos.x,
    y: pos.y,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: true,
    skipTaskbar: false,
    hasShadow: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  });
  win.loadFile('index.html');
  win.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true });
}

function expandWindow() {
  if (!isBubble) return;
  isBubble = false;
  const pos = getPosition(PANEL_W, PANEL_H);
  win.setResizable(true);
  win.setSkipTaskbar(false);
  win.setBounds({ x: pos.x, y: pos.y, width: PANEL_W, height: PANEL_H }, true);
  win.webContents.send('cognition-message', { type: 'window-mode', mode: 'expanded' });
}

function collapseWindow() {
  if (isBubble) return;
  isBubble = true;
  const pos = getPosition(BUBBLE_SIZE, BUBBLE_SIZE);
  win.setBounds({ x: pos.x, y: pos.y, width: BUBBLE_SIZE, height: BUBBLE_SIZE }, true);
  win.setResizable(false);
  win.setSkipTaskbar(true);
  win.webContents.send('cognition-message', { type: 'window-mode', mode: 'bubble' });
}

function startWebSocket() {
  wss = new WebSocketServer({ port: WS_PORT });
  console.log(`Cognition WS on ws://localhost:${WS_PORT}`);

  wss.on('connection', (ws) => {
    console.log('Claude Code connected');
    ws.send(JSON.stringify({ type: 'connected', status: 'ready', mode: isBubble ? 'bubble' : 'expanded' }));

    ws.on('message', (raw) => {
      try {
        const msg = JSON.parse(raw.toString());

        // If it's a nudge or quiz, auto-expand
        if (msg.type === 'nudge' || msg.type === 'quiz' || msg.type === 'notification') {
          if (isBubble && msg.type !== 'nudge') expandWindow();
        }

        if (win && !win.isDestroyed()) {
          win.webContents.send('cognition-message', msg);
        }
      } catch (e) {
        console.error('Bad WS message:', e);
      }
    });
  });
}

// IPC from renderer
ipcMain.on('expand', () => expandWindow());
ipcMain.on('collapse', () => collapseWindow());
ipcMain.on('toggle', () => isBubble ? expandWindow() : collapseWindow());

ipcMain.on('send-to-claude', (_, data) => {
  if (!wss) return;
  const payload = JSON.stringify(data);
  wss.clients.forEach((c) => { if (c.readyState === 1) c.send(payload); });
});

ipcMain.on('quit', () => { app.quit(); });

app.whenReady().then(() => {
  startWebSocket();
  createWindow();
});

app.on('window-all-closed', () => app.quit());
app.on('before-quit', () => { if (wss) wss.close(); });
