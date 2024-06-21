from _globals import *
import random


# this is very unnecessary: initially I thought of using "a procedural generation" but then changed my mind and went just to using random
def bytes_generator():
    while True:
        yield random.randint(0, 255)


_byte_generator_instance = bytes_generator()

Terrain_Left = [None] * 100000
Terrain_Right = [None] * 100000
River_Width = [None] * 100000
Island_Left = [None] * 100000
Island_Right = [None] * 100000

width = 200
island_width = 0
x_offset = 0
target_width = None
state = ""
N_width = 0
N_x_offset = 0
N_island_width = 0
islands_gap_counter = 0
direction = 0


def calculate_correction_to_MIDDLE_X(line):
    # negative value indicates that the right side of the terrain is wider than the left one
    # positive value indicates that the left side of the terrain is wider than the right one
    # the value can be conveniently added to GAME_SCREEN_MIDDLE_X in order to obtain adjusted X position of an object that must be in the center of the game screen
    return (Terrain_Left[line] + River_Width[line] // 2) - GAME_SCREEN_MIDDLE_X


for Terrain_Line in range(100000):
    N_lines_to_the_next_bridge = (BRIDGE_LINE - SETTLEMENT_LINES) - (Terrain_Line % BRIDGE_LINE)
    Area = Terrain_Line // BRIDGE_LINE
    is_open_sea = Area >= 26

    if islands_gap_counter > 0:
        islands_gap_counter -= 1

    if Area <= 2:
        islands_gap = 3 * GAME_SCREEN_HEIGHT

    if Area in [3, 4, 5]:
        islands_gap = 2 * GAME_SCREEN_HEIGHT

    if Area > 5:
        islands_gap = GAME_SCREEN_HEIGHT // 2

    if N_lines_to_the_next_bridge > GAME_SCREEN_HEIGHT * 2 and N_width == 0 and width >= 230 and N_island_width == 0 and (next(_byte_generator_instance) % 10 == 1) \
            and islands_gap_counter == 0 and Terrain_Line >= GAME_SCREEN_HEIGHT * 3 and Area > 0 and not is_open_sea:
        # spawning an island!
        island_height = random.randint(40, GAME_SCREEN_HEIGHT - SETTLEMENT_LINES + Area * 5)
        if island_height > GAME_SCREEN_HEIGHT:
            island_height = GAME_SCREEN_HEIGHT
        N_island_width = island_height
        island_max_width = random.randint(20, 80)
        if Area <= 2 and island_max_width > 40:
            island_max_width = 40
        island_bottom_width = random.randint(10, island_max_width)
        island_top_width = random.randint(10, island_max_width)

    if N_x_offset <= 0:
        # no active x_offest adjustments
        direction = next(_byte_generator_instance) % 3 - 1
        N_x_offset = next(_byte_generator_instance) % MAX_TERRAIN_X_OFFSET // 2 + 1

    x_offset += direction * (next(_byte_generator_instance) % 2 + 1)
    N_x_offset -= 1

    if abs(x_offset) > MAX_TERRAIN_X_OFFSET:
        direction = -direction
        if direction == 0:
            N_x_offset = 3
        else:
            N_x_offset = next(_byte_generator_instance) % MAX_TERRAIN_X_OFFSET // 2 + 1

    # If no Island is on the terrain
    if N_island_width == 0:
        #  Setting a new width
        if (next(_byte_generator_instance) % 185 == 1) and N_width == 0:
            width_addition = 160 if Area >= 8 else random.randint(161, 230)

            if Area >= 15:
                v1 = 240
                v2 = 110
            else:
                v1 = 250
                v2 = 100

            target_width = (next(_byte_generator_instance) % v1) - v2 + width_addition
            if N_lines_to_the_next_bridge <= SETTLEMENT_LINES * 10 and target_width < BRIDGE_WIDTH * 2:
                target_width = BRIDGE_WIDTH * 3
            state = "Occasional change to width"
            N_width = SETTLEMENT_LINES

            if is_open_sea:
                target_width = GAME_SCREEN_WIDTH
                N_width = SETTLEMENT_LINES * 2
                x_offset = 0
                state = "Open sea"

        # Approaching the bridge
        if N_lines_to_the_next_bridge <= SETTLEMENT_LINES * 4:
            state = "Adjusting width"
            N_width = SETTLEMENT_LINES * 4
            target_width = BRIDGE_WIDTH * 5
            x_offset = calculate_correction_to_MIDDLE_X(Terrain_Line - 1) // (SETTLEMENT_LINES * 4)
            N_x_offset = SETTLEMENT_LINES * 4 * 4  # to be re-visited

        # Approached the bridge
        if N_lines_to_the_next_bridge <= SETTLEMENT_LINES:
            state = "Approaching the Bridge"
            N_width = SETTLEMENT_LINES
            target_width = BRIDGE_WIDTH

        # Flying over the bridge
        if N_width == 0 and state == "Approaching the Bridge":
            state = "Flying over the Bridge"
            N_width = SETTLEMENT_LINES * 2
            target_width = BRIDGE_WIDTH

        # Just flew over the bridge
        if N_width == 0 and state == "Flying over the Bridge":
            state = "Just flew over the Bridge"
            N_width = SETTLEMENT_LINES
            target_width = (next(_byte_generator_instance) % 180) - 90 + 200
    else:
        # Island generation loop
        if N_island_width == island_height:
            # Island's bottom line
            island_width = island_bottom_width
        else:
            if N_island_width == 1:
                # Island's top line
                island_width = island_top_width
            else:
                island_width = random.randint((island_top_width + island_bottom_width) // 2, island_max_width)

        Island_Left[Terrain_Line] = GAME_SCREEN_MIDDLE_X - island_width // 2 + x_offset
        Island_Right[Terrain_Line] = GAME_SCREEN_MIDDLE_X + island_width // 2 + x_offset

        N_island_width -= 1
        if N_island_width == 0:
            islands_gap_counter = islands_gap

    # Adjusting the new width
    if N_width > 0 and target_width:
        width_increment = (target_width - width) // N_width
        width += width_increment
        N_width -= 1
        if width == target_width:
            width_increment = 0

    if is_open_sea:
        x_offset = 0

    Terrain_Left[Terrain_Line] = GAME_SCREEN_MIDDLE_X - width // 2 + x_offset
    Terrain_Right[Terrain_Line] = GAME_SCREEN_MIDDLE_X + width // 2 + x_offset
    River_Width[Terrain_Line] = width
