import { getClusters, getEvents } from '../lib/api';
import { telemetrySocket } from '../lib/ws';
import type { ClusterData, SummaryData, UnifiedEvent } from '../types';

interface TelemetryState {
  events: UnifiedEvent[];
  clusters: ClusterData[];
  summary: SummaryData | null;
  connected: boolean;
}

class TelemetryStore {
  private state: TelemetryState = { events: [], clusters: [], summary: null, connected: false };
  private listeners: Set<() => void> = new Set();

  constructor() {
    telemetrySocket.onMessage((msg) => {
      if (msg.type === 'event') this.state = { ...this.state, events: [msg.data, ...this.state.events].slice(0, 200) };
      if (msg.type === 'cluster_update') {
        const rest = this.state.clusters.filter((c) => c.id !== msg.data.id);
        this.state = { ...this.state, clusters: [msg.data, ...rest].slice(0, 50) };
      }
      if (msg.type === 'summary') this.state = { ...this.state, summary: msg.data };
      this.notify();
    });
  }

  getState(): TelemetryState { return this.state; }
  subscribe(listener: () => void): () => void { this.listeners.add(listener); return () => this.listeners.delete(listener); }
  private notify(): void { this.listeners.forEach((l) => l()); }

  async connect(): Promise<void> {
    telemetrySocket.connect();
    const [events, clusters] = await Promise.all([getEvents(200), getClusters(50)]);
    this.state = { ...this.state, events: events.events ?? [], clusters: clusters.clusters ?? [], connected: true };
    this.notify();
  }
}

export const telemetryStore = new TelemetryStore();
