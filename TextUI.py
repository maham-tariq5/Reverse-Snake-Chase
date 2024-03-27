from blessed import Terminal
import random
import copy
from collections import deque



# Setting up WASD keys and Arrow keys for gameplay
term = Terminal()
Up = term.KEY_UP
Right = term.KEY_RIGHT
Left = term.KEY_LEFT
Down = term.KEY_DOWN
Directions = [Left, Up, Right, Down]
Movement_Map = {Left: [0, -1], Up: [-1, 0], Right: [0, 1], Down: [1, 0]}
WASD_MAP = {'w': Up, 'a': Left, 's': Down, 'd': Right, 'W': Up, 'A': Left, 'S': Down, 'D': Right}
dead = False

##############################################
#snake and food setup, positions, shapes, speed, colours etc
 ############################################

Border = '⬜️'
Body = '🟩'
Head = '🟥'
Space = ' '
Apple = '🍎'

snake = deque([[6, 5], [6, 4], [6, 3]]) #initial snake 
food = [5, 10]  
h, w = 10, 15 # height, width
score = 0

initial_speed = 3

max_speed = 6

# S1 and S2 represents the snake's movement frequency.
S1 = 1
S2 = 2

# T represents how often the snake will grow.
T = 9

####################################

####################################

#### Setting up the screen of the game/world and main game loop ####

# messages will appear on screen as you continue playing
messages = ['you can do it!', "don't get eaten!", 'run, forest, run!', "come on you got this bestie", "you can beat it!", "outsmart the snake!"]
message = None

def list_empty_spaces(world, space):
  result = []
  for i in range(len(world)):
    for j in range(len(world[i])):
      if world[i][j] == space:
        result.append([i, j])
  return result

with term.cbreak(), term.hidden_cursor():
  # clear the screen
  print(term.home + term.clear)
  
  # Initializing the game world
  world = [[Space] * w for _ in range(h)]
  for i in range(h):
    world[i][0] = Border
    world[i][-1] = Border
  for j in range(w):
    world[0][j] = Border
    world[-1][j] = Border
  for s in snake:
    world[s[0]][s[1]] = Body
  head = snake[0]
  world[head[0]][head[1]] = Head
  world[food[0]][food[1]] = Apple
  for row in world:
    print(' '.join(row))
  print('Welcome to Reverse Snake Game')
  print('use arrow keys or WASD to move!\n')
  print("this time, your the food \n")
  print('expand window if preferred')
  

  val = ''
  moving = False
  turn = 0
   
   # The main game loop that runs the game 

  while True:
    val = term.inkey(timeout=1/initial_speed)
    if val.code in Directions or val in WASD_MAP.keys():
      moving = True
    if not moving:
      continue

    # movements of the snake
    head = snake[0]
    y_diff = food[0] - head[0]
    x_diff = food[1] - head[1]

    preferred_move = None
    if abs(y_diff) > abs(x_diff):
      if y_diff <= 0:
        preferred_move = Up
      else:
        preferred_move = Down
    else:
      if x_diff >= 0:
        preferred_move = Right
      else:
        preferred_move = Left
    
    
    preferred_moves = [preferred_move] + list(Directions)
    
    next_move = None
    for move in preferred_moves:
      movement = Movement_Map[move]
      head_copy = copy.copy(head)
      head_copy[0] += movement[0]
      head_copy[1] += movement[1]
      heading = world[head_copy[0]][head_copy[1]]
      if heading == Border:
        continue
      elif heading == Body:
        # For every M turns, the snake grows
        # longer. So, the head can move to the
        # tail's location only if turn % T != 0
        if head_copy == snake[-1] and turn % T != 0:
          next_move = head_copy
          break
        else:
          continue
      else:
        next_move = head_copy
        break
    
    if next_move is None:
      break
    
    turn += 1
    # snake only moves S - 1 out of S turns.
    # before the snake moves, clear the current
    # location of the food.
    world[food[0]][food[1]] = Space
    if turn % S2 < S1:
      snake.appendleft(next_move)
      
      # for every T turns or so, the snake grows longer and everything becomes faster
      world[head[0]][head[1]] = Body
      if turn % turn != 0:
        speed = min(initial_speed * 1.05, max_speed)
        tail = snake.pop()
        world[tail[0]][tail[1]] = Space
      world[next_move[0]][next_move[1]] = Head

    
    
    # And then the food moves
    food_copy = copy.copy(food)
    
    # First, encode the movement in food_copy
    if val.code in Directions or val in WASD_MAP.keys():
      direction = None
      if val in WASD_MAP.keys():
        direction = WASD_MAP[val]
      else:
        direction = val.code
      movement = Movement_Map[direction]
      food_copy[0] += movement[0]
      food_copy[1] += movement[1]

    # Check where the food is heading
    food_heading = world[food_copy[0]][food_copy[1]]
    
    if food_heading == Head:
      dead = True
  
    if food_heading == Space:
      food = food_copy
   
    if world[food[0]][food[1]] == Body or world[food[0]][food[1]] == Head:
      dead = True
    if not dead:
      world[food[0]][food[1]] = Apple

    print(term.move_yx(0, 0))
    for row in world:
      print(' '.join(row))
    score = len(snake) - 3
    print(f'score: {turn} - size: {len(snake)}' + term.clear_eol)
    if dead:
      break
    if turn % 50 == 0:
      message = random.choice(messages)
    if message:
      print(message + term.clear_eos)
    print(term.clear_eos, end='')


# Game over prompts

# Once the game ends the player will be prompted with one of the follwing statements
if dead:
  print('oh no the snake ate you! You lose' + term.clear_eos)
else:
  print('Congrats you won!' + term.clear_eos)

  
