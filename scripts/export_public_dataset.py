#!/usr/bin/env python3
"""Build the public tamil-film-songs-metadata dataset from a private source project.

Reads ONLY `output/full_library/full_library_proposals.csv` and `authority/*.json` from
the source project directory (never the raw audio library, never `data/catalog.sqlite3`,
never anything under `output/bulk_enrichment/` or `artwork/`). Writes fully scrubbed,
public-safe files into this repo's `data/` directory:

  - data/songs.csv   — one row per track: film/song/people names (EN + TA), year,
                        content type, confidence, and public source URLs only.
  - data/people.json — canonical singer/composer/lyricist name dictionary, mapping
                        known misspellings and aliases to standard forms.

Deliberately excluded from the export, by design (see README "What's not included"):
  - relative_path / filename / any on-disk path
  - the "current_*" raw tag columns (this user's own, possibly messy, original tags)
  - internal workflow fields (review_status jargon, audio_file_modified, export-mode
    policy fields, batch/file provenance tokens) that mean nothing outside this project
  - anything that isn't a plain http(s) URL from the "evidence" column
  - any track identified as not actually Tamil-language, or not a song at all (see
    `is_excluded` below) — the source library was scanned as a whole and picked up some
    Telugu tracks, Western classical/pop tracks, and even a few English spoken-word
    recordings along the way; this dataset promises Tamil film songs only.
  - download-site watermarks (e.g. "Some Singer - moviegalleri.blogspot.com") that ended
    up sitting in a handful of the source library's own artist tags, stripped from every
    name field by `clean_names` before anything is written out.

Run this from a checkout of both repos as siblings, e.g.:
    python scripts/export_public_dataset.py \
        --source ../tamil-music-metadata \
        --output data
"""

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

URL_RE = re.compile(r"https?://[^\s;]+")
VALID_CONFIDENCE = {"high", "medium", "low"}
CONTENT_TYPE_ALIASES = {
    "karaoke": "karaoke_backing_track",
    "instrumental_score": "instrumental_score_cue",
}

# The source library's genre tag is a reliable Telugu signal when present...
NON_TAMIL_GENRES = {"Telugu"}

# ...but a handful of tracks were tagged genre="Tamil" despite being from a different
# film/collection entirely — the genre tag was just wrong. Each of these was checked
# individually (film + composer) against Wikipedia before being added here; matched on
# (current_album, current_composer) rather than album name alone, since album titles
# can coincidentally repeat across languages/collections.
NON_TAMIL_ALBUM_COMPOSER_PAIRS = {
    ("Arya", "Devi Sri Prasad"),                          # 2004 Telugu film (Allu Arjun)
    ("Athadu", "Mani Sharma"),                            # 2005 Telugu film (Mahesh Babu)
    ("Baahubali 1", "M. M. Keeravaani"),                  # 2015 Telugu film
    ("Magadheera", "M. M. Keeravaani"),                   # 2009 Telugu film
    ("Varsham", "Devi Sri Prasad"),                       # 2004 Telugu film
    ("Vedam", "M. M. Keeravaani"),                        # 2010 Telugu film
    ("Beethoven Music Collection", "Ludwig van Beethoven"),  # Western classical, not a film
    ("Beethoven Music Collection", "Franz Schubert"),        # Western classical, not a film
    ("Love", "John Lennon & Paul McCartney"),              # The Beatles compilation, not a film
    # Note: Hamsalekha is primarily a Kannada-cinema composer but has also scored Tamil
    # films (confirmed with the library owner), so his tracks (Paruva Raagam / Paruva
    # Ragam / Captain Magal) are NOT excluded here.
}

# Not a language problem — these aren't songs at all. "Swami Vivekananda" is 3 tracks of
# his famous 1893 English-language addresses (Welcome Address, Why We Disagree, Paper on
# Hinduism), sitting in the library with genre mistagged "Tamil".
NON_SONG_ALBUMS = {"Swami Vivekananda"}

# Watermarks a couple of download sites left behind in the source library's own artist
# tags, e.g. "Yuvan Shankar Raja - moviegalleri.blogspot.com" or a bare "TamilMusica.Com"
# standing in for an unknown singer. Stripped from every name field, not just "artist",
# in case the same pattern shows up elsewhere on a future re-run.
WATERMARK_SUFFIX_RE = re.compile(r"\s*-\s*\S+\.(?:com|net|org|in)\s*$", re.I)
WATERMARK_STANDALONE = {"tamilmusica.com", "moviegalleri.blogspot.com"}


def is_excluded(row):
    if row["current_genre"] in NON_TAMIL_GENRES:
        return True
    if row["current_album"] in NON_SONG_ALBUMS:
        return True
    return (row["current_album"], row["current_composer"]) in NON_TAMIL_ALBUM_COMPOSER_PAIRS


def clean_names(value):
    """Strip download-site watermarks out of a ';'-delimited name field (also safe to run
    on a bilingual-combined string, since the watermark always trails the last name)."""
    parts = []
    for part in (value or "").split(";"):
        part = WATERMARK_SUFFIX_RE.sub("", part).strip()
        if part and part.lower() not in WATERMARK_STANDALONE:
            parts.append(part)
    return "; ".join(parts)

