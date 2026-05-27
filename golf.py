import pygame
import time

#DO NOT TOUCH
window_x = 1000
window_y = 800

#define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
grey = pygame.Color(127, 127, 127)

green = pygame.Color(0, 255, 0)
yellow = pygame.Color(255, 255, 0)

lightgreen = pygame.Color(144, 238, 144)
darkgreen = pygame.Color(53, 94, 59)

orange = pygame.Color(255, 165, 0)
red = pygame.Color(255, 0, 0)

#create stuff
pygame.init()
# pygame.display.set_icon(pygame.image.load('flag.png'))
pygame.display.set_caption('GOLF')
game_window = pygame.display.set_mode((window_x, window_y))
bigfont = pygame.font.SysFont('Bahnschrift', 24)
smallfont = pygame.font.SysFont('Bahnschrift', 16)
fps = pygame.time.Clock()

#load materials (these dont exist yet)
# ball = pygame.image.load("ball.png")
# club = pygame.image.load("club.png")
# flag = pygame.image.load("flag.png")
# hole = pygame.image.load("hole.png")

#draw level -> take inputs
#inputs -> result -> see what happens
#ie. the ball is hit in x direction. move ball with fitting speed
#every tile the ball loses some speed. green = normal friction. yellow = double friction
#on hitting wall, change direction. lose some speed.
#detect goal -> go next level
#save list of scores
def game():
	result_list = ["ball_x", "ball_y", "hole_x", "hole_y"]
	ball = ["x", "y"]
	hole = ["x", "y"]
	level_completed = True
	level_number = 1
	swing_result = ["direction", "power"]
	ball_inertia = 0
	par = 0
	taken_swings = 0
	swings_list = ["this", "list", "needs", "n+1 entries", "where", "n=totallevels", "a", "b", "c", "lorem", "ipsum"]
	#main game loop
	while (1):
		#get inputs
		for event in pygame.event.get():
			if event.type == pygame.QUIT:  
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				#left mouse button
				if event.button == 1 and ball_inertia <= 0:
					swing_result = take_swing(ball[0], ball[1])
					taken_swings += 1
					#swing_result1 is power level
					ball_inertia = 123 * swing_result[1]
					#swing_result0 is direction
					direction = swing_result[0]
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_m:
					level_completed = True
					level_number += 1
					ball_inertia = 0

		#handle movement of ball
		if ball_inertia > 0:
			#this case is a wall collision
			if check_next_tile(ball[0], ball[1], direction) == black:
				#northwest
				if direction == 1:
					#case: tile left is wall. above clear. bounce up and to right 
					if check_next_tile(ball[0], ball[1], 4) == black and check_next_tile(ball[0], ball[1], 2) == green:
						ball[0] += 1.6
						ball[1] -= 1.6
						direction = 3
						ball_inertia *= 0.75
					#case: tile left is clear. above wall. bounce down and left
					elif check_next_tile(ball[0], ball[1], 4) == green and check_next_tile(ball[0], ball[1], 2) == black:
						ball[0] -= 1.6
						ball[1] += 1.6
						direction = 6
						ball_inertia *= 0.75
					#case: corner -> bounce right and down
					elif check_next_tile(ball[0], ball[1], 4) == black and check_next_tile(ball[0], ball[1], 2) == black:
						ball[0] += 1.6
						ball[1] += 1.6
						direction = 8
						ball_inertia *= 0.75

				#north
				elif direction == 2:
					ball[1] += 2
					direction = 7
					ball_inertia *= 0.75

				#northeast
				elif direction == 3:
					#case: tile right is wall. above clear. bounce up and to left
					if check_next_tile(ball[0], ball[1], 5) == black and check_next_tile(ball[0], ball[1], 2) == green:
						ball[0] -= 1.6
						ball[1] -= 1.6
						direction = 1
						ball_inertia *= 0.75
					#case: tile right is clear. above wall. bounce down and right
					elif check_next_tile(ball[0], ball[1], 5) == green and check_next_tile(ball[0], ball[1], 2) == black:
						ball[0] += 1.6
						ball[1] += 1.6
						direction = 8
						ball_inertia *= 0.75
					#case: corner -> bounce left and down
					elif check_next_tile(ball[0], ball[1], 5) == black and check_next_tile(ball[0], ball[1], 2) == black:
						ball[0] -= 1.6
						ball[1] += 1.6
						direction = 6
						ball_inertia *= 0.75
				#west
				elif direction == 4:
					ball[0] += 2
					direction = 5
					ball_inertia *= 0.75

				#east
				elif direction == 5:
					ball[0] -= 2
					direction = 4
					ball_inertia *= 0.75

				#southwest
				elif direction == 6:
					#case: tile left is wall. below clear. bounce down and to right
					if check_next_tile(ball[0], ball[1], 4) == black and check_next_tile(ball[0], ball[1], 7) == green:
						ball[0] += 1.6
						ball[1] += 1.6
						direction = 8
						ball_inertia *= 0.75
					#case: tile left is clear. below wall. bounce up and to left
					elif check_next_tile(ball[0], ball[1], 4) == green and check_next_tile(ball[0], ball[1], 7) == black:
						ball[0] -= 1.6
						ball[1] -= 1.6
						direction = 1
						ball_inertia *= 0.75
					#case: corner -> bounce right and up
					elif check_next_tile(ball[0], ball[1], 4) == black and check_next_tile(ball[0], ball[1], 7) == black:
						ball[0] += 1.6
						ball[1] -= 1.6
						direction = 3
						ball_inertia *= 0.75

				#south
				elif direction == 7:
					ball[1] -= 2
					direction = 2
					ball_inertia *= 0.75

				#southeast
				elif direction == 8:
					#case: tile right is wall. below clear. bounce down and to rleft
					if check_next_tile(ball[0], ball[1], 5) == black and check_next_tile(ball[0], ball[1], 7) == green:
						ball[0] -= 1.6
						ball[1] += 1.6
						direction = 6
						ball_inertia *= 0.75
					#case: tile right is clear. below wall. bounce up and to right
					elif check_next_tile(ball[0], ball[1], 5) == green and check_next_tile(ball[0], ball[1], 7) == black:
						ball[0] += 1.6
						ball[1] -= 1.6
						direction = 3
						ball_inertia *= 0.75
					#case: corner -> bounce right and down
					elif check_next_tile(ball[0], ball[1], 5) == black and check_next_tile(ball[0], ball[1], 7) == black:
						ball[0] -= 1.6
						ball[1] -= 1.6
						direction = 1
						ball_inertia *= 0.75

			#on yellow tiles we are in the bunker (SAND)
			#increase the distance less while updating the inertia in the same way
			elif check_next_tile(ball[0], ball[1], direction) == yellow:
				#northwest
				if direction == 1:
					ball[0] -= 0.8
					ball[1] -= 0.8
				#north
				elif direction == 2:
					ball[1] -= 1
				#northeast
				elif direction == 3:
					ball[0] += 0.8
					ball[1] -= 0.8
				#west
				elif direction == 4:
					ball[0] -= 1
				#east
				elif direction == 5:
					ball[0] += 1
				#southwest
				elif direction == 6:
					ball[0] -= 0.8
					ball[1] += 0.8
				#south
				elif direction == 7:
					ball[1] += 1
				#southeast
				elif direction == 8:
					ball[0] += 0.8
					ball[1] += 0.8

			elif check_next_tile(ball[0], ball[1], direction) == red:
				#track scores
				swings_list[level_number] = taken_swings
				#increment level
				level_number += 1
				#set this flag so we can do other things next loop
				level_completed = True
				#stop movement of ball
				ball_inertia = 0

			else:
				#northwest
				if direction == 1:
					ball[0] -= 1.6
					ball[1] -= 1.6
				#north
				elif direction == 2:
					ball[1] -= 2
				#northeast
				elif direction == 3:
					ball[0] += 1.6
					ball[1] -= 1.6
				#west
				elif direction == 4:
					ball[0] -= 2
				#east
				elif direction == 5:
					ball[0] += 2
				#southwest
				elif direction == 6:
					ball[0] -= 1.6
					ball[1] += 1.6
				#south
				elif direction == 7:
					ball[1] += 2
				#southeast
				elif direction == 8:
					ball[0] += 1.6
					ball[1] += 1.6

			#inertia (total energy) always decreases by 2
			#yellow tiles just move the ball less per 2 units of energy expended
			ball_inertia = ball_inertia - 2

		#check if new level
		if level_completed == True:
			level_completed = False
			taken_swings = 0
			result_list = get_info(level_number)
			hole[0] = result_list[2]
			hole[1] = result_list[3]
			ball[0] = result_list[0]
			ball[1] = result_list[1]
			par = result_list[4]

		game_window.fill(green)

		#if legal hole nr -> draw ball, walls and hole
		#change this if adding new level
		if level_number <= 10:
			#draw obstacles
			draw_walls(level_number)
			#draw ball
			pygame.draw.rect(game_window, white, pygame.Rect(int(ball[0]) - 5, int(ball[1]) - 5, 10, 10))
			#draw hole
			pygame.draw.rect(game_window, red, pygame.Rect(hole[0] - 15, hole[1] - 15, 30, 30))

		#change this if adding new level
		elif level_number > 10:
			i = 1
			while i != level_number: 
				game_text = smallfont.render("Hole " + str(i) + ": Player took " + str(swings_list[i]) + " swings." , True, red)
				game_surface = game_text.get_rect()
				game_surface.midtop = (250, 200 + i * 30)
				game_window.blit(game_text, game_surface)
				#hole in one
				if swings_list[i] == 1:
					extra_text = smallfont.render("HOLE IN ONE!!!!" , True, red)
					extra_surface = extra_text.get_rect()
					extra_surface.midtop = (450, 200 + i * 30)
					game_window.blit(extra_text, extra_surface)
				#albatross
				elif get_info(i)[4] - 3 == swings_list[i]:
					extra_text = smallfont.render("Albatross!!!" , True, red)
					extra_surface = extra_text.get_rect()
					extra_surface.midtop = (450, 200 + i * 30)
					game_window.blit(extra_text, extra_surface)
				#eagle
				elif get_info(i)[4] - 2 == swings_list[i]:
					extra_text = smallfont.render("Eagle!!" , True, red)
					extra_surface = extra_text.get_rect()
					extra_surface.midtop = (450, 200 + i * 30)
					game_window.blit(extra_text, extra_surface)
				#birdie
				elif get_info(i)[4] - 1 == swings_list[i]:
					extra_text = smallfont.render("Birdie!" , True, red)
					extra_surface = extra_text.get_rect()
					extra_surface.midtop = (450, 200 + i * 30)
					game_window.blit(extra_text, extra_surface)
				#par
				elif get_info(i)[4] == swings_list[i]:
					extra_text = smallfont.render("Par" , True, red)
					extra_surface = extra_text.get_rect()
					extra_surface.midtop = (450, 200 + i * 30)
					game_window.blit(extra_text, extra_surface)
				#bogey
				elif get_info(i)[4] + 1 == swings_list[i]:
					extra_text = smallfont.render("Bogey" , True, red)
					extra_surface = extra_text.get_rect()
					extra_surface.midtop = (450, 200 + i * 30)
					game_window.blit(extra_text, extra_surface)
				#double bogey
				elif get_info(i)[4] + 2 == swings_list[i]:
					extra_text = smallfont.render("Double Bogey" , True, red)
					extra_surface = extra_text.get_rect()
					extra_surface.midtop = (450, 200 + i * 30)
					game_window.blit(extra_text, extra_surface)
				i += 1

		#draw a border around the level
		pygame.draw.rect(game_window, black, pygame.Rect(0, 0, window_x, 75))
		pygame.draw.rect(game_window, black, pygame.Rect(0, 0, 75, window_y))
		pygame.draw.rect(game_window, black, pygame.Rect(0, window_y - 75, window_x, 75))
		pygame.draw.rect(game_window, black, pygame.Rect(window_x - 75, 0, 75, window_y))

		#seriously useful debug stuff 
		# def debug_info(ball, swing_result, ball_inertia):
		# 	clicked_text = smallfont.render("ball_x: " + str(ball[0]) + " ball_y: " + str(ball[1]), True, red)
		# 	clicked_text_2 = smallfont.render("power level: " + str(swing_result[1]) + " direction: " + str(swing_result[0]), True, red)
		# 	clicked_text_1 = smallfont.render("energy remaining: " + str(ball_inertia), True, red)
	
		# 	clicked_surface = clicked_text.get_rect()
		# 	clicked_surface_2 = clicked_text_2.get_rect()
		# 	clicked_surface_1 = clicked_text_1.get_rect()

		# 	clicked_surface.midtop = (window_x - 100, 0)
		# 	clicked_surface_2.midtop = (window_x - 100, 150)
		# 	clicked_surface_1.midtop = (window_x - 100, 75)

		# 	game_window.blit(clicked_text, clicked_surface)
		# 	game_window.blit(clicked_text_2, clicked_surface_2)
		# 	game_window.blit(clicked_text_1, clicked_surface_1)
		# debug_info(ball, swing_result, ball_inertia)

		#hole/par info
		hole_text = smallfont.render("Playing on hole " + str(level_number) + ".", True, red)
		hole_surface = hole_text.get_rect()
		hole_surface.midtop = (150, 15)
		game_window.blit(hole_text, hole_surface)

		shot_text = smallfont.render("Player took " + str(taken_swings) + " swings.", True, red)
		shot_surface = shot_text.get_rect()
		shot_surface.midtop = (150, 30)
		game_window.blit(shot_text, shot_surface)

		par_text = smallfont.render("Par for this hole is " + str(par) + " swings.", True, red)
		par_surface = par_text.get_rect()
		par_surface.midtop = (150, 45)
		game_window.blit(par_text, par_surface)

		fps.tick(24)
		pygame.display.flip()

