# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import *
import random
import math

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
        tempState = state;
        for i in range(0,len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                break;
        # returns random action from all the valide actions
        return self.actionList[0];

class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,5):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
		flag = True
		possible = state.getAllPossibleActions();
		for i in range(0,len(self.actionList)):
			self.actionList[i] = possible[random.randint(0,len(possible)-1)];
		tempState = state;
		for i in range(0,len(self.actionList)):
			if tempState.isWin() + tempState.isLose() == 0:
				tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
			else:
				break;
		score_check = scoreEvaluation(tempState)
		while(flag):
			temp_actionList = self.actionList[:]
			for i in range(0,len(temp_actionList)):
				if random.choice([True, False]):
					temp_actionList[i] = possible[random.randint(0,len(possible)-1)]
				else:
					break;
			tempState = state
			for i in range(0,len(temp_actionList)):
				if tempState.isWin() + tempState.isLose() == 0:
					temp_tempState = tempState
					tempState = tempState.generatePacmanSuccessor(temp_actionList[i])
					if(tempState == None):
						flag = False
						tempState = temp_tempState
						break
				else :
					break

			temp_score_check = scoreEvaluation(tempState)
			if(score_check > temp_score_check):
				self.actionList = self.actionList[:]
			else :
				self.actionList = temp_actionList[:]
				score_check = temp_score_check
		return self.actionList[0]

class GeneticAgent(Agent):

	def registerInitialState(self, state):
		self.actionList = [[0 for x in range(5)] for y in range(8)];
		for i in range(0,8):
			for y in range(0,5):
				self.actionList[i][y] = Directions.STOP;
		return
	#Fitness Function
	def getFitness(self,Listaction,state):
		fitness = []
		ranking = []
		flag = True
		tempState = state
		for i in range(0, len(Listaction)):
			for j in range(0,len(Listaction[i])):
				if tempState.isWin() + tempState.isLose() == 0:
					temporary_state = tempState
					tempState = tempState.generatePacmanSuccessor(Listaction[i][j])
					if tempState == None:
						flag = False
						break
				else:
					break
			if tempState == None:
				flag = False
				break
			else:
				fitness.append((scoreEvaluation(tempState)))
		if not flag:
			number = 36
			return Listaction,fitness,flag,number
		else:	
			fitness = sorted(fitness, key = int)
			number = (len(fitness)*(len(fitness)+1))/2
			for i in range(0, len(fitness)):
				ranking.append(i+1)
	
			return Listaction,fitness,flag,number
	# Rank Function
	def getRank(self, number):
		if number >=28 and number < 36:
			return 7
		elif number >=21 and number < 28:
			return 6
		elif number >=15 and number < 21:
			return 5
		elif number >=10 and number < 15:
			return 4
		elif number >=6 and number < 10:
			return 3
		elif number >=3 and number < 6:
			return 2
		elif number >=1 and number < 3:
			return 1
		else:
			return 0
	#Crossover function
	def getCrossover(self,actionList, num1,num2):
		child1 = []
		child2 = []
		if (random.randint(0,70) > 70):
			return actionList[num1],actionList[num2]
		else :
			for i in range(0,5):
				num = random.randint(0,50)
				if(num < 50):
					child1.append(actionList[num1][i])
					child2.append(actionList[num2][i])
				else:
					child1.append(actionList[num2][i])
					child2.append(actionList[num1][i])
		return child1,child2
	
	#Mutation function
	def getMutation(self,ChildrenList,possible):
		for i in range(0,len(ChildrenList)):
			for y in range(0,len(ChildrenList[i])):
				num = random.randint(0,10)
				if(num <= 1):
					ChildrenList[i][y] = possible[random.randint(0,len(possible)-1)]
		return ChildrenList
	
	def getAction(self, state):
        # get all legal actions for pacman
		ranking = []
		possible = state.getAllPossibleActions();
		for i in range(0, len(self.actionList)):
			for j in range(0,len(self.actionList[i])):
				self.actionList[i][j] = possible[random.randint(0,len(possible)-1)]
		tempState = state		
		for i in range(0, len(self.actionList)):
			for j in range(0,len(self.actionList[i])):
				if tempState.isWin() +tempState.isLose() == 0:
					tempState =tempState.generatePacmanSuccessor(self.actionList[i][j])
				else:
					break
		
		flag = True
		while(flag):
			temporaryList,fitness,flag,number = self.getFitness(self.actionList,state)
			#print temporaryList
			#print fitness
			#print "-------"
			if not flag:
				childList = []
				for i in range(0, (len(temporaryList)),2):
					parent1 = self.getRank(random.randint(0,number))
					parent2 = self.getRank(random.randint(0,number))
					child1,child2 = self.getCrossover(temporaryList,parent1,parent2)
					childList.append(child1)
					childList.append(child2)
				childList = self.getMutation(childList,possible)
				self.actionList = childList[:]
			else:
				self.actionList = temporaryList [:]
		return self.actionList[7][0]

