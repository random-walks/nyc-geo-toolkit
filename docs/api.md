# API Reference

The stable reference for this package is the top-level `nyc_geo_toolkit`
namespace. This page is generated directly from that namespace so the published
API docs, the package `__all__`, and the consumer contract stay aligned.

Underscore-prefixed modules are internal implementation details and are not part
of the supported public surface.

## Loading & Discovery

::: nyc_geo_toolkit
    options:
      members:
        - list_boundary_layers
        - list_boundary_values
        - list_available_vintages
        - vintage_for_census_decade
        - load_nyc_boundaries
        - load_nyc_boundaries_geodataframe
        - load_boundaries
        - load_nyc_census_tracts
        - load_nyc_council_districts
        - load_nyc_neighborhood_tabulation_areas
        - describe_layer

## Normalization

::: nyc_geo_toolkit
    options:
      members:
        - normalize_borough_name
        - normalize_boundary_layer
        - normalize_boundary_value
        - normalize_boundary_values

## Models

::: nyc_geo_toolkit
    options:
      members:
        - BoundaryCollection
        - BoundaryFeature
        - BoundaryLayerSpec

## Conversion

::: nyc_geo_toolkit
    options:
      members:
        - boundaries_to_geojson
        - boundaries_to_dataframe

## Geodesy

::: nyc_geo_toolkit
    options:
      members:
        - haversine_distance_meters
        - walk_radius_meters
        - build_circle_polygon

## Spatial Helpers

::: nyc_geo_toolkit
    options:
      members:
        - clip_boundaries_to_bbox
        - add_osm_basemap
        - to_web_mercator
        - bbox_around

## Constants

::: nyc_geo_toolkit
    options:
      members:
        - DEFAULT_VINTAGE
        - SUPPORTED_BOROUGHS
        - SUPPORTED_BOUNDARY_GEOGRAPHIES
        - BOROUGH_BRONX
        - BOROUGH_BROOKLYN
        - BOROUGH_MANHATTAN
        - BOROUGH_QUEENS
        - BOROUGH_STATEN_ISLAND
