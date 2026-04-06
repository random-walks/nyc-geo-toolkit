# Changelog

## 0.1.7

- add optional map helpers `add_osm_basemap`, `to_web_mercator`, and `bbox_around`
  (see `nyc_geo_toolkit._basemap`), exported from the top-level namespace
- declare `contextily` as part of the `spatial` / `all` optional dependency sets

## 0.1.2

- refresh public authorship metadata to credit Blaise Albis-Burdige directly
- add `blaiseab.com` as the portfolio link on package and docs surfaces
- align README, docs, and site metadata with the same attribution model

## 0.1.1

- preserve canonical zero-padded council district identifiers such as `09`
- tighten release and packaging checks after the initial public toolkit launch

## 0.1.0

- first standalone public release of `nyc-geo-toolkit`
- extract reusable NYC geography assets and normalization helpers from `nyc311`
- ship typed boundary models, packaged GeoJSON layers, conversion helpers, and
  optional dataframe/spatial helpers
