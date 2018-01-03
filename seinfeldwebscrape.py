import requests
import re
from BeautifulSoup import BeautifulSoup
from numpy import *
url = 'http://www.seinology.com/scripts/script-22.shtml'
response = requests.get(url)
html = response.content
#print html
#content = BeautifulSoup(html)
#print content.prettify()

#print html[0:100] # to check it outputs 
#print(type(html)) # to confirm that html is a string

#finds how many characters are in the episode
html = html.split('==================================================================')[-1]
#html = html[html.index("=================================================================="):]
sep = 'the end'

insensitive_theend = re.compile(re.escape('the end'), re.IGNORECASE)
html = insensitive_theend.sub('the end', html) #converts all case combinations of 'the end' into lower case
html = html.split(sep, 1)[0] #removes everything after 'the end'

#html = re.split(sep, html, flags=re.IGNORECASE)[1]

#for i in range(0, len(html)):
#	i = i + 1

html = re.sub('&#146;', "'", html) #regex to sub out/remove parts of string with preferred text
html = re.sub('&#147;', '"', html)
html = re.sub('&#148;', '"', html)
html = re.sub('&#150;', "--", html)
html = re.sub('&Mac226;', "'", html)
html = re.sub('<br>', "", html)
html = re.sub('&nbsp;', " ", html)
html = re.sub('&quot;', '"', html)
html = re.sub('\([^)]*\)', "", html)
	#html = re.sub('[\(\[].*?[\)\]]', "", html)
	
#print(html)

"""
Notes on how to parse text - 

1) '==================================================================' indicates the beginning of episode after credits are listed
2) 'INT. COMEDY CLUB &#150; NIGHT' indicates the beginning of the comedy scene before the real episode begins.
	It sometimes comes back later in the episode and should probably be ignored as a scene in general.
3) The next 'INT.' indicates the beginning of the episode in earnest and from this point on the text is important and should be parsed. Everything before can be ignored for the current purposes of research.
4) '&#146;' is really an apostrophe (')
5) '&#150;' is really the en-dash
6) '&#147;' is really the left quote
7) '&#148;' is really the right quote
8) Remove the parenthetical comments that give context for scene
9) 'Int.' generally marks beginning and end of scenes
10) Speaking characters in scenes are shown by capitalized letters used in their names. 
	They are also the first word after a '<br />'.
11) '<br />' is the break between lines and needs to be removed
12) 'THE END' indicates the episode is over
13) there are inconsistincies in the transcipts of the seinfeld scripts. sometimes [] are used to convey scenes and sometimes the scene's location is just written. need to check per episode when doing analysis (possibly automatable).

How to Generate networks - 

1) Create variables for monologue and dialogue values 
2) monologue is the length of each character's speech per scene (measured in words) - node weight. 
	- stored in a vector
3) dialogue will form an adjacency matrix (keep it symmetrical for now) is the number of times two characters exchange conversation 
	- cooccurrence of characters in scene creates an unweighted edge between all characters in scene
	- edges are weighted by frequency of dialogue (jerry -> elaine -> jerry = +1 to initial edge weight so total weight of 2 now) 
4) There should be adjacency matrices for however many scenes in the episode.
5) the scenes adjacency matrices can be combined to the adjacency matrix for the episode.
6) later, this can be applied to seasons and series level of analysis.
7) watch how matrices change from scene to scene.

Structure of scene - 
for episodes using '[]' to signify scenes
1) '[Scene Location]'
2) 'CAPITALIZED NAME OF CHARACTER: ' 
3) next scene give by 1)
"""

"""

"""

#breaks string into list of strings separated by commas.
html = html.split()

#should split the text again into scenes separated by the [...]
# find elements in html that have[...]
i = 0

leftbrack = []
rightbrack = []

#can make this scene finder a conditional statement as we encounter other episodes that have different formatting for scene delineation
for text in html: 
	if '[' in text:
		left = html.index(text)
		left1 = i #location of '[' accounting for repeat  
		leftbrack.append(left1) #indices of [
#		print  left
	

	if ']' in text:
		right = html.index(text)
		right1 = i
		rightbrack.append(right1) #indices of ]
		#print right1 #need to figure out how to find indices of repeat scene locations
#		print  right

	i = i + 1

'''
for k in range(0,len(leftbrack)): #check for correct indices of scenes - without repeating entries being misregistered.
	print html[(leftbrack[k])], leftbrack[k]
	print '---'
	print html[(rightbrack[k])], rightbrack[k]
	print '---'
'''