#function to take a swing at the golf ball
#input coords correspond to the ball
#returns power of swing and direction of swing
def take_swing(x_coord, y_coord):
	return_value = ["direction", "power"]
	current_power = 1
	current_direction = 0
	clicked = 0

	while (1):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:  
				pygame.quit()
				quit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				#left mouse button
				if event.button == 1:
					if clicked == 0:
						clicked += 1
						return_value[0] = current_direction
					elif clicked == 1:
						return_value[1] = current_power
						return return_value
				#right mouse button cancels an input
				if event.button == 2:
					if clicked == 1:
						clicked -= 1

		current_direction = iterate_direction(current_direction)
		current_power = iterate_power(current_power)

		#draw direction
		if clicked == 0:
			#top left (diagonal)
			if current_direction == 1:
				pygame.draw.rect(game_window, green, pygame.Rect(x_coord + 15, y_coord + 15, 10, 10))
				pygame.draw.rect(game_window, grey, pygame.Rect(x_coord - 25, y_coord - 25, 10, 10))
			#top mid (up)
			elif current_direction == 2:
				pygame.draw.rect(game_window, green, pygame.Rect(x_coord - 25, y_coord - 25, 10, 10))
				pygame.draw.rect(game_window, grey, pygame.Rect(x_coord - 5, y_coord - 25, 10, 10))
			#top right diagonal
			elif current_direction == 3:
				pygame.draw.rect(game_window, green, pygame.Rect(x_coord - 5, y_coord - 25, 10, 10))
				pygame.draw.rect(game_window, grey, pygame.Rect(x_coord + 15, y_coord - 25, 10, 10))
			#left
			elif current_direction == 4:
				pygame.draw.rect(game_window, green, pygame.Rect(x_coord + 15, y_coord - 25, 10, 10))
				pygame.draw.rect(game_window, grey, pygame.Rect(x_coord - 25, y_coord - 5, 10, 10))
			#right
			elif current_direction == 5:
				pygame.draw.rect(game_window, green, pygame.Rect(x_coord - 25, y_coord - 5, 10, 10))
				pygame.draw.rect(game_window, grey, pygame.Rect(x_coord + 15, y_coord - 5, 10, 10))
			#bottom left (diagonal)
			elif current_direction == 6:
				pygame.draw.rect(game_window, green, pygame.Rect(x_coord + 15, y_coord - 5, 10, 10))
				pygame.draw.rect(game_window, grey, pygame.Rect(x_coord - 25, y_coord + 15, 10, 10))
			#bottom mid (down)
			elif current_direction == 7:
				pygame.draw.rect(game_window, green, pygame.Rect(x_coord - 25, y_coord + 15, 10, 10))
				pygame.draw.rect(game_window, grey, pygame.Rect(x_coord - 5, y_coord + 15, 10, 10))
			#bottom right diagonal
			elif current_direction == 8:
				pygame.draw.rect(game_window, green, pygame.Rect(x_coord - 5, y_coord + 15, 10, 10))
				pygame.draw.rect(game_window, grey, pygame.Rect(x_coord + 15, y_coord + 15, 10, 10))

		#draw power level
		elif clicked == 1:
			if current_power == 1:
				pygame.draw.rect(game_window, black, pygame.Rect(175, window_y - 50, 100, 25))
				pygame.draw.rect(game_window, lightgreen, pygame.Rect(150, window_y - 50, 25, 25))
			elif current_power == 2:
				pygame.draw.rect(game_window, black, pygame.Rect(200, window_y - 50, 75, 25))
				pygame.draw.rect(game_window, darkgreen, pygame.Rect(150, window_y - 50, 50, 25))
			elif current_power == 3:
				pygame.draw.rect(game_window, black, pygame.Rect(225, window_y - 50, 50, 25))
				pygame.draw.rect(game_window, yellow, pygame.Rect(150, window_y - 50, 75, 25))
			elif current_power == 4:
				pygame.draw.rect(game_window, black, pygame.Rect(250, window_y - 50, 25, 25))
				pygame.draw.rect(game_window, orange, pygame.Rect(150, window_y - 50, 100, 25))
			elif current_power == 5:
				pygame.draw.rect(game_window, red, pygame.Rect(150, window_y - 50, 125, 25))

		#comment this out for funny
		time.sleep(.333)
		pygame.display.flip()		

