# Changelog

All notable changes to this dataset are recorded here. Dates are export dates, not
necessarily publish dates.

## 2026-10-12

- Massive Tamil-script metadata expansion across the 3,035-song dataset, incorporating completed track-level research, transliteration passes, and authority updates:
  - Film titles in Tamil: expanded from 95 (3.1%) to 2,818 (92.9%).
  - Song titles in Tamil: expanded from 95 (3.1%) to 1,229 (40.5%).
  - Composers in Tamil: expanded from 2,407 (79.3%) to 2,974 (98.0%).
  - Singers in Tamil: expanded from 2,168 (71.4%) to 3,010 (99.2%).
  - Lyricists in Tamil: expanded from 80 (2.6%) to 1,272 (41.9%).
  - Billed cast added: 1,802 tracks now have verified Tamil & English cast members (up from 29).
  - Release year coverage: expanded from 2,415 (79.6%) to 2,905 (95.7%).
  - Sources: 2,936 tracks (96.7%) backed by public Wikipedia / Wikidata / official discography URLs.
- Confidence tier recalibration:
  - High confidence rose from 73 to 1,635 tracks due to multi-source verification and soundtrack track completion.
  - Medium confidence: 1,353 tracks.
  - Low confidence reduced from 511 down to 47 tracks.
- Authority dictionary (`data/people.json`):
  - Added 6 canonical music directors and artists (Deva, G. V. Prakash Kumar, T. Rajendar, Srikanth Deva, Sirpi, Mani Sharma) with variant mappings and source references (total 66 entities).
- Data quality cleaning:
  - Stripped stray `.mp3` extension from "Ival Thaane" title.
  - Stripped Apple Music boilerplate suffixes like `(Original Motion Picture Soundtrack)` and `(Background Score)` from song and film titles.

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
