from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

#Dictionary of team identifiers
team_id = {'Celtics': '1610612738',
           'Nets': '1610612751',
           'Knicks': '1610612752',
           '76ers': '1610612755',
           'Raptors': '1610612761',
           'Bulls': '1610612741',
           'Cavaliers': '1610612739',
           'Pistons': '1610612765',
           'Pacers': '1610612754',
           'Bucks': '1610612749',
           'Hawks': '1610612737',
           'Hornets': '1610612766',
           'Heat': '1610612748',
           'Magic': '1610612753',
           'Wizards': '1610612764',
           'Nuggets': '1610612743',
           'Timberwolves': '1610612750',
           'Thunder': '1610612760',
           'Blazers': '1610612757',
           'Jazz': '1610612762',
           'Warriors': '1610612744',
           'Clippers': '1610612746',
           'Lakers': '1610612747',
           'Suns': '1610612756',
           'Kings': '1610612758',
           'Mavericks': '1610612742',
           'Rockets': '1610612745',
           'Grizzlies': '1610612763',
           'Pelicans': '1610612740',
           'Spurs': '1610612759'
           }

def team_stats_finder(team):
    if team not in team_id:
        team = input("Team not in team list, retype please:\n")

    #Get team identifier
    identifier = team_id[team]

    #Import driver
    driver = webdriver.Chrome()

    #Navigate to NBA official website
    driver.get("https://www.nba.com/teams")

    #Close the "cookies" popup
    try:
        driver.find_element(By.XPATH,"//button[@class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']").click()
    except:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']")))
        driver.find_element(By.XPATH,"//button[@class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']").click()
    finally:
        pass

    #Navigate to team
    driver.find_element(By.XPATH, "//a[@href='/stats/team/" + identifier + "']").click()

    time.sleep(3)
    #create list of players
    player_stats = driver.find_elements(By.XPATH, "//a[contains(@href, '/stats/player/')]")
    player_names = [x.text for x in player_stats]

    #initialize players list
    players_list = []
    for i in range(len(player_names)):
        name = player_names[i]
        stats = driver.find_elements(By.XPATH, "//a[contains(@href, '/stats/player/')]")

        time.sleep(2.5)

        try:
            #Navigate to the player's personal stats
            stats[i].click()
        except IndexError:
            time.sleep(3)
            stats[i].click()

        time.sleep(0.5)

        #find where the PPG element is located and pull their ppg
        ppg_finder = driver.find_element(By.XPATH, "//p[text()='PPG']/following-sibling::p[@class='PlayerSummary_playerStatValue___EDg_']")
        ppg = ppg_finder.text
        if ppg == '--':
            ppg = 0.0
        else:
            ppg = float(ppg)

        #Get player's rpg
        rpg_finder = driver.find_element(By.XPATH, "//p[text()='RPG']/following-sibling::p[@class='PlayerSummary_playerStatValue___EDg_']")
        rpg = rpg_finder.text
        if rpg == '--':
            rpg = 0.0
        else:
            rpg = float(rpg)

        #Get player's apg
        apg_finder = driver.find_element(By.XPATH, "//p[text()='APG']/following-sibling::p[@class='PlayerSummary_playerStatValue___EDg_']")
        apg = apg_finder.text
        if apg == '--':
            apg = 0.0
        else:
            apg = float(apg)

        players_list.append({'Player Name': name,
                             'PPG': ppg,
                             'RPG': rpg,
                             'APG': apg})
        driver.back()
        x = pd.DataFrame(players_list)
    return x
