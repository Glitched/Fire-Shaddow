import pygame
import baseCharacter
import enemy
from board import *

pygame.init()

# Game Dimensions
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 704

# initialisation of components
game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Fire & Shadow')
clock = pygame.time.Clock()

player_dead = False

projectiles_array = []
enemies_array = []

# movement related mechanics
player_x = DISPLAY_WIDTH / 2
player_y = DISPLAY_HEIGHT / 2

dx = 0
dy = 0

# Making player
player = baseCharacter.Wizard(player_x, player_y, 20, 100, 100, 100, 100, 100, 100)
prevDir = constants.RIGHT

frame = 0
seconds = 0
score = 0



while not player_dead:
	frame += 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			player_dead = True

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_a:
				dx = -constants.CHAR_SPEED
				player.flipScript("a")
				prevDir = constants.LEFT
			elif event.key == pygame.K_d:
				dx = constants.CHAR_SPEED
				player.flipScript("d")
				prevDir = constants.RIGHT
			if event.key == pygame.K_w:
				dy = -constants.CHAR_SPEED
				player.flipScript("w")
			elif event.key == pygame.K_s:
				dy = constants.CHAR_SPEED
				player.flipScript("s")

			if event.key == pygame.K_SPACE:
				# Change image to attack image, fire shot, both based on direction
				# this function will return a projectile object
				projectiles_array.append(player.attack())

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a or event.key == pygame.K_d:
				dx = 0
			elif event.key == pygame.K_w or event.key == pygame.K_s:
				dy = 0

			if event.key == pygame.K_SPACE:
				player.attack_flip(prevDir)

	if frame >= 24:
		seconds += 1
		frame = 0
	if frame == 0 or frame == 12:
		location = enemy.random_spawn_location(DISPLAY_WIDTH, DISPLAY_HEIGHT)
		enemies_array.append(enemy.Zombie(location[0], location[1]))

	player_x += dx
	player_y += dy
	if player_x >= DISPLAY_WIDTH - constants.TILE_SIZE:
		player_x = DISPLAY_WIDTH - constants.TILE_SIZE
	if player_x <= 0:
		player_x = 0
	if player_y >= DISPLAY_HEIGHT - constants.TILE_SIZE:
		player_y = DISPLAY_HEIGHT - constants.TILE_SIZE
	if player_y <= 0:
		player_y = 0

	# handle projectile stuff

	for proj in projectiles_array:
		if proj.getX() >= DISPLAY_WIDTH \
			or proj.getX() <= 0 \
			or proj.getY() >= DISPLAY_HEIGHT \
			or proj.getY() <= 0:

			projectiles_array.remove(proj)
		else:
			proj.update(game_display)
			for badguy in enemies_array:
				if abs((proj.getX()) - badguy.x - 32) < 20 and abs((proj.getY()) - badguy.y + 32) < 20:
					badguy.health -= proj.damage
					projectiles_array.remove(proj)
					if badguy.health <= 0:
						enemies_array.remove(badguy)
						score += 1
					break

	for badguy in enemies_array:
		badguy.update(player_x, player_y)
		if abs(badguy.x - player.x) < 20 and abs(badguy.y - player.y) < 20:
			player.health -= badguy.damage

	player.setX(player_x)
	player.setY(player_y)

	draw_board(DISPLAY_WIDTH, DISPLAY_HEIGHT, game_display, player, enemies_array, projectiles_array)

	pygame.display.update()
	clock.tick(24)

	if player.health <= 0:
		player_dead = True

print(score)
pygame.quit()
quit()
