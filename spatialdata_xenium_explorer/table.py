import anndata
import numpy as np
import zarr

from .constants import cell_categories_attrs


def write_gene_counts(path, adata: anndata.AnnData):
    counts = adata.layers["counts"]

    feature_keys = list(adata.var_names) + ["Total transcripts"]
    feature_ids = feature_keys
    feature_types = ["gene"] * len(adata.var_names) + ["aggregate_gene"]

    ATTRS = {
        "major_version": 3,
        "minor_version": 0,
        "number_cells": adata.n_obs,
        "number_features": adata.n_vars + 1,
        "feature_keys": feature_keys,
        "feature_ids": feature_ids,
        "feature_types": feature_types,
    }

    data, indices, indptr = [], [], [0]

    for i in range(adata.n_vars):
        nonzero_counts = counts[:, i].data
        data.append(nonzero_counts)
        indices.append(counts[:, i].nonzero()[0])
        indptr.append(indptr[-1] + len(nonzero_counts))

    total_counts = counts.sum(1).A1
    loc = total_counts > 0
    data.append(total_counts[loc])
    indices.append(np.where(loc)[0])
    indptr.append(indptr[-1] + loc.sum())

    data = np.concatenate(data)
    indices = np.concatenate(indices)
    indptr = np.array(indptr)

    cell_id = np.ones((adata.n_obs, 2))
    cell_id[:, 0] = np.arange(1, adata.n_obs + 1)

    with zarr.ZipStore(path, mode="w") as store:
        g = zarr.group(store=store)
        cells_group = g.create_group("cell_features")
        cells_group.attrs.put(ATTRS)

        cells_group.array("cell_id", cell_id, dtype="uint32", chunks=cell_id.shape)
        cells_group.array("data", data, dtype="uint32", chunks=data.shape)
        cells_group.array("indices", indices, dtype="uint32", chunks=indices.shape)
        cells_group.array("indptr", indptr, dtype="uint32", chunks=indptr.shape)


def add_group(root: zarr.Group, index: int, values: np.ndarray, categories: list[str]):
    group = root.create_group(index)
    values_indices = [np.where(values == cat)[0] for cat in categories]
    values_cum_len = np.cumsum([len(indices) for indices in values_indices])

    indices = np.concatenate(values_indices)
    indptr = np.concatenate([[0], values_cum_len[:-1]])

    group.array("indices", indices, dtype="uint32", chunks=(len(indices),))
    group.array("indptr", indptr, dtype="uint32", chunks=(len(indptr),))


def write_cell_categories(path: str, adata: anndata.AnnData):
    categorical_columns = [
        name for name, cat in adata.obs.dtypes.items() if cat == "category"
    ]

    ATTRS = cell_categories_attrs()
    ATTRS["number_groupings"] = len(categorical_columns)

    with zarr.ZipStore(path, mode="w") as store:
        g = zarr.group(store=store)
        cell_groups = g.create_group("cell_groups")

        for i, name in enumerate(categorical_columns):
            categories = list(adata.obs[name].cat.categories)
            ATTRS["grouping_names"].append(name)
            ATTRS["group_names"].append(categories)

            add_group(cell_groups, i, adata.obs[name], categories)

        cell_groups.attrs.put(ATTRS)
