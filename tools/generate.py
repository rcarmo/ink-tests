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
    subprocess.call([
        'convert',
        '-strip',
        '-interlace', 'Plane',
        '-quality', '75',
        '-crop', 
        "%dx%d+0+0" % (config['resolutions'][resolution]['width'],  config['resolutions'][resolution]['height']),
        os.path.abspath(path_for('../output/%s-full.png' % page)),
        os.path.abspath(path_for('../output/%s.jpg' % resolution.lower().replace(' ','')))
    ])
    os.unlink(os.path.abspath(path_for('../output/%s-full.png' % page)))


config = json.loads(open(path_for('../data/config.json'),'r').read())

for p in config['pages']:
    for i in config['render']:
        render_one(
            p['name'],
            config['resolutions'][i]['width'],
            config['resolutions'][i]['height']
        )
        compress(p['name'],i)


    print p

