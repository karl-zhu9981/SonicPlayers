import random

class Node:
	def __init__(self, args):
		self.prev = None
		self.next = None
		self.pid = None
	def setPrev(self, prev):
		self.prev = prev
	def setPid(self, pid):
		self.pid = pid
	def setNext(self, nextone):
		self.next = nextone

class Memory:
	def __init__(self, args):
		self.stats = StatTracker()
		self.memory = Node()
		current = self.memory
		for i in range(0,127):
			newNode = Node()
			newNode.setPrev(current)
			current.setNext(newNode)
			current = newNode
	def allocate_mem(self, process_id, num_units):
		return -1
	def deallocate_mem(self, process_id):
		current = self.memory
		successful = -1
		while (current.next != None):
			if (current.pid == process_id):
				current.pid = None
				successful = 1
			current = current.next
		return successful
	def fragment_count(self):
		current = self.memory
		fragcount = 0
		holeSize = 0
		while (current != None):
			if (current.pid == None):
				holeSize+=1
			else:
				if (holeSize == 1 or holeSize == 2):
					fragcount+=1
				holeSize = 0
			current = current.next
		if (holeSize == 1 or holeSize == 2):
					fragcount+=1
		return fragcount

class FirstMemory(Memory):
	def allocate_mem(self, process_id, num_units):
		current = self.memory
		nodesTraversed = 1
		holeSize = 0
		while (True):
			if (current == None):
				self.stats.updateStats(-1,self.fragment_count())
				return -1
			if (current.pid == None):
				holeSize+=1
				if (holeSize==num_units):
					for i in range(0,num_units):
						current.setPid(process_id)
						current = current.prev
					self.stats.updateStats(nodesTraversed,self.fragment_count())
					return nodesTraversed
			else:
				holeSize = 0

				
			current = current.next
			nodesTraversed+=1

class NextMemory(Memory):
	def __init__(self):
		super().__init__()
		self.current = self.memory
	def allocate_mem(self, process_id, num_units):
		nodesTraversed = 1
		holeSize = 0
		for i in range(0,128):
			if (self.current.pid == None):
				holeSize+=1
				if (holeSize==num_units):
					filler = self.current
					for i in range(0,num_units):
						filler.setPid(process_id)
						filler = filler.prev
					self.stats.updateStats(nodesTraversed,self.fragment_count())
					return nodesTraversed
			else:
				holeSize = 0


			if (self.current.next == None):
				self.current = self.memory
				holeSize = 0
			else:
				self.current = self.current.next
			nodesTraversed+=1
		self.stats.updateStats(-1,self.fragment_count())
		return -1

class BestMemory(Memory):
	def allocate_mem(self, process_id, num_units):
		current = self.memory
		nodesTraversed = 1
		bestHolePos = 0
		bestHoleSize = 99999
		holeSize = 0
		holePos = 0
		while (True):
			if (current.pid == None):
				holeSize+=1
			else:
				if (holeSize == num_units):
					current = current.prev
					for i in range(0,num_units):
						current.setPid(process_id)
						current = current.prev
					self.stats.updateStats(nodesTraversed,self.fragment_count())
					return nodesTraversed
				elif (holeSize < bestHoleSize and holeSize > num_units):
					bestHoleSize = holeSize
					bestHolePos = holePos
				holeSize = 0
				holePos = nodesTraversed
			if (current.next== None):
				if(holeSize>0):
					if (holeSize == num_units):
						for i in range(0,num_units):
							current.setPid(process_id)
							current = current.prev
						return nodesTraversed
					elif (holeSize < bestHoleSize and holeSize > num_units):
						bestHoleSize = holeSize
						bestHolePos = holePos
				break
				
			current = current.next
			nodesTraversed+=1
		if (bestHoleSize==99999):
			self.stats.updateStats(-1,self.fragment_count())
			return -1
		current = self.memory
		for i in range(0,bestHolePos):
			current = current.next
			nodesTraversed+=1
		for i in range(0,num_units):
			current.pid = process_id
			current = current.next

		self.stats.updateStats(nodesTraversed,self.fragment_count())
		return nodesTraversed

