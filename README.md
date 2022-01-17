#### Data Source: https://oracleselixir.com/tools/downloads

## Summary
The purpose of this repository is to explore League of Legends professional match data from 2021, analyze the data, then visualize and explain our conclusions.

## Notes

### LolDataExploration.py

This file reads in the LoL data from 2021 matches and trims the dataset
to fit my analytical needs, then outputs the new dataset to a csv titled 2021_LoL_Pro_Player_Data.csv.

### Line by line
For a condensed version please view the file LolDataExploration.py

I started by outputting the first 5 rows and summary info of the dataframe to get an initial impression of the df.

`LoLCSV.head()`

`LoLCSV.info()`

Then I took the first 5000 rows of data and created a new df (Google denied me uploading the original 147k rows), wrote it to a csv, and uploaded it to Google Sheets so I could easily view the table. This is also doable in Python, however I used Sheets for the simplicity.

`df5000 = LoLCSV.iloc[:5000]`

`df5000.to_csv('LoL5000Matches.csv')`

[df5000 (Google Sheets)](https://docs.google.com/spreadsheets/d/1q5ft-bSBGewuYhWkR7pvZ2c4oXZbkqzmjNfosoCbfY0/edit?usp=sharing)

I discovered the data was already on the granularity level of each player per each game - perfect! Teams also had their own dedicated rows so I needed to remove those, which I did below. I went through the Google Sheet and highlighted each column I thought may be useful to my analysis. Then I copied the column names over so I could create a Python list with them.

I created `columnList` and assigned the desired column names to it as one large string.

_Columns:_

_datacompleteness	league	playoffs	date	game	patch	side	position	playername	playerid	teamname	champion	gamelength	result	kills	deaths	assists	teamkills
teamdeaths	doublekills	triplekills	quadrakills	pentakills	firstblood	firstbloodvictim	damagetochampions	dpm	damageshare	damagetakenperminute	damagemitigatedperminute	wardsplaced	wpm	controlwardsbought	visionscore	earnedgold
earned gpm	minionkills	monsterkills	monsterkillsenemyjungle	cspm	goldat10	xpat10	csat10	golddiffat10	xpdiffat10	csdiffat10	killsat10	deathsat10	goldat15	xpat15	csat15	golddiffat15 xpdiffat15	csdiffat15	killsat15_

I needed to replace the space in between each word with a comma, wrap each word with '' to create individual strings, then create a list using said strings. I utilized the `re.sub()` ReGex function to replace whitespaces with commas for all matches. Then I used the `split()` function to separate each word into strings, this returned a list of our column names as strings.  

`columnList = re.sub('\s+', ',', columnNames.strip()).split(',')`


I had my desired columns sorted into a list, now I could create a df with only these columns.

`columnDF = LoLCSV[columnList]`

I then received the follow error message: "['earned', 'gpm'] not in index." My cleanup of column names did not go as smoothly as it appeared. 'earned gpm' should have been one column, however there was a space in it so it got replaced with a comma and split into separate strings.

Rather than going through and editing the column names, I decided to drop the 'earned gpm' column entirely as other metrics such as 'gpm' and 'earnedgold' are better suited for our analytical needs.

`unwantedCol = ['earned', 'gpm']`

`columnList = [x for x in columnList if x not in unwantedCol]`

`columnDF = LoLCSV[columnList]`

And voilà! I had my desired columns. I then removed team instances from the rows as I want individual players. Team instances have the 'position' column set to 'team', I could use this to filter the rows.

I aggregated the team rows so I could validate the numbers before deletion.

`(columnDF['position'].values == 'team').sum()`

`columnDF.info()`

This returned 24526, the # of team rows. Each team has 1 team and 5 player rows per game, so 24526 should be 1/6 of our total number of rows, assuming the dataset is complete (there is a 'datacompleteness' which let's us know not all of the rows are complete). I used the `info()` function to return the summary info of our df including row count: 147276. 24526/147276 = .1665308672, or slightly below our expected ratio of 1/6 (.16666666...). If this was sensitive data, I would have dug deeper, however given the nature of this project I allowed the discrepancy.

`pd.unique(columnDF['position'])`

The above code returned our unique values within the column 'position.' The output was: ['top' 'jng' 'mid' 'bot' 'sup' 'team'], seeing as the only other values were player based positions, I moved forward and dropped the rows where position = 'team'.

`columnDF = columnDF[columnDF.position != 'team']`


I then wrote the trimmed dataset to a csv

`columnDF.to_csv('2021_LoL_Pro_Player_Data.csv')`