#print html[leftbrack]
#print rightbrack
#need to figure out hwo to iterate thru the repeating words^




#print type(leftbrack[1]) , rightbrack
scenes = [] #need to fix how scenes are found. isn't picking up scenes with multiple words in the brackets
if  len(leftbrack) == len(rightbrack): #check that they're the same length
	
		#first join entries in left and right brack that are one index number apart. then ->
		#write the command to split the html list for each entry of leftbrack
		#val = rightbrack[k]
		#print val, leftbrack[k]
#		if leftbrack[k] == val
#			html[leftbrack[k]] = html[leftbrack[k]] + rightbrack[k]
#			html.remove([leftbrack[k]+1])

#for now assume that the left bracket will successfully split the text into scenes. 
#if assumption is false then we will be left with some right brackets lying around the split scenes 
	for k in range(0, len(rightbrack)-1): #could make a dict where each scene location and scene text are a pair. would be useful for finding out how often each location is referenced.
		scenes.append(html[rightbrack[k]+1:leftbrack[k+1]]) #scenes is now the multidimensional list containing all scenes in the episode
#can find location of scenes, length of scenes...all in time (temporal)
#print scenes[17]
#print len(scenes)


"""
for j in range(0, len(html)): # finds locations of speaking characters in episode
	if html[j][0:len(html[j])].isupper() and html[j][-1] == ':' :
		print html[j], j
	j = j + 1	
"""

del scenes[0] # deletes the monologue

speaker = [] #speaker of instance
scenenum = []#scene number
linenum = []#line number
wordnum = [] #number of words spoken in instance

l = []
linecount = []
lcount = 0
w = 0
for q in range(0, len(scenes)):
	prev = 0
	lcount = 0
	k = 0
	for j in range(0, len(scenes[q])):
		if scenes[q][j][0:len(scenes[q][j])].isupper() and scenes[q][j][-1] == ':' :			
			speaker.append(scenes[q][j])
			scenenum.append(q)
			linenum.append(j)
			wordnum.append(j -1 - prev) #off by an index unit. gives number of words spoken to previous speaker.
			#need to make separate lists for character names and corresponding lists for their quotes by scene.
			#then iterate through each list with respect to it's character and scene values to create the list for number of words spoken. The index needs to be shifted which is difficult to do in loops.
			
			#print scenes[q][j], q, j, wordnum[w] #prints the speaker's name, the scene, and the word number
			w = w + 1
			k = k + 1 #counts the length of the vectors corresponding to each scene
			prev = j
		lcount = lcount + 1
	#should split lists by the value here since it's where scenes transition
	linecount.append(k)
	l.append(lcount) #finds indices of scenes
	
"""	
	speaker.append('')
	scenenum.append('')
	linenum.append('')
	wordnum.append('') #word num is counting each quote incorrectly by an additional one unit
"""

#run a separate for loop over linenum and scenenum to 


"""
for #finds the wordnum separately
	count in range(0,w-2):
	temp = 0
	wordnum[temp] = linenum[count+1] - linenum[count]
	temp = temp + 1
"""

#print len(wordnum), w, linenum.index(linenum[3])

wordnum1 = []
for a in range(1,w): #corrects the indexing problem
	wordnum1.append(wordnum[a])
	
wordnum1.append(-1) #fixes length of wordnum1 by adding a -1 at the end since it is one less than w

#--> solves big problem! 
#write another for loop with an if statement to catch last linenum in a scene 
#if wordnum[x] == -1 then the corresponding wordnum = len(linenum[x]:l[scenenum)]
#the big loop^ isn't picking up the last two character quotes in the scene and the last two scenes in the episode.



"""
new scene occurs when all three conditions occur (i.e. and): 
1) scenenum changes value, i.e. if scenenum[b] == scenenum[b-1]+1
2) linenum[b] == 0
3) wordnum[b] == -1
"""

