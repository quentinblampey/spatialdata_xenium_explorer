# CLI (command-line-interface)

## Usage

When installing `spatialdata_xenium_explorer` are written in our [getting-started guidelines](../getting_started), a new command named `spatialdata_xenium_explorer` becomes available.

!!! note "CLI helper"
    Run `spatialdata_xenium_explorer --help` to get details about all the command line purpose. You can also use this helper on any subcommand, for instance `spatialdata_xenium_explorer write --help`.

<div class="termy">
```console
// Run the spatialdata_xenium_explorer CLI helper
$ spatialdata_xenium_explorer --help
 Usage: spatialdata_xenium_explorer [OPTIONS] COMMAND [ARGS]...    
╭─ Commands ──────────────────────────────────────────────────╮
│ write        Convertion: spatialdata to the Xenium Explorer │
│ add-aligned  Add image after alignment on the explorer      │
│ update-obs   Update the cell categories for the explorer    │ 
╰─────────────────────────────────────────────────────────────╯
// Example
$ spatialdata_xenium_explorer write /path/to/sdata.zarr
... [Logs] ...
```
</div>

## Commands

**Usage**:

```console
$ spatialdata_xenium_explorer [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add-aligned`: After alignment on the Xenium Explorer,...
* `update-obs`: Update the cell categories for the Xenium...
* `write`: Convert a spatialdata object to Xenium...

### `write`

Convert a spatialdata object to Xenium Explorer's inputs

**Usage**:

```console
$ spatialdata_xenium_explorer write [OPTIONS] SDATA_PATH
```

**Arguments**:

* `SDATA_PATH`: Path to the SpatialData `.zarr` directory  [required]

**Options**:

* `--output-path TEXT`: Path to a directory where Xenium Explorer's outputs will be saved. By default, writes to the same path as `sdata_path` but with the `.explorer` suffix
* `--image-key TEXT`: Name of the image of interest (key of `sdata.images`). This argument doesn't need to be provided if there is only one image.
* `--shapes-key TEXT`: Name of the cell shapes (key of `sdata.shapes`). This argument doesn't need to be provided if there is only one shapes key or a table with only one region.
* `--points-key TEXT`: Name of the transcripts (key of `sdata.points`). This argument doesn't need to be provided if there is only one points key.
* `--gene-column TEXT`: Column name of the points dataframe containing the gene names
* `--layer TEXT`: Layer of `sdata.table` where the gene counts are saved. If `None`, uses `sdata.table.X`.
* `--lazy / --no-lazy`: If `True`, will not load the full images in memory (except if the image memory is below `ram_threshold_gb`)  [default: lazy]
* `--ram-threshold-gb INTEGER`: Threshold (in gygabytes) from which image can be loaded in memory. If `None`, the image is never loaded in memory  [default: 4]
* `--mode TEXT`: string that indicated which files should be created. `'-ib'` means everything except images and boundaries, while `'+tocm'` means only transcripts/observations/counts/metadata (each letter corresponds to one explorer file). By default, keeps everything
* `--help`: Show this message and exit.

### `add-aligned`

After alignment on the Xenium Explorer, add an image to the SpatialData object

**Usage**:

```console
$ spatialdata_xenium_explorer add-aligned [OPTIONS] SDATA_PATH IMAGE_PATH TRANSFORMATION_MATRIX_PATH
```

**Arguments**:

* `SDATA_PATH`: Path to the SpatialData `.zarr` directory  [required]
* `IMAGE_PATH`: Path to the image file to be added (`.ome.tif` used in the explorer during alignment)  [required]
* `TRANSFORMATION_MATRIX_PATH`: Path to the `matrix.csv` file returned by the Explorer after alignment  [required]

**Options**:

* `--original-image-key TEXT`: Optional original-image key on which the new image will be aligned. This doesn't need to be provided if there is only one image
* `--overwrite / --no-overwrite`: Whether to overwrite the image if existing  [default: no-overwrite]
* `--help`: Show this message and exit.

### `update-obs`

Update the cell categories for the Xenium Explorer's (i.e. what's in `adata.obs`). This is useful when you perform analysis and update your `AnnData` object

!!! note "Usage"
    This command should only be used if you updated `adata.obs`, after creation of the other explorer files.

**Usage**:

```console
$ spatialdata_xenium_explorer update-obs [OPTIONS] ADATA_PATH OUTPUT_PATH
```

**Arguments**:

* `ADATA_PATH`: Path to the anndata file (`zarr` or `h5ad`) containing the new observations  [required]
* `OUTPUT_PATH`: Path to the Xenium Explorer directory (it will update `analysis.zarr.zip`)  [required]

**Options**:

* `--help`: Show this message and exit.
