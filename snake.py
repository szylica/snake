import tkinter
import random



ROWS = 25
COLS = 25
TILE_SIZE = 25
 
WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#creating object window class tkinter
window = tkinter.Tk()

#TITLE OF THE WINDOW
window.title("Snake")

#USER CANT RESIZE THE WINDOW
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#window on the middle of the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#CALCULATING WHERE THE CORNER OF THE WINDOW SHOULD BE FOR BEING ON THE MIDDLE OF THE SCREEN 
window_x = screen_width//2 - window_width//2
window_y = screen_height//2 - window_height//2


#LOCATION OF THE WINDOW ON THE SCREEN
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#object snake, class tile - defines x and y position of snakes head
snake = Tile(5*TILE_SIZE,5*TILE_SIZE)

#object food, class tile - defines x and y position of food tile
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)

#list that contains tiles of snake's body's, tiles contains coordinates of each body part 
snake_body = [] #multiple snake tiles

#directions where snakes moving 
velocityX = 0
velocityY = 0

game_over = False
reset_game = False

score = 0

def move():
    global snake, food, snake_body, game_over, score
    if (game_over):
        return
    
    #if snake hits a wall, game over
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_WIDTH):
        game_over = True
        return
    
    #if snake hits any part of his body, game over
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    #collision with food
    #appending a tile to snake_body list 
    #generating new place for food
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        score += 1
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE

    

    #following body
    #for loop from backwards, we are replacing i element of the list(snake_body) with the previous one(FROM BACKWARDS)
    for i in range(len(snake_body)-1, -1, -1):
        #current snake_body part as a "tile"
        tile = snake_body[i]
        if (i == 0):# we are right behind snakes head so replace 2nd part with his head
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
        
    

    #moving snake to currently selected direction
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


#controling snake, function
def change_direction(e):
    global velocityX, velocityY, game_over, End_title

    #after game over, listening about a space button - restart game
    if game_over:
        if (e.keysym == "space"):
            global reset_game 
            reset_game = True

    #closing game
    if (e.keysym == "Escape"):
            window.destroy()

    #up direction, cant rotate 180 degrees
    if (e.keysym == "w" and velocityY != 1):
        velocityX = 0
        velocityY = -1

    #down direction, cant rotate 180 degrees
    if (e.keysym == "s" and velocityY != -1):
        velocityX = 0
        velocityY = 1

    #left direction, cant rotate 180 degrees
    if (e.keysym == "a" and velocityX != 1):
        velocityX = -1
        velocityY = 0

    #left direction, cant rotate 180 degrees
    if (e.keysym == "d" and velocityX != -1):
        velocityX = 1
        velocityY = 0



def draw():
    global snake, food, snake_body, game_over, score, reset_game, velocityX, velocityY
    move()

    #clearing 
    canvas.delete("all")

    #drawing red square which represents food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "red")

    #drawing green square which represents snake's food
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "green")

    #drawing every part of snakes body for the snake_body list
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "lime green")

    #Game over announcement and score 
    if (game_over):
        global End_title
        End_title = canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font= "Arial 20", text = f"Game Over: {score}", fill = "white")
    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "white")


    #setting all properties to deafault and restarting
    if (reset_game and game_over == True):
        velocityX = 0
        velocityY = 0
        snake = Tile(5*TILE_SIZE,5*TILE_SIZE)
        food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
        snake_body = []
        score = 0
        game_over = False
        canvas.delete(End_title)
        reset_game = False
        
    
    #calling "draw" function again, every 100ms
    window.after(100, draw)

draw()

window.bind("<KeyRelease>", change_direction)


window.mainloop()