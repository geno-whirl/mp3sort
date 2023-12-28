import os

from . import sort_dir

if __name__ == "__main__":
    # dir_path = os.path.expanduser("~/Music/Music_raw")
    # dest = os.path.expanduser("~/Music/Music_sorted")
    dir_path = os.path.expanduser("/media/toti/Totilio 3/Music/Music_raw")
    dest = os.path.expanduser("/media/toti/Totilio 3/Music/Music_sorted")
    sort_fields = ["genre", "artist", "album"]
    sort_dir(dir_path, dest, sort_fields)