'''

speaker1 = [] #these are going to be list of list versions of the normal variables
scenenum1 = []
linenum1 = []
c = 0
bprev = 0
for b in range(0,w):
	if wordnum1[b] == -1:
		#split the list at these b values
		#wordnum1[b] = l[c] - linenum[b]
		#need to find index of linenum[b] - obviously it's b!
		if c == 0:
			speaker1.append(speaker[0:b]) #fixes indexing issue
			scenenum1.append(scenenum[0:b])
			linenum1.append(linenum[0:b])
		
		#CURRENT LOCATION
		speaker1.append(speaker[bprev+1:b]) #making a list version of speaker
		#is recording one speaker scenes as []
		scenenum1.append(scenenum[bprev+1:b])
		linenum1.append(linenum[bprev+1:b])

		#if c == max(scenenum)

		#doesn't catch last scene
		c = c + 1 #assuming wordnum1 can only be -1 once per scene, whenever this condition is reached, increment the count on c by 1
		bprev = b
		#should consider splitting scenes when first creating these lists. 
		#we obviously know the indices where scenes end/begin bc we use these values to find things like l


		#SyntaxError: EOF while scanning triple-quoted string literal - bc i fed it a infintely nested list by accident. fixed.
		#add a split action on the vectors to make them into smaller scene lists of lists
'''

speaker_scene = []
scenenum_scene = []
linenum_scene = []
wordnum1_scene = []
#these are going to be new version of the vectors split into lists of lists by scene

prev = 0
for i in range(0,len(linecount)) :
	speaker_scene.append(speaker[prev:prev+linecount[i]])
	scenenum_scene.append(scenenum[prev:prev+linecount[i]])
	linenum_scene.append(linenum[prev:prev+linecount[i]])
	wordnum1_scene.append(wordnum1[prev:prev+linecount[i]])
	if wordnum1_scene[i][-1] == -1 :
		wordnum1_scene[i][-1] = l[i] - linenum_scene[i][-1]
	#print speaker_scene[i], scenenum_scene[i], linenum_scene[i], wordnum1_scene[i]
		#corrects the -1 appearing as last wordnum1 instead of actual number of words
		#print linenum_scene[i][-1], l[i], wordnum1_scene[i][-1]
	#if speaker_scene[i] == speaker[prev:prev+linecount[i]] and scenenum_scene[i] == scenenum[prev:prev+linecount[i]] and linenum_scene[i] == linenum[prev:prev+linecount[i]] and wordnum1_scene[i] == wordnum1[prev:prev+linecount[i]]:
	#	print 'pajamas'
	#else :
	#	print 'doody'
	prev = prev + linecount[i]

#print speaker_scene[0], wordnum1_scene[0]
'''	
for a in range(0,w):
	print speaker[a], scenenum[a], linenum[a], wordnum1[a] #catches each speakers lines except for last speaker
	#isn't recognizing text in scenes 15 and 16
	#indexing problem
'''

for i in range(len(speaker_scene)):
	for j in range(len(speaker_scene[i])):
		#create networks in this step. 
		print speaker_scene[i][j], scenenum_scene[i][j], linenum_scene[i][j],wordnum1_scene[i][j]
		#create two types of networks for scenes: 
		#1- a simplex weighted by sum of two respective characters' wordnum1
		#2- a network where two characters are connected iff they are adjacent in the speaker_scene vector
		#decide how to reduce duplicates and aggregate the information for network formation.
	print '----'

#for i in speaker_scene:
#	for j in i:
#		print j

#print scenes[6], '\n', len(scenes[16]), len(scenes) #missing last two quotes...need to find source of error
#if i already have scenes broken up by scene then why don't i break up the lists in the loop through difft scenes...?!
#print len(wordnum), w, linenum[w-3], linenum.index(linenum[w-3]), l, len(l)

#print len(linecount), speaker_scene, len(speaker)
#speaker1[2], len(speaker1[1]), c
#speaker1 is off by 1 index
#this way of indexing l is going to fail bc it only finds first entries. need a better way to find indices of new scenes
#l is an infinitely nested list? whoops - need to fix this!!! - fixed. l was being appended with empty lists instead of lcount which was the counter for l...
#slice new lists by ''
#make a condition that if the index reaches the last speaker in the scene it should check for when the next scene begins and give those lines to the last speaker.
'''
speaker.split()
scenenum.split()
linenum.split()
wordnum.split() #figure out how to make a multidimensional list for each of these lists so they are separated by scene
'''
#print len(wordnum), w
#print scenes[0]
# create a data structure for each scene that contains an index, character name, and their statement.
# keep this data sequential so that index 1->2->3 corresponds to flow of dialogue in script.
# try using a multidimensional list to store speaker and statement - [[JERRY, '...'], [ELAINE. '...']]
# each multidimensional list will then be related to a specific scene.

