# Axidraw XY

Runs the EMSL Axidraw via the cncserver API

http://axidraw.com/

https://github.com/techninja/cncserver

## Requires

  - numpy
  - scipy

## Example

Sample data can be found in `data/`. So you can try running

    ./draw_tris.py --fn ./data/triangles.2obj

To plot some triangles from the simple vector format that I use for my
algorithms. Or similarly

    ./draw_lines.py --fn ./data/line.2obj

I've named the vector format .2obj, and it is more or less a 2d version of the
.obj format. Note that this code is mostly written to run with these vector
files, but you should be able to use this for whatever purpose you have in
mind. For a simple example see `./draw_test.py`.

