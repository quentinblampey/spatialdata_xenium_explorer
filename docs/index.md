# SpatialData to Xenium Explorer

Converting any [`SpatialData`](https://github.com/scverse/spatialdata) object into files that can be open by the [Xenium Explorer](https://www.10xgenomics.com/support/software/xenium-explorer).

> *Xenium Explorer* is a registered trademark of 10x Genomics

You may also be interested in a pipeline for spatial-omics that uses this conversion to Xenium Explorer: see [Sopa](https://github.com/gustaveroussy/sopa).

## Features
- Conversion of the following data: images, cell boundaries (polygons), transcripts, cell-by-gene table, and cell categories (or observations).
- Image alignment can be made on the Xenium Explorer, and then the `SpatialData` object can be updated
- When working on the `SpatialData` or `AnnData` object, new cell categories can be easily and quickly added to the Explorer
- When selecting cells with the "lasso tool" on the Explorer, it's easy to select back these cells on the `SpatialData` or `AnnData` object
