from __future__ import annotations

import json
import logging
from pathlib import Path

import geopandas as gpd
from spatialdata import SpatialData

from . import (
    utils,
    write_cell_categories,
    write_gene_counts,
    write_image,
    write_polygons,
    write_transcripts,
)
from ._constants import FileNames, experiment_dict

log = logging.getLogger(__name__)


def write(
    path: str,
    sdata: SpatialData,
    image_key: str | None = None,
    shapes_key: str | None = None,
    points_key: str | None = None,
    gene_column: str | None = None,
    pixelsize: float = 0.2125,
    spot: bool = False,
    layer: str | None = None,
    polygon_max_vertices: int = 13,
    lazy: bool = True,
    ram_threshold_gb: int | None = 4,
    mode: str = None,
) -> None:
    """
    Transform a SpatialData object into inputs for the Xenium Explorer.
    After running this function, double-click on the `experiment.xenium` file to open it.

    !!! note "Software download"
        Make sure you have the latest version of the [Xenium Explorer](https://www.10xgenomics.com/support/software/xenium-explorer)

    Note:
        This function will create up to 6 files, depending on the `SpatialData` object and the arguments:

        - `experiment.xenium` contains some experiment metadata. Double-click on this file to open the Xenium Explorer. This file can also be created with [`write_metadata`](./#spatialdata_xenium_explorer.write_metadata).

        - `morphology.ome.tif` is the primary image. This file can also be created with [`write_image`](./#spatialdata_xenium_explorer.write_image). Add more images with `align`.

        - `analysis.zarr.zip` contains the cells categories (or clusters), i.e. `adata.obs`. This file can also be created with [`write_cell_categories`](./#spatialdata_xenium_explorer.write_cell_categories).

        - `cell_feature_matrix.zarr.zip` contains the cell-by-gene counts. This file can also be created with [`write_gene_counts`](./#spatialdata_xenium_explorer.write_gene_counts).

        - `cells.zarr.zip` contains the cells polygon boundaries. This file can also be created with [`write_polygons`](./#spatialdata_xenium_explorer.write_polygons).

        - `transcripts.zarr.zip` contains transcripts locations. This file can also be created with [`write_transcripts`](./#spatialdata_xenium_explorer.write_transcripts).

    Args:
        path: Path to the directory where files will be saved.
        sdata: A `SpatialData` object.
        image_key: Name of the image of interest (key of `sdata.images`). This argument doesn't need to be provided if there is only one image.
        shapes_key: Name of the cell shapes (key of `sdata.shapes`). This argument doesn't need to be provided if there is only one shapes key or a table with only one region.
        points_key: Name of the transcripts (key of `sdata.points`). This argument doesn't need to be provided if there is only one points key.
        gene_column: Column name of the points dataframe containing the gene names.
        pixelsize: Number of microns in a pixel. Invalid value can lead to inconsistent scales in the Explorer.
        spot: Whether the technology is based on spots
        layer: Layer of `sdata.table` where the gene counts are saved. If `None`, uses `sdata.table.X`.
        polygon_max_vertices: Maximum number of vertices for the cell polygons. A higher value will display smoother cells.
        lazy: If `True`, will not load the full images in memory (except if the image memory is below `ram_threshold_gb`).
        ram_threshold_gb: Threshold (in gygabytes) from which image can be loaded in memory. If `None`, the image is never loaded in memory.
        mode: string that indicated which files should be created. "-ib" means everything except images and boundaries, while "+tocm" means only transcripts/observations/counts/metadata (each letter corresponds to one explorer file). By default, keeps everything.
    """
    path: Path = Path(path)
    _check_explorer_directory(path)

    image_key, image = utils.get_spatial_image(sdata, image_key, return_key=True)

    ### Saving cell categories and gene counts
    if sdata.table is not None:
        adata = sdata.table

        region = adata.uns["spatialdata_attrs"]["region"]
        region = region if isinstance(region, list) else [region]

        if len(region) == 1:
            assert (
                shapes_key is None or shapes_key == region[0]
            ), f"Found only one region ({region[0]}), but `shapes_key` was provided with a different value ({shapes_key})"
            shapes_key = region[0]

        if _should_save(mode, "c"):
            write_gene_counts(path, adata, layer=layer)
        if _should_save(mode, "o"):
            write_cell_categories(path, adata)

    ### Saving cell boundaries
    shapes_key, geo_df = utils.get_element(sdata, "shapes", shapes_key, return_key=True)

    if _should_save(mode, "b") and geo_df is not None:
        geo_df = utils.to_intrinsic(sdata, geo_df, image_key)

        if sdata.table is not None:
            geo_df = geo_df.loc[adata.obs[adata.uns["spatialdata_attrs"]["instance_key"]]]

        geo_df = utils._standardize_shapes(geo_df)

        write_polygons(path, geo_df.geometry, polygon_max_vertices, pixelsize=pixelsize)

    ### Saving transcripts
    if spot and sdata.table is not None:
        df, gene_column = utils._spot_transcripts_origin(adata)
    else:
        df = utils.get_element(sdata, "points", points_key)
        df = utils.to_intrinsic(sdata, df, image_key)

    if _should_save(mode, "t") and df is not None:
        if gene_column is not None:
            write_transcripts(path, df, gene_column, pixelsize=pixelsize)
        else:
            log.warn("The argument 'gene_column' has to be provided to save the transcripts")

    ### Saving image
    if _should_save(mode, "i"):
        write_image(path, image, lazy=lazy, ram_threshold_gb=ram_threshold_gb, pixelsize=pixelsize)

    ### Saving experiment.xenium file
    if _should_save(mode, "m"):
        write_metadata(path, image_key, shapes_key, _get_n_obs(sdata, geo_df), pixelsize)

    log.info(f"Saved files in the following directory: {path}")
    log.info(f"You can open the experiment with 'open {path / FileNames.METADATA}'")


