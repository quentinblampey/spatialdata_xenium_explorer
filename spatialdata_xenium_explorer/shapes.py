from math import ceil
from pathlib import Path

import numpy as np
import zarr
from shapely.geometry import Polygon

from .constants import cell_summary_attrs, group_attrs
from .utils import pad


def write_polygons(path: Path, polygons: list[Polygon], area: np.ndarray) -> None:
    coordinates = np.stack([pad(p, 3, 13) for p in polygons])
    coordinates /= 4.705882

    num_cells = len(coordinates)
    cells_fourth = ceil(num_cells / 4)
    cells_half = ceil(num_cells / 2)

    CELLS_SUMMARY_ATTRS = cell_summary_attrs()
    GROUP_ATTRS = group_attrs()

    GROUP_ATTRS["number_cells"] = num_cells

    polygon_vertices = np.stack([coordinates, coordinates])
    num_points = polygon_vertices.shape[2]
    n_vertices = num_points // 2

    with zarr.ZipStore(path, mode="w") as store:
        g = zarr.group(store=store)
        g.attrs.put(GROUP_ATTRS)

        g.array(
            "polygon_vertices",
            polygon_vertices,
            dtype="float32",
            chunks=(1, cells_fourth, ceil(num_points / 4)),
        )

        cell_id = np.ones((num_cells, 2))
        cell_id[:, 0] = np.arange(1, num_cells + 1)
        g.array("cell_id", cell_id, dtype="uint32", chunks=(cells_half, 1))

        cell_summary = np.zeros((num_cells, 7))
        cell_summary[:, 2] = area
        g.array(
            "cell_summary",
            cell_summary,
            dtype="float64",
            chunks=(num_cells, 1),
        )
        g["cell_summary"].attrs.put(CELLS_SUMMARY_ATTRS)

        g.array(
            "polygon_num_vertices",
            np.full((2, num_cells), n_vertices),
            dtype="int32",
            chunks=(1, cells_half),
        )

        g.array(
            "seg_mask_value",
            np.arange(1, num_cells + 1),
            dtype="uint32",
            chunks=(cells_half,),
        )
