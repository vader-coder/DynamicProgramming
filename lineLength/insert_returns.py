from sys import argv,exit

def readFile(fname):
  f = open(fname)
  wordList = []
  for l in f:
      if (len(l) <= 1): # the line was empty
          continue;
      else:
          wordList += l.strip().split(' ')
  return wordList

class Table:
    def __init__(self, words, lineLimit):
        self.wordList = words
        self.M = lineLimit
        self.minPenaltyTable = [None]*len(words)#size of table
        self.n = len(words)-1
        self.minPenaltyTable[-1] = (self.M - len(self.wordList[self.n]))**2
        #each entry is min penalty from end to beginning

    def slack(self, startIndex, endIndex):
        if startIndex == endIndex:
            return self.M - len(self.wordList[startIndex])
        if startIndex > endIndex:
            endIndex = startIndex

        summation = 0
        for i in range(startIndex, endIndex+1):
            summation += len(self.wordList[i])
        summation +=  (endIndex - startIndex)#wordnum - 1
        return (self.M - summation)#summation > M, then this will be negative

    def minPenalty(self, wordIndex):#from word i to n
        if wordIndex == self.n:
            return self.minPenaltyTable[-1]
        if wordIndex > self.n:#no recusive penalty if line takes up whole thing.
            return 0
        #if self.minPenaltyTable[wordIndex] != None:
        elif self.minPenaltyTable[wordIndex] != None:
            return self.minPenaltyTable[wordIndex]


    def set(self, penalty, i):
        self.minPenaltyTable[i] = penalty


def reconstructParagraph(wordList, minBreakIndecies):
    startIndex = 0
    lineEndIndex = minBreakIndecies[0]#have it as end of line
    for i in range(len(wordList)):
        if i == lineEndIndex:
            wordList[i] += '\n'
            if lineEndIndex+1 < len(minBreakIndecies):
                lineEndIndex = minBreakIndecies[lineEndIndex+1]
        else:
            wordList[i] += ' '
    return ''.join(wordList)

def fixParagraph(words, M):
  table = Table(words, M)
  n = len(words)-1
  lineEndIndecies = [None]*len(words)
  #is it possible not to square every time and just store the lines, then calculate the penalty of the best line?

  for i in range(n, -1, -1):#n to 0, i=60 on 1st.
    currentMinimumPenaltyForSubsetFromiToN = float('+inf')#last one by default
    tIndexForMinimumPenalty = None
    passedLineLimit = False
    for t in range(i, n+1): #i to n = 60. t last word index of new line
        lineSlack = table.slack(i, t)
        if lineSlack < 0:#don't want to pass line limit
            passedLineLimit = True
            break
        squareOfSlackOfi_tLine = (table.slack(i, t))**2
        minPenaltyOfSubString = table.minPenalty(t+1)#t to end
        penaltyIncludingNewLine = squareOfSlackOfi_tLine + minPenaltyOfSubString

        if penaltyIncludingNewLine < currentMinimumPenaltyForSubsetFromiToN:
            currentMinimumPenaltyForSubsetFromiToN = penaltyIncludingNewLine
            tIndexForMinimumPenalty = t
    table.set(currentMinimumPenaltyForSubsetFromiToN, i)
    lineEndIndecies[i] = tIndexForMinimumPenalty#put break right after this word

  paragraphStr = reconstructParagraph(words, lineEndIndecies)
  return paragraphStr

def fixWebsiteText(str, M):
    wordList = str.split()
    Mint = int(M)
    if not(Mint > 0):
        return -1
    return fixParagraph(wordList, Mint)

def fromCommandLine():
    wordList = readFile(argv[2])
    return fixParagraph(wordList, int(argv[1]))
#test this one for inputs