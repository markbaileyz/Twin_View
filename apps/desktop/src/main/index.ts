import path from 'node:path';
import { app, BrowserWindow } from 'electron';
import { registerIpcHandlers } from './ipc';

let mainWindow: BrowserWindow | null = null;

function createWindow(): void {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 600,
    title: 'CCL_TwinView',
    webPreferences: {
      preload: path.join(__dirname, '..', 'preload', 'index.js'),
      contextIsolation: true,
      nodeIntegration: false,
      webviewTag: true,
    },
  });
  const devUrl = process.env.VITE_DEV_SERVER_URL ?? 'http://127.0.0.1:5173';
  mainWindow.loadURL(devUrl).catch(console.error);
}

app.whenReady().then(() => {
  registerIpcHandlers();
  createWindow();
});
