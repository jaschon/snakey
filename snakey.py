#!/usr/bin/env python3

from pynput import keyboard
import time
import random
import copy

WIN = 25 
LEVELS = { 

1: """
╔════════════════════════╗
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
""",

2: """
╔════════════════════════╗
║                        ║
║                        ║
║                        ║
║               ═════    ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║    ═════               ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║                        ║
║               ═════    ║
║                        ║
║                        ║
║   ═════                ║
║                        ║
║                        ║
║                        ║
""",

3: """
╔════════════════════════╗
║                        ║
║                        ║
║        ║               ║
║        ║               ║
║        ║               ║
║        ║               ║
║        ║               ║
║        ║               ║
║        ║               ║
║        ║               ║
╠════════╝               ║
║                        ║
║                        ║
║               ║        ║
║               ║        ║
║               ║        ║
║               ║        ║
║               ║        ║
║               ║        ║
║               ║        ║
║               ║        ║
║               ╚════════╣
║                        ║
║                        ║
""",


4: """
╔════════════════════════╗
║                        ║
║                        ║
║                        ║
║               ╔════    ║
║        ║      ║        ║
║        ║      ║        ║
║        ║      ║        ║
║        ║      ║        ║
║        ║      ║        ║
║    ════╝               ║
║                        ║
║                        ║
║                ║       ║
║                ║       ║
║                ║       ║
║                ║       ║
║       ║        ║       ║
║       ║        ╚═══    ║
║       ║                ║
║       ║                ║
║   ════╝                ║
║                        ║
║                        ║
║                        ║
""",

}


def clear_screen() -> None:
    print("\033[2J\033[H", end="")

def build_screen(level: int, lives: int) -> list:
    screen = [list(s) for s in LEVELS.get(level,LEVELS[1]).strip().split("\n")]
    screen.append(["╠════╦═══════","╦═══════════╣"])
    screen.append(["║", str(lives).center(4), "║ ", " 0", "/", str(WIN).ljust(2), " ║"," LEVEL ", str(level).ljust(2), "  ║"])
    screen.append(["╠════╩═══════╩", "═══════════╣"])
    screen.append(["║", "                       "," ║"])
    screen.append(["╚═════════════", "═══════════╝"])
    return screen

def pause_frame(pause: float) -> None:
    time.sleep(pause)

def get_input(key) -> None:
    global HEAD
    match key:
        case keyboard.Key.down:
            HEAD = "S"
        case keyboard.Key.up:
            HEAD = "N"
        case keyboard.Key.left:
            HEAD = "W"
        case _:
            HEAD = "E"

def update_pause(hit_apple: bool, score: int, pause: float):
    if hit_apple and score % 2 == 0:
        pause -= .02
    return pause

def check_apple(apple:list, snake: list) -> bool:
    if apple in snake:
        return True
    return False

def add_apple(hit_apple: bool, apple: list, snake: list, screen: list) -> list:
    while hit_apple:
        apple = [random.randint(2,len(screen[0])-2), random.randint(2,len(screen)-6)]
        if not apple in snake and screen[apple[1]][apple[0]] == " ":
            break
    return apple

def update_apple(screen: list, apple: list) -> None:
    screen[apple[1]][apple[0]] = "◉"

def update_lives(lives: int, screen: list) -> None:
    display_msg(f"LIVES {lives}", screen)

def update_score(hit_apple: bool, score: int, screen: list) -> int:
    if hit_apple:
        score += 1
        screen[-4][3] = str(score).rjust(2)
    return score

def update_screen(screen: list) -> None:
    for row in screen:
        print("".join(row))

