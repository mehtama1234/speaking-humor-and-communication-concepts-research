# Raw Material

This directory will hold:

- captured YouTube channel and playlist manifests
- transcript indexes
- cleaned transcript text
- cue-level JSON when available
- other source artifacts that support analysis

The immediate substructure is:

- `youtube/channels/` for raw `yt-dlp` captures
- `youtube/manifests/` for normalized repo-facing manifests
- `youtube/starter-manifests/` for curated first-wave transcript corpora
- `youtube/playlists/` for refreshed playlist or channel captures tied to transcript runs
- `youtube/transcripts/<slug>/` for corpus-specific transcript outputs
