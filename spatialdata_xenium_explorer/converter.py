import json
from pathlib import Path

from spatialdata import SpatialData

from . import (
    write_cell_categories,
    write_gene_counts,
    write_multiscale,
    write_polygons,
    write_transcripts,
)
from .constants import FileNames, experiment_dict


def write(path: str, sdata: SpatialData, image_key: str, gene_column: str) -> None:
    path: Path = Path(path)
    assert (
        not path.exists() or path.is_dir()
    ), f"A path to an existing file was provided. It should be a path to a directory."

    path.mkdir(parents=True, exist_ok=True)

    adata = sdata.table

    EXPERIMENT = experiment_dict(..., ..., adata.n_obs)
    with open(path / FileNames.METADATA, "w") as f:
        json.dump(EXPERIMENT, f, indent=4)

    write_gene_counts(path / FileNames.TABLE, adata)
    write_cell_categories(path / FileNames.CELL_CATEGORIES, adata)

    polygons = sdata.shapes["..."]
    # TODO: transform polygon coords to pixel
    write_polygons(path / FileNames.SHAPES, polygons)

    # TODO : make it memory efficient
    write_multiscale(path / FileNames.IMAGE, sdata.images[image_key])

    df = sdata.points["..."]
    write_transcripts(path / FileNames.POINTS, df, gene_column)
