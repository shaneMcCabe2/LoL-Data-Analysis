import pandas as pd # for data manipulation and csv read/write
import numpy as np # for array computing and math functions
import re # ReGex for string manipulation and matching

## This code block will read in the LoL data from 2021 matches and trim the dataset
## to fit my analytical needs, then output the new dataset to a csv


# read in csv data on LoL matches
LoLCSV = pd.read_csv('2021_LoL_Match_Data.csv')

# print head of dataframe and basic dataframe info
# print(LoLCSV.head())
# print(LoLCSV.info())

# chosen columns headers copied from Google Sheets
columnNames = 'datacompleteness league	playoffs	date	game	patch	side	position	playername	playerid	teamname	champion	gamelength	result	kills	deaths	assists	teamkills earned gpm	minionkills	monsterkills	monsterkillsenemyjungle	cspm	goldat10	xpat10	csat10	golddiffat10	xpdiffat10	csdiffat10	killsat10	deathsat10	goldat15	xpat15	csat15	golddiffat15 xpdiffat15 csdiffat15 killsat15 teamdeaths	doublekills	triplekills	quadrakills	pentakills	firstblood	firstbloodvictim	damagetochampions	dpm	damageshare	damagetakenperminute	damagemitigatedperminute	wardsplaced	wpm	controlwardsbought	visionscore	earnedgold'

# replace whitespace with commas using ReGex sub, then split the singular large string into a list of smaller strings separated by commas
columnList = re.sub('\s+', ',', columnNames.strip()).split(',')

# define unwanted columns in list
unwantedCol = ['earned', 'gpm']

# remove unwanted columns
columnList = [x for x in columnList if x not in unwantedCol]

# create new df with only our desired columns
columnDF = LoLCSV[columnList]

# drop team rows as we only want player level data
columnDF = columnDF[columnDF.position != 'team']

# write our (mostly) clean dataset to a csv
columnDF.to_csv('2021_LoL_Pro_Player_Data.csv')
