## [0.1.6] - tbd

### Breaking changes
- `pixelsize` is now renamed `pixel_size`

## [0.1.5] - 2024-01-30

### Added
- Support spot-based technologies like Visium
- Faster table conversion (using native CSR matrix arguments)

### Fix
- Keep right image name during image alignment

## [0.1.4] - 2024-01-11

### Fix
- When a table is sorted or filtered, the polygons are written in the right order (#2)

### Change
- Now forces using `spatialdata>=0.0.15`

## [0.1.3] - 2023-12-08

### Added
- New CLI
- Documentation
- Support both spatial images and multi-scale spatial images
- Better memory management during conversion
- Support image alignment with the explorer
- Conversion between explorer ID and AnnData ID