import pygame
import random
from enum import Enum

# 게임 상수
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 25
GAME_AREA_WIDTH = GRID_WIDTH * CELL_SIZE
GAME_AREA_HEIGHT = GRID_HEIGHT * CELL_SIZE
GAME_AREA_X = (SCREEN_WIDTH - GAME_AREA_WIDTH) // 2
GAME_AREA_Y = 50

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# 테트로미노 패턴 (회전 공식 포함)
TETROMINOES = {
    'I': {
        'color': CYAN,
        'shapes': [
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (0, 1), (0, 2), (0, 3)],
        ]
    },
    'O': {
        'color': YELLOW,
        'shapes': [
            [(0, 0), (1, 0), (0, 1), (1, 1)],
        ]
    },
    'T': {
        'color': MAGENTA,
        'shapes': [
            [(1, 0), (0, 1), (1, 1), (2, 1)],
            [(0, 0), (0, 1), (1, 1), (0, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
        ]
    },
    'S': {
        'color': GREEN,
        'shapes': [
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
        ]
    },
    'Z': {
        'color': RED,
        'shapes': [
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (0, 2)],
        ]
    },
    'J': {
        'color': BLUE,
        'shapes': [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(0, 0), (1, 0), (0, 1), (0, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 0)],
            [(1, 0), (1, 1), (0, 2), (1, 2)],
        ]
    },
    'L': {
        'color': ORANGE,
        'shapes': [
            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 0)],
            [(0, 0), (1, 0), (1, 1), (1, 2)],
        ]
    }
}

class GameState(Enum):
    PLAYING = 1
    GAME_OVER = 2
    PAUSED = 3

