export type TabId = 'overview' | 'inventory' | 'rvtools' | 'compliance' | 'alerts' | 'reports';
export interface UnifiedEvent { id: string; source_type: string; source_name: string; timestamp_utc: string; severity: string; category: string; message: string; entity?: string | null; cluster_id?: string | null }
export interface ClusterData { id: string; signature: string; start_ts: string; end_ts: string; severity_max: string; count: number; sample_messages: string[]; involved_sources: string[] }
export interface SummaryData { id: string; generated_at: string; content: string; cluster_ids: string[] }
