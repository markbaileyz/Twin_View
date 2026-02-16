import { BACKEND_URL } from '@/shared/constants';

export async function getEvents(limit = 200): Promise<any> {
  return fetch(`${BACKEND_URL}/events?limit=${limit}`).then((r) => r.json());
}
export async function getClusters(limit = 50): Promise<any> {
  return fetch(`${BACKEND_URL}/clusters?limit=${limit}`).then((r) => r.json());
}
export async function startDemo(): Promise<any> { return fetch(`${BACKEND_URL}/demo/start`, { method: 'POST' }).then((r) => r.json()); }
export async function stopDemo(): Promise<any> { return fetch(`${BACKEND_URL}/demo/stop`, { method: 'POST' }).then((r) => r.json()); }
