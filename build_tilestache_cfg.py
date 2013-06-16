#!/usr/bin/python

# Builds a "master" tilestache.cfg from as list of subdirectories
# containing tilestache.cfg files, modifying relative paths
# in layers where necessary.

from os import path, walk
import json

allLayers = {}

def modifyPaths(relpath, layer):
  if 'provider' in layer.keys():
    if 'mapfile' in layer['provider'].keys():
      localpath = layer['provider']['mapfile'];
      if not path.isabs(localpath):
        layer['provider']['mapfile'] = path.join(relpath, localpath)

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
    
# List of source subdirs and (optional) layer prefixes
srcDirs = [
    ('osm', ''),
    ('TopOSM2/processed', 'toposm2-')
    ]

# Process each source dir
for (dirpath, prefix) in srcDirs:
  processTilestacheCfg(dirpath, prefix)

# Build new tilestache.conf - modify as needed
tsConf = {
  'cache': {'name': 'Test'},
  'layers': allLayers
}

# Format nicely and write to file
with open('tilestache.cfg', 'w') as dest:
  dest.write(json.dumps(tsConf, sort_keys=True,
    indent=2, separators=(',', ': ')))

