import pygame
import sys
import random
import pygame_gui

# Khởi tạo Pygame
pygame.init()

# Cài đặt kích thước màn hình ban đầu
screen_width = 1560
screen_height = 900

# Kích thước lưới mặc định và các tùy chọn
default_cell_size = 10
grid_sizes = {
    "Nhỏ": 15,
    "Trung bình": 10,
    "Lớn": 5
}
current_cell_size = default_cell_size

# Tính toán số lượng hàng và cột dựa trên kích thước ô hiện tại
cols = screen_width // current_cell_size
rows = (screen_height - 150) // current_cell_size  # Để lại thêm không gian cho nút kích thước

# Màu sắc
live_color = (255, 255, 255)  # Trắng
dead_color = (0, 0, 0)      # Đen
grid_color = (50, 50, 50)    # Xám

# Tạo màn hình
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Conway's Game of Life")

# Quản lý giao diện người dùng
manager = pygame_gui.UIManager((screen_width, screen_height))

# Vị trí các nút điều khiển
button_start = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, screen_height - 90), (100, 30)),
                                            text='Bắt đầu',
                                            manager=manager)
button_stop = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, screen_height - 90), (100, 30)),
                                           text='Dừng',
                                           manager=manager)
button_next = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((230, screen_height - 90), (100, 30)),
                                           text='Tiếp theo',
                                           manager=manager)
button_reset = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((340, screen_height - 90), (100, 30)),
                                            text='Đặt lại',
                                            manager=manager)

# Thanh trượt tốc độ
speed_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, screen_height - 50), (200, 30)),
                                                     start_value=200, value_range=(50, 1000),
                                                     manager=manager)
speed_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((220, screen_height - 50), (150, 30)),
                                          text='Tốc độ (ms): 200',
                                          manager=manager)

# Các nút chọn kích thước lưới
size_small_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, screen_height - 90), (100, 30)),
                                                 text='Nhỏ',
                                                 manager=manager)
size_medium_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((560, screen_height - 90), (100, 30)),
                                                  text='Trung bình',
                                                  manager=manager)
size_large_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((670, screen_height - 90), (100, 30)),
                                                 text='Lớn',
                                                 manager=manager)
size_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((450, screen_height - 130), (200, 30)),
                                          text='Kích thước lưới:',
                                          manager=manager)

# Tạo lưới ban đầu
grid = [[0 for _ in range(cols)] for _ in range(rows)]
simulation_running = False
update_interval = 200
last_update_time = 0

# Hàm để vẽ lưới
def draw_grid():
    for row in range(rows):
        for col in range(cols):
            color = live_color if grid[row][col] == 1 else dead_color
            pygame.draw.rect(screen, color, (col * current_cell_size, row * current_cell_size, current_cell_size - 1, current_cell_size - 1))
            pygame.draw.rect(screen, grid_color, (col * current_cell_size, row * current_cell_size, current_cell_size - 1, current_cell_size - 1), 1)

# Hàm để tính toán thế hệ tiếp theo của lưới
def update_grid():
    global grid, cols, rows
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            live_neighbors = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    neighbor_row = (row + i + rows) % rows
                    neighbor_col = (col + j + cols) % cols
                    live_neighbors += grid[neighbor_row][neighbor_col]

            if grid[row][col] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[row][col] = 0
                elif 2 <= live_neighbors <= 3:
                    new_grid[row][col] = 1
            else:
                if live_neighbors == 3:
                    new_grid[row][col] = 1
    grid = new_grid

# Hàm để thay đổi kích thước lưới
def change_grid_size(size_name):
    global current_cell_size, cols, rows, grid
    if size_name in grid_sizes:
        current_cell_size = grid_sizes[size_name]
        cols = screen_width // current_cell_size
        rows = (screen_height - 150) // current_cell_size
        grid = [[0 for _ in range(cols)] for _ in range(rows)]
        print(f"Kích thước lưới: {size_name} ({cols}x{rows}, ô {current_cell_size}px)")

# Vòng lặp chính của trò chơi
running = True
clock = pygame.time.Clock()

while running:
    time_delta = clock.tick(60) / 1000.0
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not simulation_running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y < screen_height - 150:  # Chỉ cho phép tương tác với lưới
                col = mouse_x // current_cell_size
                row = mouse_y // current_cell_size
                if 0 <= row < rows and 0 <= col < cols:
                    grid[row][col] = 1 - grid[row][col]
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button_start:
                simulation_running = True
                button_start.set_text('Tiếp tục')
                button_stop.enable()
                print("Bắt đầu/Tiếp tục mô phỏng")
            elif event.ui_element == button_stop:
                simulation_running = False
                button_start.set_text('Bắt đầu')
                button_stop.disable()
                print("Dừng mô phỏng")
            elif event.ui_element == button_next:
                if not simulation_running:
                    update_grid()
                    print("Tính toán thế hệ tiếp theo")
            elif event.ui_element == button_reset:
                simulation_running = False
                button_start.set_text('Bắt đầu')
                button_stop.disable()
                grid = [[0 for _ in range(cols)] for _ in range(rows)]
                print("Đặt lại lưới")
            elif event.ui_element == size_small_button:
                change_grid_size("Nhỏ")
            elif event.ui_element == size_medium_button:
                change_grid_size("Trung bình")
            elif event.ui_element == size_large_button:
                change_grid_size("Lớn")
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == speed_slider:
                update_interval = int(event.value)
                speed_label.set_text(f'Tốc độ (ms): {update_interval}')

        manager.process_events(event)

    if simulation_running:
        if current_time - last_update_time > update_interval:
            update_grid()
            last_update_time = current_time

    screen.fill(dead_color)
    draw_grid()
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()