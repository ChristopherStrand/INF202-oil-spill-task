import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv


def plotting_mesh(cells):
    plt.figure()
    h = 1000
    w = 1000
    image = np.zeros((h, w, 3), np.uint8)
    oil_values = [cell.oil_amount for cell in cells]
    max_oil = max(oil_values)
    min_oil = min(oil_values)
    sm = plt.cm.ScalarMappable(
        cmap="viridis", norm=plt.Normalize(vmin=min_oil, vmax=max_oil)
    )
    sm.set_array(oil_values)

    cbar_ax = plt.gca().inset_axes([1.05, 0.1, 0.05, 0.8])
    plt.colorbar(sm, cax=cbar_ax, label="Oil Amount")

    for cell in cells:
        coords = []
        for point in cell.points:
            coords.append(point.coordinates)
        coords = np.array(coords)

        color = plt.cm.viridis((cell.oil_amount - min_oil) / (max_oil - min_oil))
        plt.gca().add_patch(plt.Polygon(coords, color=color, alpha=0.9))

    plt.title("Mesh Plot")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.gca().set_aspect("equal")
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    plt.savefig("mesh_plot.png")
    plt.show()
