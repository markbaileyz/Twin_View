import { ipcMain } from 'electron';
import { deleteCredential, listCredentialKeys, loadCredential, saveCredential } from './credentials';

export function registerIpcHandlers(): void {
  ipcMain.handle('credentials:save', (_, key: string, plaintext: string) => saveCredential(key, plaintext));
  ipcMain.handle('credentials:load', (_, key: string) => loadCredential(key));
  ipcMain.handle('credentials:delete', (_, key: string) => deleteCredential(key));
  ipcMain.handle('credentials:list', () => listCredentialKeys());
}
