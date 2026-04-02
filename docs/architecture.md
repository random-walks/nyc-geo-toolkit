# Architecture

`nyc-geo-toolkit` is structured as a small data-first package.

## Flow

```mermaid
flowchart LR
    packagedData[PackagedBoundaryData] --> resources[load_boundary_payload]
    resources --> loaders[load_nyc_boundaries]
    loaders --> models[BoundaryCollection]
    models --> conversions[boundaries_to_geojson / boundaries_to_dataframe]
    models --> clipping[clip_boundaries_to_bbox]
    loaders --> spatialHelpers[load_nyc_boundaries_geodataframe]
```

## Modules

- `nyc_geo_toolkit._catalog` for layer metadata
- `nyc_geo_toolkit._normalize` for layer and value normalization
- `nyc_geo_toolkit._resources` for packaged data access
- `nyc_geo_toolkit._geojson` for parsing GeoJSON into typed models
- `nyc_geo_toolkit._loaders` for boundary loading and optional GeoDataFrame
  helpers
- `nyc_geo_toolkit._conversions` for GeoJSON and DataFrame conversion helpers
- `nyc_geo_toolkit._ops` for generic clipping operations
