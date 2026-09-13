# Changelog

All notable changes to this dataset are recorded here. Dates are export dates, not
necessarily publish dates.

## 2026-09-13

- Initial public export: 3,030 songs, 60 people.
- Filtered the source library down to Tamil-language content only: excluded 10 tracks
  correctly tagged `genre=Telugu`, plus 32 more tagged `genre=Tamil` in error (*Arya*,
  *Athadu*, *Baahubali 1*, *Magadheera*, *Varsham*, *Vedam* — all Telugu films — and two
  Western classical/pop tracks). See `scripts/export_public_dataset.py` for the exact
  list.
- Normalized two data-quality quirks inherited from the source project: a non-standard
  `needs_review` confidence label (12 rows) mapped to `low`, and duplicate `content_type`
  labels (`karaoke` / `instrumental_score`) merged into their canonical form.
- Repository renamed from `tamil-film-song-metadata` to `tamil-film-songs-metadata`.
