import { useSyncExternalStore } from 'react';
import { navigationStore } from '../store/navigationStore';

export function useNavigation() {
  return useSyncExternalStore((cb) => navigationStore.subscribe(cb), () => navigationStore.getState());
}