#helper function that iterates on the power level
#power levels as such
#dark green (1) -> light green -> yellow -> orange -> red (5)
def iterate_power(power):
	if power < 5:
		power += 1
	else:
		power = 1
	return power

#helper function that iterates on the direction
#where 1 is top left, 2 is top mid, 8 is bottom right, etc.
def iterate_direction(direction):
	if direction < 8:
		direction += 1
	else:
		direction = 1
	return direction

#function that checks the tile on a coordinate
#should eventually be used to get info about collision, friction, or if it's a hole etc.
def check_next_tile(x_coord, y_coord, direction):
	#northwest
	if direction == 1:
		color = game_window.get_at((x_coord - 15, y_coord - 15))
	#north
	elif direction == 2:
		color = game_window.get_at((x_coord - 5, y_coord - 15))
	#northeast
	elif direction == 3:
		color = game_window.get_at((x_coord + 5, y_coord - 15))
	#west
	elif direction == 4:
		color = game_window.get_at((x_coord - 15, y_coord - 5))
	#east
	elif direction == 5:
		color = game_window.get_at((x_coord + 5, y_coord - 5))
	#southwest
	elif direction == 6:
		color = game_window.get_at((x_coord - 15, y_coord + 5))
	#south
	elif direction == 7:
		color = game_window.get_at((x_coord - 5, y_coord + 5))
	#southeast
	elif direction == 8:
		color = game_window.get_at((x_coord + 5, y_coord + 5))
	return color

