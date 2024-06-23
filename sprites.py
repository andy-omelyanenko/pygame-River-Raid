import _globals
import random
import terrain
from sounds import *
import pygame


class Player(pygame.sprite.Sprite):
    Lives: int = None
    Score: int = 0
    is_flying: bool = None
    Game_Over: bool = False
    player_has_crashed_counter: int = None
    Fuel: float = None
    points_for_extra_life: int = 10000
    next_extra_life_points: int = None
    is_landing: bool = False
    has_landed: bool = False
    landing_countdown: int = None
    landing_x: int = _globals.GAME_SCREEN_MIDDLE_X - 58
    is_ESC_pressed: bool = False

    def __init__(self, x, y, the_Bridge):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("rsc/images/player.png").convert_alpha()
        self.the_Bridge = the_Bridge

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        _globals.Area = 0 if not _globals.Debugging else 23
        Player.Lives = 5
        Player.Score = 0
        Player.next_extra_life_points = Player.Score + Player.points_for_extra_life
        Player.Game_Over = False
        Player.is_landing = False
        Player.has_landed = False
        Player.is_ESC_pressed = False

    def is_colliding_with_terrain(self):
        left_middle_coordinates = (self.rect.left, self.rect.center[1])
        right_middle_coordinates = (self.rect.right, self.rect.center[1])

        c1 = _globals.Screen.get_at(left_middle_coordinates)
        c2 = _globals.Screen.get_at(right_middle_coordinates)
        return (c1[0] == 0 and c1[1] == 255 and c1[2] == 0) or (c2[0] == 0 and c2[1] == 255 and c2[2] == 0)

    def is_crashed_into_the_bridge(self):
        if self.the_Bridge not in _globals.Scenery:
            return False
        return pygame.sprite.collide_rect(self.the_Bridge, self) and not self.the_Bridge.is_hit

    def has_just_crashed(self):
        Player.is_flying = False
        Player.player_has_crashed_counter = 130
        Player.Lives -= 1
        Player.Game_Over = Player.Lives <= 0
        Sounds.engine(False)
        Sounds.explosion()
        _globals.Scenery.add(Explosion(self.rect.centerx, self.rect.centery, 250))

    def update(self):
        if self.rect.left < 10:
            self.rect.left = 10
        elif self.rect.right > _globals.GAME_SCREEN_WIDTH - 10:
            self.rect.right = _globals.GAME_SCREEN_WIDTH - 10

        if Player.is_landing:
            if Player.landing_countdown > 0:
                x_delta = Player.landing_x - self.rect.centerx
                self.rect.centerx += x_delta // Player.landing_countdown
                Player.landing_countdown -= 1


