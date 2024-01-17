import typer

app = typer.Typer()

SDATA_HELPER = "Path to the SpatialData `.zarr` directory"


@app.command()
def write(
    sdata_path: str = typer.Argument(help=SDATA_HELPER),
    output_path: str = typer.Option(
        None,
        help="Path to a directory where Xenium Explorer's outputs will be saved. By default, writes to the same path as `sdata_path` but with the `.explorer` suffix",
    ),
    image_key: str = typer.Option(
        None,
        help="Name of the image of interest (key of `sdata.images`). This argument doesn't need to be provided if there is only one image.",
    ),
    shapes_key: str = typer.Option(
        None,
        help="Name of the cell shapes (key of `sdata.shapes`). This argument doesn't need to be provided if there is only one shapes key or a table with only one region.",
    ),
    points_key: str = typer.Option(
        None,
        help="Name of the transcripts (key of `sdata.points`). This argument doesn't need to be provided if there is only one points key.",
    ),
    gene_column: str = typer.Option(
        None, help="Column name of the points dataframe containing the gene names"
    ),
    pixelsize: float = typer.Option(
        0.2125,
        help="Number of microns in a pixel. Invalid value can lead to inconsistent scales in the Explorer.",
    ),
    spot: bool = typer.Option(False, help="Whether the technology is based on spots"),
    layer: str = typer.Option(
        None,
        help="Layer of `sdata.table` where the gene counts are saved. If `None`, uses `sdata.table.X`.",
    ),
    lazy: bool = typer.Option(
        True,
        help="If `True`, will not load the full images in memory (except if the image memory is below `ram_threshold_gb`)",
    ),
    ram_threshold_gb: int = typer.Option(
        4,
        help="Threshold (in gygabytes) from which image can be loaded in memory. If `None`, the image is never loaded in memory",
    ),
    mode: str = typer.Option(
        None,
        help="string that indicated which files should be created. `'-ib'` means everything except images and boundaries, while `'+tocm'` means only transcripts/observations/counts/metadata (each letter corresponds to one explorer file). By default, keeps everything",
    ),
):
    """Convert a spatialdata object to Xenium Explorer's inputs"""
    from pathlib import Path

    import spatialdata

    from spatialdata_xenium_explorer import write

    sdata = spatialdata.read_zarr(sdata_path)

    if output_path is None:
        output_path = Path(sdata_path).with_suffix(".explorer")

    write(
        output_path,
        sdata,
        image_key=image_key,
        shapes_key=shapes_key,
        points_key=points_key,
        gene_column=gene_column,
        pixelsize=pixelsize,
        spot=spot,
        layer=layer,
        lazy=lazy,
        ram_threshold_gb=ram_threshold_gb,
        mode=mode,
    )


@app.command()
def update_obs(
    adata_path: str = typer.Argument(
        help="Path to the anndata file (`zarr` or `h5ad`) containing the new observations"
    ),
    output_path: str = typer.Argument(
        help="Path to the Xenium Explorer directory (it will update `analysis.zarr.zip`)",
    ),
):
    """Update the cell categories for the Xenium Explorer's (i.e. what's in `adata.obs`). This is useful when you perform analysis and update your `AnnData` object

    Usage:
        This command should only be used if you updated `adata.obs`, after creation of the other explorer files.
    """
    from pathlib import Path

    import anndata

    from spatialdata_xenium_explorer import write_cell_categories

    path = Path(adata_path)

    if path.is_dir():
        adata = anndata.read_zarr(path)
    else:
        adata = anndata.read_h5ad(path)

    write_cell_categories(output_path, adata)


@app.command()
def add_aligned(
    sdata_path: str = typer.Argument(help=SDATA_HELPER),
    image_path: str = typer.Argument(
        help="Path to the image file to be added (`.ome.tif` used in the explorer during alignment)"
    ),
    transformation_matrix_path: str = typer.Argument(
        help="Path to the `matrix.csv` file returned by the Explorer after alignment"
    ),
    original_image_key: str = typer.Option(
        None,
        help="Optional original-image key (of sdata.images) on which the new image will be aligned. This doesn't need to be provided if there is only one image",
    ),
    overwrite: bool = typer.Option(False, help="Whether to overwrite the image if existing"),
):
    """After alignment on the Xenium Explorer, add an image to the SpatialData object"""
    import spatialdata

    from spatialdata_xenium_explorer import align
    from spatialdata_xenium_explorer.core.images import ome_tif

    sdata = spatialdata.read_zarr(sdata_path)
    image = ome_tif(image_path)

    align(
        sdata, image, transformation_matrix_path, overwrite=overwrite, image_key=original_image_key
    )
