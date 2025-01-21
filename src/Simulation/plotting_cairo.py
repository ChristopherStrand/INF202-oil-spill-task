import cairo
import numpy as np
import os
import matplotlib.pyplot as plt


def plotting_mesh(cells, dt, cells_in_area, images_folder):
    """
    Plots a mesh using Cairo for effecient plotting of large meshes.
    """
    width = 1424
    height = 1024
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)

    # defining the plot size and margins from  total size
    plot_margin = 0.05
    colorbar_width = 0.1 * width
    plot_width = width * (1 - 3 * plot_margin) - colorbar_width
    plot_height = height * (1 - 2 * plot_margin)
    plot_x = width * plot_margin
    plot_y = height * plot_margin

    # adding a background color
    context.set_source_rgb(255, 255, 255)
    context.rectangle(0, 0, width, height)
    context.fill()

    # added a black frame around plot
    context.set_source_rgb(0, 0, 0)
    context.set_line_width(2)
    context.rectangle(plot_x, plot_y, plot_width, plot_height)
    context.stroke()

    # Define a function to map oil amount to color
    def map_color(value):
        norm = min(max(value, 0), 1)
        return plt.cm.viridis(norm)[:3]

    # looping over all cells and plotting them in the plot area
    for cell in cells:
        coords = np.array(cell.coordinates)
        corrected_coords = [
            (
                plot_x + x * plot_width,
                plot_y + (1 - y) * plot_height,
            )
            for x, y in coords
        ]

        # goes through the coordinates and draws the cell
        context.move_to(corrected_coords[0][0], corrected_coords[0][1])
        for x, y in corrected_coords[1:]:
            context.line_to(x, y)
        context.close_path()

        # then fills the cells with the color based on the oil amount/colormap (viridis)
        color = map_color(cell.oil_amount)
        context.set_source_rgb(*color)
        context.fill()

        # if cell in fish areas, draw a black border around the cell
        if cell in cells_in_area:
            context.set_source_rgb(102, 178, 255)
            context.fill()

    # defining size for colorbar
    colorbar_x_start = plot_x + plot_width + 20
    colorbar_y_start = plot_y
    colorbar_height = plot_height

    # drawing the colorbar
    for i, value in enumerate(np.linspace(0, 1, 100)):
        color = map_color(value)
        y_start = colorbar_y_start + (99 - i) * (colorbar_height / 100)
        y_end = colorbar_y_start + (100 - i) * (colorbar_height / 100)

        context.set_source_rgb(*color)
        context.rectangle(colorbar_x_start, y_start, colorbar_width, y_end - y_start)
        context.fill()

    # drawing the colorbar labels
    context.set_source_rgb(0, 0, 0)
    context.set_font_size(15)
    for i, tick in enumerate(np.linspace(0, 1, 11)):
        label_y = colorbar_y_start + colorbar_height - i * (colorbar_height / 10)
        context.move_to(colorbar_x_start + colorbar_width + 10, label_y)
        context.show_text(f"{tick:.1f}")

    # saving the plot to a file
    filename = os.path.join(images_folder, f"mesh_plot{dt}.png")
    surface.write_to_png(filename)
