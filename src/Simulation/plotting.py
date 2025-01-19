import numpy as np
import os
import matplotlib.pyplot as plt

def plotting_mesh(cells: list[object], dt: float, cells_in_area: list[object], images_folder: str):
    """
    plots a mesh representing the oil distrobution at a spesific time and saves the plot as an image file
    """
    # defines size and makes an empty numpy array
    plt.figure()
    h = 1000
    w = 1000
    image = np.zeros((h, w, 3), np.uint8)
    # retrieves the oil amount from each cell object
    oil_values = [cell.oil_amount for cell in cells]
    # finds max/min values of all oil amounts
    max_oil = max(oil_values)
    min_oil = min(oil_values)
    # maps oil amounts to colors using viridis colormap and normalized
    sm = plt.cm.ScalarMappable(
        cmap="viridis", norm=plt.Normalize(vmin=min_oil, vmax=max_oil)
    )
    # oil amount as the data for the colormap
    sm.set_array(oil_values)

    # creates a colorbar
    cbar_ax = plt.gca().inset_axes([1.05, 0.1, 0.05, 0.8])
    plt.colorbar(sm, cax=cbar_ax, label="Oil Amount")

    for cell in cells:
        coords = [point.coordinates for point in cell.points]
        coords = np.array(coords)

        # maps the oil_amoount to a color in the colormap
        color = plt.cm.viridis((cell.oil_amount - min_oil) / (max_oil - min_oil))
        # adds the cell to the plot with the color determined by the oil amount
        plt.gca().add_patch(plt.Polygon(coords, color=color, alpha=0.9))

    for cell in cells_in_area:
        coords = np.array([point.coordinates for point in cell.points])
        plt.gca().add_patch(plt.Polygon(coords, color="cyan", alpha=0.4))

    plt.title("Mesh Plot")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.gca().set_aspect("equal")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    filename = os.path.join(images_folder, f"mesh_plot{dt}.png")
    plt.savefig(filename)
    #plt.show()
    
