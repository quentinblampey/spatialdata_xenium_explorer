# SpatialData to Xenium Explorer

Converting any [`SpatialData`](https://github.com/scverse/spatialdata) object into files that can be open by the [Xenium Explorer](https://www.10xgenomics.com/support/software/xenium-explorer).

> *Xenium Explorer* is a registered trademark of 10x Genomics

## Installation

```sh
pip install spatialdata_xenium_explorer
```

## Usage

You can use our [CLI](TODO) or [API](TODO), see examples below. It will create up to 6 files, among which a file called `experiment.xenium`. Double-click on this file to open it on the [Xenium Explorer](https://www.10xgenomics.com/support/software/xenium-explorer/downloads) (make sure you have the latest version of the software).

### CLI

```sh
spatialdata_xenium_explorer write /path/to/sdata.zarr
```

### API

```python
import spatialdata
import spatialdata_xenium_explorer

sdata = spatialdata.read_zarr("...")

spatialdata_xenium_explorer.write("/path/to/directory", sdata, image_key, shapes_key, points_key, gene_column)
```

## Future improvements and contributions

This package is still in early development. Contributions are welcome (new issues, pull requests, ...).