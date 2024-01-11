# SpatialData to Xenium Explorer

[![PyPI](https://img.shields.io/pypi/v/spatialdata_xenium_explorer.svg)](https://pypi.org/project/spatialdata_xenium_explorer)
[![Downloads](https://static.pepy.tech/badge/spatialdata_xenium_explorer)](https://pepy.tech/project/spatialdata_xenium_explorer)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://quentinblampey.github.io/spatialdata_xenium_explorer/)
![Build](https://github.com/quentinblampey/spatialdata_xenium_explorer/workflows/ci/badge.svg)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![License](https://img.shields.io/pypi/l/spatialdata_xenium_explorer.svg)](https://github.com/quentinblampey/spatialdata_xenium_explorer/blob/master/LICENSE)
[![Imports: isort](https://img.shields.io/badge/imports-isort-blueviolet)](https://pycqa.github.io/isort/)

Converting any [`SpatialData`](https://github.com/scverse/spatialdata) object into files that can be open by the [Xenium Explorer](https://www.10xgenomics.com/support/software/xenium-explorer).

> *Xenium Explorer* is a registered trademark of 10x Genomics

You may also be interested in a pipeline for spatial-omics that uses this conversion to Xenium Explorer: see [Sopa](https://github.com/gustaveroussy/sopa).

## Installation

Requirement: `python>=3.9`

```sh
pip install spatialdata_xenium_explorer
```

## Features

- Conversion of the following data: images, cell boundaries (polygons), transcripts, cell-by-gene table, and cell categories (or observations).
- Image alignment can be made on the Xenium Explorer, and then the `SpatialData` object can be updated
- When working on the `SpatialData` or `AnnData` object, new cell categories can be easily and quickly added to the Explorer
- When selecting cells with the "lasso tool" on the Explorer, it's easy to select back these cells on the `SpatialData` or `AnnData` object

## Usage

You can use our CLI or API, see examples below. It will create up to 6 files, among which a file called `experiment.xenium`. Double-click on this file to open it on the [Xenium Explorer](https://www.10xgenomics.com/support/software/xenium-explorer/downloads) (make sure you have the latest version of the software).

### CLI

```sh
spatialdata_xenium_explorer write /path/to/sdata.zarr
```

Check [our documentation](https://quentinblampey.github.io/spatialdata_xenium_explorer/cli) for more details.

### API

```python
import spatialdata
import spatialdata_xenium_explorer

sdata = spatialdata.read_zarr("...")

spatialdata_xenium_explorer.write("/path/to/directory", sdata, image_key, shapes_key, points_key, gene_column)
```

Check [our documentation](https://quentinblampey.github.io/spatialdata_xenium_explorer/api) for more details.

## Contributing

This package is still in early development. Contributions are welcome (new issues, pull requests, ...).