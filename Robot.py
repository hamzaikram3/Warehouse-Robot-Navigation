import heapq

# Directions for moving in the grid (Up, Down, Left, Right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def manhattan_distance(start, end):
    """Calculate the Manhattan distance heuristic"""
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def a_star(grid, start, end):
    """Implement A* algorithm to find the shortest path from start to end"""
    
    # Priority queue for open set (nodes to be evaluated)
    open_set = []
    heapq.heappush(open_set, (0, start))  # (f_score, current_position)
    
    # Dictionaries for parent and scores
    came_from = {}
    g_score = {start: 0}  # Cost from start to the current node
    f_score = {start: manhattan_distance(start, end)}  # Estimated total cost
    
    while open_set:
        current_f_score, current = heapq.heappop(open_set)

        if current == end:
            # Reconstruct the path from end to start
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        for direction in DIRECTIONS:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            # Check if the neighbor is within bounds and not an obstacle
            if (0 <= neighbor[0] < len(grid)) and (0 <= neighbor[1] < len(grid[0])) and grid[neighbor[0]][neighbor[1]] != 1:
                tentative_g_score = g_score[current] + 1  # Every step has a cost of 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None  # No path found

def print_grid(grid, path=None):
    """Print the grid with the robot's path"""
    for i in range(len(grid)):
        row = ""
        for j in range(len(grid[i])):
            if (i, j) in path:
                row += "R "  # R for robot's path
            elif grid[i][j] == 1:
                row += "# "  # # for obstacles
            else:
                row += ". "  # . for empty space
        print(row)

def get_grid_input():
    """Get the grid input from the user"""
    while True:
        try:
            # Get grid dimensions
            rows = int(input("Enter the number of rows in the grid: "))
            cols = int(input("Enter the number of columns in the grid: "))
            
            grid = []
            print("Enter the grid row by row (use 0 for empty space and 1 for obstacle):")
            
            # Get grid values from the user
            for i in range(rows):
                while True:
                    row = input(f"Enter row {i + 1} values (0 or 1, space-separated): ").split()
                    if len(row) == cols and all(val in ['0', '1'] for val in row):
                        grid.append([int(val) for val in row])
                        break
                    else:
                        print("Invalid row input. Please enter 0s and 1s only.")
            
            return grid, (0, 0), (rows - 1, cols - 1)  # Start at top-left and end at bottom-right
        
        except ValueError:
            print("Please enter valid integers for rows and columns.")

# Get the grid from the user
grid, start, end = get_grid_input()

# Find the shortest path using A* algorithm
path = a_star(grid, start, end)

# Print the results
if path:
    print("\nPath found:")
    print(path)
    print("\nGrid with robot's path:")
    print_grid(grid, path)
else:
    print("\nNo path found!")
