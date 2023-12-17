# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json


def convert_time_to_int(time_str):
    # Check if the time is in 12-hour format (contains AM or PM)
    if 'AM' in time_str or 'PM' in time_str:
        # Parse 12-hour format
        parsed_time = datetime.strptime(time_str, '%I:%M%p')
    else:
        # Parse 24-hour format
        parsed_time = datetime.strptime(time_str, '%H:%M')

    return parsed_time.hour


class ActionCheckIfOpen(Action):
    def name(self) -> Text:
        return "action_check_if_open"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        requested_day = tracker.get_slot('day').lower().capitalize()
        requested_time = tracker.get_slot('time')

        with open('actions/opening_hours.json') as json_file:
            data = json.load(json_file)
            hours = data['items'].get(requested_day, None)

            if hours and hours['open'] <= convert_time_to_int(requested_time) < hours['close']:
                dispatcher.utter_message(text=f"We're open on {requested_day} at {requested_time}.")
            else:
                dispatcher.utter_message(text=f"We're closed on {requested_day} at {requested_time}.")

        return []


class ActionCheckOpenNow(Action):
    def name(self) -> Text:
        return "action_check_open_now"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        now = datetime.now()
        requested_day = now.strftime("%A").lower().capitalize()
        requested_time = convert_time_to_int(now.strftime('%H:%M'))

        with open('actions/opening_hours.json') as json_file:
            data = json.load(json_file)
            hours = data['items'].get(requested_day, None)

            if hours and hours['open'] <= int(requested_time) < hours['close']:
                dispatcher.utter_message(text=f"Yes, we are open now.")
            else:
                dispatcher.utter_message(text=f"No, we are closed.")

        return []


class ActionCheckOpeningHours(Action):
    def name(self) -> Text:
        return "action_check_opening_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        requested_day = tracker.get_slot('day').lower().capitalize()
        dispatcher.utter_message(text=f"requested_day is {requested_day}")
        with open('actions/opening_hours.json') as json_file:
            data = json.load(json_file)
            hours = data['items'].get(requested_day, None)
            dispatcher.utter_message(text=f"We're open on {requested_day} from {hours['open']} to {hours['close']}.")

        return []


class ActionListMenu(Action):

    def name(self) -> Text:
        return "action_list_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('actions/menu.json') as json_file:
            data = json.load(json_file)
            menu_items = data['items']

            response = "Here's our menu:\n"
            for item in menu_items:
                response += f"- {item['name']}: ${item['price']}\n"

            dispatcher.utter_message(text=response)

        return []


class ActionTakeOrder(Action):

    def name(self) -> Text:
        return "action_take_order"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_items = tracker.get_slot("menu_item")
        special_request_keyword = tracker.get_slot("special_request_keyword")
        special_request_items = tracker.get_slot("special_request_item")

        dispatcher.utter_message(text=f"order items: {order_items}")
        dispatcher.utter_message(text=f"special request keyword: {special_request_keyword}")
        dispatcher.utter_message(text=f"special requests items: {special_request_items}")

        # Load menu items from JSON file
        with open('actions/menu.json', 'r') as file:
            menu = json.load(file)["items"]

        menu_names = [item["name"] for item in menu]

        validated_order = []
        for item in order_items:
            if item in menu_names:
                validated_order.append(item)
            else:
                dispatcher.utter_message(text=f"Sorry, we don't have {item} on the menu.")

        # Construct order confirmation message
        if validated_order:
            order_confirmation = "You have ordered: "
            order_confirmation += ", ".join(validated_order)
            if special_request:
                order_confirmation += ". With special requests: "
                order_confirmation += ", ".join(special_request_items)
            dispatcher.utter_message(text=order_confirmation)
        else:
            dispatcher.utter_message(text="Please choose items from our menu.")

        return []