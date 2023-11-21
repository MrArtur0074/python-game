import random
from collections import deque

def movePlayer(visible_zone, store):
    def is_valid_position(position):
        return 0 <= position[0] < len(visible_zone) and 0 <= position[1] < len(visible_zone[0])

    def is_passable(position):
        return visible_zone[position[0]][position[1]] != 0

    def find_fruits(visible_zone):
        fruits = []
        for i in range(len(visible_zone)):
            for j in range(len(visible_zone[0])):
                if visible_zone[i][j] == 3:
                    fruits.append((i, j))
        return fruits

    def explore_map(player_position, store, explored_edges, last_direction):
        # Реализуйте исследование всей карты
        # ...

        # Возвращаем случайное направление
        possible_directions = ['top', 'bottom', 'left', 'right']
        if store.get('prev_direction'):
            # Исключаем направление, противоположное предыдущему случайному шагу
            opposite_direction = {'top': 'bottom', 'bottom': 'top', 'left': 'right', 'right': 'left'}
            possible_directions.remove(opposite_direction[store['prev_direction']])

        # Исключаем направления, которые ведут к уже изученным краям карты
        possible_directions = [d for d in possible_directions if not is_edge_explored(player_position, d, explored_edges)]

        # Исключаем направления, которые ведут к краю карты
        possible_directions = [d for d in possible_directions if not leads_to_edge(player_position, d, last_direction)]

        if not possible_directions:
            return explore_map(player_position, store, explored_edges, last_direction)

        random_direction = random.choice(possible_directions)
        store['prev_direction'] = random_direction

        return random_direction, store

    def is_edge_explored(position, direction, explored_edges):
        next_position = get_next_position(position, direction)
        return next_position in explored_edges

    def leads_to_edge(position, direction, last_direction):
        next_position = get_next_position(position, direction)

        # Проверяем, что направление не ведет к краю карты
        if next_position[0] in {0, len(visible_zone)-1} or next_position[1] in {0, len(visible_zone[0])-1}:
            # Проверяем, что направление не в том же направлении, что и предыдущее
            return direction != last_direction

        return False

    def get_next_position(position, direction):
        if direction == 'top':
            return position[0] - 1, position[1]
        elif direction == 'bottom':
            return position[0] + 1, position[1]
        elif direction == 'left':
            return position[0], position[1] - 1
        elif direction == 'right':
            return position[0], position[1] + 1

    def get_direction(current_position, neighbor):
        if neighbor[0] < current_position[0]:
            return 'top'
        elif neighbor[0] > current_position[0]:
            return 'bottom'
        elif neighbor[1] < current_position[1]:
            return 'left'
        elif neighbor[1] > current_position[1]:
            return 'right'
        return None

    player_position = [(i, row.index(2)) for i, row in enumerate(visible_zone) if 2 in row][0]

    # Ищем фрукты вне видимой зоны
    all_fruits = find_fruits(visible_zone)
    for fruit in all_fruits:
        if abs(fruit[0] - player_position[0]) > 2 or abs(fruit[1] - player_position[1]) > 2:
            # Фрукт вне видимой зоны, исследуем всю карту
            return explore_map(player_position, store, set(), None)

    queue = deque([(player_position, [])])
    visited = set()
    explored_edges = set()
    last_direction = None

    while queue:
        current_position, path = queue.popleft()

        if visible_zone[current_position[0]][current_position[1]] == 3:
            if path:
                next_step = path[0]
                if next_step[0] < player_position[0]:
                    return 'top', store
                elif next_step[0] > player_position[0]:
                    return 'bottom', store
                elif next_step[1] < player_position[1]:
                    return 'left', store
                elif next_step[1] > player_position[1]:
                    return 'right', store

        visited.add(current_position)

        neighbors = [(current_position[0] - 1, current_position[1]),
                     (current_position[0] + 1, current_position[1]),
                     (current_position[0], current_position[1] - 1),
                     (current_position[0], current_position[1] + 1)]

        for neighbor in neighbors:
            if is_valid_position(neighbor) and is_passable(neighbor) and neighbor not in visited:
                if len(path) >= 3 and path[0] == path[2] and neighbor == path[1]:
                    continue  # Пропускаем ход, образующий круг

                queue.append((neighbor, path + [neighbor]))

                # Добавляем край карты в множество изученных краев
                if neighbor[0] in {0, len(visible_zone)-1} or neighbor[1] in {0, len(visible_zone[0])-1}:
                    explored_edges.add(neighbor)

                # Запоминаем направление
                last_direction = get_direction(current_position, neighbor)

    # Если путь не найден, возвращаем случайное направление
    return explore_map(player_position, store, explored_edges, last_direction)