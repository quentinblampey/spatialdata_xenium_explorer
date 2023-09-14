# Spatialdata to Xenium Explorer
Converting any SpatialData object into files that can be open by the Xenium Explorer

## Installation

This repository is currently in development. You can still test it out, but you may exeprience issues.

`pip install git+https://github.com/quentinblampey/spatialdata_xenium_explorer.git`

## Usage

```python
import spatialdata
import spatialdata_xenium_explorer

sdata = spatialdata.read_zarr("...")
image_key = "..." # The name of the MultiscaleSpatialImage to be exported

spatialdata_xenium_explorer.write("/path/to/directory", sdata, image_key)
```

This will create up to 6 files, among which a file called `experiment.xenium`. Double-click on this file to open it on the [Xenium Explorer](https://www.10xgenomics.com/support/software/xenium-explorer/downloads) (make sure you have the latest version of the software).