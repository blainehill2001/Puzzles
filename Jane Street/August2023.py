import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def plot_cube(ax, position):
    # Define the vertices of the unit cube
    vertices = [
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1],
    ]

    # Translate the cube to the specified position
    translated_vertices = [
        [v[0] + position[0], v[1] + position[1], v[2] + position[2]]
        for v in vertices
    ]

    # Define the faces of the unit cube using the vertices
    faces = [
        [
            translated_vertices[0],
            translated_vertices[1],
            translated_vertices[2],
            translated_vertices[3],
        ],
        [
            translated_vertices[4],
            translated_vertices[5],
            translated_vertices[6],
            translated_vertices[7],
        ],
        [
            translated_vertices[0],
            translated_vertices[1],
            translated_vertices[5],
            translated_vertices[4],
        ],
        [
            translated_vertices[2],
            translated_vertices[3],
            translated_vertices[7],
            translated_vertices[6],
        ],
        [
            translated_vertices[0],
            translated_vertices[3],
            translated_vertices[7],
            translated_vertices[4],
        ],
        [
            translated_vertices[1],
            translated_vertices[2],
            translated_vertices[6],
            translated_vertices[5],
        ],
    ]

    # Plot the cube
    ax.add_collection3d(
        Poly3DCollection(faces, linewidths=1, edgecolors="k", alpha=0.1)
    )


def main():
    # Create a 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Create the big cube by arranging the unit cubes
    for x in range(3):
        for y in range(3):
            for z in range(3):
                plot_cube(ax, position=(x, y, z))

    # Set axis labels and limits
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xlim([0, 3])
    ax.set_ylim([0, 3])
    ax.set_zlim([0, 3])

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()
