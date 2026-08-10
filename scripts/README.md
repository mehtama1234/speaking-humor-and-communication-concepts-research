# Scripts

Utility scripts for transcript capture, corpus indexing, and repo validation.

Date: August 10, 2026.

## Purpose

These scripts support three different parts of the workspace:

- source capture
- transcript-to-analysis workflow
- site and markdown validation

## Source capture

### `capture_youtube_channel_manifest.py`

Use this to capture a stable flat-playlist manifest for a YouTube channel,
playlist, or video feed.

Typical output:

- `raw-material/youtube/channels/<slug>.json`
- `raw-material/youtube/manifests/<slug>.json`

Use this when:

- identifying a new source channel
- refreshing a source manifest
- capturing a channel before transcript work begins

## Transcript workflow

### `download_youtube_playlist_transcripts.py`

Use this to capture transcript artifacts for a curated starter corpus.

Typical output under:

- `raw-material/youtube/transcripts/<slug>/`

This includes:

- raw VTT subtitle files
- cleaned transcript text
- cue JSON
- transcript indexes
- summary metadata

### `build_course_session_inventory.py`

Use this after transcript capture to generate a markdown session inventory for
one corpus.

Typical output:

- `analysis/<slug>-session-inventory.md`

Use this when:

- turning transcript output into a scannable course/session map
- preparing session briefs or theme extraction

## Validation

### `validate_site_data.js`

Checks:

- duplicate slugs in `site/data.js`
- broken cross-collection slug references
- missing `linkedFiles` targets

### `validate_markdown_refs.js`

Checks:

- backticked repo-path references in `README.md`
- backticked repo-path references in `analysis/`
- backticked repo-path references in `raw-material/README.md`

### `validate_all.sh`

Runs the full default validation sequence:

1. `node scripts/validate_site_data.js`
2. `node scripts/validate_markdown_refs.js`
3. `node --check site/data.js`
4. `node --check site/app.js`

Use this as the default repo-quality check after changing analysis or site
files.

## Recommended default commands

Capture one starter corpus:

```bash
python3 scripts/download_youtube_playlist_transcripts.py \
  --course-root . \
  --manifest raw-material/youtube/starter-manifests/ultraspeaking-wave-1.json
```

Build its session inventory:

```bash
python3 scripts/build_course_session_inventory.py \
  --course-root . \
  --manifest raw-material/youtube/starter-manifests/ultraspeaking-wave-1.json \
  --output analysis/ultraspeaking-wave-1-session-inventory.md
```

Run the repo validation stack:

```bash
./scripts/validate_all.sh
```
