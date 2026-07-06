"""Render the readme preview image (offscreen, no viewer needed).

    uv run python docs/render_preview.py          # writes docs/hood_preview.png

Tessellates the assembly and renders it shaded with VTK (already present via
cadquery), using the part colours from `hood.geometry.COLORS`. Depth peeling
keeps the translucent walls/plenum looking right.
"""

from __future__ import annotations

import sys
from pathlib import Path

import vtk
from PIL import Image, ImageChops

sys.path.insert(0, str(Path(__file__).parents[1]))  # repo root, for `hood`

from hood.assembly import build_hood

OUT = Path(__file__).parent / "hood_preview.png"
W, H = 1600, 1100


def actor_for(shape) -> vtk.vtkActor:
    verts, tris = shape.tessellate(0.5)
    pts = vtk.vtkPoints()
    for v in verts:
        pts.InsertNextPoint(v.X, v.Y, v.Z)
    cells = vtk.vtkCellArray()
    for t in tris:
        cells.InsertNextCell(3, t)
    poly = vtk.vtkPolyData()
    poly.SetPoints(pts)
    poly.SetPolys(cells)

    normals = vtk.vtkPolyDataNormals()
    normals.SetInputData(poly)
    normals.SetFeatureAngle(35)
    normals.SplittingOn()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(normals.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    r, g, b, a = tuple(shape.color) if shape.color else (0.7, 0.7, 0.7, 1.0)
    prop = actor.GetProperty()
    prop.SetColor(r, g, b)
    prop.SetOpacity(a)
    prop.SetSpecular(0.3)
    prop.SetSpecularPower(20)
    prop.SetDiffuse(0.85)
    prop.SetAmbient(0.25)
    return actor


def autocrop(path: Path, pad: int = 40) -> Image.Image:
    img = Image.open(path).convert("RGB")
    bg = Image.new("RGB", img.size, (255, 255, 255))
    bbox = ImageChops.difference(img, bg).getbbox()
    if bbox:
        l, t, r, b = bbox
        img = img.crop((max(l - pad, 0), max(t - pad, 0),
                        min(r + pad, img.width), min(b + pad, img.height)))
    return img


def main() -> None:
    hood = build_hood()

    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)
    ren.SetUseDepthPeeling(True)
    ren.SetMaximumNumberOfPeels(50)
    ren.SetOcclusionRatio(0.05)
    for leaf in hood.leaves:
        ren.AddActor(actor_for(leaf))

    win = vtk.vtkRenderWindow()
    win.SetOffScreenRendering(1)
    win.SetAlphaBitPlanes(1)
    win.SetMultiSamples(0)
    win.SetSize(W, H)
    win.AddRenderer(ren)

    # Above front-right, angled so the filter/plenum/blower stack at the back
    # stays visible past the frame.
    c = hood.bounding_box().center()
    cam = ren.GetActiveCamera()
    cam.SetFocalPoint(c.X, c.Y, c.Z)
    cam.SetPosition(c.X + 1600, c.Y - 1000, c.Z + 750)
    cam.SetViewUp(0, 0, 1)
    ren.ResetCamera()

    win.Render()
    grab = vtk.vtkWindowToImageFilter()
    grab.SetInput(win)
    grab.SetInputBufferTypeToRGB()
    grab.Update()
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(str(OUT))
    writer.SetInputConnection(grab.GetOutputPort())
    writer.Write()

    img = autocrop(OUT)
    img.save(OUT)
    print(f"wrote {OUT} ({img.width}x{img.height})")


if __name__ == "__main__":
    main()
