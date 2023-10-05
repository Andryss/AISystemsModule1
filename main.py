import re
import sys

import pyswip

phrase_regex = re.compile(r"я (?P<name>.*), хочу (?P<actions>[\w ,]+)", re.IGNORECASE)
# я Петя, хочу убивать, проверять, лечить, дружить, соперничать, игроков, роли, состояния, отношения


def read_input() -> list[str]:
    line = input(f"Напиши запрос в формате 'я <ИМЯ>, хочу <ДЕЙСТВИЕ1>[, <ДЕЙСТВИЕ2>]...':\n")
    groups = phrase_regex.findall(line)
    if len(groups) == 0:
        raise Exception("неправильный формат ввода")
    tokens = [groups[0][0].strip().lower()]
    for group in groups[0][1].split(","):
        stripped = group.strip().lower()
        if len(stripped) > 0:
            tokens.append(stripped)
    return tokens


prolog = pyswip.Prolog()


def init_prolog():
    prolog.consult("mafia.pl")


def user_exists(name: str) -> bool:
    result = list(prolog.query(f"игрок({name})."))
    return len(result) > 0


def one_param_query(query: str, variable: str) -> list[str]:
    answer = list(prolog.query(query))
    result = list(map(lambda x: x[variable], answer))
    return result


def two_param_query(query: str, var1: str, var2: str) -> list[tuple[str, str]]:
    answer = list(prolog.query(query))
    result = list(map(lambda x: (x[var1], x[var2]), answer))
    return result


def убивать(name: str):
    role = one_param_query(f"имеет_роль({name}, X).", "X")[0]
    print(f"Твоя роль - {role}")
    victims = one_param_query(f"может_убить({name}, X).", "X")
    if len(victims) == 0:
        print("Ты никого не можешь убить")
    else:
        print(f"Ты можешь убить кого-нибудь из следующих игроков: {victims}")


def проверять(name: str):
    role = one_param_query(f"имеет_роль({name}, X).", "X")[0]
    print(f"Твоя роль - {role}")
    victims = one_param_query(f"может_проверить({name}, X).", "X")
    if len(victims) == 0:
        print("Ты никого не можешь проверить")
    else:
        print(f"Ты можешь проверить кого-нибудь из следующих игроков: {victims}")


def лечить(name: str):
    role = one_param_query(f"имеет_роль({name}, X).", "X")[0]
    print(f"Твоя роль - {role}")
    victims = one_param_query(f"может_вылечить({name}, X).", "X")
    if len(victims) == 0:
        print("Ты никого не можешь вылечить")
    else:
        print(f"Ты можешь вылечить кого-нибудь из следующих игроков: {victims}")


def дружить(name: str):
    acquaintances = one_param_query(f"знакомые({name}, X).", "X")
    opponents = one_param_query(f"соперники({name}, X).", "X")
    future_friends_count = len(acquaintances) + len(opponents)
    if future_friends_count == 0:
        print("Ты ни с кем не сможешь подружиться")
    else:
        print(f"Ты можешь подружиться с кем-нибудь из своих знакомых: {acquaintances}")
        print(f"Но если постараешься, то также можешь подружиться с кем-нибудь из своих соперников: {opponents}")


def соперничать(name: str):
    acquaintances = one_param_query(f"знакомые({name}, X).", "X")
    friends = one_param_query(f"друзья({name}, X).", "X")
    future_opponents_count = len(acquaintances) + len(friends)
    if future_opponents_count == 0:
        print("Ты ни с кем не сможешь соперничать")
    else:
        print(f"Ты можешь соперничать с кем-нибудь из своих знакомых: {acquaintances}")
        print(f"Но если постараешься, то также можешь соперничать с кем-нибудь из своих друзей: {friends}")


def игроков(name: str):
    players = one_param_query(f"игрок(X).", "X")
    print(f"Все игроки: {players}")


def роли(name: str):
    role = one_param_query(f"имеет_роль({name}, X).", "X")[0]
    print(f"Твоя роль - {role}")
    roles = one_param_query(f"роль(X).", "X")
    print(f"Все представленные роли: {roles}")
    print(f"По правилам игры нельзя узнать роли других игроков")
    if role == "комиссар":
        print(f"Но поскольку твоя роль \"комиссар\", то ты можешь узнавать роли")


def состояния(name: str):
    self_state = one_param_query(f"имеет_состояние({name}, X).", "X")[0]
    print(f"Твое состояние - {self_state}")
    states = one_param_query(f"состояние(X).", "X")
    print(f"Все представленные состояния: {states}")
    for state in states:
        players = one_param_query(f"имеет_состояние(X, {state}).", "X")
        if name in players:
            players.remove(name)
        print(f"Игроки с состоянием \"{state}\": {players}")


def отношения(name: str):
    relations = one_param_query(f"отношение(X).", "X")
    print(f"Все представленные отношения: {relations}")
    for relation in relations:
        pairs = two_param_query(f"имеет_отношение(X, Y, {relation})", "X", "Y")
        print(f"Все пары с отношением \"{relation}\": {pairs}")


actions_to_functions = {
    "убивать": убивать,
    "проверять": проверять,
    "лечить": лечить,
    "дружить": дружить,
    "соперничать": соперничать,
    "игроков": игроков,
    "роли": роли,
    "состояния": состояния,
    "отношения": отношения,
}


def run():
    init_prolog()
    tokens = read_input()
    name, actions = tokens[0], tokens[1:]

    if not user_exists(name):
        print(f"Игрока {name} не существует :(\n", file=sys.stderr)
        return

    errors = []

    print("*звуки работающей машины*")
    for action in actions:
        if action not in actions_to_functions:
            errors.append(action)
        else:
            print("---")
            print(f"Хочу {action}:")
            actions_to_functions[action](name)
            print("---")
    print("*звуки выключения машины*")

    if len(errors) > 0:
        print(f"несуществующие действия {errors} (список действий: {list(actions_to_functions.keys())})",
              file=sys.stderr)


if __name__ == '__main__':
    run()
