########################################################################################################
#                                                                                                      #
#     Covid-19-Creating a Realtime CoronaVirus Outbreak Notification System Using Python Programming   #
#                                                                                                      #
########################################################################################################

from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from plyer import notification
import time

while True:
    URL = "https://www.mohfw.gov.in/"
    try:
        r = requests.get(URL)
    except:
        notification.notify("Network Problem", "Please check your internet connection")

    soup = bs(r.content, "html5lib")
    tables = soup.find_all("table")

    for table in tables:

        # Take the Html Table into DataFrame
        df_list = pd.read_html(str(table))

        # Remove 1st Column From Table(DataFrame)
        df = df_list[0].loc[:, df_list[0].columns != 'S. No.']

        # Apply the Filter on Table (Retrive the Data For some state only)
        state_list = ['Andhra Pradesh', 'Maharashtra', 'Telengana', 'Delhi']

        ## If you want notification for all States then remove comment from next line
        # state_list = df['Name of State / UT'][:-2].tolist()
        filter_df = df[df['Name of State / UT'].isin(state_list)]

        # Convert DataFrane to List
        df = [filter_df.columns.values.tolist()] + filter_df.values.tolist()

        # Create Notification for each Record(State)
        for rec in df[1:]:
            nTitle = 'Case of Covid 19'
            nText = f"State : {rec[0]}\nCases: {rec[1]} & Cured: {rec[2]}\nDeath: {rec[3]}"
            notification.notify(title=nTitle,
                                message=nText,
                                app_icon=r"coronavirus-2073661-1755123.ico",
                                timeout=15)
            time.sleep(16)

    time.sleep(900)
