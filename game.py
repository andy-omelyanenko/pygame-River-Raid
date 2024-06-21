from pygame import *
import _globals
import intro
import status_bar
from sprites import *
from terrain import *
from sounds import *

pygame.init()
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SCALED if _globals.Debugging else pygame.FULLSCREEN | SCALED)
_globals.Screen = screen

pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
is_ESC_pressed: bool = False
the_Bridge = Bridge()

while not Player.is_ESC_pressed:
    intro.Intro()
    intro.wait_for_key_press()
    Sounds.music(False)

    if not Player.is_ESC_pressed:
        the_Player = Player(GAME_SCREEN_MIDDLE_X, GAME_SCREEN_HEIGHT - 12, the_Bridge)
        the_Carrier = None
        is_open_sea = False


        # Game Cycle that repeats for as long as the player has lives
        while not Player.Game_Over:
            Sounds.engine_previous_value = None
            Sounds.engine("normal")

            Player.is_flying = True
            Player.Fuel = 100
            the_Player_Missile = None
            Player_Missile.ready_to_fire = 0
            the_Player.rect.centerx = GAME_SCREEN_MIDDLE_X

            the_Bridge.Line = None
            the_Bridge.is_hit = False
            the_Bridge_Tank = None

            Helicopter.Count = 0
            Tank.Count = 0
            Jetcraft.Count = 0
            _globals.Enemy_Count = 0

            screen.fill((0, 0, 255))

            _globals.Line = _globals.Area * _globals.BRIDGE_LINE
            line_increment = 2

            Fuels = pygame.sprite.Group()

            Sprites = pygame.sprite.Group()
            _globals.Sprites = Sprites

            Enemy_Missiles = pygame.sprite.Group()
            _globals.Enemy_Missiles = Enemy_Missiles
            _globals.Scenery = pygame.sprite.Group()

            is_paused = False
            Player.player_has_crashed_counter = 0

            # The real gameplay cycle
            while Player.is_flying or Player.player_has_crashed_counter > 0:
                ticks_before = pygame.time.get_ticks()
                screen.fill((0, 0, 255))

                pressed = pygame.key.get_pressed()

                if pressed[K_LEFT] and not the_Player.is_landing:
                    the_Player.rect.x -= 3
                    if the_Player_Missile:
                        the_Player_Missile.rect.x -= 2

                if pressed[K_RIGHT] and not the_Player.is_landing:
                    the_Player.rect.x += 3
                    if the_Player_Missile:
                        the_Player_Missile.rect.x += 2

                if pressed[K_SPACE] and not the_Player.is_landing:
                    if not the_Player_Missile and Player.is_flying and pygame.time.get_ticks() > Player_Missile.ready_to_fire:
                        the_Player_Missile = Player_Missile(the_Player.rect.centerx, the_Player.rect.centery - 10)
                        Player_Missile.ready_to_fire = pygame.time.get_ticks() + 120

                for event in pygame.event.get():
                    if event.type == QUIT:
                        Player.is_flying = False
                        Player.Game_Over = True
                        is_ESC_pressed = True

                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            Player.is_flying = False
                            Player.Game_Over = True

                        if event.key == K_RETURN and _globals.Debugging:
                            pygame.display.toggle_fullscreen()

                        if event.key == K_UP and not the_Player.is_landing:
                            line_increment = 3

                        if event.key == K_DOWN and not the_Player.is_landing:
                            line_increment = 1

                    if event.type == KEYUP:
                        if event.key == K_DOWN or event.key == K_UP:
                            line_increment = 2
                        else:
                            if event.key == K_PAUSE or event.key == K_END or event.key == K_p:
                                is_paused = not is_paused
                                if is_paused:
                                    Sounds.engine(None)
                                else:
                                    # on resuming after pause we'll have to set previous sound to None or False
                                    # otherwise it'll wrongly think it's still playing "normal" speed sound (which it's not)
                                    Sounds.engine_previous_value = None

                if is_paused:
                    pygame.time.wait(250)
                    continue

                is_no_bridge_interference = BRIDGE_LINE - (_globals.Line % BRIDGE_LINE + GAME_SCREEN_HEIGHT) > SETTLEMENT_LINES
                is_island = Island_Left[_globals.Line + GAME_SCREEN_HEIGHT - 12] is not None
                x_correction = calculate_correction_to_MIDDLE_X(_globals.Line + GAME_SCREEN_HEIGHT - 12)
                river_width = River_Width[_globals.Line + GAME_SCREEN_HEIGHT - 12]

                # Drawing the terrain
                if not is_open_sea:
                    for i in range(GAME_SCREEN_HEIGHT + 1):  # To investigate why +1 makes sense
                        if Terrain_Left[_globals.Line + i] > 0:
                            pygame.draw.line(screen, (0, 255, 00), (0, GAME_SCREEN_HEIGHT - i), (Terrain_Left[_globals.Line + i], GAME_SCREEN_HEIGHT - i))
                            pygame.draw.line(screen, (0, 255, 00), (Terrain_Right[_globals.Line + i], GAME_SCREEN_HEIGHT - i), (GAME_SCREEN_WIDTH - 1, GAME_SCREEN_HEIGHT - i))
                            if Island_Left[_globals.Line + i] is not None:
                                pygame.draw.line(screen, (0, 255, 00), (Island_Left[_globals.Line + i], GAME_SCREEN_HEIGHT - i), (Island_Right[_globals.Line + i], GAME_SCREEN_HEIGHT - i))

                    # Drawing terrain scenery
                    if River_Width[_globals.Line + GAME_SCREEN_HEIGHT] <= 220 and _globals.Line % 30 == 0 and random.randint(0, 3) == 1 and is_no_bridge_interference and Player.is_flying:
                        x = random.randint(0, 86)
                        if random.randint(1, 2) == 1:
                            x = GAME_SCREEN_WIDTH - x
                        _globals.Scenery.add(Mountain(x, 0))

                max_rnd = 7 if _globals.Area < 10 else 15
                rnd = random.randint(0, max_rnd)

                # Spawning enemy sprites
                _flg_enemy_spawned = False
                if _globals.Line % 35 == 0 and rnd in [0, 1, 2, 5, 6, 7, 8, 9, 10, 11] and Player.is_flying and River_Width[_globals.Line + GAME_SCREEN_HEIGHT - 12] >= 30 \
                        and is_no_bridge_interference and _globals.Area < _globals.FINAL_AREA:
                    if not is_island:
                        x = GAME_SCREEN_MIDDLE_X + random.randint(0, 31) - 15
                    else:
                        if random.randint(1, 2) == 1:
                            x = GAME_SCREEN_MIDDLE_X - 62
                        else:
                            x = GAME_SCREEN_MIDDLE_X + 62
                    if rnd == 0 or River_Width[_globals.Line + GAME_SCREEN_HEIGHT - 12] < 80:
                        the_sprite = Balloon(x + x_correction, 0)
                    else:
                        if rnd == 1:
                            the_sprite = Ship(x + x_correction, 0)
                        else:
                            the_sprite = Helicopter(x + x_correction, 0)

                    if not the_sprite.is_colliding_with_terrain():
                        Sprites.add(the_sprite)
                        _flg_enemy_spawned = True

                # Spawning Fuel
                if _globals.Line % 35 == 0 and ((rnd in [3, 4]) or (_globals.Line - Fuel_Tank.most_recently_added_at_line > GAME_SCREEN_HEIGHT * 2) and not _flg_enemy_spawned) \
                        and River_Width[_globals.Line + GAME_SCREEN_HEIGHT - 12] >= 30 and is_no_bridge_interference and Player.is_flying and not the_Carrier:
                    spread = river_width - 20
                    x = GAME_SCREEN_MIDDLE_X + random.randint(0, spread) - spread // 2
                    sprite = Fuel_Tank(x + x_correction, 0)
                    if not sprite.is_colliding_with_terrain():
                        Fuels.add(sprite)
                        Fuel_Tank.most_recently_added_at_line = _globals.Line

                if Player.is_flying:
                    fuels_colliding_with_player = pygame.sprite.spritecollide(the_Player, Fuels, dokill=False)
                    if fuels_colliding_with_player:
                        if Player.Fuel < 100:
                            Player.Fuel += 1
                            Sounds.refuelling()
                        else:
                            Sounds.fuel_tank_is_full()

                # Spawning an enemy jetcraft
                if Jetcraft.Count < _globals.Area // 5 and is_no_bridge_interference and _globals.Line % 50 == 1 and random.randint(0, 7) == 1 and _globals.Area < _globals.FINAL_AREA:
                    Sprites.add(Jetcraft())

                max_tanks = 0
                if 1 <= _globals.Area <= 2:
                    max_tanks = 1
                elif 3 <= _globals.Area <= 6:
                    max_tanks = 2
                elif 7 <= _globals.Area <= 10:
                    max_tanks = 3
                elif 11 <= _globals.Area < 20:
                    max_tanks = 4
                elif _globals.Area >= 21:
                    max_tanks = 5

                # Spawning a stationary Tank
                if not the_Carrier and Tank.Count < max_tanks and River_Width[_globals.Line + GAME_SCREEN_HEIGHT] <= 300 and _globals.Line % 30 == 0 and random.randint(0, 3) == 1 and is_no_bridge_interference \
                        and Player.is_flying:
                    direction = random.randint(0, 1) + 1
                    if direction == 1:
                        x = Terrain_Left[_globals.Line + GAME_SCREEN_HEIGHT] - 25
                    else:
                        x = Terrain_Right[_globals.Line + GAME_SCREEN_HEIGHT] + 25
                    _globals.Scenery.add(Tank(x, 0, direction, is_moving=False, is_in_battle_mode=True))

                enemies_player_crashed_into = pygame.sprite.spritecollide(the_Player, Sprites, dokill=False)
                player_is_hit_by_missiles = pygame.sprite.spritecollide(the_Player, Enemy_Missiles, dokill=False)
                if (the_Player.is_colliding_with_terrain() or enemies_player_crashed_into or player_is_hit_by_missiles or the_Player.is_crashed_into_the_bridge()) and Player.is_flying:
                    the_Player.has_just_crashed()
                    for sprite in enemies_player_crashed_into:
                        sprite.kill()
                        _globals.Scenery.add(Explosion(sprite.rect.centerx, sprite.rect.centery))

                # enemies get killed by "friendly fire"
                enemy_casualties = enemies_hit_by_enemy_missiles = pygame.sprite.groupcollide(Sprites, Enemy_Missiles, True, True)
                for sprite in enemy_casualties:
                    _globals.Scenery.add(Explosion(sprite.rect.centerx, sprite.rect.centery))
                    Sounds.explosion()

                # Approaching the Bridge
                if the_Bridge not in _globals.Scenery and not the_Carrier and _globals.Line % BRIDGE_LINE >= BRIDGE_LINE - GAME_SCREEN_HEIGHT + the_Bridge.rect.height // 2:
                    _bridge_line = _globals.Line + GAME_SCREEN_HEIGHT - the_Bridge.rect.height // 2
                    x_bridge_correction = calculate_correction_to_MIDDLE_X(_bridge_line)
                    the_Bridge.rect.center = (GAME_SCREEN_MIDDLE_X + x_bridge_correction, 0)
                    the_Bridge.Line = _globals.Line + GAME_SCREEN_HEIGHT + SETTLEMENT_LINES - the_Bridge.rect.height // 2
                    the_Bridge.is_hit = False
                    the_Bridge.prepare()
                    _globals.Scenery.add(the_Bridge)
                    the_Bridge_Tank = Tank(0, 5 if _globals.Area == _globals.FINAL_AREA - 1 else 10, 1)
                    the_Bridge_Tank.is_on_the_bridge_line = True
                    the_Bridge_Tank.firing_distance = BRIDGE_WIDTH * 2
                    Sprites.add(the_Bridge_Tank)

                    if _globals.Area == _globals.FINAL_AREA - 1:
                        # Krimskiy Bridge
                        _globals.Scenery.add(Bridge_Sign(GAME_SCREEN_MIDDLE_X + x_bridge_correction - 150, -50))

                if the_Player_Missile:
                    sprites_hit_by_player_missile = pygame.sprite.spritecollide(the_Player_Missile, Sprites, dokill=True)
                    fuels_hit_by_player_missile = pygame.sprite.spritecollide(the_Player_Missile, Fuels, dokill=True)
                    combined_objects_hit_by_player_missile = sprites_hit_by_player_missile + fuels_hit_by_player_missile
                    if combined_objects_hit_by_player_missile:
                        # Player missile must have hit an object
                        the_Player_Missile = None
                        Sounds.explosion()
                        for sprite in combined_objects_hit_by_player_missile:
                            _globals.Scenery.add(Explosion(sprite.rect.centerx, sprite.rect.centery))
                            Player.Score += sprite.Points
                            # Extra life for 10000 points
                            if Player.Score >= Player.next_extra_life_points:
                                Player.next_extra_life_points = Player.Score + Player.points_for_extra_life
                                Player.Lives += 1
                                Sounds.funfair()

                if the_Player_Missile:
                    screen.blit(the_Player_Missile.image, the_Player_Missile.rect)
                    the_Player_Missile.rect.centery -= 12
                    if the_Player_Missile.rect.bottom <= 0 or the_Player_Missile.is_colliding_with_terrain():
                        the_Player_Missile = None
                    if the_Bridge in _globals.Scenery and not the_Bridge.is_hit and the_Player_Missile:
                        the_Bridge.is_hit = pygame.sprite.collide_rect(the_Bridge, the_Player_Missile)
                        if the_Bridge.is_hit:
                            the_Bridge.prepare()
                            the_Player_Missile = None
                            _globals.Area += 1
                            Sounds.bridge_explosion()
                            a = the_Bridge.rect.centerx - BRIDGE_WIDTH // 2
                            b = the_Bridge.rect.centerx + BRIDGE_WIDTH // 2
                            x = a
                            while x <= b:
                                _globals.Scenery.add(Explosion(x, the_Bridge.rect.centery + 8, 100))
                                x += 20
                            if abs(the_Bridge_Tank.rect.centerx - GAME_SCREEN_MIDDLE_X) <= BRIDGE_WIDTH - 25:
                                # the Bridge Tank is hit along with the Bridge
                                Player.Score += 1000
                                the_Bridge_Tank.kill()
                            else:
                                # the Bridge is hit but the tank isn't
                                Player.Score += 500
                                the_Bridge_Tank.is_in_battle_mode = (the_Bridge_Tank.rect.centerx < GAME_SCREEN_MIDDLE_X and the_Bridge_Tank.direction == 1) or \
                                                                    (GAME_SCREEN_MIDDLE_X < the_Bridge_Tank.rect.centerx and the_Bridge_Tank.direction == -1)
                                the_Bridge_Tank.is_moving = not the_Bridge_Tank.is_in_battle_mode

                _globals.Scenery.draw(screen)
                Sprites.draw(screen)
                Fuels.draw(screen)
                Enemy_Missiles.draw(screen)
                if Player.is_flying:
                    the_Player.update()
                    screen.blit(the_Player.image, the_Player.rect)

                if Player.is_flying:
                    if (_globals.Line > _globals.FINAL_LINE) and not Player.has_landed:
                        # Well Done!
                        Player.has_landed = True
                        Sounds.engine(False)
                        intro.Congratulations()
                        Player.is_flying = False
                        Player.Game_Over = True

                    if not Player.has_landed:
                        _globals.Line += line_increment
                    is_open_sea = (_globals.Line - _globals.GAME_SCREEN_HEIGHT * 3) // _globals.BRIDGE_LINE >= 26
                    if not the_Carrier and _globals.Line >= _globals.CARRIER_LINE:
                        the_Carrier = Carrier()
                        _globals.Scenery.add(the_Carrier)
                        if Player.Fuel < 75:
                            Player.Fuel = 75
                        Player.is_landing = True
                        Player.landing_countdown = 70

                    if not Player.has_landed:
                        if line_increment == 2:
                            Sounds.engine("normal")
                        else:
                            if line_increment > 2:
                                Sounds.engine("fast")
                            else:
                                Sounds.engine("slow")

                        Player.Fuel -= 0.06
                        if Player.Fuel < 25:
                            Sounds.low_fuel()
                        if Player.Fuel <= 0:
                            Sounds.out_of_fuel()
                            the_Player.has_just_crashed()
                else:
                    Player.player_has_crashed_counter -= 1

                if not Player.has_landed:
                    for sprite in Sprites:
                        if Player.is_flying:
                            sprite.rect.center = [sprite.rect.centerx, sprite.rect.centery + line_increment]
                        sprite.update()
                        if sprite.rect.centery > GAME_SCREEN_HEIGHT:
                            sprite.kill()

                    for sprite in Fuels:
                        if Player.is_flying:
                            sprite.rect.center = [sprite.rect.centerx, sprite.rect.centery + line_increment]
                        if sprite.rect.centery > GAME_SCREEN_HEIGHT:
                            sprite.kill()

                    for sprite in _globals.Scenery:
                        if Player.is_flying:
                            sprite.rect.center = [sprite.rect.centerx, sprite.rect.centery + line_increment]
                        sprite.update()
                        if (sprite.rect.centery > GAME_SCREEN_HEIGHT) and (sprite != the_Carrier):
                            sprite.kill()

                    for sprite in Enemy_Missiles:
                        if Player.is_flying:
                            sprite.rect.center = [sprite.rect.centerx, sprite.rect.centery + line_increment]
                        sprite.update()


                # Status bar
                status_bar.fill_with_black()
                status_bar.display_lives()
                status_bar.display_score()
                status_bar.display_fuel()
                status_bar.display_area()

                pygame.display.update()
                # Forcing FPS limit
                ticks_elapsed = pygame.time.get_ticks() - ticks_before
                pygame.time.wait(1000 // 52 - ticks_elapsed)
                # print(ticks_elapsed)

                # end of game control cycle

        Sounds.engine(False)

pygame.quit()
