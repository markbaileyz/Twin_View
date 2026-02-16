import { useEffect, useSyncExternalStore } from 'react';
import { telemetryStore } from '../store/telemetryStore';

export function useTelemetry() {
  const state = useSyncExternalStore((cb) => telemetryStore.subscribe(cb), () => telemetryStore.getState());
  useEffect(() => { telemetryStore.connect().catch(console.error); }, []);
  return state;
}
