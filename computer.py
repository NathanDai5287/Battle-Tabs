from board import Board

import neat
import os
import random
import pickle

generation = 0

def fitness(genomes, config):
	
	global generation

	generation += 1

	nets = []
	players = []
	ge = []
	for genome_id, genome in genomes:
		genome.fitness = 0  # start with fitness level of 0
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)

		try:
			with open('boards.pkl', 'rb') as f:
				players.append(pickle.load(f))
		except EOFError:
			players.append(Board())
				
		
		ge.append(genome)

	for i, player in enumerate(players):
		output = 0
		# outputs = list(map(int, nets[i].activate((output))))

		# make a move
		if (any(0 <= i <= 6 for i in outputs)):
			if (0 <= outputs[0] <= 6):
				if (0 <= outputs[1] <= 6):
					score = player.guess(tuple(outputs))
				else:
					score = player.guess((outputs[0], random.randint(0, 6)))
			else:
				score = player.guess((random.randint(0, 6), outputs[1]))
		else:
			score = player.guess((random.randint(0, 6), random.randint(0, 6)))
		
		with open('boards.pkl', 'r+b') as f:
			pickle.dump(player, f)

		ge[i].fitness += score



def run(config):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config)
	population = neat.Population(config)
	population.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	population.add_reporter(stats)

	# Run for up to 50 generations.
	winner = population.run(fitness, 50)

	# show final stats
	print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config.txt')
	run(config_path)