#function to get level info. returns ball starting coordinates, end hole coordinates and number of shots for a par.
def get_info(level_number):
	#structure of returned list is denoted here.
	return_value = ["ball_x", "ball_y", "hole_x", "hole_y", "par"]

	if level_number == 1:
		#start coordinates
		return_value[0] = 150
		return_value[1] = window_y / 2 - 50
		#end coordinates
		return_value[2] = window_x - 150
		return_value[3] = window_y / 2 + 50
		#par value
		return_value[4] = 3

	elif level_number == 2:
		#start coordinates
		return_value[0] = 150
		return_value[1] = window_y / 2
		#end coordinates
		return_value[2] = window_x - 150
		return_value[3] = window_y / 2
		#par value
		return_value[4] = 3

	elif level_number == 3:
		#start coordinates
		return_value[0] = 150
		return_value[1] = 150
		#end coordinates
		return_value[2] = window_x - 150
		return_value[3] = 150
		#par value
		return_value[4] = 4

	elif level_number == 4:
		#start coordinates
		return_value[0] = 150
		return_value[1] = window_y - 150
		#end coordinates
		return_value[2] = window_x - 150
		return_value[3] = 175
		#par value
		return_value[4] = 4

	elif level_number == 5:
		#spawn
		return_value[0] = 180
		return_value[1] = 150
		#flag
		return_value[2] = window_x - 230
		return_value[3] = window_y - 150
		#par
		return_value[4] = 3

	elif level_number == 6:
		#spawn
		return_value[0] = window_x - 200
		return_value[1] = 450
		#flag
		return_value[2] = 200
		return_value[3] = window_y - 150
		#par
		return_value[4] = 4
	
	elif level_number == 7:
		#spawn
		return_value[0] = (window_x / 2) + 75
		return_value[1] = (window_y / 2) - 75
		#flag
		return_value[2] = (window_x / 2) - 75
		return_value[3] = (window_y / 2) - 75
		#par
		return_value[4] = 4
	
	elif level_number == 8:
		#spawn
		return_value[0] = 3 * window_x / 14 - 75
		return_value[1] = 2.5 * (window_y / 7)  
		#flag
		return_value[2] = window_x - 3 * (window_x / 14) + 75
		return_value[3] = 2.5 * (window_y / 7)
		#par
		return_value[4] = 3

	elif level_number == 9:
		#spawn
		return_value[0] = 111
		return_value[1] = 111  
		#flag
		return_value[2] = window_x / 2
		return_value[3] = window_y / 2 - 50
		#par
		return_value[4] = 6

	elif level_number == 10:
		#spawn
		return_value[0] = window_x / 3 - 100
		return_value[1] = 5 * (window_y / 8)
		#flag
		return_value[2] = 8 * (window_x / 12) + 65
		return_value[3] = window_y - 275
		#par
		return_value[4] = 6

	return return_value

