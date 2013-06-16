#!/usr/bin/python

# Builds a "master" tilestache.cfg from as list of subdirectories
# containing tilestache.cfg files.

from os import path, walk
import json

allLayers = {}

def modifyPaths(relpath, layer):
  # fix layer->provider->mapfile
  if 'provider' in layer.keys():
    if 'mapfile' in layer['provider'].keys():
      localpath = layer['provider']['mapfile'];
      if not path.isabs(localpath):
        layer['provider']['mapfile'] = path.join(relpath, localpath)
  # fix layer->

def processTilestacheCfg(relpath, layerPrefix = ''):
  filename = path.join(relpath, 'tilestache.cfg')
  if not path.isfile(filename):
    print "Warning: tilestache.cfg not found in", relpath
    return;
  print "Processing", filename, 'layers:'
  with open(filename, 'r') as file:
    j = json.load(file)
  layers = j['layers']
  for layer in layers.keys():
    layername = layerPrefix + layer
    print "  " + layername
    modifyPaths(relpath, layers[layer])
    if layername in allLayers.keys():
      print "Warning: Skipping duplicate layer name", layername
    else:
      allLayers[layername] = layers[layer]
    
#def process(relPath):
  

#with open('tilestache.cft','r') as infile:
#  srctext = infile.read()
#  data = json.load(srctext)
#  layers = data['layers']  

# List of source subdirs and (optional) layer prefixes
srcDirs = [
    ('osm', ''),
    ('TopOSM2/processed', 'toposm2-')
    ]

#for (pathname, dirnames, filenames) in walk('.', True, None, True):
#  if pathname == '.': continue
#  if 'tilestache.cfg' in filenames:
#    processTilestacheCfg(pathname)

# Process each source dir
for (dirpath, prefix) in srcDirs:
  processTilestacheCfg(dirpath, prefix)

# Build new tilestache.conf
tsConf = {
  'cache': {'name': 'Test'},
  'layers': allLayers
}

# Format nicely and write to file
with open('tilestache.cfg', 'w') as dest:
  dest.write(json.dumps(tsConf, sort_keys=True,
    indent=2, separators=(',', ': ')))

#processTilestacheCfg('TopOSM2/processed')

