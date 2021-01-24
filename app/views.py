from django.shortcuts import render
from django.http import HttpResponse
from app.models import Player
from datetime import date
from datetime import datetime
from django.contrib import messages

#external
import requests


players = [
    {
        "id":1,
        "first_name":"Kyle",
        "last_name":"Lowry",
        "position":"G",
    },
    {
        "id":2,
        "first_name":"Pascal",
        "last_name":"Siakam",
        "position":"F",
    },
    {
        "id":3,
        "first_name":"Fred",
        "last_name":"Vanvleet",
        "position":"G",
    },
    {
        "id":237,
        "first_name":"LeBron",
        "last_name":"James",
        "position":"F",
    }
]

def home(request):    
    return render(request,'home.html')

def page(request):
    result_general = {}
    result_last_five_games = {}
    list_season_averages = {}
    #result_season_averages = {}
    #temp_season_averages = {}

    
    # Code Snippet to Populate Databse with API Data.
    # all_players = {}
    # all_players_url = 'https://www.balldontlie.io/api/v1/players'
    # response_all_players = requests.get(all_players_url)
    # temp_all_players = response_all_players.json()
    # result_all_players = temp_all_players['data']
    # for i in result_all_players:
    #     player_data = Player(
    #         player_id = i['id'],
    #         first_name = i['first_name'],
    #         last_name = i['last_name']
    #     )
    #     player_data.save()
    #     all_players = Player.objects.all().order_by('-id')


    if 'new_Text' in request.GET:
        string = request.GET.get('new_Text')
        lowercase_string = string.lower()

        # Todays date and date four months ago:
        today = date.today()
        past_day_int = today.day
        past_day_str = str(past_day_int).zfill(2)
        past_month_int = (today.month - 4) % 12
        past_month_str = str(past_month_int).zfill(2)
        past_year_str = str(today.year + ((today.month - 4) // 12))
        four_months_before = past_year_str + '-' + past_month_str + '-' + past_day_str
        today_date = str(today)

        try: 
            if lowercase_string.islower():
            # Primitive Search Function Code - Splits it by ' '. 
            # Checks first and last name database values.
            #fullNameList = string.split(' ')
            # id = ''
            # for i in players:
            #     if i['first_name'] == fullNameList[0] and i['last_name'] == fullNameList[1]:
            #         id = i['id']

                url_list = []
                general_data_url = 'https://www.balldontlie.io/api/v1/players?search=%s' %string
                response_general = requests.get(general_data_url)
                temp_result_general = response_general.json()
                result_general = temp_result_general['data']
                if len(result_general) > 1:
                    messages.error(request, "Too many players with the name \"%s\"." %string)
                player_id = result_general[0]['id']

                # FIRST GAME YEAR DATA
                first_game_season_url = 'https://www.balldontlie.io/api/v1/stats?per_page=1&player_ids[]=%s' %player_id
                response_first_game_season = requests.get(first_game_season_url)
                temp_first_game_season = response_first_game_season.json()
                result_first_game_season = temp_first_game_season['data']
                first_game_season = result_first_game_season[0]['game']['season']

                # LAST GAME YEAR DATA
                last_five_games_url = 'https://www.balldontlie.io/api/v1/stats?player_ids[]=%s&start_date=%s&end_date=%s&per_page=100' %(player_id,four_months_before,today_date)
                response_last_five_games = requests.get(last_five_games_url)
                temp_result_last_five_games = response_last_five_games.json()
                result_last_five_games = temp_result_last_five_games['data']

                result_last_page = temp_result_last_five_games['meta']
                last_page =  int(result_last_page['total_pages'])

                last_game_season = result_last_five_games[0]['game']['season']

                # TRYING TO GET A NEW METHOD TO WORK TO GET RETIRED PLAYERS
                # DOESN'T WORK BECAUSE API DATA IS NOT SORTED
                # all_games_url = 'https://www.balldontlie.io/api/v1/stats?player_ids[]=%s&end_date=%s&per_page=1' %(player_id,today_date)
                # response_all_games = requests.get(all_games_url)
                # temp_result_all_games = response_all_games.json()
                # result_last_page = temp_result_all_games['meta']
                # last_page =  int(result_last_page['total_pages'])

                # last_game_game_url = 'https://www.balldontlie.io/api/v1/stats?player_ids[]=%s&end_date=%s&page=%s&per_page=1' %(player_id,today_date,last_page)
                # response_last_game = requests.get(last_game_game_url)
                # temp_result_last_game = response_last_game.json()
                # result_last_game = temp_result_last_game['data']
                # last_game_season = result_last_game[0]['game']['season']

                list_season_averages = []
                for i in range(int(first_game_season),int(last_game_season)+1):
                    working_season = i
                    season_averages_url = 'https://www.balldontlie.io/api/v1/season_averages?player_ids[]=%s&season=%s' %(player_id,working_season)
                    response_season_averages = requests.get(season_averages_url)
                    temp_season_averages = response_season_averages.json()
                    result_season_averages = temp_season_averages['data']
                    if result_season_averages == []:
                        result_season_averages = [{}]
                    result_season_averages = result_season_averages[0]
                    list_season_averages.append(result_season_averages)
        except:
            messages.error(request,"No data for given player(s). Please choose another.")


    return render(request, 'page.html',{'season_averages':list_season_averages, 'general_info': result_general, 'last_five_games':result_last_five_games})