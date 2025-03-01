#!/usr/bin/env python3

'''
A Python-script that extracts and organises highlights/notes from the "My Clippings.txt" file on a Kindle e-reader. Formats for Obsidian.

Usage: ./extract-kindle-clippings.py <My Clippings.txt file> -o [<optional: output directory>]

Github repository: https://github.com/dannberg/kindle-clippings-to-obsidian

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
'''

import re
import hashlib
from dateutil.parser import parse
import os
from datetime import datetime, timedelta, timezone
import getpass
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='Extract and organize highlights and notes from Kindle "My Clippings.txt" file'
    )
    parser.add_argument('input_file', nargs='?', default='My Clippings.txt',
                      help='Path to My Clippings.txt file (default: My Clippings.txt)')
    parser.add_argument('-o', '--output', default='./clippings',
                      help='Output directory (default: ./clippings)')
    return parser.parse_args()

args = parse_args()
infile = args.input_file
outpath = args.output

# Check if input file exists
if not os.path.isfile(infile):
    username = getpass.getuser()
    infile = os.path.join('/media', username, 'Kindle', 'documents/My Clippings.txt')
    if not os.path.isfile(infile):
        print('Could not find "My Clippings.txt", please provide the file location as an argument')
        sys.exit(1)

# Create output directory if it doesn't exist
if not os.path.isdir(outpath):
    os.makedirs(outpath, exist_ok=True)

def getvalidfilename(filename):
    import unicodedata
    clean = unicodedata.normalize('NFKD', filename)
    return re.sub('[^\w\s()\'.?!:-]', '', clean)

note_sep = '=========='

commentstr = '.. '  # RST (reStructuredText) comment

regex_title = re.compile('^(.*)\((.*)\)$')
regex_info = re.compile(r'^- (\S+) (.*)[\s|]+Added on\s+(.+)$')
regex_loc = re.compile('Loc\. ([\d\-]+)')
regex_page = re.compile('Page ([\d\-]+)')
regex_date = re.compile('Added on\s+(.+)$')

regex_hashline = re.compile('^\.\.\s*([a-fA-F0-9]+)' + '\s*')

pub_title = {}
pub_author = {}
pub_notes = {}
pub_hashes = {}

notes = {}
locations = {}
types = {}
dates = {}

existing_hashes = {}

print('Scanning output dir', outpath)
for directory, subdirlist, filelist in os.walk(outpath):
    for fname in filelist:
        _, ext = os.path.splitext(fname)
        if ext.lower() == '.md':
            print('Found Markdown file', fname, 'in directory', directory)
            # open file, find comment lines, store hashes
            md = open(directory + '/' + fname, 'r')
            line = md.readline()
            lines = 0
            hashes = 0
            while line:
                lines += 1
                findhash_result = regex_hashline.findall(line)
                if len(findhash_result):
                    foundhash = findhash_result[0]
                    existing_hashes[foundhash] = fname
                    hashes += 1
                line = md.readline()
            md.close()
            print(hashes, 'hashes found in', lines, 'scanned lines')
        else:
            print('File', fname, 'does not seem to be Markdown, skipping', ext)

print('Found', len(existing_hashes), 'existing note hashes')
print('Processing clippings file', infile)

mc = open(infile, 'r')

mc.read(1)  # Skip first character

line = mc.readline().strip()

while line:

    key = line.strip()
    result_title = regex_title.findall(key)    # Extract title and author
    line = mc.readline().strip()                # Read information line
    note_type, location, date = regex_info.findall(line)[0]    # Extract note type, location and date
    result_loc = regex_loc.findall(location)
    result_page = regex_page.findall(location)
    if len(result_title):
        title, author = result_title[0]
    else:
        title = key
        author = 'Unknown'

    if len(result_loc):
        note_loc = result_loc[0]
    else:
        note_loc = ''

    if len(result_page):
        note_page = result_page[0]
    else:
        note_page = ''

    note_text = ''
    line = mc.readline()                # Skip empty line
    line = mc.readline().strip()

    while line != note_sep:
        note_text += line + '\n'
        line = mc.readline().strip()

    note_hash = hashlib.sha256(note_text.strip().encode('utf8')).hexdigest()[:8]

    if key not in pub_notes:
        pub_notes[key] = []
        pub_hashes[key] = []

    pub_title[key] = title.strip()
    pub_author[key] = author.strip()
    pub_notes[key].append(note_text.strip())
    pub_hashes[key].append(note_hash)

    locstr = ''
    if note_loc:
        locstr = 'loc.' + note_loc
    if note_page:
        if note_loc:
            locstr += ', '
        locstr += 'p.' + note_page

    try:
        datestr = str(parse(date))
    except:
        datestr = date

    notes[note_hash] = note_text.strip()
    locations[note_hash] = locstr
    types[note_hash] = note_type
    dates[note_hash] = datestr

    line = mc.readline().strip()

