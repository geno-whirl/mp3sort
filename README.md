# mp3sort

Allows to sort an mp3 library into a given folder structure by metadata values.

## Usage

```python
geno-whirl.mp3sort.sort_dir(dir_path: str, dest: str, sort_fields: list[str])
```

Finds all music files in `dir_path` and moves them into `dest`, in folders
determined by the tree structure defined by the sorting fields. If `sort_fields` is
["genre", "artist", "album"], will first make a folder for each genre, within it
make a folder for each artist and within each of them make a folder for each album.

Fields are recovered from music file metadata by means of the `music_tag` package (installed via `pip`).
See documentation for available fields.