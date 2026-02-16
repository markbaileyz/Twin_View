import { useTelemetry } from '../../hooks/useWebSocket';

export function OverviewPage() {
  const telemetry = useTelemetry();
  return <div><h2>Overview</h2><p>Events: {telemetry.events.length} | Clusters: {telemetry.clusters.length}</p></div>;
}
