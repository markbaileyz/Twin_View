import { useNavigation } from '../../hooks/useNavigation';
import { theme } from '../../theme';
import { ExportToolbar } from '../export/ExportToolbar';
import { AlertsPage } from '../pages/AlertsPage';
import { CompliancePage } from '../pages/CompliancePage';
import { InventoryPage } from '../pages/InventoryPage';
import { OverviewPage } from '../pages/OverviewPage';
import { ReportsPage } from '../pages/ReportsPage';
import { RvtoolsPage } from '../pages/RvtoolsPage';
import { TopTabBar } from './TopTabBar';

export function MainCanvas() {
  const nav = useNavigation();
  const page = nav.activeTab === 'overview' ? <OverviewPage /> : nav.activeTab === 'inventory' ? <InventoryPage /> : nav.activeTab === 'rvtools' ? <RvtoolsPage /> : nav.activeTab === 'compliance' ? <CompliancePage /> : nav.activeTab === 'alerts' ? <AlertsPage /> : <ReportsPage />;
  return <main style={{ flex: 1, background: theme.bg.canvas, display: 'flex', flexDirection: 'column' }}>
    <TopTabBar active={nav.activeTab} />
    <div style={{ padding: theme.spacing.sm, color: theme.text.secondary }}>Home</div>
    <div style={{ flex: 1, overflow: 'auto', padding: theme.spacing.md }}>{page}</div>
    <ExportToolbar />
  </main>;
}
