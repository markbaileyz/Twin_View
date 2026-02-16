export const theme = {
  bg: { app: '#0f0f1a', sidebar: '#131325', canvas: '#161628', card: '#1c1c36', cardHover: '#22223d', inspector: '#131325', header: '#111122', input: '#1a1a30', overlay: 'rgba(0,0,0,0.55)' },
  border: { subtle: '#2a2a45', default: '#33335a', active: '#6366f1', focus: '#818cf8' },
  text: { primary: '#e8e8f0', secondary: '#9d9db8', muted: '#6b6b85', inverse: '#0f0f1a', link: '#818cf8' },
  accent: { primary: '#6366f1', primaryHover: '#818cf8', secondary: '#4aa3df', danger: '#ef4444', success: '#22c55e' },
  severity: { info: '#38bdf8', warning: '#fbbf24', error: '#f87171', critical: '#ef4444' },
  spacing: { xs: 4, sm: 8, md: 12, lg: 16, xl: 20, xxl: 24, xxxl: 32 },
  radius: { sm: 4, md: 8, lg: 12, xl: 16, round: '50%' },
  font: { family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', size: { sm: '11px', base: '13px', lg: '14px', heading: '24px' }, weight: { medium: 500, semibold: 600, bold: 700 } },
  layout: { sidebarWidth: 240, sidebarCollapsed: 48, inspectorWidth: 320, headerHeight: 44, tabBarHeight: 36, breadcrumbHeight: 32 },
};

export function severityColor(sev: string): string {
  return theme.severity[sev as keyof typeof theme.severity] ?? theme.text.muted;
}
