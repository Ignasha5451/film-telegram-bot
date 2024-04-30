"""
Module: tele_bot_API/util/messages.py
Defines messages used by the bot for providing help, advanced search guidance, and history display.
"""

# Help message providing an overview of the bot's functionality and available commands
help_message = """
<b>{bot_name}</b> bot is a special bot based on the following free Rapid API:
https://rapidapi.com/gox-ai-gox-ai-default/api/ott-details

This bot supports the following commands:

🎬 Film search (by title):
A command that takes the title of a movie and displays basic information about it.

🔎 Film advanced search (by params):
A command that takes various parameters such as release year, IMDb rating, genre, language etc. 
and returns N movies corresponding to them.

🕒 Last arrivals:
A command that returns N latest arrivals from different platforms.

📜 History:
A command that displays the history of the last N requests.

👋 Hello:
A command that says "Hello" to the user.

📞 Help:
A command that briefly describes the bot and the available commands
"""

# Message providing guidance for advanced search parameters
advanced_search_message = """
Enter the parameters you want to search by (you can combine any parameters).

<b>The parameters can be the following:</b>
Start year: Enter any year between 1970 to 2022 to get results.
End year: Enter any year from 1970 to 2022 to get results (must be no less than start year).
Min IMDb: Enter any IMDb rating value between 0 to 10 to get results.
Max IMDb: Enter any IMDb rating value between 0 to 10 to get results (must be no less than min IMDb).
Genre: Use comma seperated values to enter multiple genre eg : action, horror.
Sort: Enter values highestrated , lowestrated , latest , oldest to sort results accodingly.
Count: Enter how many movies matching the parameters you want to receive (maximum 50, default 10).

<b>The message should look like:</b>
Start year: 2000
End year: 2010
Min IMDb: 5
Max IMDb: 7
Genre: action, horror
Sort: latest
Count: 10
"""

# Message template for displaying history information
history_message = """
Your request:
{request}

My response:
{response}

Response send date and time:
{datetime}
"""
