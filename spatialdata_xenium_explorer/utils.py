from __future__ import annotations

import logging
from pathlib import Path

import dask.array as da
import dask.dataframe as dd
import dask_image.ndinterp
import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
from anndata import AnnData
from multiscale_spatial_image import MultiscaleSpatialImage
from shapely.geometry import MultiPolygon, Point, Polygon
from spatial_image import SpatialImage
from spatialdata import SpatialData
from spatialdata.models import SpatialElement
from spatialdata.transformations import Identity, get_transformation, set_transformation

from ._constants import ShapesConstants

log = logging.getLogger(__name__)


def explorer_file_path(path: str, filename: str, is_dir: bool):
    path: Path = Path(path)

    if is_dir:
        path = path / filename

    return path


def int_cell_id(explorer_cell_id: str) -> int:
    """Transforms an alphabetical cell id from the Xenium Explorer to an integer ID

    E.g., int_cell_id('aaaachba-1') = 10000"""
    code = explorer_cell_id[:-2] if explorer_cell_id[-2] == "-" else explorer_cell_id
    coefs = [ord(c) - 97 for c in code][::-1]
    return sum(value * 16**i for i, value in enumerate(coefs))


def str_cell_id(cell_id: int) -> str:
    """Transforms an integer cell ID into an Xenium Explorer alphabetical cell id

    E.g., str_cell_id(10000) = 'aaaachba-1'"""
    coefs = []
    for _ in range(8):
        cell_id, coef = divmod(cell_id, 16)
        coefs.append(coef)
    return "".join([chr(97 + coef) for coef in coefs][::-1]) + "-1"


def get_intrinsic_cs(
    sdata: SpatialData, element: SpatialElement | str, name: str | None = None
) -> str:
    """Gets the name of the intrinsic coordinate system of an element

    Args:
        sdata: A SpatialData object
        element: `SpatialElement`, or its key
        name: Name to provide to the intrinsic coordinate system if not existing. By default, uses the element id.

    Returns:
        Name of the intrinsic coordinate system
    """
    if name is None:
        name = f"_{element if isinstance(element, str) else id(element)}_intrinsic"

    if isinstance(element, str):
        element = sdata[element]

    for cs, transform in get_transformation(element, get_all=True).items():
        if isinstance(transform, Identity):
            return cs

    set_transformation(element, Identity(), name)
    return name


def to_intrinsic(
    sdata: SpatialData, element: SpatialElement | str, element_cs: SpatialElement | str
):
    """Transforms a `SpatialElement` into the intrinsic coordinate system of another `SpatialElement`

    Args:
        sdata: A SpatialData object
        element: `SpatialElement` to transform, or its key
        element_cs: `SpatialElement` of the target coordinate system, or its key

    Returns:
        The `SpatialElement` after transformation in the target coordinate system
    """
    if isinstance(element, str):
        element = sdata[element]
    cs = get_intrinsic_cs(sdata, element_cs)
    return sdata.transform_element_to_coordinate_system(element, cs)


def get_key(sdata: SpatialData, attr: str, key: str | None = None):
    if key is not None:
        return key

    elements = getattr(sdata, attr)

    if len(elements) != 1:
        log.warn(
            f"Trying to get an element key of `sdata.{attr}`, but it contains multiple values and no key was provided. It will not be saved to the xenium explorer."
        )
        return None

    return next(iter(elements.keys()))


def get_element(sdata: SpatialData, attr: str, key: str | None = None, return_key: bool = False):
    key = get_key(sdata, attr, key)
    value = sdata[key] if key is not None else None
    return (key, value) if return_key else value


def get_spatial_image(
    sdata: SpatialData, key: str | None = None, return_key: bool = False
) -> SpatialImage | tuple[str, SpatialImage]:
    """Gets a SpatialImage from a SpatialData object (if the image has multiple scale, the `scale0` is returned)

    Args:
        sdata: SpatialData object.
        key: Optional image key. If `None`, returns the only image (if only one), or raises an error.
        return_key: Whether to also return the key of the image.

    Returns:
        If `return_key` is False, only the image is returned, else a tuple `(image_key, image)`
    """
    assert not (
        key is None and len(sdata.images) > 1
    ), "When the SpatialData contains more than one image, please provide 'image_key'"

    key = get_key(sdata, "images", key)

    assert key is not None, "At least one image in `sdata.images` is required"

    image = sdata.images[key]
    if isinstance(image, MultiscaleSpatialImage):
        image = SpatialImage(next(iter(image["scale0"].values())))

    if return_key:
        return key, image
    return image