def update_player(snake: list, head: str, hit_apple: bool, screen: list) -> None:
    if not hit_apple: 
        begin = snake.pop(0)
        screen[begin[1]][begin[0]] = " "
    match head:
        case "N":
            snake.append([snake[-1][0], snake[-1][1]-1])
            headchar = "╽"
        case "S":
            snake.append([snake[-1][0], snake[-1][1]+1])
            headchar = "╿"
        case "W":
            snake.append([snake[-1][0]-1, snake[-1][1]])
            headchar = "╼"
        case "E" | _:
            snake.append([snake[-1][0]+1, snake[-1][1]])
            headchar = "╾"
    for p in range(len(snake)):
        if p == 0 and len(snake)-1 > p:
            screen[snake[p][1]][snake[p][0]] = get_snake_piece(snake[p+1],snake[p],snake[p])
        elif p == len(snake)-1:
            screen[snake[p][1]][snake[p][0]] = get_snake_piece(snake[p],snake[p],snake[p-1])
        else:
            screen[snake[p][1]][snake[p][0]] = get_snake_piece(snake[p-1],snake[p],snake[p+1])
    screen[snake[-1][1]][snake[-1][0]] = headchar

def get_snake_piece(start: list, middle:list, end: list) -> str:
    #all hor
    if start[0] == middle[0] == end[0]:
        return "┃"
    #all vert
    elif start[1] == middle[1] == end[1]:
        return "━"
    #L bend
    elif (start[1] < middle[1] and end[0] > middle[0]) or (end[1] < middle[1] and start[0] > middle[0]):
        return "┗"
    #right bend
    elif (start[0] > middle[0] and end[1] > middle[1]) or (end[0] > middle[0] and start[1] > middle[1]):
        return "┏"
    #J bend
    elif (start[1] < middle[1] and end[0] < middle[0]) or (end[1] < middle[1] and start[0] < middle[0]):
        return "┛"
    #left bend
    elif (start[0] < middle[0] and end[1] > middle[1]) or (end[0] < middle[0] and start[1] > middle[1]):
        return "┓"
    else:
        return "X"

def check_ending(snake: list, playfield: list, score: int, lives: int) -> tuple:
    if snake[-1] in snake[:-2] or snake[-1][1] >= len(playfield)-6 or playfield[snake[-1][1]][snake[-1][0]] != " ":
        return False, lives-1, False
    elif score >= WIN:
        return False, lives, True
    return True, lives, False

def check_win(lives: int, level: int) -> None:
    if lives == 0:
        game_over(build_screen(level, lives))
    elif level >= len(LEVELS):
        win_screen(build_screen(level, lives))

def win_screen(playfield) -> None:
    display_msg("YOU WIN!", playfield)
    exit()

def game_over(playfield: list) -> None:
    display_msg("GAME OVER!", playfield)
    exit()

def start_screen(screen) -> None:
    display_msg("PRESS ENTER TO START", screen)
    input()
    display_msg(" ", screen)

def display_msg(msg: str, screen: list) -> None:
    clear_screen()
    screen[-2][1] = "\33[1;5m " + msg.ljust(22) + "\33[0m"
    update_screen(screen)

def main() -> None:
    try:
        pause = .3
        for l in LEVELS:
            pause_frame(.5)
            run_level(l, pause)
            pause -= .03 
    except KeyboardInterrupt:
        exit()


def run_level(level:int, orig_pause: float) -> None:
    listener = keyboard.Listener(on_press=get_input)
    listener.start()
    lives = 3 
    win = False
    while lives and not win:
        global HEAD
        HEAD = random.choice(("E", "S"))
        hit_apple = False
        pause = orig_pause
        game = True
        score = 0
        snake = [[1,3],[2,3],[3,3]]
        screen = build_screen(level, lives)
        playfield = copy.deepcopy(screen)
        apple = add_apple(True, [], snake, screen)
        update_lives(lives, screen)
        start_screen(screen)
        while game:
            clear_screen()
            update_player(snake, HEAD, hit_apple, screen)
            hit_apple = check_apple(apple, snake)
            score = update_score(hit_apple, score, screen)
            apple = add_apple(hit_apple, apple, snake, screen)
            pause = update_pause(hit_apple, score, pause)
            update_apple(screen, apple)
            update_screen(screen)
            game, lives, win = check_ending(snake, playfield, score, lives)
            pause_frame(pause)
    listener.stop()
    check_win(lives, level)

if __name__ == "__main__":
    main()
