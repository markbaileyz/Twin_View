import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  platform: process.platform,
  credentials: {
    save: (key: string, plaintext: string) => ipcRenderer.invoke('credentials:save', key, plaintext),
    load: (key: string) => ipcRenderer.invoke('credentials:load', key),
    delete: (key: string) => ipcRenderer.invoke('credentials:delete', key),
    list: () => ipcRenderer.invoke('credentials:list'),
  },
});
