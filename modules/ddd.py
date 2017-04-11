# -*- coding: utf-8 -*-


def get_mid_2d(v):
  from numpy import array

  mi = v.min(axis=0).squeeze()
  ma = v.max(axis=0).squeeze()
  midx = mi[0]+ma[0]
  midy = mi[1]+ma[1]
  move = array([[midx, midy]])*0.5
  return move

def order_edges(edges):
  ev_dict = {}
  ve_dict = {}
  e_visited = {}
  v_ordered = []
  e_order = []

  for e, (v1, v2) in enumerate(edges):
    ev_dict[e] = [v1, v2]

    if v1 in ve_dict:
      ve_dict[v1].append(e)
    else:
      ve_dict[v1] = [e]

    if v2 in ve_dict:
      ve_dict[v2].append(e)
    else:
      ve_dict[v2] = [e]

  e_start = 0
  for v, ee in ve_dict.items():
    if len(ee) < 2:
      e_start = ee[0]
      break

  e_visited[e_start] = True

  vcurr = ev_dict[e_start][1]
  vend = ev_dict[e_start][0]

  v_ordered.append(vend)
  v_ordered.append(vcurr)
  e_order.append(e_start)

  while vend != vcurr:
    try:
      if ve_dict[vcurr][0] in e_visited:
        e = ve_dict[vcurr][1]
      else:
        e = ve_dict[vcurr][0]

      e_visited[e] = True
      e_order.append(e)

      v1, v2 = ev_dict[e]

      if v1 == vcurr:
        vcurr = v2
      else:
        vcurr = v1

      v_ordered.append(vcurr)

    except Exception as e:
      break

  return e_order, v_ordered

def get_distinct_edges_from_tris(faces):
  hit_edges = set()
  edges = []

  hn = 0
  en = 0

  for v1, v2, v3 in faces:
    for e in [
        tuple(sorted([v1, v2])),
        tuple(sorted([v2, v3])),
        tuple(sorted([v3, v1]))
        ]:

      if e not in hit_edges:

        edges.append(e)
        hit_edges.add(e)
        en += 1

      else:
        hn += 1

  print('final edges', en)
  print('duplicates ignored', hn)

  return edges

def spatial_concat_2d(paths, eps=1.e-9):
  from numpy.linalg import norm
  from numpy import row_stack

  res = []
  curr = paths[0]
  concats = 0
  for p in paths[1:]:
    if p.shape[0] < 2:
      print('WARNING: path with only one vertex.')
      continue
    if norm(p[0, :]-curr[-1, :]) < eps:
      curr = row_stack([curr, p[1:, :]])
      concats += 1
    else:
      res.append(curr)
      curr = p

  res.append(curr)

  print('concats: ', concats)
  print('original paths: ', len(paths))
  print('number after concatination: ', len(res))

  print()

  return res

def spatial_sort_2d(paths, init_rad=0.01):
  from numpy import array
  from numpy import zeros
  from numpy.linalg import norm
  from scipy.spatial import cKDTree as kdt

  num = len(paths)

  res = []

  unsorted = set(range(2*num))

  xs = zeros((2*num, 2), 'float')
  x_path = zeros(2*num, 'int')

  for i, path in enumerate(paths):
    xs[i, :] = path[0, :]
    xs[num+i, :] = path[-1, :]

    x_path[i] = i
    x_path[num+i] = i

  tree = kdt(xs)

  count = 0
  pos = array([0, 0], 'float')

  while count < num:

    rad = init_rad
    while True:

      near = tree.query_ball_point(pos, rad)
      cands = list(set(near).intersection(unsorted))
      if not cands:
        rad *= 2.0
        continue

      dst = norm(pos - xs[cands, :], axis=1)
      cp = dst.argmin()
      uns = cands[cp]
      break

    path_ind = x_path[uns]
    path = paths[path_ind]

    if uns >= num:
      res.append(path[::-1])
      pos = paths[path_ind][0, :]
      unsorted.remove(uns)
      unsorted.remove(uns-num)

    else:
      res.append(path)
      pos = paths[path_ind][-1, :]
      unsorted.remove(uns)
      unsorted.remove(uns+num)

    count += 1

  return res

def spatial_sort_dots_2d(vertices, init_rad=0.01):
  from numpy import array
  from numpy import arange
  from numpy.linalg import norm
  from scipy.spatial import cKDTree as kdt

  num = len(vertices)

  res = []

  unsorted = set(arange(num).astype('int'))

  tree = kdt(vertices)

  count = 0
  pos = array([0, 0], 'float')

  while count < num:

    rad = init_rad
    while True:

      near = tree.query_ball_point(pos, rad)
      cands = list(set(near).intersection(unsorted))
      if not cands:
        rad *= 2.0
        continue

      dst = norm(pos - vertices[cands, :], axis=1)
      cp = dst.argmin()
      uns = cands[cp]
      break

    path = vertices[uns]

    res.append(path)
    pos = vertices[uns, :]
    unsorted.remove(uns)

    count += 1
  return res

