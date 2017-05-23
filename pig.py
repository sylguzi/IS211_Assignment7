#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 7 pig game"""
from abc import ABCMeta, abstractmethod
import argparse
#import sys
import random

ROLL = 'r'
HOLD = 'h'
VALID_CHOICE = [ROLL, HOLD]
END_OF_GAME_SCORE = 100

random.seed(0)

class Die(object):
	def roll(self):
		return random.randint(1, 6)

class Player(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def make_decision(self):
		raise NotImplementedError('this is not implemented')

class HumanPlayer(Player):
	def make_decision(self):
		msg = ''
		while True:
			choice = raw_input(msg)
			if choice in VALID_CHOICE:
				return choice
			else:
				msg = 'Please enter \'{}\' or \'{}\': '.format(ROLL, HOLD)

class AIPlayer(Player):
	def make_decision(self):
		return HOLD

class Game(object):
	def __init__(self, human_players = 2, ai_players = 0):
		self.human_players = human_players
		self.ai_players = ai_players
		self.reset()
	
	def reset(self):
		self.die = Die()
		self.players = \
			[HumanPlayer() for x in range(self.human_players)] \
			+ [AIPlayer() for x in range(self.ai_players)]
		self.net_score = [0 for x in range(self.human_players + self.ai_players)]
		self.current_turn_score = 0
		self.player_turn_index = 0
		self.max_player = self.human_players + self.ai_players
	
	def add_turn_score(self, score):
		self.current_turn_score += score
		self.net_score[self.player_turn_index] += score

	def hold_score(self):
		# self.net_score[self.player_turn_index] += self.current_turn_score
		self.current_turn_score = 0

	def is_end_game(self):
		if any(score >= END_OF_GAME_SCORE for score in self.net_score):
			print 'Player {} won!'.format(self.player_turn_index + 1)
			self.reset()
			return True
		else:
			return False

	def next_player(self):
		self.current_turn_score = 0
		self.player_turn_index = (self.player_turn_index + 1) % self.max_player

	def apply_rule(self, choice):
		player_name = self.player_turn_index + 1
		if choice == HOLD:
			self.hold_score()
			print 'Player {} net score is now {}'.format(
				player_name, self.net_score[self.player_turn_index])
			self.next_player()
		elif choice == ROLL:
			roll = self.die.roll()
			print 'Player {} rolled {}'.format(player_name, roll)
			if roll == 1:
				self.add_turn_score(-self.current_turn_score)
				self.next_player()
				print 'Player {} lost turn'.format(player_name)
			else:
				self.add_turn_score(roll)
				print 'Player {} scored {} for this turn and net {}'.format(
					player_name,
					self.current_turn_score,
					self.net_score[self.player_turn_index])
		print ''

	def run(self):
		msg = 'Would you like to roll or hold? [{}/{}] '.format(ROLL, HOLD)
		while not self.is_end_game():
			print 'It\'s the turn of player {}.'.format(self.player_turn_index + 1)
			print msg
			choice = self.players[self.player_turn_index].make_decision()
			self.apply_rule(choice)

		return self.player_turn_index

def parseArg():
	parser = argparse.ArgumentParser(description='Pig game.')
	parser.add_argument('--numPlayers', help='how many players?', required=False)
	parser.add_argument('--multiGame', help='how many rounds?', required=False)
	return parser.parse_args()

if __name__ == '__main__':
	params = parseArg()
	try:
		parsedNumPlayers = int(params.numPlayers)
		numPlayers = parsedNumPlayers if parsedNumPlayers >= 2 else 2
	except:
		numPlayers = 2

	try:
		parsedMultiGame = int(params.multiGame)
		multiGame = parsedMultiGame if parsedMultiGame >= 1 else 1
	except:
		multiGame = 1

	round = 0
	winner_round = [0 for _ in range(numPlayers)]

	while round < multiGame:
		game = Game(numPlayers)
		winner_index = game.run()
		winner_round[winner_index] += 1
		round += 1

	for (i, score) in enumerate(winner_round):
		print 'Player {} won {} times'.format(i + 1, score)