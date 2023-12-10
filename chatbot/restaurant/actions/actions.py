# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json

class ActionCheckOpeningHours(Action):

    def name(self) -> Text:
        return "action_check_opening_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        requested_day = tracker.get_slot('day')
        requested_time = tracker.get_slot('time')

        # Load opening hours from JSON file
        with open('opening_hours.json') as json_file:
            data = json.load(json_file)
            hours = data['items'].get(requested_day, None)

            # Check if the restaurant is open
            if hours and hours['open'] <= requested_time <= hours['close']:
                dispatcher.utter_message(text=f"We're open on {requested_day} at {requested_time}.")
            else:
                dispatcher.utter_message(text=f"We're closed on {requested_day} at {requested_time}.")

        return []

class ActionListMenu(Action):

    def name(self) -> Text:
        return "action_list_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Load menu items from JSON file
        with open('menu.json') as json_file:
            data = json.load(json_file)
            menu_items = data['items']

            # Create a response with menu items
            response = "Here's our menu:\n"
            for item in menu_items:
                response += f"- {item['name']}: ${item['price']}\n"

            dispatcher.utter_message(text=response)

        return []

# Define more custom actions as needed
