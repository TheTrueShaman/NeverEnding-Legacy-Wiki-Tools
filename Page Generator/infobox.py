import requests
import json


def load_data(url="http://orteil.dashnet.org/legacy/data.js"):
    data = requests.get(url)
    with open('data.txt', 'w') as f:
        # May want to change to .content instead of .text in the future
        f.write(data.content.decode('utf-8-sig'))


def parse_data():
    with open('game_json.txt', 'r') as f:
        mod_data = f.read()
    json_object = json.loads(mod_data)
    #print(json_object)
    return json_object


def create_page(name, game_data):
    if not name in game_data['gameObjects'].keys():
        return "Object does not exist"

    game_object = game_data['gameObjects'][name]
    object_keys = game_object.keys()

    type_conversion = {'res': 'resource',
                       'unit': 'unit',
                       'tech': 'research',
                       'trait': 'trait',
                       'policy': 'policy',
                       'achiev': 'achievement'}

    text = '{{Infobox ' + type_conversion[game_object['type']] + '\n'
    text += '|title = ' + name.title() + '\n'
    text += '|image = ' + name.title() + '.png\n'

    # Limit
    if 'limit' in object_keys:
        text += '|limited = [[' + game_object['limit'].title() + ']]\n'

    # Cost
    if ('cost' in object_keys) and (len(game_object['cost']) > 0):
        text += '|cost = '
        for cost in game_object['cost']:
            text += str(game_object['cost'][cost]) + ' [[' + cost.title() + ']], '
        text = text.rstrip(', ')
        text += '\n'

    # Requirements
    if ('req' in object_keys) and (len(game_object['req']) > 0):
        text += '|requirements = '
        for req in game_object['req']:
            if not game_object['req'][req]:
                text += 'Not '
            text += '[[' + req.title() + ']], '
        text = text.rstrip(', ')
        text += '\n'

    # TODO: Effects
    # Use
    if ('use' in object_keys) and (len(game_object['use']) > 0):
        text += '|uses = '
        for use in game_object['use']:
            text += str(game_object['use'][use]) + ' [[' + use.title() + ']], '
        text = text.rstrip(', ')
        text += '\n'

    # Upkeep
    if ('upkeep' in object_keys) and (len(game_object['upkeep']) > 0):
        text += '|upkeep = '
        for upkeep in game_object['upkeep']:
            text += str(game_object['upkeep'][upkeep]) + ' [[' + upkeep.title() + ']], '
        text = text.rstrip(', ')
        text += '\n'

    # Staff
    if ('staff' in object_keys) and (len(game_object['staff']) > 0):
        text += '|staff = '
        for staff in game_object['staff']:
            text += str(game_object['staff'][staff]) + ' [[' + staff.title() + ']], '
        text = text.rstrip(', ')
        text += '\n'

    # StartWith
    if ('startWith' in object_keys) and (game_object['startWith'] != 0):
        text += '|start_with = ' + str(game_object['startWith']) + '\n'

    # LimitPer
    if ('limitPer' in object_keys) and (len(game_object['limitPer']) > 0):
        text += '|limit_per = '
        for limit in game_object['limitPer']:
            text += str(game_object['limitPer'][limit]) + ' [[' + limit.title() + ']], '
        text = text.rstrip(', ')
        text += '\n'

    # TODO: turnToByContext
    # TODO: Maybe implement category and partOf
    text += '}}\n'

    # Effects
    crafting = False
    gathering = False
    gathering_amount_col = False
    wasting = False
    explore = False
    funcs = False
    add_free = False
    mult = False
    provide = False

    if ('effects' in object_keys) and (len(game_object['effects']) > 0):
        text += "== Effects ==\n"
        print(game_object['effects'])
        for i in range(len(game_object['effects'])):
            if game_object['effects'][i]['type'] == 'convert':
                crafting = True
            elif game_object['effects'][i]['type'] == 'gather':
                gathering = True
                if ('amount' in game_object['effects'][i].keys()) or ('max' in game_object['effects'][i].keys()):
                    gathering_amount_col = True
            elif game_object['effects'][i]['type'] == 'waste':
                wasting = True
            elif game_object['effects'][i]['type'] == 'explore':
                exploring = True
            elif game_object['effects'][i]['type'] == 'function':
                funcs = True
            elif game_object['effects'][i]['type'] == 'add_free':
                add_free = True
            elif game_object['effects'][i]['type'] == 'mult':
                mult = True
            elif game_object['effects'][i]['type'] == 'provide':
                provide = True
            else:
                print("Unknown effect type: " + game_object['effects'][i]['type'])

    # TODO
    if gathering:
        text += "=== Gathering ===\n"
        text += "{| class=\"wikitable\" \n!Mode \n!Context \n!Product \n"
        if gathering_amount_col:
            text += "!Amount / Max \n"
        text += "!Frequency (per [[tick]]) \n!Requirements \n"

        for i in range(len(game_object['effects'])):
            if game_object['effects'][i]['type'] == 'gather':
                effect = game_object['effects'][i]
                effect_keys = effect.keys()

                text += process_mode(game_object, effect, effect_keys)

                if 'context' in effect_keys:
                    text += '|' + effect['context'].title() + '\n'
                else:
                    text += '|None\n'

                if ('what' in effect_keys) and (len(effect['what']) > 0):
                    text += '|'
                    for product in effect['what']:
                        text += str(effect['what'][product]) + ' [[' + product.title() + ']], '
                    text = text.rstrip(', ')
                    text += '\n'
                else:
                    text += '|Any from context\n'

                if ('amount' in effect_keys) or ('max' in effect_keys):
                    text += '|'
                elif gathering_amount_col:
                    text += '|Unspecified\n'
                if 'amount' in effect_keys:
                    text += 'Amount: ' + str(effect['amount']) + '\n'
                if 'max' in effect_keys:
                    text += 'Max: ' + str(effect['max']) + '\n'

                frequency = 1
                if 'every' in effect_keys:
                    frequency = frequency / effect['every']
                if 'repeat' in effect_keys:
                    frequency = frequency * effect['repeat']
                # Yes, I made decision to include chance here
                if 'chance' in effect_keys:
                    frequency = frequency * effect['chance']
                text += '|' + str(frequency) + '\n'

                text += process_req(game_object, effect, effect_keys)

        text += "|}\n"

    # Crafting / Converting
    if crafting:
        text += "=== Crafting ===\n"
        text += "{| class=\"wikitable\" \n!Mode \n!Materials \n!Product \n!Frequency (per [[tick]]) \n!Requirements \n"
        for i in range(len(game_object['effects'])):
            if game_object['effects'][i]['type'] == 'convert':
                effect = game_object['effects'][i]
                effect_keys = effect.keys()

                text += process_mode(game_object, effect, effect_keys)

                if ('from' in effect_keys) and (len(effect['from']) > 0):
                    text += '|'
                    for material in effect['from']:
                        text += str(effect['from'][material]) + ' [[' + material.title() + ']], '
                    text = text.rstrip(', ')
                    text += '\n'

                if ('into' in effect_keys) and (len(effect['into']) > 0):
                    text += '|'
                    for product in effect['into']:
                        text += str(effect['into'][product]) + ' [[' + product.title() + ']], '
                    text = text.rstrip(', ')
                    text += '\n'

                frequency = 1
                if 'every' in effect_keys:
                    frequency = frequency / effect['every']
                if 'repeat' in effect_keys:
                    frequency = frequency * effect['repeat']
                # Yes, I made decision to include chance here for conversions
                if 'chance' in effect_keys:
                    frequency = frequency * effect['chance']
                text += '|' + str(frequency) + '\n'

                text += process_req(game_object, effect, effect_keys)
        text += "|}\n"

    return text


