class InventoryStore {
  private state = { hierarchy: [], importId: null as string | null, expandedNodes: new Set<string>(), searchQuery: '', loading: false, error: null as string | null, totals: { datacenters: 0, clusters: 0, hosts: 0, vms: 0 } };
  private listeners: Set<() => void> = new Set();
  getState() { return this.state; }
  subscribe(listener: () => void): () => void { this.listeners.add(listener); return () => this.listeners.delete(listener); }
  private notify(): void { this.listeners.forEach((l) => l()); }
}

export const inventoryStore = new InventoryStore();
