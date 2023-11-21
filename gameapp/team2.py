import random

def movePlayer(game_map, store):
    def find_player(game_map):
        for i, row in enumerate(game_map):
            for j, cell in enumerate(row):
                if cell == 2:
                    return i, j

    player_position = find_player(game_map)

    # Check for available food at the player's position
    if game_map[player_position[0]][player_position[1]] == 3:
        game_map[player_position[0]][player_position[1]] = 1  # Set the space to free

    # Check for available food within a radius of 2 cells
    for i in range(max(0, player_position[0] - 2), min(len(game_map), player_position[0] + 3)):
        for j in range(max(0, player_position[1] - 2), min(len(game_map[0]), player_position[1] + 3)):
            if game_map[i][j] == 3:
                # Move towards the visible food
                if i < player_position[0]:
                    return 'top', store
                elif i > player_position[0]:
                    return 'bottom', store
                elif j < player_position[1]:
                    return 'left', store
                elif j > player_position[1]:
                    return 'right', store

    # Randomly select a direction if no visible food
    directions = ['top', 'bottom', 'left', 'right']
    side = random.choice(directions)

    # Update the store for future calls
    store['previous_direction'] = side

    # Check for obstacles in the chosen direction
    if side == 'top' and game_map[player_position[0] - 1][player_position[1]] != 0:
        return side, store
    elif side == 'bottom' and game_map[player_position[0] + 1][player_position[1]] != 0:
        return side, store
    elif side == 'left' and game_map[player_position[0]][player_position[1] - 1] != 0:
        return side, store
    elif side == 'right' and game_map[player_position[0]][player_position[1] + 1] != 0:
        return side, store
    else:
        # Choose a different direction if the chosen one has an obstacle
        return random.choice([d for d in directions if d != side]), store
