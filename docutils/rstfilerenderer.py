#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import io
import os

from docutils.core import publish_string
from docutils.writers.html5_polyglot import Writer
#import cgi
#import cgitb; cgitb.enable()  # for troubleshooting

# print "Content-type: text/html"
# print

sys.stdin.flush()
rstfilename = sys.stdin.read()
rstfilename = os.path.abspath(rstfilename.replace('\n',''))
rst_dir = os.path.split(rstfilename)[0]
source_base_dir = '/var/www/jonglaria.org/html'
rel_path = os.path.relpath(source_base_dir, rst_dir)
stylesheet_paths = str(os.path.join(source_base_dir,'minimal.css')) + ',' + str(os.path.join(source_base_dir,'code.css'))

new_depth = rstfilename.count(os.sep)-source_base_dir.count(os.sep)

#'embed_stylesheet' : False,

overrides = {'stylesheet_path' : stylesheet_paths,
             '_disable_config': True,
             'title' : 'Jonglaria e.V.',
             'syntax_highlight': 'short',
             'math_output': 'MathML',
             'generator' : None}



rstfile = io.open(rstfilename, mode='r', encoding='utf-8')

rstinput = rstfile.read()

# Add this to get text scale better on mobile devices:
rstinput += """


.. meta::
   :viewport: width=device-width, initial-scale=1.0
"""

rstfile.close()


#rst_conversion = publish_string(rstinput, source_path=rstfilename, writer=Writer(), settings=None, settings_overrides=overrides)
rst_conversion = publish_string(rstinput, writer=Writer(), settings=None, settings_overrides=overrides)

# raise Exception(type(rst_conversion.decode("utf-8")))

print(rst_conversion.decode("utf-8").replace("""</li>
<li>""","</li><li>"))

sys.stdout.flush()

