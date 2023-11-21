from collections import deque

from django.http import JsonResponse
from django.shortcuts import render
import random
from gameapp.models import GameMap
from .team2 import movePlayer


def get_field_around_player(player_symbol, radius, map):
    for i, row in enumerate(map):
        for j, element in enumerate(row):
            if element == player_symbol:
                player_position = (i, j)
                break

    field_around_player = []
    for i in range(max(0, player_position[0] - radius), min(len(map), player_position[0] + radius + 1)):
        row = []
        for j in range(max(0, player_position[1] - radius), min(len(map[0]), player_position[1] + radius + 1)):
            row.append(map[i][j])
        field_around_player.append(row)

    return field_around_player

def move(direction, data):
    data["player_moves"] += 1
    player_position = [(i, row.index(2)) for i, row in enumerate(data["map"]) if 2 in row][0]

    new_position = None

    # Поиск позиции куда нужно пойти
    if direction == 'left':
        new_position = (player_position[0], player_position[1] - 1)
    elif direction == 'right':
        new_position = (player_position[0], player_position[1] + 1)
    elif direction == 'top':
        new_position = (player_position[0] - 1, player_position[1])
    elif direction == 'bottom':
        new_position = (player_position[0] + 1, player_position[1])

    if 0 <= new_position[0] < 10 and 0 <= new_position[1] < 10:
        # Проверяем, не стоит ли на новой позиции стена
        if data["map"][new_position[0]][new_position[1]] != 0:
            if data["map"][new_position[0]][new_position[1]] == 3:
                data["amount_food"] -= 1
            data["map"][player_position[0]][player_position[1]] = 1
            data["map"][new_position[0]][new_position[1]] = 2

    return data

def index(request):
    # Ваши данные
    map_data = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 3, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 1, 1, 3, 0, 0, 1, 0],
        [0, 1, 1, 1, 2, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 0, 0, 3, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    amount_food = 5
    player_moves = 0
    store = {}

    # Объединяем данные в один JSON
    combined_data = {
        'map': map_data,
        'amount_food': amount_food,
        'player_moves': player_moves,
        'store': store,
    }

    print(combined_data)

    try:
        game_map = GameMap.objects.get(id=1)
        game_map.data = combined_data
        game_map.save()
    except GameMap.DoesNotExist:
        GameMap.objects.create(id=1, data=combined_data)

    return render(request, 'index.html', {'map': combined_data})

def start_game(request):
    previous_game_map = GameMap.objects.get(id=1)
    previous_data = previous_game_map.data

    limited_map = get_field_around_player(2, 2, previous_data["map"])
    direction, previous_data["store"] = movePlayer(limited_map, previous_data["store"])
    new_data = move(direction, previous_data)

    # Сохранение новой карты в объекте GameMap с id=1
    game_map, _ = GameMap.objects.get_or_create(id=1)
    game_map.data = new_data
    game_map.save()

    return JsonResponse({'map': new_data})
