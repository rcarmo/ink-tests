#!/bin/env python
"""
Multiple resolution browser image generator

Created by: Rui Carmo
License: MIT
"""

import os, sys, json, subprocess

# Utility functions

def path_for(name):
    """Build relative paths to current script"""
    return os.path.join(os.path.dirname(sys.argv[0]),name)


def render_one(page, width, height, zoom=1):
    """Render a single resolution of a given page"""
    subprocess.call([
        os.path.abspath(path_for('webkit2png-cocoa')),
        '--width=%d' % (width * zoom),
        '--height=%d' % (height * zoom),
        '--filename=%s' % page.lower().replace(' ',''),
        '--dir=%s' % os.path.abspath(path_for('../output')),
        '--zoom=%s' % zoom,
        '-F',
        'file://' + os.path.abspath(path_for('../%s' % page))
    ])
    

def compress(page, resolution):
    """Compresses and clips the image"""
    in_file = os.path.abspath(path_for('../output/%s-full.png' % page))
    out_file = os.path.abspath(path_for('../output/%s-%s.jpg' % (os.path.splitext(page)[0], resolution. lower().replace(' ',''))))
    subprocess.call([
        'convert',
        '-strip',
        '-interlace', 'Plane',
        '-quality', '75',
        '-crop', 
        "%dx%d+0+0" % (config['resolutions'][resolution]['width'], config['resolutions'][resolution]['height']),
        in_file,
        out_file
    ])
    os.unlink(in_file)
    return os.path.basename(out_file)


# Load configuration file
config = json.loads(open(path_for('../data/config.json'),'r').read())

# Load README.md template
buffer = open('README.md','r').read()

# Add table header
rows = ['<tr><td></td><th>' + '</th><th>'.join(config['render']) + '</th></tr>']

for p in config['pages']:
    # Add link to HTML
    row = ['<a href="%s">%s</a>' % (p['name'],p['name'])]
    for i in config['render']:
        render_one(
            p['name'],
            config['resolutions'][i]['width'],
            config['resolutions'][i]['height']
        )
        # Add each image
        row.append('<img src="output/%s" style="width: 320px; height: auto;">' % compress(p['name'],i))
    # Add complete row
    rows.append('<tr><td>' + '</td><td>'.join(row) + '</td></tr>')

# Assemble table
table = '<table>\n' + '\n'.join(rows) + '</table>'

# Write new README.md
open('../README.md','w').write(buffer % table)
