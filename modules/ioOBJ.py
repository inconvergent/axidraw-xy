# -*- coding: utf-8 -*-

def load_2d(fn):
  from codecs import open
  from numpy import row_stack

  vertices = []
  edges = []
  faces = []
  lines = []

  with open(fn, 'r', encoding='utf8') as f:
    for l in f:
      if l.startswith('#'):
        continue

      values = l.split()
      if not values:
        continue
      if values[0] == 'v':
        vertices.append([float(v) for v in values[1:]])

      if values[0] == 'e':
        edge = [int(v.split('//')[0])-1 for v in values[1:]]
        edges.append(edge)

      if values[0] == 'f':
        face = [int(v.split('//')[0])-1 for v in values[1:]]
        faces.append(face)

      if values[0] == 'l':
        line = [int(v.split('//')[0])-1 for v in values[1:]]
        lines.append(line)

  try:
    edges = row_stack(edges)
  except ValueError:
    edges = None

  try:
    faces = row_stack(faces)
  except ValueError:
    faces = None

  try:
    vertices = row_stack(vertices)
  except ValueError:
    vertices = None

  return {
      'edges': edges,
      'faces': faces,
      'vertices': vertices,
      'lines': lines
      }

