class Versions:
    EXPERIMENT = [2, 0]


class ExplorerConstants:
    GRID_SIZE = 250
    QUALITY_SCORE = 40


EXPERIMENT = {
    "major_version": Versions.EXPERIMENT[0],
    "minor_version": Versions.EXPERIMENT[1],
    "run_start_time": "N/A",
    "preservation_method": "N/A",
    "num_cells": 0,
    "transcripts_per_cell": 0,
    "transcripts_per_100um": 0,
    "cassette_name": "N/A",
    "slide_id": "N/A",
    "panel_design_id": "N/A",
    "panel_name": "N/A",
    "panel_organism": "Human",
    "panel_num_targets_predesigned": 0,
    "panel_num_targets_custom": 0,
    "pixel_size": 0.2125,
    "instrument_sn": "N/A",
    "instrument_sw_version": "N/A",
    "analysis_sw_version": "xenium-1.3.0.5",
    "experiment_uuid": "",
    "cassette_uuid": "",
    "roi_uuid": "",
    "z_step_size": 3.0,
    "well_uuid": "",
    "calibration_uuid": "N/A",
    "images": {
        "morphology_filepath": "morphology.ome.tif",
        "morphology_mip_filepath": "morphology_mip.ome.tif",
        "morphology_focus_filepath": "morphology_focus.ome.tif",
    },
    "xenium_explorer_files": {
        "transcripts_zarr_filepath": "transcripts.zarr.zip",
        "cells_zarr_filepath": "cells.zarr.zip",
        "cell_features_zarr_filepath": "cell_feature_matrix.zarr.zip",
        "analysis_zarr_filepath": "analysis.zarr.zip",
        "analysis_summary_filepath": "analysis_summary.html",
    },
}
