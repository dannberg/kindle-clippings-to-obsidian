# kindle-clippings

Based on [kindle-clippings by Ivzon](https://github.com/lvzon/kindle-clippings)

# How to run

`./extract-kindle-clippings.py [<My Clippings.txt file> [<output directory>]]`

Example:

`./extract-kindle-clippings.py /Users/dannberg/Desktop/Temp/My\ Clippings.txt /Users/dannberg/Desktop/Temp/clippings/`

If not specified, the default input file is `./My Clippings.txt` or `/media/$USER/Kindle/documents/My Clippings.txt`. The default output directory is `./clippings/`.

# What it does

This script reads the `My Clippings.txt` file, which is stored in the `documents`-folder on a Kindle e-reader, extracts the notes and highlights and stores these as separate text files for each publication (e-book, PDF, etc.) in a clippings directory. These clippings files can then be edited, reorganised and re-ordered within the clippings directory, and only new highlights and notes will be added the next time the script is run. The output files use reStructured Text (RST) formatting, so that they can be easily converted into new e-books, which include metadata on the publications (title, author). Metadata on the notes/highlights (location, date, type, partial SHA256-hash) is written as an RST-comment before each note, so this information can be found in the text files but becomes invisible if they are converted into e-books or other output document types (PDF, word processor files, etc.).

This script requires Python 3 and is written for use on Linux, Mac, BSD and other Unix-derivatives, although it will probably also work on Windows (I can't test this as I don't run Windows, so feel free to open issues, or better, create a fix and commit a pull request if it doesn't work). I've tested the script with the `My Clippings.txt` file from my first-generation Kindle. Please open an issue or commit a fix if it doesn't work with later Kindle-versions.

# Example output

```Highlights from The Culture Code
================================

Authors:: [[Daniel Coyle]]
Reading Status:: #read
Recommended By::
Tags:: #Books
# Highlights
    - Laszlo Bock, former head of People Analytics at Google, recommends that leaders ask their people three questions: •  What is one thing that I currently do that you’d like me to continue to do? •  What is one thing that I don’t currently do frequently enough that you think I should do more often?
    - What can I do to make you more effective? “The key is to ask not for five or ten things but just one,” Bock says. “That way it’s easier for people to answer. And when a leader asks for feedback in this way, it makes it safe for the people who work with them to do the same. It can get contagious.”
    - “One of the things I say most often is probably the simplest thing I say,” says Givechi. “ ‘Say more about that.’ ”
    - motivation is not a possession but rather the result of a two-part process of channeling your attention: Here’s where you’re at and Here’s where you want to go.
```

# How it works

The script works by scanning `My Clippings.txt` and generating a SHA-256 hash for each note, which is stored in the output file comments. When the script is run, it scans all RST-files in the output directory for hashes, and only writes the notes and highlights which weren't found in the output directory. Publications which have only one or two notes/highlights don't get their own output file, but the notes/highlights are appended to `short_notes.rst`, together with the author and title of the publication. Each output file is given the time and date of the most recent note/highlight.

Because the script only scans the hashes in the comments, you're free to rename, move, split, combine, amend and otherwise edit the output files, as long as you keep the comment lines (the lines starting with `..`), keep the files within the output directory (or subdirectories thereof) and keep the `.rst` file extension. You can move comment lines anywhere in the RST-file, and even safely delete or change the actual notes/highlights. You can also safely combine output files from different e-readers or other sources.


    Copyright 2018, Levien van Zon (gnuritas.org)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

