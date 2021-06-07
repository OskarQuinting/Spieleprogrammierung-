import pygame
import os
from time import sleep
from random import random

class Board():
    def __init__(self, size, prob):
        self.size = size
        self.prob = prob
        self.lost = False
        self.numClicked = 0
        self.numNonBombs = 0
        self.setBoard()

        
    def setBoard(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                hasBomb = random() < self.prob
                if (not hasBomb):
                    self.numNonBombs += 1
                piece = Piece(hasBomb)
                row.append(piece)
            self.board.append(row)
        self.setNeighbors()

    def setNeighbors(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.getPiece((row, col))
                neighbors = self.getListOfNeighbors((row, col))
                piece.setNeighbors(neighbors)

    def getListOfNeighbors(self, index):
        neighbors = []
        for row in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                outOfBounds = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = row == index[0] and col == index[1]
                if (same or outOfBounds):
                    continue
                neighbors.append(self.getPiece((row, col)))
        return neighbors

    def getSize(self):
        return self.size

    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    def handleClick(self, piece, flag):
        if (piece.getClicked() or (not flag and piece.getFlagged())):
            return
        if (flag):
            piece.toggleFlag()
            return
        piece.click()
        if (piece.getHasBomb()):
            self.lost = True
            return
        self.numClicked += 1
        if (piece.getNumAround() != 0):
            return
        for neighbor in piece.getNeighbors():
            if (not neighbor.getHasBomb() and not neighbor.getClicked()):
                self.handleClick(neighbor, False)

    def getLost(self):
        return self.lost

    def getWon(self):
        return self.numNonBombs == self.numClicked

class Piece():
    def __init__(self, hasBomb):
        self.hasBomb = hasBomb
        self.clicked = False
        self.flagged = False

    def getHasBomb(self):
        return self.hasBomb

    def getClicked(self):
        return self.clicked

    def getFlagged(self):
        return self.flagged

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
        self.setNumAround()

    def setNumAround(self):
        self.numAround = 0
        for piece in self.neighbors:
            if (piece.getHasBomb()):
                self.numAround += 1

    def getNumAround(self):
        return self.numAround

    def toggleFlag(self):
        self.flagged = not self.flagged

    def click(self):
        self.clicked = True

    def getNeighbors(self):
        return self.neighbors

class Game():
	def __init__(self, board, screenSize):
		self.board = board
		self.screenSize = screenSize
		self.pieceSize = self.screenSize[0] // self.board.getSize() [1], self.screenSize[1] // self.board.getSize()[0]
		self.loadImages()

	def run(self):
		pygame.init()
		self.screen = pygame.display.set_mode(self.screenSize)
		running = True
		while running:
			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					running = False
				if (event.type == pygame.KEYDOWN):
					if (event.key == pygame.K_q):
						running = False
				if (event.type == pygame.MOUSEBUTTONDOWN):
					position = pygame.mouse.get_pos()
					rightClick = pygame.mouse.get_pressed()[2]
					self.handleClick(position, rightClick)
			self.draw()
			pygame.display.flip()
			if (self.board.getWon()):
				sound = pygame.mixer.Sound("win.wav")
				sound.play()
				sleep(3)
				running = False
#				if (input("Willst du noch eine Runde Spielen? Ja/Nein") == "Ja"):
#					os.execv(sys.argv[0], sys.argv)
#				else:
#					running = False
		pygame.QUIT()

	def draw(self):
		topLeft = (0, 0)
		for row in range(self.board.getSize() [0]):
			for col in range(self.board.getSize()[1]):
				piece = self.board.getPiece((row, col))
				image = self.getImage(piece)
				self.screen.blit(image, topLeft)
				topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
			topLeft = 0, topLeft[1] + self.pieceSize[1]

	def loadImages(self):
		self.images = {}
		for fileName in os.listdir("images"):
			if (not fileName.endswith(".png")):
				continue
			image = pygame.image.load(r"images/" + fileName)
			image = pygame.transform.scale(image, self.pieceSize)
			self.images[fileName.split(".") [0]] = image

	def getImage(self, piece):
		string = None
		if (piece.getClicked()):
			string = "bomb-at-clicked-block" if piece.getHasBomb() else str(piece.getNumAround())
		else:
			string = "flag" if piece.getFlagged() else "empty-block"
		return self.images[string]

	def handleClick(self, position, rightClick):
		if (self.board.getLost()):
			return
		index = position[1] // self.pieceSize[1], position[0] // self.pieceSize[0]
		piece = self.board.getPiece(index)
		self.board.handleClick(piece, rightClick)

        
if __name__ == '__main__':
    size = (9,9)
    prob = 0.1
    board = Board(size, prob)
    screenSize = (800, 800)
    game = Game(board, screenSize)
    game.run()