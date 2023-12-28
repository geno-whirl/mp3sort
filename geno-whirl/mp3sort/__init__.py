# ===============================
# mp3sort
# ===============================
# Tomás Lungenstrass, 2023
"""
Allows to sort an mp3 library into a given folder structure by metadata values.

Routine Listing
---------------
sort_dir: function
    Find recursively all music files and sort in folders according to given sort fields.

"""

__version__ = "0.1.0"

import os
from collections import defaultdict

import music_tag
from tqdm import tqdm

_invalid_characters = ["?", "/", ":", '"', "<", ">"]
_repl_char = "_"


def _replace_invalid_chars(s: str) -> str:
    for c in _invalid_characters:
        s = s.replace(c, _repl_char)
    return s


def get_all_music_files_in_dir(dir_path):
    music_files: dict[str, music_tag.file.AudioFile] = {}
    extraneous_files: list[str] = []
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                music_files[filepath] = music_tag.load_file(filepath)
            except NotImplementedError:
                extraneous_files.append(filepath)

    return music_files, extraneous_files


def sort_dir(dir_path: str, dest: str, sort_fields: list[str]):
    """
    Find recursively all music files and sort in folders according to given sort fields.

    Finds all music files in `dir_path` and moves them into `dest`, in folders
    determined by the tree structure defined by the sorting fields. If `sort_fields` is
    ["genre", "artist", "album"], will first make a folder for each genre, within it
    make a folder for each artist and within each of them make a folder for each album.

    Fields are recovered from music file metadata by means of the `music_tag` package.
    See documentation for available fields.
    """
    if len(sort_fields) == 0:
        raise ValueError("No sorting fields given.")

    # get music files with metadata
    music_files, extraneous_files = get_all_music_files_in_dir(dir_path=dir_path)

    # construct sort tree
    def _sort_tree_constructor(sort_fields) -> defaultdict:
        if len(sort_fields) == 1:
            return defaultdict(list)
        else:
            return defaultdict(lambda: _sort_tree_constructor(sort_fields[1:]))

    sort_tree = _sort_tree_constructor(sort_fields)

    # populate sorted tree
    for filepath, music_file in tqdm(
        music_files.items(), desc="Sorting music files..."
    ):
        field_values = [music_file[sort_field].value for sort_field in sort_fields]
        node = sort_tree
        for field_value in field_values:
            node = node[field_value]
        node.append(filepath)

    # move files to respective directories
    def make_dir_from_tree(sort_tree, dest):
        # make directory
        if not os.path.exists(dest):
            os.mkdir(dest)

        # if at list level, populate directory
        if isinstance(sort_tree, list):
            for filepath in sort_tree:
                filename = os.path.basename(filepath)
                dest_filepath = os.path.join(dest, filename)
                os.rename(filepath, dest_filepath)
            return

        # if still at dict level, recurse over sort fields
        for sort_value, sub_sort_tree in tqdm(sort_tree.items()):
            sort_value = _replace_invalid_chars(sort_value)
            make_dir_from_tree(sub_sort_tree, os.path.join(dest, sort_value))

    make_dir_from_tree(sort_tree, dest)

    pass