class WorstMemory(Memory):
	def allocate_mem(self, process_id, num_units):
		current = self.memory
		nodesTraversed = 1
		bestHolePos = 0
		bestHoleSize = 0
		holeSize = 0
		holePos = 0
		while (True):
			if (current.pid == None):
				holeSize+=1
			else:
				if (holeSize > bestHoleSize):
					bestHoleSize = holeSize
					bestHolePos = holePos
				holeSize = 0
				holePos = nodesTraversed
			if (current.next== None):
				if(holeSize>0):
					if (holeSize > bestHoleSize):
						bestHoleSize = holeSize
						bestHolePos = holePos
				break
				
			current = current.next
			nodesTraversed+=1
		if (bestHoleSize==0):
			self.stats.updateStats(-1,self.fragment_count())
			return -1
		current = self.memory
		if (bestHoleSize>=num_units):
			for i in range(0,bestHolePos):
				current = current.next
				nodesTraversed+=1
			for i in range(0,num_units):
				current.pid = process_id
				current = current.next
			self.stats.updateStats(nodesTraversed,self.fragment_count())
			return nodesTraversed
		else:
			self.stats.updateStats(-1,self.fragment_count())
			return -1

class RequestGenerator:
	def __init__(self):
		self.currentIDs = []
	def getRequest(self):
		args = []
		alloOrDeallo = bool(random.getrandbits(1))
		if(alloOrDeallo):
			args = self.getAllocationRequest()
		else:
			if (len(self.currentIDs)==0):
				args = self.getAllocationRequest()
			else:
				args = self.getDeallocationRequest()
		return args
	def getAllocationRequest(self):
		pid = random.randint(1,99999)
		while(pid in self.currentIDs):
			pid = random.randint(1,99999)
		self.currentIDs.append(pid)
		size = random.randint(3,10)
		return [True,pid,size]
	def getDeallocationRequest(self):
		return [False,self.currentIDs.pop(random.randint(0,len(self.currentIDs)-1)),0]

class StatTracker:
	def __init__(self):
		self.alloCount = 0
		self.fragCount = 0
		self.deniedCount = 0
		self.successCount = 0
		self.totalNodes = 0
	def updateStats(self, alloResult, fragResult):
		self.alloCount += 1
		if (alloResult==-1):
			self.deniedCount += 1
		else:
			self.totalNodes += alloResult
			self.successCount += 1
			self.fragCount += fragResult
	def printStats(self):
		print("Average fragments:", '{:.2f}'.format(self.fragCount/self.successCount))
		print("Average Nodes Travelled: ", '{:.2f}'.format(self.totalNodes/self.successCount))
		print("Deny Rate: ", '{:.2f}'.format(self.deniedCount/self.alloCount*100), "%", sep="")

class Simulation:
	def __init__(self):
		self.firstMemory = FirstMemory()
		self.nextMemory = NextMemory()
		self.bestMemory = BestMemory()
		self.worstMemory = WorstMemory()
		self.reqGen = RequestGenerator()

	def run(self):
		for i in range(0,20):
			args = self.reqGen.getAllocationRequest()
			self.firstMemory.allocate_mem(args[1],args[2])
			self.nextMemory.allocate_mem(args[1],args[2])
			self.bestMemory.allocate_mem(args[1],args[2])
			self.worstMemory.allocate_mem(args[1],args[2])

		for i in range(0,10000):
			args = self.reqGen.getRequest()
			if (args[0]):
				self.firstMemory.allocate_mem(args[1],args[2])
				self.nextMemory.allocate_mem(args[1],args[2])
				self.bestMemory.allocate_mem(args[1],args[2])
				self.worstMemory.allocate_mem(args[1],args[2])
			else:
				self.firstMemory.deallocate_mem(args[1])
				self.nextMemory.deallocate_mem(args[1])
				self.bestMemory.deallocate_mem(args[1])
				self.worstMemory.deallocate_mem(args[1])

		print("First Fit:")
		self.firstMemory.stats.printStats()
		print()
		print("Next Fit:")
		self.nextMemory.stats.printStats()
		print()
		print("Best Fit:")
		self.bestMemory.stats.printStats()
		print()
		print("Worst Fit:")
		self.worstMemory.stats.printStats()


test = Simulation()
test.run()