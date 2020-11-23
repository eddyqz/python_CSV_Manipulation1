# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 20:47:36 2020

@author: eddyz

Rice 3 Week 4 Final Project
"""

# """
# Project for Week 4 of "Python Data Analysis".
# Processing CSV files with baseball stastics.

# Be sure to read the project description page for further information
# about the expected behavior of the program.
# """

import csv

##
## Provided code from Week 3 Project
##

def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    table = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table

##
## Provided formulas for common batting statistics
##

# Typical cutoff used for official statistics
MINIMUM_AB = 500


def batting_average(info, batting_stats):
    """
	

	Parameters
	----------
	info : A dictionary containing information about the file
	batting_stats : A dictionary of batting statistics

	Returns
	-------
	The batting average as a float

	"""
	
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return hits / at_bats
    else:
        return 0
	
	
def onbase_percentage(info, batting_stats):
    """
	

	Parameters
	----------
	info : Dictionary containing information about the file
	batting_stats : 

	Returns
	-------
	None.

	"""
	
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    walks = float(batting_stats[info["walks"]])
    if at_bats >= MINIMUM_AB:
        return (hits + walks) / (at_bats + walks)
    else:
        return 0
	
	
def slugging_percentage(info, batting_stats):
    """
	

	Parameters
	----------
	info : A dictionary with information about the file
	batting_stats : A dictionary of batting statistics (values are strings)

	Returns
	-------
	The slugging percentage as a float

	"""
	
    hits = float(batting_stats[info["hits"]])
    doubles = float(batting_stats[info["doubles"]])
    triples = float(batting_stats[info["triples"]])
    home_runs = float(batting_stats[info["homeruns"]])
    singles = hits - doubles - triples - home_runs
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return (singles + 2 * doubles + 3 * triples + 4 * home_runs) / at_bats
    else:
        return 0



##
## Part 1: Functions to compute top batting statistics by year
##


def filter_by_year(statistics, year, yearid):
    # test successful       
    """
	

	Parameters
	----------
	statistics : List of batting statistics dictionaries
	year : Year to filter by
	yearid : Year ID field in statistics

	Returns
	-------
	A list of batting statistics dictionaries that are from the input year.

	"""
	
    year_statistics = []
	
    # year_id_index = statistics[0].index(yearid)
	
    for inner_dict in statistics:
        if int(inner_dict[yearid]) == int(year):
            year_statistics.append(inner_dict)
		   
	
    return year_statistics


def top_player_ids(info, statistics, formula, numplayers):
	# test successful
    """
	

	Parameters
	----------
	info : Dictionary containing the names of columns in the table
	statistics : List of batting statistics dictionaries
	formula : function that takes an info dictionary and a batting statistics 
				dictionary as input and computes a compound stastistic
	numplayers : Number of top playes to return

	Returns
	-------
	A list of tuples, player ID and compound statistic computed by formula, 
	of the top numplayers players sorted in decreasing order of the 
	computed statistic.

	"""
	
    top_players_by_statistic = []
    all_players_by_statistic = []
	
    for inner_dict in statistics:
# 	    inner_tuple = ()
        inner_tuple = (inner_dict[info["playerid"]], formula(info, inner_dict))
        all_players_by_statistic.append(inner_tuple)
	
    all_players_by_statistic.sort(key=lambda pair: pair[1], reverse = True)	
	
    top_players_by_statistic.extend(all_players_by_statistic[:numplayers])
	
    return top_players_by_statistic


def lookup_player_names(info, top_ids_and_stats):
	# tests successful
    """
    Inputs:
      info              - Baseball data information dictionary
      top_ids_and_stats - list of tuples containing player IDs and
                          computed statistics
    Outputs:
      List of strings of the form "x.xxx --- FirstName LastName",
      where "x.xxx" is a string conversion of the float stat in
      the input and "FirstName LastName" is the name of the player
      corresponding to the player ID in the input.
    """
    list_of_stats_and_names = [] # the list to be returned at the end
	
    batting_stats_list = read_csv_as_list_dict(info["masterfile"], info["separator"], info["quote"])
    
    for inner_tuple in top_ids_and_stats:
        player_firstname = "" 
        player_lastname = ""
		
        for row in batting_stats_list:
            if row[info["playerid"]] == inner_tuple[0]:
                player_firstname = row[info["firstname"]]
                player_lastname = row[info["lastname"]]
				
				
        stat_string = "{0:.3f} --- {1} {2}".format(inner_tuple[1], player_firstname, player_lastname)
	    
        list_of_stats_and_names.append(stat_string)
		
    return list_of_stats_and_names