def _check_explorer_directory(path: Path):
    assert (
        not path.exists() or path.is_dir()
    ), f"A path to an existing file was provided. It should be a path to a directory."
    path.mkdir(parents=True, exist_ok=True)


def _should_save(mode: str | None, character: str):
    if mode is None:
        return True

    assert len(mode) and mode[0] in [
        "-",
        "+",
    ], f"Mode should be a string that starts with '+' or '-'"

    return character in mode if mode[0] == "+" else character not in mode


def _get_n_obs(sdata: SpatialData, geo_df: gpd.GeoDataFrame) -> int:
    if sdata.table is not None:
        return sdata.table.n_obs
    return len(geo_df) if geo_df is not None else 0


def write_metadata(
    path: str,
    image_key: str = "NA",
    shapes_key: str = "NA",
    n_obs: int = 0,
    is_dir: bool = True,
    pixelsize: float = 0.2125,
):
    """Create an `experiment.xenium` file that can be open by the Xenium Explorer.

    Note:
        This function alone is not enough to actually open an experiment. You will need at least to wrun `write_image`, or create all the outputs with `write_explorer`.

    Args:
        path: Path to the Xenium Explorer directory where the metadata file will be written
        image_key: Key of `SpatialData` object containing the primary image used on the explorer.
        shapes_key: Key of `SpatialData` object containing the boundaries shown on the explorer.
        n_obs: Number of cells
        is_dir: If `False`, then `path` is a path to a single file, not to the Xenium Explorer directory.
        pixelsize: Number of microns in a pixel. Invalid value can lead to inconsistent scales in the Explorer.
    """
    path = utils.explorer_file_path(path, FileNames.METADATA, is_dir)

    with open(path, "w") as f:
        metadata = experiment_dict(image_key, shapes_key, n_obs, pixelsize)
        json.dump(metadata, f, indent=4)
