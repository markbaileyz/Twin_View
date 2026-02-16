import { AppShell } from './components/layout/AppShell';
import { ConnectionWizard } from './components/connections/ConnectionWizard';
import { useNavigation } from './hooks/useNavigation';
import { navigationStore } from './store/navigationStore';
import { theme } from './theme';

export default function App() {
  const nav = useNavigation();
  return <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', background: theme.bg.app, color: theme.text.primary, fontFamily: theme.font.family }}>
    <header style={{ height: theme.layout.headerHeight, borderBottom: `1px solid ${theme.border.subtle}`, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: `0 ${theme.spacing.md}px`, background: theme.bg.header }}>
      <strong style={{ color: theme.accent.primary }}>CCL_TwinView</strong>
      <div style={{ display: 'flex', gap: theme.spacing.sm }}>
        <button>Demo</button>
        <button onClick={() => navigationStore.setShowConnectionWizard(true)}>Connect</button>
      </div>
    </header>
    <AppShell />
    {nav.showConnectionWizard && <ConnectionWizard />}
  </div>;
}
