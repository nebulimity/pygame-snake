import pygame

# 1) pre-init at 44.1 kHz
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

# 2) load your converted mono/stereo WAV
pygame.mixer.music.load("mule.wav")
pygame.mixer.music.play()
print("▶ Playing at", pygame.mixer.get_init())  # should be (44100, -16, 2)
pygame.time.delay(2000)                          # let it play 2 s

# 3) restart at 88.2 kHz
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.mixer.init(frequency=88200, size=-16, channels=2)
pygame.mixer.music.load("mule.wav")
pygame.mixer.music.play()
print("▶ Now at", pygame.mixer.get_init())      # should be (88200, -16, 2)
pygame.time.delay(2000)