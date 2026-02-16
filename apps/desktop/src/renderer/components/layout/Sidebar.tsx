import { navigationStore } from '../../store/navigationStore';
import { theme } from '../../theme';

export function Sidebar({ collapsed }: { collapsed: boolean }) {
  return <aside style={{ width: collapsed ? theme.layout.sidebarCollapsed : theme.layout.sidebarWidth, background: theme.bg.sidebar, borderRight: `1px solid ${theme.border.subtle}`, padding: theme.spacing.md }}>
    <button onClick={() => navigationStore.toggleSidebar()}>☰</button>
    {!collapsed && <div style={{ color: theme.text.primary, marginTop: theme.spacing.md }}>Navigation / Inventory</div>}
  </aside>;
}