class Tetromino:
    def __init__(self, shape_type):
        self.shape_type = shape_type
        self.color = TETROMINOES[shape_type]['color']
        self.shapes = TETROMINOES[shape_type]['shapes']
        self.rotation = 0
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0

    def get_blocks(self):
        """현재 회전 상태의 블록 좌표 반환"""
        shape = self.shapes[self.rotation % len(self.shapes)]
        return [(self.x + x, self.y + y) for x, y in shape]

    def rotate(self):
        """테트로미노 회전"""
        self.rotation = (self.rotation + 1) % len(self.shapes)

    def move_left(self):
        """왼쪽으로 이동"""
        self.x -= 1

    def move_right(self):
        """오른쪽으로 이동"""
        self.x += 1

    def move_down(self):
        """아래로 이동"""
        self.y += 1

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # 게임 상태 초기화
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_tetromino = self._get_random_tetromino()
        self.next_tetromino = self._get_random_tetromino()
        self.state = GameState.PLAYING
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500  # 밀리초 단위

    def _get_random_tetromino(self):
        """랜덤 테트로미노 생성"""
        return Tetromino(random.choice(list(TETROMINOES.keys())))

    def _is_valid_position(self, tetromino, offset_x=0, offset_y=0):
        """테트로미노 위치가 유효한지 확인"""
        for x, y in tetromino.get_blocks():
            x += offset_x
            y += offset_y
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return False
            if y >= 0 and self.grid[y][x] != 0:
                return False
        return True

    def _place_tetromino(self):
        """테트로미노를 그리드에 배치"""
        for x, y in self.current_tetromino.get_blocks():
            if y >= 0:
                self.grid[y][x] = self.current_tetromino.color

    def _clear_lines(self):
        """완성된 라인 제거"""
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y][x] != 0 for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)

        for y in sorted(lines_to_clear, reverse=True):
            del self.grid[y]
            self.grid.insert(0, [0] * GRID_WIDTH)

        if lines_to_clear:
            cleared_count = len(lines_to_clear)
            self.lines_cleared += cleared_count
            self.score += cleared_count * cleared_count * 100
            self.level = 1 + self.lines_cleared // 10

    def _spawn_new_tetromino(self):
        """새 테트로미노 생성"""
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = self._get_random_tetromino()

        # 새 테트로미노가 스폰될 수 없으면 게임 오버
        if not self._is_valid_position(self.current_tetromino):
            self.state = GameState.GAME_OVER

    def handle_input(self):
        """입력 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_p:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                elif event.key == pygame.K_r and self.state == GameState.GAME_OVER:
                    self.__init__()  # 게임 재시작

            if self.state != GameState.PLAYING:
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self._is_valid_position(self.current_tetromino, offset_x=-1):
                        self.current_tetromino.move_left()
                elif event.key == pygame.K_RIGHT:
                    if self._is_valid_position(self.current_tetromino, offset_x=1):
                        self.current_tetromino.move_right()
                elif event.key == pygame.K_UP:
                    self.current_tetromino.rotate()
                    if not self._is_valid_position(self.current_tetromino):
                        self.current_tetromino.rotate()
                        self.current_tetromino.rotate()
                        self.current_tetromino.rotate()
                elif event.key == pygame.K_DOWN:
                    if self._is_valid_position(self.current_tetromino, offset_y=1):
                        self.current_tetromino.move_down()
                        self.score += 1

        return True

    def update(self, delta_time):
        """게임 로직 업데이트"""
        if self.state != GameState.PLAYING:
            return

        self.fall_time += delta_time

        # 테트로미노 자동 하강
        if self.fall_time >= self.fall_speed - (self.level - 1) * 50:
            self.fall_time = 0
            if self._is_valid_position(self.current_tetromino, offset_y=1):
                self.current_tetromino.move_down()
            else:
                self._place_tetromino()
                self._clear_lines()
                self._spawn_new_tetromino()

    def draw(self):
        """화면 그리기"""
        self.screen.fill(BLACK)

        # 게임 영역 테두리 그리기
        pygame.draw.rect(self.screen, WHITE, 
                        (GAME_AREA_X, GAME_AREA_Y, GAME_AREA_WIDTH, GAME_AREA_HEIGHT), 2)

        # 그리드에 배치된 블록 그리기
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] != 0:
                    pygame.draw.rect(self.screen, self.grid[y][x],
                                   (GAME_AREA_X + x * CELL_SIZE, 
                                    GAME_AREA_Y + y * CELL_SIZE, 
                                    CELL_SIZE - 1, CELL_SIZE - 1))

        # 현재 테트로미노 그리기
        if self.state != GameState.GAME_OVER:
            for x, y in self.current_tetromino.get_blocks():
                if y >= 0:
                    pygame.draw.rect(self.screen, self.current_tetromino.color,
                                   (GAME_AREA_X + x * CELL_SIZE, 
                                    GAME_AREA_Y + y * CELL_SIZE, 
                                    CELL_SIZE - 1, CELL_SIZE - 1))

        # 정보 표시 (오른쪽)
        info_x = GAME_AREA_X + GAME_AREA_WIDTH + 30
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (info_x, 50))

        level_text = self.font.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(level_text, (info_x, 100))

        lines_text = self.font.render(f'Lines: {self.lines_cleared}', True, WHITE)
        self.screen.blit(lines_text, (info_x, 150))

        # Next 테트로미노 표시
        next_label = self.small_font.render('Next:', True, WHITE)
        self.screen.blit(next_label, (info_x, 220))
        for x, y in self.next_tetromino.get_blocks():
            pygame.draw.rect(self.screen, self.next_tetromino.color,
                           (info_x + x * CELL_SIZE, 
                            250 + y * CELL_SIZE, 
                            CELL_SIZE - 1, CELL_SIZE - 1))

        # 게임 오버 메시지
        if self.state == GameState.GAME_OVER:
            game_over_text = self.font.render('GAME OVER', True, RED)
            self.screen.blit(game_over_text, (GAME_AREA_X + 50, GAME_AREA_Y + GAME_AREA_HEIGHT // 2 - 50))
            restart_text = self.small_font.render('Press R to Restart', True, WHITE)
            self.screen.blit(restart_text, (GAME_AREA_X + 80, GAME_AREA_Y + GAME_AREA_HEIGHT // 2))

        # 일시 정지 메시지
        if self.state == GameState.PAUSED:
            paused_text = self.font.render('PAUSED', True, YELLOW)
            self.screen.blit(paused_text, (GAME_AREA_X + 80, GAME_AREA_Y + GAME_AREA_HEIGHT // 2 - 50))

        # 조작 설명 (왼쪽)
        controls_y = GAME_AREA_Y + GAME_AREA_HEIGHT + 20
        controls = [
            "Controls:",
            "Arrow Keys: Move/Rotate",
            "Up Arrow: Rotate",
            "Down Arrow: Drop",
            "P: Pause/Resume",
            "ESC: Exit"
        ]
        for i, text in enumerate(controls):
            control_text = self.small_font.render(text, True, LIGHT_GRAY)
            self.screen.blit(control_text, (GAME_AREA_X, controls_y + i * 20))

        pygame.display.flip()

    def run(self):
        """게임 실행"""
        running = True
        while running:
            delta_time = self.clock.tick(60)  # 60 FPS
            running = self.handle_input()
            self.update(delta_time)
            self.draw()

        pygame.quit()

if __name__ == '__main__':
    game = TetrisGame()
    game.run()
