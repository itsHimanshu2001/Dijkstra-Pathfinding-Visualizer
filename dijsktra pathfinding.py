from typing import DefaultDict
import pygame
import math
from queue import PriorityQueue
from collections import defaultdict

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))    #display area 
pygame.display.set_caption("A* Path Finding Algorithm")

#color defined using RGB
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):   #spot in a cell 
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):  #draws the rectangular cell of the defined color
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):   #this stores all the neighbours for a node in neighbors list
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):   #lower than function
		return False


def h(p1, p2):   #heuristic function (manhattan function) to calc shortest distance bw two points
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, start, current, draw):
	while current in came_from:
		if(came_from[current] == start):  # i dont want start node to get colored with purple so i stopped it earlier
			break
		current = came_from[current]
		current.make_path()   #first we define the color for the current coordinate/cell
		draw()   #then we call draw function which make a rect of defined rectangle of the x,y(top left corner) to width,width (bottom right corner)[in this case we left it blank because we changed the color of current already and only need to draw it]
		#note: if we want to draw a rect then we need top left coord and bottom right coord 


def algorithm(draw, grid, start, end):     #A* algo implementation

    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    d = defaultdict(lambda: float("inf")) #map which stores infinite by default
    d[start] = 0
    visited = {start} #set
    came_from = {}  #dictionary

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit

        current = open_set.get()[2]
        visited.remove(current)  #it will store which nodes have been visited(which node is in pq)

        if current == end:
            reconstruct_path(came_from, start,end,draw)
            end.make_end()
            return True

        for nbr in current.neighbors:
            node_dist = d[current] + 1

            if node_dist < d[nbr]:
                came_from[nbr] = current
                d[nbr] = node_dist
                if nbr not in visited:
                    count+=1
                    open_set.put((d[nbr],count,nbr))
                    visited.add(nbr)
                    nbr.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False    
	

def make_grid(rows, width):    #defines the structure of grid and insert spots in each rows
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)  #i,j is coordinate where we insert the spot(where coloring is done) ; gap is width of the each cell and rows defines total_rows in grid
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):  #draw the gridlines in the grid
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))  #for horizontal girdlines
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))  #for vertical guidlines


def draw(win, grid, rows, width):   #main function for drawing the whole grid
	win.fill(WHITE)                  #fill window with white color whole

	for row in grid:              #build the grid
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)  #call gridlines builder 
	pygame.display.update()    #update the changes on window display


def get_clicked_pos(pos, rows, width):  #returns the col and row posn when clicked on a certain coordinate by mouse
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50  #no of rows
	grid = make_grid(ROWS, width)  

	start = None   #coordinate of starting point
	end = None    #coord of destination

	run = True    #how long does the program will take input (run tells that we can give inputs and if our algo is running run = False for the time being)
	while run:
		draw(win, grid, ROWS, width) #make the whole grid by calling draw each time the loop runs so that it looks like it is there the whole time
		for event in pygame.event.get():  #events getter
			if event.type == pygame.QUIT:  #if esc then we stop the loop
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT MOUSE CLICK
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end: #first we check if we have marked start or not ; start and end must not be at same posn
					start = spot
					start.make_start()

				elif not end and spot != start: #then destination
					end = spot
					end.make_end()

				elif spot != end and spot != start: #if both start and end is marked then we mark obstacles
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT MOUSE CLICK
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()   #right click removes the spot at that coord
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)