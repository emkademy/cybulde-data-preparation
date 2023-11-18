from fastapi import FastAPI
from hydra.utils import instantiate

from cybulde.utils.config_utils import load_pickle_config

config = load_pickle_config(
    config_path="./cybulde/configs/automatically_generated", config_name="data_processing_config"
)

dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)


app = FastAPI()


@app.get("/process_data")
def process_data(text: str) -> dict[str, str]:
    return {"cleaned_text": dataset_cleaner_manager(text)}
