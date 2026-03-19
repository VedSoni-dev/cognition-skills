const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('cognition', {
  onMessage: (cb) => ipcRenderer.on('cognition-message', (_, d) => cb(d)),
  send: (data) => ipcRenderer.send('send-to-claude', data),
  expand: () => ipcRenderer.send('expand'),
  collapse: () => ipcRenderer.send('collapse'),
  toggle: () => ipcRenderer.send('toggle'),
  quit: () => ipcRenderer.send('quit'),
});
