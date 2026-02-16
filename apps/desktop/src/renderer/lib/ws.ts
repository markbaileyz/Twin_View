import { BACKEND_WS_URL } from '@/shared/constants';

type Handler = (msg: any) => void;

class TelemetrySocket {
  private ws: WebSocket | null = null;
  private handlers = new Set<Handler>();
  private reconnectDelay = 1000;

  connect(): void {
    if (this.ws && this.ws.readyState <= 1) return;
    this.ws = new WebSocket(`${BACKEND_WS_URL}/ws/telemetry`);
    this.ws.onmessage = (event) => {
      const parsed = JSON.parse(event.data);
      this.handlers.forEach((h) => h(parsed));
    };
    this.ws.onclose = () => {
      setTimeout(() => this.connect(), this.reconnectDelay);
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, 30000);
    };
    this.ws.onopen = () => { this.reconnectDelay = 1000; };
  }

  onMessage(handler: Handler): () => void {
    this.handlers.add(handler);
    return () => this.handlers.delete(handler);
  }
}

export const telemetrySocket = new TelemetrySocket();
