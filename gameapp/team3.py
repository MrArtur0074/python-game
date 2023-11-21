def movePlayer(map, store):

    def player_location(map, player_symbol):
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == player_symbol:
                    map[i][j] = -1
                    return [i, j]

    def move(map, log, location):
        dirs = [[-1, 0], [0, 1], [0, -1], [1, 0]]
        dir_names = ['top', 'right', 'left', 'bottom']

        y = location[0]
        x = location[1]

        map[y][x] = -1

        cross_road = []
        for i in dirs:
            try:
                if map[y + i[0]][x + i[1]] > 0:
                    cross_road.append(i)
            except:
                continue

        dir_index = 0
        if len(cross_road) == 0:
            dir_index = 3 - dir_names.index(log[-1])
            log.pop()
        else:
            dir_index = dirs.index(cross_road[0])
            log.append(dir_names[dir_index])

        location[0] = y + dirs[dir_index][0]
        location[1] = x + dirs[dir_index][1]

        return dir_names[dir_index]

    def expand_map(map, location, in_map, in_location, dir):
        if not map:
            return in_map.copy(), in_location.copy()

        map_size = [len(map), len(map[0])]
        in_map_size = [len(in_map), len(in_map[0])]

        empty = -2

        if dir == 'bottom':
            origin_y = location[0] + in_map_size[0] - in_location[0] - 1
            origin_x = location[1] - in_location[1]
            if map_size[0] == origin_y:
                map.append([empty] * map_size[1])
            for i in range(in_map_size[1]):
                if map[origin_y][origin_x + i] == empty:
                    map[origin_y][origin_x + i] = in_map[-1][i]

        elif dir == 'right':
            origin_y = location[0] - in_location[0]
            origin_x = location[1] + in_map_size[1] - in_location[1] - 1
            if map_size[1] == origin_x:
                print(in_map_size)
                for i in map:
                    i.append(empty)
            for i in range(in_map_size[0]):
                if map[origin_y + i][origin_x] == empty:
                    map[origin_y + i][origin_x] = in_map[i][-1]

        elif dir == 'top':
            origin_y = location[0] - in_location[0]
            origin_x = location[1] - in_location[1]
            if 0 > origin_y:
                map.insert(0, [empty] * map_size[1])
            for i in range(in_map_size[1]):
                if map[origin_y][origin_x + i] == empty:
                    map[origin_y][origin_x + i] = in_map[0][i]
        else:
            origin_y = location[0] - in_location[0]
            origin_x = location[1] - in_location[1]
            if 0 > origin_x:
                for i in map:
                    i.insert(0, empty)
            for i in range(in_map_size[0]):
                if map[origin_y + i][origin_x] == empty:
                    map[origin_y + i][origin_x] = in_map[i][0]

        return map, location

    if not store:
        store = [[], [], [], ""]  # map, log, location, turn

    location = player_location(map, 2)

    store[0], store[2] = expand_map(store[0], store[2], map, location, store[3])

    store[3] = move(store[0], store[1], store[2])

    '''
    for i in map:
        format = [str(j).rjust(2) for j in i]
        res = ' '.join(format)
        print(res)
    print(store[3])
    '''
    print(store[3])

    return store[3], store