def resize(xarr: xr.DataArray, scale_factor: float) -> da.Array:
    """Resize a xarray image

    Args:
        xarr: A `xarray` array
        scale_factor: Scale factor of resizing, e.g. `2` will decrease the width by 2

    Returns:
        Resized dask array
    """
    resize_dims = [dim in ["x", "y"] for dim in xarr.dims]
    transform = np.diag([scale_factor if resize_dim else 1 for resize_dim in resize_dims])
    output_shape = [
        size // scale_factor if resize_dim else size
        for size, resize_dim in zip(xarr.shape, resize_dims)
    ]

    return dask_image.ndinterp.affine_transform(
        xarr.data, matrix=transform, output_shape=output_shape
    )


def resize_numpy(
    arr: np.ndarray, scale_factor: float, dims: list[str], output_shape: list[int]
) -> np.ndarray:
    """Resize a numpy image

    Args:
        arr: a `numpy` array
        scale_factor: Scale factor of resizing, e.g. `2` will decrease the width by 2
        dims: List of dimension names. Only `"x"` and `"y"` are resized.
        output_shape: Size of the output array

    Returns:
        Resized array
    """
    resize_dims = [dim in ["x", "y"] for dim in dims]
    transform = np.diag([scale_factor if resize_dim else 1 for resize_dim in resize_dims])

    return dask_image.ndinterp.affine_transform(
        arr, matrix=transform, output_shape=output_shape
    ).compute()


def _check_integer_dtype(dtype: np.dtype):
    assert np.issubdtype(
        dtype, np.integer
    ), f"Expecting image to have an intenger dtype, but found {dtype}"


def scale_dtype(arr: np.ndarray, dtype: np.dtype) -> np.ndarray:
    """Change the dtype of an array but keep the scale compared to the type maximum value.

    !!! note "Example"
        For an array of dtype `uint8` being transformed to `np.uint16`, the value `255` will become `65535`

    Args:
        arr: A `numpy` array
        dtype: Target `numpy` data type

    Returns:
        A scaled `numpy` array with the dtype provided.
    """
    _check_integer_dtype(arr.dtype)
    _check_integer_dtype(dtype)

    if arr.dtype == dtype:
        return arr

    factor = np.iinfo(dtype).max / np.iinfo(arr.dtype).max
    return (arr * factor).astype(dtype)


def _standardize_shapes(geo_df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if geo_df.geometry.map(lambda geom: isinstance(geom, Polygon)).all():
        return geo_df

    if geo_df.geometry.map(lambda geom: isinstance(geom, Point)).all():
        if not ShapesConstants.RADIUS in geo_df:
            log.warn(
                f"GeoDataFrame contains only Point objects, but no column '{ShapesConstants.RADIUS}' was found. Using default {ShapesConstants.RADIUS}={ShapesConstants.DEFAULT_POINT_RADIUS}"
            )
            geo_df[ShapesConstants.RADIUS] = ShapesConstants.DEFAULT_POINT_RADIUS

        geo_df.geometry = geo_df.apply(lambda row: row.geometry.buffer(row.radius), axis=1)
        return geo_df

    if geo_df.geometry.map(lambda geom: isinstance(geom, MultiPolygon)).all():
        log.warn(
            "GeoDataFrame contains only MultiPolygon objects. For each MultiPolygon, only the Polygon with the largest area will be shown"
        )

        geo_df.geometry = geo_df.geometry.map(
            lambda multi_polygon: max(multi_polygon.geoms, key=lambda geom: geom.area)
        )
        return geo_df

    raise ValueError(
        "The provided shapes contain unsupported types, or contain a mix of multiple types. Supported types: Polygon, Point, MultiPolygon."
    )


def _spot_transcripts_origin(adata: AnnData) -> tuple[dd.DataFrame, str]:
    gene_column = "gene"
    df = pd.DataFrame(
        {"x": [0] * adata.n_vars, "y": [0] * adata.n_vars, gene_column: adata.var_names}
    )
    df = dd.from_pandas(df, chunksize=10_000)
    return df, gene_column
