import { useNavigation } from '../../hooks/useNavigation';
import { InspectorPanel } from './InspectorPanel';
import { MainCanvas } from './MainCanvas';
import { Sidebar } from './Sidebar';

export function AppShell() {
  const nav = useNavigation();
  return <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
    <Sidebar collapsed={nav.sidebarCollapsed} />
    <MainCanvas />
    <InspectorPanel />
  </div>;
}
