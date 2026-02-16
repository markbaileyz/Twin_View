import { navigationStore } from '../../store/navigationStore';
import { theme } from '../../theme';
import type { TabId } from '../../types';

const tabs: TabId[] = ['overview', 'inventory', 'rvtools', 'compliance', 'alerts', 'reports'];

export function TopTabBar({ active }: { active: TabId }) {
  return <div style={{ display: 'flex', gap: theme.spacing.sm, padding: theme.spacing.sm, borderBottom: `1px solid ${theme.border.subtle}` }}>{tabs.map((tab) => <button key={tab} onClick={() => navigationStore.setActiveTab(tab)} style={{ background: 'transparent', color: active === tab ? theme.accent.primary : theme.text.secondary, border: 'none', textTransform: 'capitalize' }}>{tab}</button>)}</div>;
}