mc.close()

def get_user_book_selection(titles):
    # Create a sorted list of unique titles
    unique_titles = sorted(list(set(titles.values())))
    
    print("\nSelect a book (or books) to output:")
    print("[0]: All books")
    for i, title in enumerate(unique_titles, 1):
        print(f"[{i}]: {title}")
    
    while True:
        try:
            selection = input("\nInput one or more numbers, separated by a space: ").strip()
            numbers = [int(num) for num in selection.split()]
            
            # Validate input
            if not numbers:
                print("Please enter at least one number")
                continue
                
            # Check if 0 is selected
            if 0 in numbers:
                return unique_titles
                
            # Validate range of numbers
            if any(num < 0 or num > len(unique_titles) for num in numbers):
                print(f"Please enter numbers between 0 and {len(unique_titles)}")
                continue
                
            # Return selected titles
            return [unique_titles[num-1] for num in numbers]
            
        except ValueError:
            print("Please enter valid numbers separated by spaces")
            continue

# Get user selection
selected_titles = get_user_book_selection(pub_title)

# Modify the main processing loop to only process selected books
for key in pub_title.keys():
    # Skip if this book wasn't selected
    if pub_title[key] not in selected_titles:
        continue
        
    nr_notes = len(pub_notes[key])
    author = pub_author[key]
    title = pub_title[key]
    short_title = title.split('|')[0]
    short_title = short_title.split(' - ')[0]
    short_title = short_title.split('. ')[0]
    if len(short_title) > 128:
        short_title = short_title[:127]
    if (nr_notes > 2):
        fname = author + ' - ' + short_title.strip() + '.md'
        short = 0
    else:
        fname = 'short_notes.md'
        short = 1

    new_hashes = 0
    for note_hash in pub_hashes[key]:
        if note_hash not in existing_hashes:
            new_hashes += 1

    if new_hashes > 0:
        print(new_hashes, 'new notes found for', title)
    else:
        continue            # Skip to next title if there are no new hashes

    outfile = os.path.join(outpath, getvalidfilename(fname))

    newfile = os.path.isfile(outfile)

    out = open(outfile, 'a')

    if short:
        # Short note, output a small header and append to short note file
        if author != 'Unknown':
            titlestr = author + ' - ' + title
        else:
            titlestr = title
        out.write(titlestr + '\n')
        out.write(('-' * len(titlestr)) + '\n\n')
    elif not newfile:
        # Many notes, output with header and metadata in a separate file
        titlestr = 'Highlights from ' + title
        out.write(titlestr + '\n')
        out.write(('=' * len(titlestr)) + '\n\n')
        if author != 'Unknown':
            out.write('Authors:: [[' + author + ']]' + '\n')
        out.write('Recommended By:: \nTags:: [[📚 Books]]\n\n# ' + title + '\n\n### Highlights\n')

    last_date = datetime.now()

    for note_hash in pub_hashes[key]:
        note = notes[note_hash]
        note_type = types[note_hash]
        note_date = dates[note_hash]
        note_loc = locations[note_hash]
        if note_hash in existing_hashes:
            print('Note', note_hash, 'is already in', existing_hashes[note_hash])
        else:
            print('Adding new note to', outfile + ':', note_hash, note_type, note_loc, note_date)

            comment = str(commentstr + note_hash + ' ; ' + note_type + ' ; ' + note_loc + ' ; ' + note_date)

            if short:
                comment += ' ; ' + author + ' ; ' + title

            # this adds metadata before each note.
            # out.write(comment + '\n\n')
            out.write('- ' + note + '\n')
        try:
            last_date = parse(note_date)
        except:
            pass

    out.close()

    # Update file modification time to time of last note

    if last_date.tzinfo is None or last_date.tzinfo.utcoffset(last_date) is None:
        epoch = datetime(1970, 1, 1)
    else:
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    note_timestamp = (last_date - epoch) / timedelta(seconds=1)
    os.utime(outfile, (note_timestamp, note_timestamp))
