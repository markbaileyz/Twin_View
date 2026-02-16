import type { TabId } from '../types';

interface BreadcrumbItem { label: string; type: 'home' | 'datacenter' | 'cluster' | 'host' | 'vm'; }
interface NavigationState { activeTab: TabId; breadcrumbs: BreadcrumbItem[]; sidebarCollapsed: boolean; inspectorOpen: boolean; showConnectionWizard: boolean; }

class NavigationStore {
  private state: NavigationState = { activeTab: 'overview', breadcrumbs: [{ label: 'Home', type: 'home' }], sidebarCollapsed: false, inspectorOpen: false, showConnectionWizard: false };
  private listeners: Set<() => void> = new Set();
  getState(): NavigationState { return this.state; }
  subscribe(listener: () => void): () => void { this.listeners.add(listener); return () => this.listeners.delete(listener); }
  private notify(): void { this.listeners.forEach((l) => l()); }

  setActiveTab(tab: TabId): void { this.state = { ...this.state, activeTab: tab, breadcrumbs: [{ label: 'Home', type: 'home' }], inspectorOpen: false }; this.notify(); }
  toggleSidebar(): void { this.state = { ...this.state, sidebarCollapsed: !this.state.sidebarCollapsed }; this.notify(); }
  setShowConnectionWizard(show: boolean): void { this.state = { ...this.state, showConnectionWizard: show }; this.notify(); }
}

export const navigationStore = new NavigationStore();
