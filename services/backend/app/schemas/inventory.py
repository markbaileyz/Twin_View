from pydantic import BaseModel


class VmNode(BaseModel):
    name: str
    powerstate: str = "unknown"
    os: str = "unknown"
    cpu: int = 0
    memory_mb: int = 0
    entity_type: str = "vm"


class HostNode(BaseModel):
    name: str
    vms: list[VmNode]
    vm_count: int
    entity_type: str = "host"


class ClusterNode(BaseModel):
    name: str
    hosts: list[HostNode]
    host_count: int
    vm_count: int
    entity_type: str = "cluster"


class DatacenterNode(BaseModel):
    name: str
    clusters: list[ClusterNode]
    cluster_count: int
    host_count: int
    vm_count: int
    entity_type: str = "datacenter"


class InventoryHierarchy(BaseModel):
    import_id: str
    datacenters: list[DatacenterNode]
    total_datacenters: int
    total_clusters: int
    total_hosts: int
    total_vms: int
