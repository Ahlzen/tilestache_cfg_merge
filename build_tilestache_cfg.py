#!/usr/bin/python

# Builds a "master" tilestache.cfg from as list of subdirectories
# containing tilestache.cfg files, modifying relative paths
# in layers where necessary.

from os import path, walk
import json

# List of source subdirs and (optional) layer prefixes
# Modify this list as needed:
srcDirs = [
    ('osm_massgis_tiles/server', ''),
    ('lonely_buildings', ''),
    ('TopOSM2/processed', 'toposm2-')
]

# Base structure of new tilestache.conf
# Modify as needed:
tsConf = {
  'cache': {'name': 'Test'},
  'layers': {}
}

allLayers = {}

def modifyPaths(relpath, layer):
  'Modifies the path of nodes referencing files'
  if 'provider' in layer.keys():
    if 'mapfile' in layer['provider'].keys():
      localpath = layer['provider']['mapfile'];
      if not path.isabs(localpath):
        layer['provider']['mapfile'] = path.join(relpath, localpath)

def addPrefix(prefix, parent, nodeName, nodeValue, applicableKeyNames):
  'Adds layer prefix to nodes referencing other layers'
  if isinstance(nodeValue, dict):
    for key in nodeValue.keys():
      addPrefix(prefix, nodeValue, key, \
         nodeValue[key], applicableKeyNames)     
  elif isinstance(nodeValue, list):
    for child in nodeValue:
      addPrefix(prefix, nodeValue, None, child, applicableKeyNames)
  else:
    if nodeName in applicableKeyNames:
      parent[nodeName] = prefix + nodeValue

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
    addPrefix(layerPrefix, layers, layer, layers[layer], ['src','mask'])
    if layername in allLayers.keys():
      print "Warning: Skipping duplicate layer name", layername
    else:
      allLayers[layername] = layers[layer]
    

# Process each source dir
for (dirpath, prefix) in srcDirs:
  processTilestacheCfg(dirpath, prefix)
tsConf['layers'] = allLayers

# Format nicely and write to file
with open('tilestache.cfg', 'w') as dest:
  dest.write(json.dumps(tsConf, sort_keys=True,
    indent=2, separators=(',', ': ')))

