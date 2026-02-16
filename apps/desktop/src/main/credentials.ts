import fs from 'node:fs';
import path from 'node:path';
import { app, safeStorage } from 'electron';

function storePath(): string {
  return path.join(app.getPath('userData'), 'credentials.enc.json');
}
function readStore(): Record<string, string> {
  try { return JSON.parse(fs.readFileSync(storePath(), 'utf8')); } catch { return {}; }
}
function writeStore(store: Record<string, string>): void {
  fs.writeFileSync(storePath(), JSON.stringify(store, null, 2), 'utf8');
}
export function saveCredential(key: string, plaintext: string): boolean {
  if (!safeStorage.isEncryptionAvailable()) return false;
  const store = readStore();
  store[key] = safeStorage.encryptString(plaintext).toString('base64');
  writeStore(store);
  return true;
}
export function loadCredential(key: string): string | null {
  const encoded = readStore()[key];
  if (!encoded || !safeStorage.isEncryptionAvailable()) return null;
  return safeStorage.decryptString(Buffer.from(encoded, 'base64'));
}
export function deleteCredential(key: string): void {
  const store = readStore();
  delete store[key];
  writeStore(store);
}
export function listCredentialKeys(): string[] {
  return Object.keys(readStore());
}
