import { navigationStore } from '../../store/navigationStore';
import { theme } from '../../theme';

export function ConnectionWizard() {
  return <div style={{ position: 'fixed', inset: 0, background: theme.bg.overlay, display: 'grid', placeItems: 'center' }}>
    <div style={{ width: 720, background: theme.bg.card, color: theme.text.primary, padding: theme.spacing.xxl }}>
      <h2>Connect Source</h2>
      <p>Step 1: pick vCenter, SSH, or RVTools.</p>
      <button onClick={() => navigationStore.setShowConnectionWizard(false)}>Close</button>
    </div>
  </div>;
}
