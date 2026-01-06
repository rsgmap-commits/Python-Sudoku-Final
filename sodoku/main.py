# -*- coding: utf-8 -*-
import pygame
import time

# --- 設定 ---
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 700
TILE_SIZE = 60

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 初始化 pygame
pygame.init()

# 字體
FONT = pygame.font.SysFont("comicsans", 40)

# 題庫
board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

original_board = [row[:] for row in board]

def solve_silently(grid):
    """無聲求解"""
    find = find_empty(grid)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if is_valid(grid, i, (row, col)):
            grid[row][col] = i
            if solve_silently(grid):
                return True
            grid[row][col] = 0

    return False

def draw_grid(win):
    """繪製網格"""
    for i in range(10):
        if i % 3 == 0:
            thick = 4
        else:
            thick = 1
        
        pygame.draw.line(win, BLACK, (0, i * TILE_SIZE), (540, i * TILE_SIZE), thick)
        pygame.draw.line(win, BLACK, (i * TILE_SIZE, 0), (i * TILE_SIZE, 540), thick)

def draw_numbers(win, grid):
    """畫數字"""
    for i in range(9):
        for j in range(9):
            num = grid[i][j]
            if num != 0:
                if original_board[i][j] != 0:
                    color = GREEN
                else:
                    color = RED

                text = FONT.render(str(num), 1, color)
                x = j * TILE_SIZE + (TILE_SIZE - text.get_width()) / 2
                y = i * TILE_SIZE + (TILE_SIZE - text.get_height()) / 2
                win.blit(text, (x, y))

def is_valid(grid, num, pos):
    """檢查是否合法"""
    row, col = pos

    # 檢查行
    for j in range(9):
        if j != col and grid[row][j] == num:
            return False

    # 檢查列
    for i in range(9):
        if i != row and grid[i][col] == num:
            return False

    # 檢查 3x3 九宮格
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if (i != row or j != col) and grid[i][j] == num:
                return False

    return True

def find_empty(grid):
    """尋找空格"""
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

def is_board_complete(grid):
    """檢查是否填滿"""
    for row in grid:
        if 0 in row:
            return False
    return True

def is_board_valid(grid):
    """檢查棋盤有效性"""
    for i in range(9):
        for j in range(9):
            num = grid[i][j]
            if num != 0:
                grid[i][j] = 0
                if not is_valid(grid, num, (i, j)):
                    grid[i][j] = num
                    return False
                grid[i][j] = num
    return True

def main():
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku - Interactive")
    clock = pygame.time.Clock()
    
    # 使用列表而不是全局變量，避免 UnboundLocalError
    player_board = [row[:] for row in board]
    sol_board = [row[:] for row in board]
    
    solve_silently(sol_board)
    
    selected = None
    message = "Select a cell to fill (1-9)"
    message_time = 0
    
    running = True
    
    while running:
        clock.tick(30)
        win.fill(WHITE)
        
        draw_grid(win)
        draw_numbers(win, player_board)
        
        if selected:
            row, col = selected
            if original_board[row][col] == 0:
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(win, BLUE, rect, 3)
        
        pygame.draw.line(win, BLACK, (0, 540), (540, 540), 2)
        
        # 畫主訊息 (更大更清晰)
        msg_font = pygame.font.SysFont("comicsans", 28, bold=True)
        msg_text = msg_font.render(message, 1, BLACK)
        win.blit(msg_text, (20, 550))
        
        # 畫幫助文字
        help_font = pygame.font.SysFont("comicsans", 16)
        help_text = help_font.render("H=Hint  SPACE=Check  R=Reset  ENTER=Solve", 1, GRAY)
        win.blit(help_text, (20, 585))
        
        if is_board_complete(player_board) and is_board_valid(player_board):
            message = "You Win!"
            pygame.display.set_title("Sudoku - Completed!")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pos[1] < 540:
                    col = pos[0] // TILE_SIZE
                    row = pos[1] // TILE_SIZE
                    if 0 <= row < 9 and 0 <= col < 9:
                        if original_board[row][col] == 0:
                            selected = (row, col)
                            message = f"Selected ({row},{col})"
                            message_time = 120
            
            elif event.type == pygame.KEYDOWN:
                # 數字鍵 1-9
                if pygame.K_1 <= event.key <= pygame.K_9:
                    if selected is None:
                        message = "Select a cell first!"
                        message_time = 120
                    else:
                        row, col = selected
                        num = event.key - pygame.K_0
                        player_board[row][col] = num
                        message = f"Filled {num}"
                        message_time = 120
                
                # Delete/Backspace
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE or event.key == pygame.K_0:
                    if selected is not None:
                        row, col = selected
                        player_board[row][col] = 0
                        message = "Cleared"
                        message_time = 120
                
                # Space - Check
                elif event.key == pygame.K_SPACE:
                    if selected is None:
                        message = "Select cell!"
                        message_time = 120
                    else:
                        row, col = selected
                        if player_board[row][col] == 0:
                            message = "Empty"
                            message_time = 120
                        elif player_board[row][col] == sol_board[row][col]:
                            message = "Correct!"
                            message_time = 120
                        else:
                            message = "Wrong!"
                            message_time = 120
                
                # H - Hint
                elif event.key == pygame.K_h:
                    if selected is None:
                        message = "Select cell!"
                        message_time = 120
                    else:
                        row, col = selected
                        if player_board[row][col] == 0:
                            hint_num = sol_board[row][col]
                            player_board[row][col] = hint_num
                            message = f"Hint: {hint_num}"
                            message_time = 120
                        else:
                            message = "Already filled"
                            message_time = 120
                
                # R - Reset
                elif event.key == pygame.K_r:
                    for i in range(9):
                        for j in range(9):
                            player_board[i][j] = board[i][j]
                    selected = None
                    message = "Reset!"
                    message_time = 120
                
                # Enter - Solve
                elif event.key == pygame.K_RETURN:
                    for i in range(9):
                        for j in range(9):
                            player_board[i][j] = sol_board[i][j]
                    message = "Solved!"
                    message_time = 120
        
        if message_time > 0:
            message_time -= 1
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()

