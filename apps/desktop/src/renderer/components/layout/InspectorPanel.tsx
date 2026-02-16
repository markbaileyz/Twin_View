import { theme } from '../../theme';

export function InspectorPanel() {
  return <aside style={{ width: theme.layout.inspectorWidth, background: theme.bg.inspector, borderLeft: `1px solid ${theme.border.subtle}`, padding: theme.spacing.md, color: theme.text.secondary }}>Inspector</aside>;
}
