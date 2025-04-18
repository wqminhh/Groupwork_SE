import ita
import time  # Để thêm một chút thời gian chờ giữa các khung hình

def lifegame_step(data):
    """Tính toán thế hệ tiếp theo của Game of Life."""
    rows = len(data)
    cols = len(data[0])
    new_data = ita.array.make2d(rows, cols)
    for i in range(rows):
        for j in range(cols):
            live_neighbors = count_neighbor(data, i, j)
            new_data[i][j] = lifegame_rule(data[i][j], live_neighbors)
    return new_data

def count_neighbor(data, i, j):
    """Đếm số lượng ô sống xung quanh ô (i, j)."""
    rows = len(data)
    cols = len(data[0])
    count = 0
    for x in range(max(0, i - 1), min(rows, i + 2)):
        for y in range(max(0, j - 1), min(cols, j + 2)):
            if (x != i or y != j) and data[x][y] == 1:
                count += 1
    return count

def lifegame_rule(cur, neighbor):
    """Áp dụng luật chơi của Game of Life."""
    if cur == 1:  # Ô hiện tại đang sống
        if neighbor < 2 or neighbor > 3:
            return 0  # Chết vì thiếu dân số hoặc quá tải dân số
        elif 2 <= neighbor <= 3:
            return 1  # Tiếp tục sống
    else:  # Ô hiện tại đang chết
        if neighbor == 3:
            return 1  # Sinh sản
        else:
            return 0  # Vẫn chết

def lifegame_animation(initial_data, steps):
    """Tạo hoạt ảnh Game of Life."""
    history = ita.array.make1d(steps, dtype=object)
    current_data = initial_data
    for i in range(steps):
        history[i] = current_data
        current_data = lifegame_step(current_data)
    return history

# Kiểm thử với glider
glider_animation = lifegame_animation(ita.lifegame_glider(), 50)
ita.plot.animation_show(glider_animation, interval=200) # interval tính bằng mili giây

# Kiểm thử với acorn
acorn_animation = lifegame_animation(ita.lifegame_acorn(), 100)
ita.plot.animation_show(acorn_animation, interval=200) # interval tính bằng mili giây