def process_mode(game_object, effect, effect_keys):
    mode_column = '|-\n'
    if 'mode' in effect_keys:
        mode_column += '|' + game_object['modes'][effect['mode']]['name'].title() + '\n'
    elif 'notMode' in effect_keys:
        mode_column += '|Not ' + game_object['modes'][effect['notMode']]['name'].title() + '\n'
    else:
        mode_column += '|Always\n'
    return mode_column


def process_req(game_object, effect, effect_keys):
    req_column = '|'
    if ('req' in effect_keys) and (len(effect['req']) > 0):
        for req in effect['req']:
            if not effect['req'][req]:
                req_column += 'Not '
            req_column += '[[' + req.title() + ']], '
        req_column = req_column.rstrip(', ')
    elif 'mode' in effect_keys:
        if (('req' in game_object['modes'][effect['mode']].keys()) and
                (len(game_object['modes'][effect['mode']]['req']) > 0)):
            for req in game_object['modes'][effect['mode']]['req']:
                if not game_object['modes'][effect['mode']]['req'][req]:
                    req_column += 'Not '
                req_column += '[[' + req.title() + ']], '
            req_column = req_column.rstrip(', ')
        else:
            req_column += 'None'
    else:
        req_column += 'None'
    req_column += '\n'
    return req_column


if __name__ == '__main__':
    link = ""
    load_data()
    game_object_data  = parse_data()
    response = ""
    while response != "exit":
        response = input("For what would you like to create an infobox? ").lower()
        infobox = create_page(response, game_object_data)
        print(infobox)