## Node class with the attributes of each node
class MCTSnode():
	
	def __init__(self,state,action = None,parent = None):
		#state to get the values of actions of the state
		self.visits = 0
		self.score = 0
		self.children = []
		self.parent = parent
		self.expanded = False
		self.action = action
		self.unexploredActions = state.getLegalPacmanActions()
	
	
		
class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
		def registerInitialState(self, state):
			self.i = 0
			return;
		
		def __init__(self):
			self.UCTConstant = 1
			self.flag_Constant = True
		## Tree Policy Function
		def MCTSTreePolicy(self,node,state):
			while node.expanded == False:
				if len(node.unexploredActions) > 0 :
					return self.MCTSExpand(node,state)
				else:
					previous = node
					node = self.MCTSSelection(node)
					if node is previous:
						break
			return node 
		
		## Expansion Function
		def MCTSExpand(self,node,state):
			unexplored = node.unexploredActions
			node_value = node
			current = state
			action_sequence = []
			node_sequence = []
			while node.parent != None:
				action_sequence.append(node.action)
				node_sequence.append(node)
				node = node.parent	
			while action_sequence:
				temp_current = current.generatePacmanSuccessor(action_sequence[-1])
				temp_node = node_sequence.pop(-1)
				if temp_current == None:
					return None
					break
				elif temp_current.isWin() + temp_current.isLose() == 1:
					self.Backup(temp_node,normalizedScoreEvaluation(root,temp_current))					
				else :	
					current = temp_current
				
				del action_sequence[-1]
			state = current
			legal = state.getLegalPacmanActions()
			if node_value.unexploredActions:
				node_value.expanded = False
			else:
				node_value.expanded = True
			for action in legal:
				if action in unexplored:
					new_state = state.generatePacmanSuccessor(action)
					if new_state == None:
						self.flag_Constant = False
						return None
						break
					child = MCTSnode(new_state,action,node_value)
					node_value.children.append(child)
					node_value.unexploredActions.remove(action)
					break

			return node_value.children[-1]
		
		##Default Policy Function
		def DefaultPolicy(self,node,state):
			current_node = node
			root = state
			current = state
			action_sequence = []
			node_sequence = []
			while node.parent != None:
				action_sequence.append(node.action)
				node_sequence.append(node)
				node = node.parent
			while len(action_sequence) > 0:
				temp_current = current.generatePacmanSuccessor(action_sequence[-1])
				temp_node = node_sequence.pop(-1)
				if temp_current == None : 
					self.flag_Constant = False
					return None
					break
				elif temp_current.isWin() + temp_current.isLose() == 1:
					self.Backup(temp_node,normalizedScoreEvaluation(root,temp_current))
				else:
					current = temp_current
				del action_sequence[-1]
			for i in range(0,5):
				if(current == None):
					print "Default Policy reached terminal state 2nd condition"
					return None
					break
				else:	
					if current.isWin() + current.isLose() == 1:
						self.Backup(current_node,normalizedScoreEvaluation(root,temp_state))
					else:
						legal = current.getLegalPacmanActions()
						random_action = legal[random.randint(0,len(legal)-1)]
						temp_state = current.generatePacmanSuccessor(random_action)
						if(temp_state == None):
							return None
							break
						else:	
							if temp_state.isWin() + temp_state.isLose() == 1:
								self.Backup(current_node,normalizedScoreEvaluation(root,temp_state))
							current = temp_state
			normalized_score = normalizedScoreEvaluation(root,current)
			return normalized_score
		
		## Back Propogation Function
		def Backup(self,node,current_score):
			backup_flag = True
			while backup_flag:
				node.score = node.score + current_score
				node.visits = node.visits + 1
				if node.parent == None:
					return False
					break
				node = node.parent
		
		## Selection Function	
		def MCTSSelection(self,node):
			length = len(node.children)
			Q_node = node.score
			UCTmax = 0
			best_node = node
			for i in range(0,length):
				childnode = node.children[i]
				UCTScore = (childnode.score/childnode.visits) + self.UCTConstant*math.sqrt((2*math.log(node.visits))/childnode.visits)
				if UCTScore > UCTmax:
					UCTmax  = UCTScore
					best_node = childnode
			return best_node
		
	# GetAction Function: Called with every frame
		def getAction(self, state):
			node = MCTSnode(state)
			self.flag_Constant = True
			while self.flag_Constant:
				front = self.MCTSTreePolicy(node,state)
				if front == None:
					break
				if not self.flag_Constant : 
					break
				score = self.DefaultPolicy(front,state)
				if score == None:
					break
				if not self.flag_Constant : 
					break
				self.Backup(front,score)
			
			most_Visited = 0 
			best_node = node
			best_score = -1000
			## to get the best node based on the number of visits, if the number of visits are same , then on the basis of the score
			for i in range(len(node.children)):
				child_node = node.children[i]
				if(child_node.visits > most_Visited):
					most_Visited = child_node.visits
					best_node = child_node
					best_score = child_node.score
				elif child_node.visits == most_Visited :
					if child_node.score > best_score :
						best_score = child_node.score
						best_node = child_node
			return best_node.action
