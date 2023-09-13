import json

from .constants import EXPERIMENT


def write_experiment(path, run_name, tissue, region_name, uuid):
    EXPERIMENT["run_name"] = run_name
    EXPERIMENT["panel_tissue_type"] = tissue
    EXPERIMENT["region_name"] = region_name
    EXPERIMENT["experiment_uuid"] = uuid

    with open(path, "w") as f:
        json.dump(EXPERIMENT, f, indent=4)


def write(path, sdata):
    ...
