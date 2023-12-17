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
        order_item = tracker.get_slot("menu_item")
        special_request_keyword = tracker.get_slot("special_request_keyword")
        special_request_item = tracker.get_slot("special_request_item")
        order = tracker.get_slot("order")

        if not order:
            order = []

        with open('actions/menu.json', 'r') as file:
            menu = json.load(file)["items"]

        menu_names = [item["name"] for item in menu]

        if order_item in menu_names:
            if special_request_item and special_request_keyword:
                order.append(f"{order_item} - {special_request_keyword} {special_request_item}")
            else:
                order.append(f"{order_item}")
        else:
            dispatcher.utter_message(text=f"Sorry, we don't have {order_item} on the menu.")
            return [SlotSet("menu_item", None),
                    SlotSet("special_request_keyword", None),
                    SlotSet("special_request_item", None)]

        dispatcher.utter_message("Certainly! Adding to order. Would you like to add something else?")

        return [SlotSet("order", order),
                SlotSet("menu_item", None),
                SlotSet("special_request_keyword", None),
                SlotSet("special_request_item", None)]


class ActionShowOrder(Action):
    def name(self):
        return "action_show_order"

    def run(self, dispatcher, tracker, domain):
        order = tracker.get_slot("order")

        if not order:
            dispatcher.utter_message("Your order is empty.")

        else:
            dispatcher.utter_message("As far you have ordered: ")
            for item in order:
                dispatcher.utter_message(f"- {item}")
            dispatcher.utter_message("Is that all?")
        return []


class ActionFinalizeOrder(Action):
    def name(self):
        return "action_finalize_order"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        order = tracker.get_slot("order")
        if not order or len(order) == 0:
            dispatcher.utter_message("Your order is empty. Please add something before proceeding!")
            return []

        with open('actions/menu.json', 'r') as file:
            menu = json.load(file)["items"]

            delivery_time = 0
            for item in order:
                for menu_item in menu:
                    item_name = item.split()[0].lower().capitalize()
                    if menu_item["name"] == item_name:
                        delivery_time += menu_item["preparation_time"]

            dispatcher.utter_message(text="Your order: ")
            for item in order:
                dispatcher.utter_message(f"- {item}")
            dispatcher.utter_message(f"Your estimated delivery time: {delivery_time}")

        return [SlotSet("order", None)]
