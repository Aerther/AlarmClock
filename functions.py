import os
import pygame

pygame.mixer.init()
# Function to play sound
def playSound(soundPath: str):
    sound = pygame.mixer.Sound(soundPath)
    sound.play()        

# Function to get the path of a file
def getPathFile(directory: str, fileName: str):
    return os.path.join(".", directory, fileName)