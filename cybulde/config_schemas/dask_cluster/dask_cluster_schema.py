from dataclasses import field
from typing import Any, Optional

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, SI
from pydantic.dataclasses import dataclass


@dataclass
class WorkerClassConfig:
    pass


@dataclass
class DaskClusterConfig:
    _target_: str = MISSING
    n_workers: int = 1


@dataclass
class LocalDaskClusterConfig(DaskClusterConfig):
    _target_: str = "dask.distributed.LocalCluster"
    memory_limit: str = "auto"
    processes: bool = True
    threads_per_worker: int = 1
    scheduler_port: int = 8786
    silence_logs: int = 30
    host: Optional[str] = None
    dashboard_address: str = ":8787"
    asynchronous: bool = False
    blocked_handlers: Optional[list[str]] = None
    service_kwargs: Optional[dict[str, dict]] = None
    security: Optional[bool] = None
    protocol: Optional[str] = None
    interface: Optional[str] = None
    worker_class: Optional[WorkerClassConfig] = None


@dataclass
class GCPDaskClusterConfig(DaskClusterConfig):
    _target_: str = "dask_cloudprovider.gcp.GCPCluster"
    projectid: str = SI("${infrastructure.project_id}")
    zone: str = SI("${infrastructure.zone}")
    network: str = SI("${infrastructure.network}")
    network_projectid: Optional[str] = SI("${infrastructure.project_id}")
    machine_type: str = "n1-standard-1"
    source_image: str = "projects/ubuntu-os-cloud/global/images/ubuntu-minimal-2004-focal-v20220203"
    docker_image: Optional[str] = "daskdev/dask:latest"
    docker_args: str = ""
    extra_bootstrap: Optional[list[str]] = field(
        default_factory=lambda: ["gcloud auth configure-docker --quiet europe-west4-docker.pkg.dev"]
    )
    ngpus: Optional[int] = 0
    gpu_type: Optional[str] = None
    filesystem_size: int = 50  # In GBs
    disk_type: str = "pd-standard"
    on_host_maintenance: str = "TERMINATE"

    n_workers: int = 0
    worker_class: str = "dask.distributed.Nanny"
    worker_options: dict[str, Any] = field(default_factory=lambda: {})
    env_vars: dict[str, str] = field(default_factory=lambda: {})
    scheduler_options: dict[str, str] = field(default_factory=lambda: {})
    silence_logs: Optional[bool] = None
    asynchronous: Optional[bool] = None
    security: bool = True
    preemptible: Optional[bool] = False
    debug: Optional[bool] = False
    instance_labels: Optional[dict[str, str]] = None


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="local_dask_cluster_schema", node=LocalDaskClusterConfig, group="dask_cluster")
    cs.store(name="gcp_dask_cluster_schema", node=GCPDaskClusterConfig, group="dask_cluster")
