import os, sys, json, subprocess

# Utility functions

def path_for(name):
    """Build relative paths to current script"""
    return os.path.join(os.path.dirname(sys.argv[0]),name)

def render_one(page, width, height, zoom=1):
    print locals()
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
    out_file = '../output/%s-%s.jpg' % (os.path.splitext(page)[0], resolution. lower().replace(' ',''))
    subprocess.call([
        'convert',
        '-strip',
        '-interlace', 'Plane',
        '-quality', '75',
        '-crop', 
        "%dx%d+0+0" % (config['resolutions'][resolution]['width'], config['resolutions'][resolution]['height']),
        in_file,
        os.path.abspath(path_for(out_file))
    ])
    os.unlink(in_file)
    return os.path.basename(out_file)


config = json.loads(open(path_for('../data/config.json'),'r').read())
buffer = open('README.md','r').read()


rows = ['<tr><td></td><th>' + '</th><th>'.join(config['render']) + '</th></tr>']

for p in config['pages']:
    row = ['<a href="%s">%s</a>' % (p['name'],p['name'])]
    for i in config['render']:
        render_one(
            p['name'],
            config['resolutions'][i]['width'],
            config['resolutions'][i]['height']
        )
        row.append('<img src="output/%s" style="width: 320px; height: auto;">' % compress(p['name'],i))
    rows.append('<tr><td>' + '</td><td>'.join(row) + '</td></tr>')

table = '<table>\n' + '\n'.join(rows) + '</table>'

open('../README.md','w').write(buffer % table)


