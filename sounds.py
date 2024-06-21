import pygame
pygame.mixer.init()
pygame.mixer.music.set_volume(0.05)


class Sounds:
    engine_previous_value = None
    fuelling_status = None
    pygame.mixer.set_num_channels(11)
    channel = pygame.mixer.Channel(10)

    engine_sound = pygame.mixer.Sound("rsc/sounds/engine.wav")
    engine_sounds = {"slow": pygame.mixer.Sound("rsc/sounds/engine-slow.wav"), "normal": pygame.mixer.Sound("rsc/sounds/engine.wav"), "fast": pygame.mixer.Sound("rsc/sounds/engine-fast.wav")}
    player_missile_sound = pygame.mixer.Sound("rsc/sounds/player-missile.wav")
    player_missile_sound.set_volume(0.2)
    explosion_sound = pygame.mixer.Sound("rsc/sounds/explosion.wav")
    explosion_sound.set_volume(0.1)
    bridge_explosion_sound = pygame.mixer.Sound("rsc/sounds/bridge-explosion.ogg")
    bridge_explosion_sound.set_volume(0.2)
    enemy_missile_sound = pygame.mixer.Sound("rsc/sounds/enemy-missile.ogg")
    enemy_missile_sound.set_volume(0.1)
    tank_shell_sound = pygame.mixer.Sound("rsc/sounds/tank.wav")
    tank_shell_sound.set_volume(0.15)

    refuelling_sound = pygame.mixer.Sound("rsc/sounds/fuel-up.wav")
    refuelling_sound.set_volume(0.2)

    fuel_tank_is_full_sound = pygame.mixer.Sound("rsc/sounds/fuel-tank-filled.wav")
    fuel_tank_is_full_sound.set_volume(0.2)

    low_fuel_sound = pygame.mixer.Sound("rsc/sounds/low-fuel.wav")
    low_fuel_sound.set_volume(0.5)

    out_of_fuel_sound = pygame.mixer.Sound("rsc/sounds/out-of-fuel.wav")
    out_of_fuel_sound.set_volume(0.5)

    funfair_sound = pygame.mixer.Sound("rsc/sounds/funfair.wav")
    funfair_sound.set_volume(0.7)

    landed_sound = pygame.mixer.Sound("rsc/sounds/landed.ogg")
    landed_sound.set_volume(0.7)

    medal_sound = pygame.mixer.Sound("rsc/sounds/medal.ogg")
    medal_sound.set_volume(0.7)

    @staticmethod
    def music(play: bool):
        if play:
            pygame.mixer.music.load('rsc/sounds/music.ogg')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    @staticmethod
    def engine(speed):
        if speed == Sounds.engine_previous_value:
            return

        Sounds.engine_sound.stop()

        if not speed:
            return

        Sounds.engine_sound = Sounds.engine_sounds[speed]
        Sounds.engine_sound.set_volume(0.1)
        Sounds.engine_sound.play(-1)
        Sounds.engine_previous_value = speed

    @staticmethod
    def player_missile():
        Sounds.player_missile_sound.play()

    @staticmethod
    def explosion():
        Sounds.explosion_sound.play()

    @staticmethod
    def bridge_explosion():
        Sounds.bridge_explosion_sound.play()

    @staticmethod
    def enemy_missile():
        Sounds.enemy_missile_sound.play()

    @staticmethod
    def tank_shell():
        Sounds.tank_shell_sound.play()

    @staticmethod
    def refuelling():
        # interrupting "low fuel" sound when refuelling
        if Sounds.fuelling_status == "low fuel":
            Sounds.channel.stop()

        if not Sounds.channel.get_busy():
            Sounds.fuelling_status = "refuelling"
            Sounds.channel.play(Sounds.refuelling_sound)

    @staticmethod
    def low_fuel():
        if not Sounds.channel.get_busy():
            Sounds.fuelling_status = "low fuel"
            Sounds.channel.play(Sounds.low_fuel_sound)

    @staticmethod
    def fuel_tank_is_full():
        if not Sounds.channel.get_busy():
            Sounds.fuelling_status = "tank is full"
            Sounds.channel.play(Sounds.fuel_tank_is_full_sound)

    @staticmethod
    def out_of_fuel():
        # interrupting "low fuel" sound when refuelling
        Sounds.channel.stop()

        if not Sounds.channel.get_busy():
            Sounds.fuelling_status = "out of fuel"
            Sounds.channel.play(Sounds.out_of_fuel_sound)

    @staticmethod
    def funfair():
        # interrupting any other sounds on the channel
        Sounds.channel.stop()

        if not Sounds.channel.get_busy():
            Sounds.fuelling_status = "funfair"
            Sounds.channel.play(Sounds.funfair_sound)

    @staticmethod
    def medal():
        Sounds.medal_sound.play()

    @staticmethod
    def landed():
        Sounds.landed_sound.play()

    @staticmethod
    def anthem(play: bool):
        if play:
            pygame.mixer.music.load('rsc/sounds/anthem.oga')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(1)
        else:
            pygame.mixer.music.stop()