#this function draws the walls/tiles of the level
#every loop the field is refreshed with green tiles
#this draws black (or yellow) tiles where need be
def draw_walls(level_number):
	if level_number == 1:
		pygame.draw.rect(game_window, black, pygame.Rect(0, 0, window_x, window_y / 3))
		pygame.draw.rect(game_window, black, pygame.Rect(0, 2 * (window_y / 3), window_x, window_y / 3 ))
	elif level_number == 2:
		pygame.draw.rect(game_window, black, pygame.Rect(0, 0, window_x, window_y / 3))
		pygame.draw.rect(game_window, black, pygame.Rect(0, 2 * (window_y / 3), window_x, window_y / 3 ))
		pygame.draw.rect(game_window, yellow, pygame.Rect(4 * window_x / 10, window_y / 3 + (window_y / 12), window_x / 5, window_y / 6 ))
	elif level_number == 3:
		pygame.draw.rect(game_window, black, pygame.Rect((window_x / 2) - 10, 0, 30, window_y - 250))
	elif level_number == 4:
		pygame.draw.rect(game_window, black, pygame.Rect(0, 2 * (window_y / 3), 2 * (window_y / 3), 50))
		pygame.draw.rect(game_window, black, pygame.Rect(window_y / 2, (window_y / 3), 2 * (window_y / 3), 50))
	elif level_number == 5:
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 3 - 50, window_y / 2, window_x / 9, 50))
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 2, window_y / 2, window_x / 9, 50))
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 3 - 50, 0, 50, window_y / 2))
		pygame.draw.rect(game_window, black, pygame.Rect(2 * (window_y / 3) + 50, window_y / 2, 50, window_y / 2))
		pygame.draw.rect(game_window, yellow, pygame.Rect(window_x / 2, window_y / 6, window_x / 4, window_y / 5))
	elif level_number == 6:
		pygame.draw.rect(game_window, black, pygame.Rect((window_x / 3) - 30, window_y / 3, 30, window_y / 3 + 1))
		pygame.draw.rect(game_window, black, pygame.Rect(2 * (window_x / 3), window_y / 3, 30, window_y / 3 + 1))
		pygame.draw.rect(game_window, black, pygame.Rect(0, 2 * (window_y / 3), window_x / 3, 30))
		pygame.draw.rect(game_window, black, pygame.Rect(2 * (window_x / 3), 2 * (window_y / 3), window_x / 3, 30))
	elif level_number == 7:
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 2 - 20, 0, 40, 3 * (window_y / 4)))
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 4, window_y / 2 - 20, window_x / 2, 40))
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 4 - 20, window_y / 4, 40, window_y / 4))
		pygame.draw.rect(game_window, black, pygame.Rect(3 * (window_x / 4) - 20, window_y / 4, 40, window_y / 4))
	elif level_number == 8:
		pygame.draw.rect(game_window, black, pygame.Rect(75, 75, window_x, window_y / 7))
		pygame.draw.rect(game_window, black, pygame.Rect(1.5 * (window_x / 7), 1.5 *(window_y / 7), 4 * (window_x / 7), window_y / 7))
		pygame.draw.rect(game_window, black, pygame.Rect(2.5 * (window_x / 7), 2.5 *(window_y / 7), 2 * (window_x / 7), window_y / 7))
		pygame.draw.rect(game_window, black, pygame.Rect(3 * (window_x / 7), 3.5 *(window_y / 7) - 1, 1 * (window_x / 7), window_y / 7))
		pygame.draw.rect(game_window, black, pygame.Rect(75, window_y - 150, window_x, window_y / 7))
	elif level_number == 9:
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 6, 5 * (window_y / 7), 4 * (window_x / 6), 50))
		pygame.draw.rect(game_window, black, pygame.Rect((window_x / 6), 75, 50, 3 * (window_x / 6)))
		pygame.draw.rect(game_window, black, pygame.Rect(5 * (window_x / 6) - 51, 150, 50, 4 * (window_x / 9)))
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 6 + 125, 1.5 * (window_y / 7) - 21, 4 * (window_x / 6) - 125, 50))
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 6 + 125, 1.5 * (window_y/ 7) - 21, 50, 3 * (window_x / 9) - 25))
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 6 + 125, (window_y / 2) + 25, window_x / 2 - 105, 40))
		pygame.draw.rect(game_window, black, pygame.Rect(4 * (window_x / 6) - 30, 2 * (window_y / 7) + 50, 50, 3 * (window_x / 9) - 180))
	elif level_number == 10:
		pygame.draw.rect(game_window, black, pygame.Rect(0, 3 * (window_y / 4) - 20, window_x / 3 + 20, 40))
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 3 - 20, window_y / 2, 40, window_y / 4))

		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 5 - 7, window_y / 2 - 20, window_y / 5, 40))
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 3 - 20, window_y / 2, 40, window_y / 4))

		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 5 - 20, window_y / 4 + 20, 40, window_y / 4))
		pygame.draw.rect(game_window, black, pygame.Rect((window_x / 2) - 20, 0, 40, window_y - 150))

		pygame.draw.rect(game_window, yellow, pygame.Rect(window_x / 2 + 100, 150, (window_x / 5) + 50, window_y / 4))
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 2 + 150, window_y / 2 + 35, window_y / 5, 40))

		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 2 + 150, window_y / 2 + 35, 40, window_y / 4 + 100))
		pygame.draw.rect(game_window, black, pygame.Rect(window_x / 2 + 275, window_y / 2 + 35, 40, window_y / 4 - 50))
	return

game()