def compute_top_stats_year(info, formula, numplayers, year):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
      year        - Year to filter by
    Outputs:
      Returns a list of strings for the top numplayers in the given year
      according to the given formula.
    """
    statistics = read_csv_as_list_dict(info["battingfile"], info["separator"], info["quote"])
    statistics_for_year = filter_by_year(statistics, year, info["yearid"])
	
    top_ids_and_stats = top_player_ids(info, statistics_for_year, formula, numplayers)
	
    return lookup_player_names(info, top_ids_and_stats)



##
## Part 2: Functions to compute top batting statistics by career
##

def nested_dict_to_list_dict(nested_dict):
    """
 	

 	Parameters
 	----------
 	nested_dict : Nested dict

 	Returns
 	-------
 	A list of dictionaries containing all the same data

 	"""
 	
    list_dict = []
	
    for key in nested_dict:
        list_dict.append(nested_dict[key])
	
    return list_dict

def aggregate_by_player_id(statistics, playerid, fields):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      playerid   - Player ID field name
      fields     - List of fields to aggregate
    Output:
      Returns a nested dictionary whose keys are player IDs and whose values
      are dictionaries of aggregated stats.  Only the fields from the fields
      input will be aggregated in the aggregated stats dictionaries.
    """
	
    career_stats = {}
	
    for row in statistics:
        inner_dict = {}
        inner_dict[playerid] = row[playerid]
	    
        for field in fields:
            # if len(career_stats) > 0:
				# if the career_stats (outer dictionary) isn't empty
                if row[playerid] in career_stats:
                    if field in career_stats[row[playerid]]:
                        career_stats[row[playerid]][field] += int(row[field])
                    else:
                        career_stats[row[playerid]][field] = int(row[field])
                else:
                    career_stats[row[playerid]] = inner_dict
                    inner_dict[field] = int(row[field])
				# if the inner_dict already has a value for the stat category,
				# (meaning this row is for a player who has already been
				# added), then the current row's stat category value is 
				# added to the pre-existing total
            # else:
				# if the outer dictionary is empty, which would only happen
				# for the first field in the first row in statistics 
				# (first player)
                # career_stats[row[playerid]] = inner_dict
                # inner_dict[field] = int(row[field])
				# if the inner_dict doesn't already exist (i.e. this is the
				# first time the player has appeared in the table),
				# the stat category's total is set to be 
				# the current row's stat category value
	        
		    
		
    return career_stats


