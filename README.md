`import pandas as pd` # for data analysis and csv reading
`import numpy as np` # for linear algebra
`import re` # regex, didn't need to add to pipenv to use
# read in csv data on LoL matches
`LoLCSV = pd.read_csv('2021_LoL_Match_Data.csv')`

# print head of table
`print(LoLCSV.head())`

`print(LoLCSV.info())`

# create a df with the first 5000 rows for easier viewing (google denied me uploading 147k by 121 to sheets)
`df5000 = LoLCSV.iloc[:5000]`
`df5000.to_csv('LoL5000Matches.csv')`

`print(df5000.info())`

# from here we uploaded the csv to google sheets for easy column and row visualization
# I saw the data was on the granularity level of each player per each game - PERFECT!
# However, teams were included in the rows so I need to remove those
# I copied and pasted the column/metric names I wanted to keep for my new sub-df

datacompleteness	league	playoffs	date	game	patch	side	position	playername	playerid	teamname	champion	gamelength	result	kills	deaths	assists	teamkills
teamdeaths	doublekills	triplekills	quadrakills	pentakills	firstblood	firstbloodvictim	damagetochampions	dpm	damageshare	damagetakenperminute	damagemitigatedperminute	wardsplaced	wpm	controlwardsbought	visionscore	earnedgold
earned gpm	minionkills	monsterkills	monsterkillsenemyjungle	cspm	goldat10	xpat10	csat10	golddiffat10	xpdiffat10	csdiffat10	killsat10	deathsat10	goldat15	xpat15	csat15	golddiffat15 xpdiffat15	csdiffat15	killsat15

# I was going to go through and add '', in between each word to help built my array of columns I want
# but this is a repetitive task, and what is a programming language good for if not automating repetitive tasks?
# I can replace the space in between each word with a , and then add '' to the beginning and end of each item in my list, creating one long string
# Since I'll have on long string, I can then use the split function to split each word in our array.

# re.sub function replaces matches with a string the text, \s matches string containing any whitespace character, the + matches all
#  ',' is the replacement, columnNames.strip() is the input string
# we now have one big string of our strings separated by commas, the split(',') function separates our single large string into smaller strings
# and does this by separating based on the ,
`columnList = re.sub('\s+', ',', columnNames.strip()).split(',')`

# we have our desired columns sorted into a list, now we can create a df with only
# our desired columns. `columnDF = LoLCSV[columnList]`

# error: ['earned', 'gpm'] not in index. Our cleanup of column names did not go as smoothly as it appeared. earned gpm should be one column, however there was a space in it so it got replaced with a comma and split into separate strings.

# Back to sheets we go. This is where I'm glad I added the trimmed dataset to sheets, as it enables me to have an easy visual spreadsheet to reference. While you can also do this in Python, I'm in the learning process and much more comfortable with spreadsheets. So while slower than Python, I am able to easily catch discrepancies and errors and then fix them. earned gpm is a metric that is not significant for my analysis, and I want to drop it from the columnList, however to solve I would append the correct 'earnedGpm' to my columnList and drop the ['earned', 'gpm'] values from my list.

# remove unwanted columns
`unwantedCol = ['earned', 'gpm']`

`columnList = [x for x in columnList if x not in unwantedCol]`

`columnDF = LoLCSV[columnList]`
# and voilà! we have only our desired columns
# time to remove team instances from the rows as we only want individual player data
# teams have the position column set to 'team', we can use this to filter our data


`(columnDF['position'].values == 'team').sum()`
# this returns 24526, the # of team rows. before we delete these rows, let's validate that the numbers make sense each team has 1 team and 5 player rows per game, so our 24526 should be 1/6 of our total number of rows, assuming the dataset is complete.

`columnDF.info()`
# will return the basic info of our df including row "entries" count: 147276. 24526/147276 = .1665308672, or slightly below our expected ratio of 1/6 (.16666666...), let's inspect.

`pd.unique(columnDF['position'])`
# this returns our unique values witin the column 'position'
# the output was: ['top' 'jng' 'mid' 'bot' 'sup' 'team'], seeing as the only other values are player based positions, I am going to move forward and drop the rows where position = 'team'. I will then check for duplicate player rows considering our ratio of team rows to player rows was slightly off.


`columnDF = columnDF[columnDF.position != 'team']`
# drop the rows with position = team. we then check `columnDF.info()`again to see if we were successful. we get 122730 rather than the expected 122750 (147276-24526). Since I'm working with this dataset for fun and the nature of the data is non-imperative being video game outcomes, I will move forward so I can start analyzing the data. If this were for work or my previous role in healthcare for example, I would be much more meticulous about small discrepancies like this.
