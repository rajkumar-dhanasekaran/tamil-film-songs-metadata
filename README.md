# tamil-film-songs-metadata

A public-domain (CC0) dataset of Tamil film song metadata — film, song title, composer,
singer(s), and lyricist(s), each in both English and Tamil script — sourced from
Wikipedia, Wikidata, and manual research, with a source URL for every credit that's
verified rather than guessed.

This is a byproduct of standardizing one personal music library, not a scrape of "all
Tamil film music": it covers the Tamil-language tracks that library contained (3,038 of
them), spanning films from 1961 to the mid-2020s. The source library was scanned as a
whole and picked up a handful of Telugu and Western tracks along the way; those are
filtered out (see "What's not included" and `scripts/export_public_dataset.py`) so this
stays a Tamil-only dataset. It is not exhaustive, but every row that carries a source URL
has been checked against that source, not auto-generated.

## Files

- **`data/songs.csv`** — one row per track.
- **`data/people.json`** — a canonical English/Tamil name dictionary for singers,
  composers, and lyricists, with known misspellings mapped to the correct spelling and a
  source for each. This is in the exact format the companion
  [`music-metadata-toolkit`](../music-metadata-toolkit)'s `--authority` flag expects, so
  you can point that tool at this file directly.

### `songs.csv` columns

| Column | Meaning |
|---|---|
| `film_en` / `film_ta` / `film_bilingual` | Film title, English / Tamil script / combined display form |
| `song_title_en` / `song_title_ta` / `song_title_bilingual` | Song title, same three forms |
| `composer_en` / `composer_ta` / `composer_bilingual` | Music director / composer |
| `singers_en` / `singers_ta` / `singers_bilingual` | Playback singer(s), `;`-separated if more than one |
| `lyricists_en` / `lyricists_ta` / `lyricists_bilingual` | Lyricist(s), `;`-separated |
| `cast_en` / `cast_ta` | Film's billed cast, where known (from Wikidata) |
| `content_type` | `vocal_song`, `instrumental_score_cue`, `theme_music`, `karaoke_backing_track`, or `unknown` (not specifically flagged as one of the others — most likely a normal song, just not separately confirmed) |
| `year` | Film/soundtrack release year, where known |
| `confidence` | `high` / `medium` / `low` — see below |
| `sources` | `;`-separated public URLs (Wikipedia, Wikidata, etc.) backing this row's credits |

The bilingual columns follow one rule: Tamil script preferred, with the English form
added in parentheses only when it differs — e.g. `இளையராஜா (Ilaiyaraaja)`. If a Tamil
form isn't known yet, the column falls back to English alone.

### Confidence

- **`high`** — credits corroborated by multiple independent sources or confirmed via
  the film's own soundtrack listing.
- **`medium`** — a name has been corrected to its canonical spelling (see `people.json`)
  or an album/film has been identified with reasonable certainty, but full track-level
  credits aren't independently confirmed yet.
- **`low`** — largely unresolved. Present in the dataset for completeness (so this
  library's actual coverage is honestly represented), not because the data is reliable.

As of the last export: 73 rows high-confidence, 2,451 medium, 514 low (out of 3,038).
Treat `medium` and `low` rows as leads to verify, not settled facts.

## What's not included, on purpose

This dataset was extracted from a private personal-library project. Deliberately left
out of every file here:

- Any file path, filename, or folder structure from the source library.
- The source library owner's original (often inconsistent) tags — only the
  researched/corrected values are published.
- Internal workflow labels (review-batch names, QA status jargon) that mean nothing
  outside that project.
- Anything from the `evidence` field that wasn't a plain `http(s)` URL.
- Non-Tamil tracks: the source library also held some Telugu film tracks (10 tagged
  `genre=Telugu`, plus a few more — *Arya*, *Athadu*, *Baahubali 1*, *Magadheera*,
  *Varsham*, *Vedam* — mistakenly tagged `genre=Tamil`) and a couple of Western
  classical/pop tracks (Beethoven, The Beatles) that had the same wrong genre tag. 45
  tracks were excluded this way; the exact list is in `NON_TAMIL_ALBUM_COMPOSER_PAIRS`
  at the top of `scripts/export_public_dataset.py`, in the open.

If you want to see exactly how the export was scrubbed, `scripts/export_public_dataset.py`
is the (small, readable) script that produced these files.

## Regenerating this dataset

You don't need the source project to *use* this dataset — `data/songs.csv` and
`data/people.json` are the deliverable. `scripts/export_public_dataset.py` exists so the
export is auditable and reproducible, not because you need to run it:

```bash
python scripts/export_public_dataset.py --source /path/to/source-project --output data
```

## Using this with music-metadata-toolkit

```bash
music-metadata propose ./my-project/data/catalog.sqlite3 \
  --authority /path/to/tamil-film-songs-metadata/data/people.json \
  --field-pack tamil-english \
  --output-dir ./my-project/output/proposals
```

## Contributing corrections

Found a wrong credit or a missing Tamil title? Please open an issue or PR with a source
URL — this dataset's entire value is that every claim is checkable, so corrections need
one too.

## License

[CC0 1.0 Universal](LICENSE) — public domain. Use it for anything, no attribution
required (though a link back is always appreciated).

---

**Last updated:** 2026-09-13 · 3,038 songs · see [CHANGELOG.md](CHANGELOG.md) for what
changed between exports.
