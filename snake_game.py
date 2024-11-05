import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = '7620913375:AAGMfjfL_RvRsKPzjp3zlc8zYLJKLQPG4Bc'

board_size = 10
snake = [(5, 5)]
food = (random.randint(0, board_size - 1), random.randint(0, board_size - 1))
direction = 'RIGHT'
score = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to Snake Game!\nUse /up, /down, /left, /right to move the snake.\nType /board to see the game board.")
    await show_board(update)

async def show_board(update: Update) -> None:
    global board_size, snake, food
    board = ""

    for i in range(board_size):
        for j in range(board_size):
            if (i, j) in snake:
                board += "🐍"
            elif (i, j) == food:
                board += "🍎"
            else:
                board += "⬜"
        board += "\n"

    await update.message.reply_text(board + f"\nScore: {score}")

async def move_snake(update: Update, new_direction: str) -> None:
    global snake, food, direction, score

    if new_direction == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif new_direction == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif new_direction == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif new_direction == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    head_x, head_y = snake[0]

    if direction == 'UP':
        head_x -= 1
    elif direction == 'DOWN':
        head_x += 1
    elif direction == 'LEFT':
        head_y -= 1
    elif direction == 'RIGHT':
        head_y += 1

    new_head = (head_x, head_y)

    if (head_x < 0 or head_x >= board_size or head_y < 0 or head_y >= board_size or new_head in snake):
        await update.message.reply_text("Game Over! You collided. Type /start to play again.")
        reset_game()
        return

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        food = (random.randint(0, board_size - 1), random.randint(0, board_size - 1))
    else:
        snake.pop()

    await show_board(update)

def reset_game():
    global snake, food, direction, score
    snake = [(5, 5)]
    food = (random.randint(0, board_size - 1), random.randint(0, board_size - 1))
    direction = 'RIGHT'
    score = 0

async def up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await move_snake(update, 'UP')

async def down(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await move_snake(update, 'DOWN')

async def left(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await move_snake(update, 'LEFT')

async def right(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await move_snake(update, 'RIGHT')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('up', up))
    application.add_handler(CommandHandler('down', down))
    application.add_handler(CommandHandler('left', left))
    application.add_handler(CommandHandler('right', right))
    application.add_handler(CommandHandler('board', show_board))

    application.run_polling()