def compute_top_stats_career(info, formula, numplayers):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
    """
	
    statistics = read_csv_as_list_dict(info["battingfile"], info["separator"], info["quote"])
    
    aggregated_statistics = aggregate_by_player_id(statistics, info["playerid"], info["battingfields"])
    
    list_aggregated_stats = nested_dict_to_list_dict(aggregated_statistics)
	# used my own function here to turn the nested dict into a list of dicts

    top_ids_and_stats = top_player_ids(info, list_aggregated_stats, formula, numplayers)
	
    return lookup_player_names(info, top_ids_and_stats)


##
## Provided testing code
##

def test_baseball_statistics():
    """
    Simple testing code.
    """

    #
    # Dictionary containing information needed to access baseball statistics
    # This information is all tied to the format and contents of the CSV files
    #
    baseballdatainfo = {"masterfile": "Master_2016.csv",   # Name of Master CSV file
                        "battingfile": "Batting_2016.csv", # Name of Batting CSV file
                        "separator": ",",                  # Separator character in CSV files
                        "quote": '"',                      # Quote character in CSV files
                        "playerid": "playerID",            # Player ID field name
                        "firstname": "nameFirst",          # First name field name
                        "lastname": "nameLast",            # Last name field name
                        "yearid": "yearID",                # Year field name
                        "atbats": "AB",                    # At bats field name
                        "hits": "H",                       # Hits field name
                        "doubles": "2B",                   # Doubles field name
                        "triples": "3B",                   # Triples field name
                        "homeruns": "HR",                  # Home runs field name
                        "walks": "BB",                     # Walks field name
                        "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]}

    print("Top 5 batting averages in 1923")
    top_batting_average_1923 = compute_top_stats_year(baseballdatainfo, batting_average, 5, 1923)
    for player in top_batting_average_1923:
        print(player)
    print("")

    print("Top 10 batting averages in 2010")
    top_batting_average_2010 = compute_top_stats_year(baseballdatainfo, batting_average, 10, 2010)
    for player in top_batting_average_2010:
        print(player)
    print("")

    print("Top 10 on-base percentage in 2010")
    top_onbase_2010 = compute_top_stats_year(baseballdatainfo, onbase_percentage, 10, 2010)
    for player in top_onbase_2010:
        print(player)
    print("")

    print("Top 10 slugging percentage in 2010")
    top_slugging_2010 = compute_top_stats_year(baseballdatainfo, slugging_percentage, 10, 2010)
    for player in top_slugging_2010:
        print(player)
    print("")

    # You can also use lambdas for the formula
    #  This one computes onbase plus slugging percentage
    print("Top 10 OPS in 2010")
    top_ops_2010 = compute_top_stats_year(baseballdatainfo,
                                          lambda info, stats: (onbase_percentage(info, stats) +
                                                               slugging_percentage(info, stats)),
                                          10, 2010)
    for player in top_ops_2010:
        print(player)
    print("")

    print("Top 20 career batting averages")
    top_batting_average_career = compute_top_stats_career(baseballdatainfo, batting_average, 20)
    for player in top_batting_average_career:
        print(player)
    print("")
	
	#########################
	# My own tests
	
    # print(top_player_ids(baseballdatainfo, read_csv_as_list_dict("batting1.csv", ",", "\""), batting_average, 4))
    # print(lookup_player_names(baseballdatainfo, top_player_ids(baseballdatainfo, read_csv_as_list_dict("Batting_2016.csv", ",", "\""), batting_average, 5)))


# Make sure the following call to test_baseball_statistics is
# commented out when submitting to OwlTest/CourseraTest.

test_baseball_statistics()

# Some progress tests

# print(filter_by_year(read_csv_as_list_dict("batting1.csv", ",", "\""), 2021, "year"))
# print(aggregate_by_player_id([{'player': '1', 'stat1': '3', 'stat2': '4', 'stat3': '5'},
# {'player': '1', 'stat1': '2', 'stat2': '1', 'stat3': '8'},
# {'player': '1', 'stat1': '5', 'stat2': '7', 'stat3': '4'}],
# 'player', ['stat1']))
# print()
# print(aggregate_by_player_id([{'player': '1', 'stat1': '3', 'stat2': '4', 'stat3': '5'},
# {'player': '2', 'stat1': '1', 'stat2': '2', 'stat3': '3'},
# {'player': '3', 'stat1': '4', 'stat2': '1', 'stat3': '6'}],
# 'player', ['stat1', 'stat3']))
# print()
# print("test 3: ")
# print(aggregate_by_player_id([{'player': '1', 'stat1': '3', 'stat2': '4', 'stat3': '5'},
# {'player': '1', 'stat1': '2', 'stat2': '1', 'stat3': '8'},
# {'player': '1', 'stat1': '5', 'stat2': '7', 'stat3': '4'}],
# 'player', ['stat1']))
# print(compute_top_stats_career({'masterfile': 'master1.csv', 'battingfile': 'batting1.csv', 'separator': ',', 'quote': '"', 
# 'playerid': 'player', 'firstname': 'firstname', 'lastname': 'lastname', 'yearid': 'year', 
# 'atbats': 'atbats', 'hits': 'hits', 'doubles': 'doubles', 'triples': 'triples', 'homeruns': 'homers', 'walks': 'walks', 
# 'battingfields': ['atbats', 'hits', 'doubles', 'triples', 'homers', 'walks']},
# batting_average, 4))