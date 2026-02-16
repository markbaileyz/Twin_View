import { theme } from '../../theme';

export function ExportToolbar() {
  return <div style={{ borderTop: `1px solid ${theme.border.subtle}`, padding: theme.spacing.sm, display: 'flex', gap: theme.spacing.sm }}>
    <select><option>Current View</option><option>All Data</option></select>
    <select><option>Excel (.xlsx)</option><option>CSV</option><option>JSON</option></select>
    <button style={{ background: theme.accent.primary, color: theme.text.primary, border: 'none' }}>⬇ Export</button>
  </div>;
}
