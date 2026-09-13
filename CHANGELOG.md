# Changelog

All notable changes to this dataset are recorded here. Dates are export dates, not
necessarily publish dates.

## 2026-09-13

- Initial public export: 3,038 songs, 60 people.
- Filtered the source library down to Tamil-language content only: excluded 10 tracks
  correctly tagged `genre=Telugu`, plus 33 more tagged `genre=Tamil` in error (*Arya*,
  *Athadu*, *Baahubali 1*, *Magadheera*, *Varsham*, *Vedam* — all Telugu films — and two
  Western classical/pop tracks). Tracks composed by Hamsalekha (*Paruva Raagam*/*Paruva
  Ragam*, *Captain Magal*) were initially excluded too on the assumption he's
  Kannada-only, then restored after confirming he has also scored Tamil films. See
  `scripts/export_public_dataset.py` for the exact exclusion list.
- Normalized two data-quality quirks inherited from the source project: a non-standard
  `needs_review` confidence label (12 rows) mapped to `low`, and duplicate `content_type`
  labels (`karaoke` / `instrumental_score`) merged into their canonical form.
- Repository renamed from `tamil-film-song-metadata` to `tamil-film-songs-metadata`.
- Follow-up pass after publishing found two more issues, now fixed (3,035 songs):
  excluded 3 tracks under "Swami Vivekananda" that turned out to be his English-language
  1893 speeches, not Tamil songs; and stripped download-site watermarks (e.g. "- some
  site.blogspot.com", or a bare site name) that had ended up in the artist tag on 8
  tracks, via a new `clean_names()` step in the export script.
