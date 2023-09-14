# SpatialData to Xenium Explorer
Converting any [`SpatialData`](https://github.com/scverse/spatialdata) object into files that can be open by the [Xenium Explorer](https://www.10xgenomics.com/support/software/xenium-explorer).

## Installation

This package is currently in development. You can test it out, but you may experience some issues.

`pip install git+https://github.com/quentinblampey/spatialdata_xenium_explorer.git`

## Usage

```python
import spatialdata
import spatialdata_xenium_explorer

sdata = spatialdata.read_zarr("...")

spatialdata_xenium_explorer.write("/path/to/directory", sdata, image_key, shapes_key, points_key, gene_column)
```

For more details about the arguments, see the [function docstrings](https://github.com/quentinblampey/spatialdata_xenium_explorer/blob/master/spatialdata_xenium_explorer/converter.py#L29).

This will create up to 6 files, among which a file called `experiment.xenium`. Double-click on this file to open it on the [Xenium Explorer](https://www.10xgenomics.com/support/software/xenium-explorer/downloads) (make sure you have the latest version of the software).

## Future improvements and contributions

Contributions are welcome. Some of the most urgent features to be added:

- Support all types of images (not just `MultiscaleSpatialImage`)
- Better user experience (less arguments)
- Write `.tif` image without loading the spatial image in memory
- Write transcripts without computing the whole coordinates