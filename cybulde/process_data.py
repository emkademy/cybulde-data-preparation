from cybulde.config_schemas.data_processing_config_schema import DataProcessingConfig
from cybulde.utils.config_utils import get_config
from cybulde.utils.data_utils import get_raw_data_with_version
from cybulde.utils.gcp_utils import access_secret_version

from hydra.utils import instantiate


@get_config(config_path="../configs", config_name="data_processing_config")
def process_data(config: DataProcessingConfig) -> None:
    github_access_token = access_secret_version(config.infrastructure.project_id, config.github_access_token_secret_id)

    get_raw_data_with_version(
        version=config.version,
        data_local_save_dir=config.data_local_save_dir,
        dvc_remote_repo=config.dvc_remote_repo,
        dvc_data_folder=config.dvc_data_folder,
        github_user_name=config.github_user_name,
        github_access_token=github_access_token,
    )

    dataset_reader_manager = instantiate(config.dataset_reader_manager)

    df = dataset_reader_manager.read_data()

    print(df.head())
    print(df["dataset_name"].unique().compute())


if __name__ == "__main__":
    process_data()  # type: ignore