SONG_COLUMNS = [
    "film_en", "film_ta", "film_bilingual",
    "song_title_en", "song_title_ta", "song_title_bilingual",
    "composer_en", "composer_ta", "composer_bilingual",
    "singers_en", "singers_ta", "singers_bilingual",
    "lyricists_en", "lyricists_ta", "lyricists_bilingual",
    "cast_en", "cast_ta",
    "content_type", "year", "confidence", "sources",
]


def extract_urls(evidence):
    return "; ".join(dict.fromkeys(URL_RE.findall(evidence or "")))


def export_songs(proposals_csv, output_path):
    with proposals_csv.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    excluded = [row for row in rows if is_excluded(row)]
    rows = [row for row in rows if not is_excluded(row)]

    output_rows = []
    for row in rows:
        output_rows.append({
            "film_en": clean_names(row["album_english"]),
            "film_ta": clean_names(row["album_tamil"]),
            "film_bilingual": clean_names(row["album_bilingual"]),
            "song_title_en": row["title_english"],
            "song_title_ta": row["title_tamil"],
            "song_title_bilingual": row["title_bilingual"],
            "composer_en": clean_names(row["composer_english"]),
            "composer_ta": clean_names(row["composer_tamil"]),
            "composer_bilingual": clean_names(row["composer_bilingual"]),
            "singers_en": clean_names(row["artist_english"]),
            "singers_ta": clean_names(row["artist_tamil"]),
            "singers_bilingual": clean_names(row["artist_bilingual"]),
            "lyricists_en": clean_names(row["lyricist_english"]),
            "lyricists_ta": clean_names(row["lyricist_tamil"]),
            "lyricists_bilingual": clean_names(row["lyricist_bilingual"]),
            "cast_en": clean_names(row["grouping_cast_english"]),
            "cast_ta": clean_names(row["grouping_cast_tamil"]),
            "content_type": CONTENT_TYPE_ALIASES.get(row["content_type"], row["content_type"]),
            "year": row["film_year_or_date"] or row["soundtrack_year_or_date"],
            # A handful of source rows (~12) carried a non-standard workflow label
            # ("needs_review") in this column instead of high/medium/low; treat those
            # conservatively as low rather than exposing an internal label externally.
            "confidence": row["confidence"] if row["confidence"] in VALID_CONFIDENCE else "low",
            "sources": extract_urls(row["evidence"]),
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SONG_COLUMNS)
        writer.writeheader()
        writer.writerows(output_rows)
    return output_rows, excluded


def export_people(authority_paths, output_path):
    entities = {}
    for path in authority_paths:
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for item in payload.get("entities", []):
            entity_id = item["id"]
            merged = entities.setdefault(entity_id, {
                "id": entity_id,
                "roles": set(),
                "preferred_names": {},
                "known_variants": set(),
                "sources": set(),
                "notes": "",
            })
            merged["roles"].update(item.get("roles", []))
            if item.get("preferred_english"):
                merged["preferred_names"]["en"] = item["preferred_english"]
            if item.get("preferred_tamil"):
                merged["preferred_names"]["ta"] = item["preferred_tamil"]
            merged["known_variants"].update(item.get("known_local_variants", []))
            merged["sources"].update(item.get("sources", []))
            if item.get("notes") and not merged["notes"]:
                merged["notes"] = item["notes"]

    payload = {
        "schema_version": 1,
        "description": "Canonical English/Tamil name dictionary for Tamil film music singers, "
                       "composers, and lyricists, mapping variant spellings and aliases to standard forms.",
        "entities": [
            {
                "id": entity["id"],
                "roles": sorted(entity["roles"]),
                "preferred_names": entity["preferred_names"],
                "known_variants": sorted(entity["known_variants"]),
                "sources": sorted(entity["sources"]),
                **({"notes": entity["notes"]} if entity["notes"] else {}),
            }
            for entity in sorted(entities.values(), key=lambda e: e["id"])
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True, help="Path to the private tamil-music-metadata checkout")
    parser.add_argument("--output", type=Path, required=True, help="Directory to write songs.csv / people.json into")
    args = parser.parse_args()

    proposals_csv = args.source / "output" / "full_library" / "full_library_proposals.csv"
    authority_paths = [
        args.source / "authority" / "entities.json",
        args.source / "authority" / "pilot_people_candidates.json",
    ]

    songs, excluded = export_songs(proposals_csv, args.output / "songs.csv")
    people = export_people(authority_paths, args.output / "people.json")

    excluded_by_album = defaultdict(int)
    for row in excluded:
        excluded_by_album[(row["current_album"], row["current_composer"], row["current_genre"])] += 1

    print(json.dumps({
        "songs_exported": len(songs),
        "songs_excluded_non_tamil": len(excluded),
        "excluded_by_album_composer_genre": {f"{album} | {composer} | {genre}": count
                                              for (album, composer, genre), count in sorted(excluded_by_album.items())},
        "people_exported": len(people["entities"]),
        "output": str(args.output),
    }, indent=2))


if __name__ == "__main__":
    main()