class Player_Missile(pygame.sprite.Sprite):
    ready_to_fire: int = None

    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.image.load("rsc/images/player_missile.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        Sounds.player_missile()

    def is_colliding_with_terrain(self):
        if self.rect.top <= 1:
            return True
        top_coordinates = (self.rect.left, self.rect.top)
        c1 = _globals.Screen.get_at(top_coordinates)
        return c1[0] == 0 and c1[1] == 255 and c1[2] == 0


class Bridge(pygame.sprite.Sprite):
    def __init__(self):
        # Calling the parent class (Sprite) constructor
        super().__init__()

        self.frames = []
        self.frames.append(pygame.image.load("rsc/images/bridge.png").convert_alpha())
        self.frames.append(pygame.image.load("rsc/images/bridge_hit.png").convert_alpha())
        self.frames.append(pygame.image.load("rsc/images/bridge_C.png").convert_alpha())
        self.is_hit = False
        self.image = self.frames[0]
        self.rect = self.image.get_rect()

    def prepare(self):
        if self.is_hit:
            self.image = self.frames[1]
        else:
            self.image = self.frames[2] if _globals.Area == _globals.FINAL_AREA - 1 else self.frames[0]


class Bridge_Sign(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.frames = []
        self.frames.append(pygame.image.load("rsc/images/bridge_sign.png").convert_alpha())
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Ship(pygame.sprite.Sprite):
    Points = 100

    def __init__(self, x, y):
        super().__init__()
        self.screen = _globals.Screen
        self.direction = 1 if random.randint(1, 2) == 1 else -1
        self.holding_frames = random.randint(0, 400 - _globals.Area * 5) if _globals.Area > 0 else 5000
        self.frames = []
        self.frames.append(pygame.image.load("rsc/images/ship1.png").convert_alpha())
        self.frames.append(pygame.image.load("rsc/images/ship2.png").convert_alpha())
        self.current_frame = 0 if self.direction == 1 else 1
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        _globals.Enemy_Count += 1

    def is_colliding_with_terrain(self):
        left_middle_coordinates = (self.rect.left, self.rect.center[1])
        right_middle_coordinates = (self.rect.right, self.rect.center[1])
        center_coordinates = (self.rect.centerx, self.rect.centery)

        if self.direction == -1:
            c = self.screen.get_at(left_middle_coordinates)
        else:
            c = self.screen.get_at(right_middle_coordinates)
        c2 = self.screen.get_at(center_coordinates)
        return (c[0] == 0 and c[1] == 255 and c[2] == 0) or (c2[0] == 0 and c2[1] == 255 and c2[2] == 0)

    def update(self):
        if self.holding_frames > 0:
            self.holding_frames -= 1
            return
        self.rect.x += self.direction
        if self.is_colliding_with_terrain():
            self.direction = -self.direction
            self.current_frame = 0 if self.direction == 1 else 1
            self.image = self.frames[self.current_frame]

    def kill(self):
        super().kill()
        _globals.Enemy_Count -= 1


class Balloon(pygame.sprite.Sprite):
    Points = 50

    def __init__(self, x, y):
        super().__init__()
        self.screen = _globals.Screen
        self.image = pygame.image.load("rsc/images/balloon.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = 1 if random.randint(1, 2) == 1 else -1
        self.holding_frames = random.randint(0, 400 - _globals.Area * 5) if _globals.Area > 0 else 5000
        _globals.Enemy_Count += 1

    def is_colliding_with_terrain(self):
        left_middle_coordinates = (self.rect.left, self.rect.center[1])
        right_middle_coordinates = (self.rect.right, self.rect.center[1])

        if self.direction == -1:
            c = self.screen.get_at(left_middle_coordinates)
        else:
            c = self.screen.get_at(right_middle_coordinates)
        return c[0] == 0 and c[1] == 255 and c[2] == 0

    def update(self):
        if self.holding_frames > 0:
            self.holding_frames -= 1
            return
        self.rect.x += self.direction
        if self.is_colliding_with_terrain():
            self.direction = -self.direction

    def kill(self):
        super().kill()
        _globals.Enemy_Count -= 1


class Enemy_Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.direction = direction
        self.image = pygame.image.load("rsc/images/enemy_missile.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        Sounds.enemy_missile()

    def is_colliding_with_terrain(self):
        line = _globals.Line + _globals.GAME_SCREEN_HEIGHT - self.rect.centery - 1
        return (self.rect.centerx < terrain.Terrain_Left[line] + 7) or (self.rect.centerx > terrain.Terrain_Right[line] - 7) \
               or (self.rect.top < 0) or (self.rect.bottom > _globals.GAME_SCREEN_HEIGHT - 1) \
               or (terrain.Island_Left[line] and ((self.direction == 1 and self.rect.centerx > terrain.Island_Left[line]) or (self.direction == -1 and self.rect.centerx < terrain.Island_Right[line])))

    def update(self):
        if self.is_colliding_with_terrain():
            self.kill()
        else:
            self.rect.centerx += self.direction * 9


class Jetcraft(pygame.sprite.Sprite):
    Points = 200
    Count = 0

    def __init__(self):
        super().__init__()
        self.direction = 1 if random.randint(1, 2) == 1 else -1
        self.frames = []
        self.frames.append(pygame.image.load("rsc/images/jetcraft1.png").convert_alpha())
        self.frames.append(pygame.image.load("rsc/images/jetcraft2.png").convert_alpha())
        self.current_frame = 0 if self.direction == 1 else 1
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        y = random.randint(0, _globals.GAME_SCREEN_HEIGHT * 2 // 3)
        x = 0 if self.direction == 1 else _globals.GAME_SCREEN_WIDTH - 1
        self.rect.center = (x, y)
        Jetcraft.Count += 1

    def update(self):
        self.rect.x += self.direction * 3

    def kill(self):
        super().kill()
        Jetcraft.Count -= 1


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, frames_to_live=20):
        super().__init__()
        self.frames_to_live = frames_to_live
        self.frames = []
        self.frames.append(pygame.image.load("rsc/images/explosion1.png").convert_alpha())
        self.frames.append(pygame.image.load("rsc/images/explosion2.png").convert_alpha())
        self.frames.append(pygame.image.load("rsc/images/explosion3.png").convert_alpha())
        self.current_frame = random.randint(0, 2)
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if self.frames_to_live <= 0:
            self.kill()
        else:
            self.frames_to_live -= 1
            self.current_frame = random.randint(0, 2)
            self.image = self.frames[self.current_frame]


class Helicopter(pygame.sprite.Sprite):
    Count = 0
    Points = 150

    def __init__(self, x, y):
        super().__init__()
        self.screen = _globals.Screen
        self.direction = 1 if random.randint(1, 2) == 1 else -1
        self.holding_frames = random.randint(0, 400 - _globals.Area * 4) if _globals.Area > 0 else 5000
        self.frames = []
        self.frames.append(pygame.image.load("rsc/images/helicopter1.png").convert_alpha())
        self.frames.append(pygame.image.load("rsc/images/helicopter2.png").convert_alpha())
        self.frames.append(pygame.image.load("rsc/images/helicopter3.png").convert_alpha())
        self.frames.append(pygame.image.load("rsc/images/helicopter4.png").convert_alpha())
        self.current_frame = 0 if self.direction == 1 else 2
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        Helicopter.Count += 1
        _globals.Enemy_Count += 1

    def is_colliding_with_terrain(self):
        left_middle_coordinates = (self.rect.left, self.rect.center[1])
        right_middle_coordinates = (self.rect.right, self.rect.center[1])

        c1 = self.screen.get_at(left_middle_coordinates)
        c2 = self.screen.get_at(right_middle_coordinates)

        return (c1[0] == 0 and c1[1] == 255 and c1[2] == 0) or (c2[0] == 0 and c2[1] == 255 and c2[2] == 0)

        # if self.direction == -1:
        #     c = self.screen.get_at(left_middle_coordinates)
        # else:
        #     c = self.screen.get_at(right_middle_coordinates)
        # return c[0] == 0 and c[1] == 255 and c[2] == 0

    def update(self):
        if self.holding_frames > 0:
            self.holding_frames -= 1
        else:
            self.rect.x += self.direction
            if self.is_colliding_with_terrain():
                self.direction = -self.direction
                if self.direction == 1:
                    self.current_frame = 0
                else:
                    self.current_frame = 3

        if _globals.Area >= 4 and random.randint(0, 80) == 1:
            _globals.Enemy_Missiles.add(Enemy_Missile(self.rect.centerx + self.direction * 12, self.rect.centery, self.direction))

        if pygame.time.get_ticks() % 2 == 0:
            return
        self.current_frame += 1
        if self.current_frame == 2:
            self.current_frame = 0
        if self.current_frame == 4:
            self.current_frame = 2
        self.image = self.frames[self.current_frame]

    def kill(self):
        super().kill()
        _globals.Enemy_Count -= 1
        Helicopter.Count -= 1


class Tank(pygame.sprite.Sprite):
    Count = 0
    max_firing_range = int(_globals.BRIDGE_WIDTH * 1.5)
    min_firing_range = _globals.BRIDGE_WIDTH - 20

    def __init__(self, x, y, direction, is_moving=True, is_in_battle_mode=False):
        super().__init__()
        self.screen = _globals.Screen
        self.firing_distance = random.randint(Tank.min_firing_range, Tank.max_firing_range + 1)
        self.direction = 1 if direction == 1 else -1
        self.is_in_battle_mode = is_in_battle_mode
        self.is_moving = is_moving
        self.is_firing = False
        self.is_on_the_bridge_line = False
        self.frames = []
        self.frames.append(pygame.image.load("rsc/images/tank1.png").convert_alpha())
        self.frames.append(pygame.image.load("rsc/images/tank2.png").convert_alpha())
        self.frames.append(pygame.image.load("rsc/images/tank3.png").convert_alpha())
        self.frames.append(pygame.image.load("rsc/images/tank4.png").convert_alpha())
        self.current_frame = 0 if self.direction == 1 else 2
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        Tank.Count += 1

    def update(self):
        if self.is_in_battle_mode:
            if (not self.is_firing) and (random.randint(0, 120) == 1):
                if self.direction == 1:
                    # shooting to the right
                    tank_shell = Tank_Shell(self.rect.right, self.rect.centery - 7, self.rect.right + self.firing_distance, self)
                else:
                    # shooting to the left
                    tank_shell = Tank_Shell(self.rect.left, self.rect.centery - 7, self.rect.left - self.firing_distance, self)
                _globals.Scenery.add(tank_shell)
                self.is_firing = True
                Sounds.tank_shell()
        else:
            # if it's not in battle mode then it must be moving
            if self.is_moving:
                self.rect.x += self.direction * 2

        # checking if the tank has finished its march
        if (self.rect.right <= 0) or (self.rect.right >= _globals.GAME_SCREEN_WIDTH - 1):
            self.kill()
            return

        # chassis animation
        if pygame.time.get_ticks() % 3 != 0:
            return
        self.current_frame += 1
        if self.current_frame == 2:
            self.current_frame = 0
        elif self.current_frame == 4:
            self.current_frame = 2
        self.image = self.frames[self.current_frame]

    def kill(self):
        super().kill()
        Tank.Count -= 1


class Tank_Shell(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, tank, frames_to_live=55):
        super().__init__()
        self.frames_in_flight = frames_to_live - 20
        self.x = x
        self.y = y
        self.target_x = target_x
        self.tank = tank
        self.frames_to_live = frames_to_live
        self.current_frame = 0
        self.has_reached_the_destination = False

        self.image = pygame.Surface((10, 10))
        self.image.set_colorkey((0, 0, 0))
        self.rect = pygame.draw.circle(self.image, (255, 255, 255), (3, 3), 1, 1)
        self.rect.center = (x, y)
        _globals.Screen.blit(self.image, self.rect)

    def update(self):
        # if (self.current_frame >= self.frames_to_live) or (self.x >= self.target_x):
        if self.current_frame >= self.frames_to_live:
            self.kill()
            self.tank.is_firing = False
        else:
            if self.current_frame <= self.frames_in_flight:
                delta_x = (self.target_x - self.x) // 10
                self.x += delta_x
                self.rect.center = (self.x, self.rect.centery)
            else:
                self.x = self.target_x
                radius = self.current_frame - self.frames_in_flight
                self.y = self.rect.centery

                if not self.has_reached_the_destination:
                    self.has_reached_the_destination = True
                    _globals.Scenery.remove(self)
                    _globals.Enemy_Missiles.add(self)

                self.image = pygame.Surface((2 * radius + 1, 2 * radius + 1))
                self.image.set_colorkey((0, 0, 0))
                self.rect = pygame.draw.circle(self.image, (255, 255, 255), (radius + 1, radius + 1), radius, radius)
                self.rect.center = (self.x, self.y)

            self.current_frame += 1


class Mountain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("rsc/images/scenery_big.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Fuel_Tank(pygame.sprite.Sprite):
    Points = 50
    most_recently_added_at_line = 0

    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        self.frames.append(pygame.image.load("rsc/images/fuel.png").convert_alpha())
        self.current_frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def is_colliding_with_terrain(self):
        c1 = _globals.Screen.get_at((self.rect.centerx, self.rect.centery))
        c2 = _globals.Screen.get_at((self.rect.left, self.rect.centery))
        c3 = _globals.Screen.get_at((self.rect.right, self.rect.centery))

        return (c1[0] == 0 and c1[1] == 255 and c1[2] == 0) or (c2[0] == 0 and c2[1] == 255 and c2[2] == 0) or (c3[0] == 0 and c3[1] == 255 and c3[2] == 0)


class Carrier(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("rsc/images/Carrier.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.centerx = _globals.GAME_SCREEN_MIDDLE_X
