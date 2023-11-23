import requests
import re


def load_data(url="http://orteil.dashnet.org/legacy/data.js"):
    data = requests.get(url)
    with open('data.txt', 'w') as f:
        # May want to change to .content instead of .text in the future
        f.write(data.text)


def parse_data():
    with open('data.txt', 'r') as f:
        data = f.read()
    game_objects = []
    while True:
        match = re.search(r"new G\..+?{", data)
        if not match:
            break
        data = data[match.span()[1]:]
        a = data
        counter = 1
        while counter > 0:
            current = re.search(r'[{}]', a)
            if current[0] == '{':
                counter += 1
            else:
                counter -= 1
            a = a[current.span()[1]:]
        game_objects.append(match[0] + data[:len(data) - len(a)])

    with open('game_objects.txt', 'w') as f:
        match_str = ""
        separator = '--------'
        for game_object in game_objects:
            object_name = re.search(r"name:'(.+?)',", game_object)[1]
            match_str += separator + object_name + separator + str(len(re.findall(r"\n", game_object)) + 1) \
                + separator + "\n" + game_object + "\n\n\n"
        f.write(match_str)


def create_infobox(name):
    separator = '--------'
    with open('game_objects.txt', 'r') as f:
        data = f.read()
        match = re.search(separator+name+separator+r"(\d+)"+separator, data)
        if not match:
            return "Invalid input."
        game_object = re.search(r"(?:.*?\n){" + match[1] + "}", data[match.span()[1] + 1:])[0]
    valid_types = ['Res', 'Unit', 'Tech', 'Trait', 'Policy', 'Achiev']
    data_type = re.search(r"new G\.(.+?)\({", game_object)[1]
    if data_type not in valid_types:
        return "Game Object is not of a valid type."
    # print(data_type)
    type_names = ['resource', 'unit', 'research', 'trait', 'policy', 'achievement']
    infobox = '{{Infobox ' + type_names[valid_types.index(data_type)] + '\n'
    infobox += '|title = ' + name.title() + '\n'
    infobox += '|image = ' + name.title() + '.png\n'
    # Limit
    object_limit = re.search(r"limit:'(.+?)',", game_object)
    if object_limit:
        infobox += '|limited = [[' + object_limit[1].title() + ']]\n'
    # Cost
    object_cost = re.search(r"cost:{('.+?':\d+,?)},", game_object)
    if object_cost:
        costs = re.findall(r"'(.+?)':(\d+)(,?)", object_cost[0])
        infobox += '|cost = '
        for cost in costs:
            infobox += cost[1] + ' [[' + cost[0].title() + ']]'
            if cost[2]:
                infobox += ', '
        infobox += '\n'
    # Requirements
    object_req = re.search(r"req:{('.+?':(?:true|false),?)},", game_object)
    if object_req:
        reqs = re.findall(r"'(.+?)':(true|false)(,?)", object_req[0])
        infobox += '|requirements = '
        for req in reqs:
            if req[1] == 'false':
                infobox += 'Not '
            infobox += '[[' + req[0].title() + ']]'
            if req[2]:
                infobox += ', '
        infobox += '\n'
    # TODO: Effects
    # TODO: Use
    # TODO: Upkeep
    # TODO: Staff
    # TODO: StartWith
    object_start_with = re.search(r"startWith:(true|\d+)", game_object)
    if object_start_with:
        print(object_start_with[0])
    # LimitPer
    object_limit_per = re.search(r"limitPer:{('.+?':\d+,?)},", game_object)
    if object_limit_per:
        limit_per = re.findall(r"'(.+?)':(\d+)(,?)", object_limit_per[0])
        infobox += '|limit_per = '
        for limit in limit_per:
            infobox += limit[1] + ' [[' + limit[0].title() + ']]'
            if limit[2]:
                infobox += ', '
        infobox += '\n'
    # TODO: turnToByContext
    # TODO: Maybe implement category and partOf
    infobox += '}}'
    return infobox


if __name__ == '__main__':
    link = ""
    load_data()
    parse_data()
    response = ""
    while response != "exit":
        response = input("For what would you like to create an infobox? ").lower()
        print(create_infobox(response))
