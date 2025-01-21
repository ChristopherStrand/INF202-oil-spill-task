import cairo
import numpy as np
import matplotlib.pyplot as plt
import os


def plotting_mesh(cells, dt, cells_in_area, images_folder):
    """
    Efficiently plots a mesh using Cairo for 2D rendering.
    """
    width, height = 1024, 1024
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)

    # Skaler koordinater
    context.scale(width, -height)
    context.translate(0, -1)

    # Forbered fargemapping
    oil_values = np.array([cell.oil_amount for cell in cells])
    max_oil, min_oil = oil_values.max(), oil_values.min()

    def map_color(value):
        norm = (value - min_oil) / (max_oil - min_oil)
        return plt.cm.viridis(norm)[:3]  # RGB (0-1)

    # Tegn cellene
    for cell in cells:
        coords = np.array(cell.coordinates)
        context.move_to(coords[0][0], coords[0][1])
        for x, y in coords[1:]:
            context.line_to(x, y)
        context.close_path()

        # Sett farge og fyll polygon
        color = map_color(cell.oil_amount)
        context.set_source_rgb(*color)
        context.fill()

        # Marker fiskeområder
        if cell in cells_in_area:
            context.set_source_rgb(0, 1, 1)  # Cyan
            context.set_line_width(0.005)
            context.stroke()

    # Lagre plottet
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    filename = os.path.join(images_folder, f"mesh_plot_{dt:.2f}.png")
    surface.write_to_png(filename)
    print(f"Plott lagret til: {filename}")
