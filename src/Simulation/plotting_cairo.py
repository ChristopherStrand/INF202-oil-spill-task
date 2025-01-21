import cairo
import numpy as np
import os
import matplotlib.pyplot as plt  # For viridis colormap


def plotting_mesh(cells, dt, cells_in_area, images_folder):
    """
    Plots a mesh using Cairo, with a fixed colorbar from 0 to 1 and numeric labels.
    """
    width = 1324
    height = 1024
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)

    plot_margin = 0.05  # Margin rundt plottet (5% av canvas)
    colorbar_width = 0.1 * width  # Bredde på fargekartet (10% av canvas)
    plot_width = width * (1 - 3 * plot_margin) - colorbar_width
    plot_height = height * (1 - 2 * plot_margin)
    plot_x_start = width * plot_margin
    plot_y_start = height * plot_margin

    # Tegn bakgrunn for hele canvas
    context.set_source_rgb(0.9, 0.9, 0.9)  # Lys grå bakgrunn
    context.rectangle(0, 0, width, height)
    context.fill()

    # Tegn ramme rundt plottet
    context.set_source_rgb(0, 0, 0)  # Svart farge
    context.set_line_width(2)
    context.rectangle(plot_x_start, plot_y_start, plot_width, plot_height)
    context.stroke()

    # Skaler cellene for å passe i plottområdet
    def map_color(value):
        # Normaliser verdien til området [0, 1]
        norm = min(max(value, 0), 1)  # Sørg for at verdien alltid er i [0, 1]
        return plt.cm.viridis(norm)[:3]

    for cell in cells:
        coords = np.array(cell.coordinates)
        scaled_coords = [
            (
                plot_x_start + x * plot_width,
                plot_y_start + (1 - y) * plot_height,
            )
            for x, y in coords
        ]

        # Tegn cellen
        context.move_to(scaled_coords[0][0], scaled_coords[0][1])
        for x, y in scaled_coords[1:]:
            context.line_to(x, y)
        context.close_path()

        color = map_color(cell.oil_amount)
        context.set_source_rgb(*color)
        context.fill()

        # Marker celler i fiskeområdet
        if cell in cells_in_area:
            context.set_line_width(1)
            context.stroke()

    # Tegn fargekart (colorbar) på høyre side
    colorbar_x_start = plot_x_start + plot_width + 20
    colorbar_y_start = plot_y_start
    colorbar_height = plot_height

    for i, value in enumerate(np.linspace(0, 1, 100)):
        color = map_color(value)
        y_start = colorbar_y_start + (99 - i) * (colorbar_height / 100)  # Reversert
        y_end = colorbar_y_start + (100 - i) * (colorbar_height / 100)

        context.set_source_rgb(*color)
        context.rectangle(colorbar_x_start, y_start, colorbar_width, y_end - y_start)
        context.fill()

    # Legg til etiketter på fargekartet
    context.set_source_rgb(0, 0, 0)  # Svart tekstfarge
    context.set_font_size(15)

    # Fargekartverdier
    for i, tick in enumerate(np.linspace(0, 1, 11)):  # 0 til 1 med 10 steg
        label_y = colorbar_y_start + colorbar_height - i * (colorbar_height / 10)
        context.move_to(colorbar_x_start + colorbar_width + 10, label_y)
        context.show_text(f"{tick:.1f}")

    # Lagre plottet som PNG
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    filename = os.path.join(images_folder, f"mesh_plot_{dt}.png")
    surface.write_to_png(filename)
    print(f"Plott lagret til: {filename}")
