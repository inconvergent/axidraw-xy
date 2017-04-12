# -*- coding: utf-8 -*-

from numpy import array
from numpy import row_stack

def get_bounding_box(xy):
  mi = xy.min(axis=0).squeeze()
  ma = xy.max(axis=0).squeeze()
  xd = ma[0]-mi[0]
  yd = ma[1]-mi[1]
  return mi, ma, xd, yd

def print_values(mi, ma, xd, yd):
  print(('x: min {:0.08f} max {:0.08f} d {:0.08f}'.format(mi[0], ma[0], xd)))
  print(('y: min {:0.08f} max {:0.08f} d {:0.08f}'.format(mi[1], ma[1], yd)))

def do_scale(xy):
  _, _, xd, yd = get_bounding_box(xy)
  xy /= max(xd, yd)

def fit(vertices):
  from modules.ddd import get_mid_2d as get_mid
  vertices -= get_mid(vertices)
  do_scale(vertices)
  vertices[:, :] += array([[0.5]*2])

def get_paths_from_n_files(
    pattern,
    skip=0,
    steps=1,
    stride=1,
    spatial_sort=True,
    spatial_concat=False,
    spatial_concat_eps=1.e-9
    ):
  from glob import glob
  from modules.ioOBJ import load_2d as load
  from modules.ddd import spatial_sort_2d as sort
  from modules.ddd import spatial_concat_2d as concat

  vertices = []
  lines = []
  vnum = 0

  files = sorted(glob(pattern))

  for fn in files[skip:steps:stride]:
    print(fn)
    data = load(fn)
    v = data['vertices']
    l = data['lines']
    vn = len(v)
    vertices.append(v)
    lines.append(array(l, 'int')+vnum)
    vnum += vn

  vertices = row_stack(vertices)

  fit(vertices)
  print('scaled size:')
  print_values(*get_bounding_box(vertices))

  paths = [row_stack(vertices[li, :]) for li in lines]

  paths = sort(paths) if spatial_sort else paths
  paths = concat(paths, spatial_concat_eps) if spatial_concat else paths

  return paths

def get_paths_from_file(
    fn,
    spatial_sort=True,
    spatial_concat=False,
    spatial_concat_eps=1.e-9
    ):
  from modules.ioOBJ import load_2d as load
  from modules.ddd import spatial_sort_2d as sort
  from modules.ddd import spatial_concat_2d as concat

  data = load(fn)
  vertices = data['vertices']
  lines = data['lines']

  fit(vertices)
  print('scaled size:')
  print_values(*get_bounding_box(vertices))

  paths = [row_stack(vertices[l, :]) for l in lines]

  paths = sort(paths) if spatial_sort else paths
  paths = concat(paths, spatial_concat_eps) if spatial_concat else paths
  return paths

def get_tris_from_file(
    fn,
    spatial_sort=True,
    spatial_concat=False,
    spatial_concat_eps=1.0e-9
    ):
  from modules.ioOBJ import load_2d as load
  from modules.ddd import get_distinct_edges_from_tris
  from modules.ddd import spatial_sort_2d as sort
  from modules.ddd import spatial_concat_2d as concat

  data = load(fn)
  vertices = data['vertices']

  fit(vertices)
  print('scaled size:')
  print_values(*get_bounding_box(vertices))

  edges = get_distinct_edges_from_tris(data['faces'])
  paths = [row_stack(p) for p in vertices[edges, :]]

  paths = sort(paths) if spatial_sort else paths
  paths = concat(paths, spatial_concat_eps) if spatial_concat else paths
  return paths

def get_dots_from_file(
    fn,
    spatial_sort=True,
    ):
  from modules.ioOBJ import load_2d as load
  from modules.ddd import spatial_sort_dots_2d as sort

  data = load(fn)
  vertices = data['vertices']

  fit(vertices)
  dots = vertices
  print('scaled size:')
  print_values(*get_bounding_box(vertices))

  dots = sort(dots) if spatial_sort else dots
  return dots

def get_edges_from_file(
    fn,
    spatial_sort=True,
    spatial_concat=False,
    spatial_concat_eps=1.0e-9
    ):
  from modules.ioOBJ import load_2d as load
  from modules.ddd import spatial_sort_2d as sort
  from modules.ddd import spatial_concat_2d as concat

  data = load(fn)
  vertices = data['vertices']

  fit(vertices)
  print('scaled size:')
  print_values(*get_bounding_box(vertices))

  edges = data['edges']
  paths = [row_stack(p) for p in vertices[edges, :]]

  paths = sort(paths) if spatial_sort else paths
  paths = concat(paths, spatial_concat_eps) if spatial_concat else paths
  print('edges: ', len(paths))
  return paths

