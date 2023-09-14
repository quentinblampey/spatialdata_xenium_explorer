# spatialdata_xenium_explorer
Converting any SpatialData object into files that can be open by the Xenium Explorer

## Installation

This repository is currently in development. You can still test it out, but you may exeprience issues.

`pip install git+https://github.com/quentinblampey/spatialdata_xenium_explorer.git`

## Usage

```python
import spatialdata_xenium_explorer

spatialdata_xenium_explorer.write("/path/to/directory", sdata, image_key)
```