import requests
from pprint import pprint
from tkinter import *

from dotenv import load_dotenv
import os

load_dotenv()
# window = Tk()

# label = Label(window, text="Résultats TOP 14")
# label.pack()

# window.mainloop()

# ------------------------------

url = "https://api-rugby.p.rapidapi.com/"

headers = {
		"X-RapidAPI-Key": os.getenv("X-RAPIDAPI-KEY"),
		"X-RapidAPI-Host": os.getenv("X-RAPIDAPI-HOST")
	}


# ------------------------------


def get_matches_from_league(id_league: str, season: str) -> dict:
	"""Fonction permettant de récupérer tous les matchs passés, en cours et à venir d'une compétition

	Args:
		id_league (str): ID de la compétition
		season (str): Saison souhaitée

	Return:
		Un dictionnaire avec les informations sur les matchs avec le format :
			"date" : La date et l'heure du match
			"home" : L'équipe à domicile
			"away" : L'équie à l'extérieur
			"results" : Le résultat du match
	"""
    
	games_url = url + "games"

	querystring = {"league":id_league,"season":season}

	headers = {
		"X-RapidAPI-Key": os.getenv("X-RAPIDAPI-KEY"),
		"X-RapidAPI-Host": os.getenv("X-RAPIDAPI-HOST")
	}

	response = requests.get(games_url, headers=headers, params=querystring)
	response_json = response.json()["response"]

	list_match = []

	for match in response_json:
		info_match = {
			"date": match["date"].split("T")[0] + " " + match["date"].split("T")[1].split("+")[0],
			"home": match["teams"]["home"]["name"],
			"away": match["teams"]["away"]["name"],
			"results": str(match["scores"]["home"]) + " - " + str(match["scores"]["away"])
		}
		list_match.append(info_match)
		
	return list_match

def get_id_teams(id_league: str, season: str) -> dict:
	"""Une fonction permettant de récupérer un dictionnaire mettant en relation les équipes d'une compétition et leur ID

	Args:
		id_league (str): ID de la compétition
		season (str): Saison souhaitée

	Returns:
		dict: Un dictionnaire de chaînes de caractères
	"""

	teams_url = url + "teams"

	params = {"league": id_league, "season": season}
	response = requests.get(teams_url, headers=headers, params=params)
	response_json = response.json()["response"]

	teams_id = []

	for team in response_json:
		info_team = {
			"name": team["name"],
			"id": team["id"]
		}

		teams_id.append(info_team)

	return teams_id

# match_top14_2023 = get_matches_from_league("16", "2023")
# pprint(match_top14_2023)

pprint(get_id_teams("16", "2023"))