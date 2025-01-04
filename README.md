# kindle-clippings-to-obsidian

You can use this Python3 script to easily format all your Kindle Highlights for easy import into [Obsidian](https://obsidian.md/), a super-charged notetaking app for connected thoughts. Based on [kindle-clippings by Ivzon](https://github.com/lvzon/kindle-clippings).

It creates separate text files for each of your books.

❗ I use this tool as part of my larger [Obsidian Book Note system](https://dannb.org/blog/2022/recalling-books-youve-read-made-easy/). I've got a few other Obsidian systems documented as well, and I'll link to those as the end of this readme in case anyone is interested.

# Requirements
- Python 3
- Terminal

# How to run

1. As you're reading on your Kindle, highlight passages that you'd like to save for export to Obsidian.

2. Connect your Kindle to your computer, navigate to the `documents` folder and locate the file `My Clippings.txt`. I like to save this document to my computer, but you can run this script directly from the Kindle if you want. Just make sure you're specifying a local output directory.

3. You'll now want to run the Python script, using your `My Clippings.txt` file as the input. Navigate to the directory where `extract-kindle-clippings.py` lives, and run the following commands in your Terminal.

First, make the script executable:

`chmod +x extract-kindle-clippings.py`

Then, run the script, including both the past of your txt document and an output directory:

`./extract-kindle-clippings.py [<path to My Clippings.txt file>] -o [<output directory>]`

Example:

`./extract-kindle-clippings.py /Users/dannberg/Desktop/Temp/My\ Clippings.txt -o /Users/dannberg/Desktop/Temp/clippings/`

If the input file is not specified, the default input file is `./My Clippings.txt` or `/media/$USER/Kindle/documents/My Clippings.txt`.

If an output flag and directory is not specified, the default output directory is `clippings/` in the current directory. If `clippings/` does not exist, it will be created.

After running the script, you'll be presented with a list of all books found in your clippings file. You can:
- Enter `0` to process all books
- Enter a single number to process one specific book
- Enter multiple numbers separated by spaces to process several books
- If `0` is included with other numbers, all books will be processed

4. Navigate to the new `clippings` directory, open the text file of the book you want, and copy/paste into Obsidian.

## Example output

```
Highlights from The Personal MBA: Master the Art of Business
============================================================

Authors:: [[Josh Kaufman]]
Recommended By::
Tags:: [[📚 Books]]

# The Personal MBA: Master the Art of Business

### Highlights
- It is important that students bring a certain ragamuffin, barefoot irreverence to their studies; they are not here to worship what is known, but to question it. —JACOB BRONOWSKI, WRITER AND PRESENTER OF THE ASCENT OF MAN
- Every successful business (1) creates or provides something of value that (2) other people want or need (3) at a price they’re willing to pay, in a way that (4) satisfies the purchaser’s needs and expectations and (5) provides the business sufficient revenue to make it worthwhile for the owners to continue operation.
```

## Customizing the output

I've customized the output to fit the way that I like to process my books in Obsidian. You may do things differently in your own Obsidian Vault. If you'd like to customize the output format, it's super easy to do.

Open `extract-kindle-clippings.py` in your code editor of choice (such as Sublime Text) and navigate to lines 226 - 231. You can then edit the strings to match your desired format. Adding `\n` inline will create a new line in the output file. Line 231 is a great example of how a single string will show as multiple lines in the output file.

## Note about Notes

The Kindle allows users to add Notes to books in addition to just highlights. This isn't something that I do myself, so the formatting may be imperfect. However, these Notes should be captured by this script alongside Highlights. It just may take some additional manual formatting to make them pretty for Obsidian.

# What it does

This script reads the `My Clippings.txt` file, which is stored in the `documents`-folder on a Kindle e-reader, extracts the notes and highlights and stores these **as separate text files for each publication** (e-book, PDF, etc.) in a clippings directory.

These clippings files can then be edited, reorganized and re-ordered within the clippings directory, and only new highlights and notes will be added the next time the script is run. The output files use reStructured Text (RST) formatting, so that they can be easily converted into new e-books, which include metadata on the publications (title, author). Metadata on the notes/highlights (location, date, type, partial SHA256-hash) is written as an RST-comment before each note, so this information can be found in the text files but becomes invisible if they are converted into e-books or other output document types (PDF, word processor files, etc).

This script requires Python 3 and is written for use on Linux, Mac, BSD and other Unix-derivatives, although it will probably also work on Windows (I can't test this as I don't run Windows, so feel free to open issues, or better, create a fix and commit a pull request if it doesn't work). I've tested the script with the `My Clippings.txt` file from my first-generation Kindle Oasis.

# How it works

The script works by scanning `My Clippings.txt` and generating a SHA-256 hash for each note, which is stored in the output file comments. When the script is run, it scans all Markdown files in the output directory for hashes, and only writes the notes and highlights which weren't found in the output directory. Publications which have only one or two notes/highlights don't get their own output file, but the notes/highlights are appended to `short_notes.md`, together with the author and title of the publication. Each output file is given the time and date of the most recent note/highlight.

Because the script only scans the hashes in the comments, you're free to rename, move, split, combine, amend and otherwise edit the output files, as long as you keep the comment lines (the lines starting with `..`), keep the files within the output directory (or subdirectories thereof) and keep the `.md` file extension. You can move comment lines anywhere in the RST-file, and even safely delete or change the actual notes/highlights. You can also safely combine output files from different e-readers or other sources.

# My other Obsidian & Productivity Systems

**Blogs**
- [Obsidian Daily Note system](https://dannb.org/blog/2022/obsidian-daily-note-template/)
- [Obsidian People Note system](https://dannb.org/blog/2022/obsidian-people-note-template/)
- [Obsidian Book Note system](https://dannb.org/blog/2022/recalling-books-youve-read-made-easy/)
- [Daily Driver Task Management System](https://dannb.org/blog/2020/daily-driver-task-management-system/)

**Videos**
- [My Obsidian Daily Note Template video](https://youtu.be/v84uSIqqVPQ)
- [My Obsidian Meeting Note Template video](https://youtu.be/Ud16HOQoS5Q)
- [My Obsidian People Note Template video](https://youtu.be/N8K41HDRI3o)

**Additional links**
- [dannb.org](https://dannb.org)
- [Monthly newsletter](https://dannb.org/newsletter)

# License

    Copyright 2025, Dann Berg (dannb.org)

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

