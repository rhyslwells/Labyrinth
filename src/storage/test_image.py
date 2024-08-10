import numpy as np
from PIL import Image

def test_save_to_image(filename):
    width, height = 10, 10
    color_map = {
        '.': (255, 255, 255),  # White
        '#': (0, 0, 0),        # Black
        'X': (255, 0, 0),      # Red
        'O': (0, 255, 0)       # Green
    }
    
    # Create a grid with various patterns
    grid = np.full((height, width), '.', dtype=str)
    
    # Add black borders
    grid[0, :] = '#'
    grid[-1, :] = '#'
    grid[:, 0] = '#'
    grid[:, -1] = '#'
    
    # Add a diagonal red line
    for i in range(1, height-1):
        grid[i, i] = 'X'
    
    # Add a green square in the center
    for i in range(4, 6):
        for j in range(4, 6):
            grid[i, j] = 'O'
    
    cell_size = 20  # Size of each cell in pixels
    
    # Create an empty image array
    image_data = np.zeros((height * cell_size, width * cell_size, 3), dtype=np.uint8)
    
    # Fill the image array based on the grid
    for y in range(height):
        for x in range(width):
            color = color_map.get(grid[y, x], (255, 255, 255))  # Default to white if color not found
            image_data[y * cell_size:(y + 1) * cell_size, x * cell_size:(x + 1) * cell_size] = color
    
    # Convert the image array to an image object
    img = Image.fromarray(image_data)
    
    # Save the image
    img.save(filename)
    print(f"Saved image to {filename}")

# Test the function
test_save_to_image("test_image.png")
