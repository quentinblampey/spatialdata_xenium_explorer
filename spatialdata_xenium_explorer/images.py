from pathlib import Path

import numpy as np
import tifffile as tf
from multiscale_spatial_image import MultiscaleSpatialImage

from .constants import image_metadata, image_options


def to_uint8(arr):
    print(f"Writing image of shape {arr.shape}")
    return (arr // 256).astype(np.uint8)


def write_multiscale(
    output_path: Path,
    multiscale: MultiscaleSpatialImage,
    pixelsize: float = 0.2125,
):
    scale_names = list(multiscale.children)
    channel_names = list(multiscale[scale_names[0]].c.values)

    metadata = image_metadata(channel_names, pixelsize)

    with tf.TiffWriter(output_path, bigtiff=True) as tif:
        tif.write(
            to_uint8(multiscale[scale_names[0]]["image"].values),
            subifds=len(scale_names) - 1,
            resolution=(1e4 / pixelsize, 1e4 / pixelsize),
            metadata=metadata,
            **image_options(),
        )

        for i, scale in enumerate(scale_names[1:]):
            tif.write(
                to_uint8(multiscale[scale]["image"].values),
                subfiletype=1,
                resolution=(
                    1e4 * 2 ** (i + 1) / pixelsize,
                    1e4 * 2 ** (i + 1) / pixelsize,
                ),
                **image_options(),
            )
