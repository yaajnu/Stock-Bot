# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions



# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union
from nsetools import Nse
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

nse=Nse()

class StockForm(Action):

    def name(self) -> Text:
        return "stock_form"

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        return {
            'stock_price':[
                self.from_entity(entity='stock_code'),
                self.from_intent(intent='deny',value="None")
            ]
        }
    def run(self,
     dispatcher: CollectingDispatcher,
     tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        stock_code=next(tracker.get_latest_entity_values('stock_code',None))

        if nse.is_valid_code(stock_code):
            stock_nse=nse.get_quote(f'{stock_code}')
            price=stock_nse['basePrice']
            company=stock_nse['companyName']
            msg=f'The current stock price of {company} is {price}'
            dispatcher.utter_message(msg)
            dispatcher.utter_message("Would you like to check other stocks' prices")
        else:
            msg='Please enter correct code'
            dispatcher.utter_message(msg)


        return []

class select_action(Action):
    def name(self):
        return "select_action"
    
    def run(self,dispatcher: CollectingDispatcher,
     tracker: Tracker, domain: Dict[Text, Any]):
        buttons=[]
        buttons.append({ "title": "Find out the profit/loss of your portfolio in real-time", "payload": "/inform{\'opc\':  \'1\' }"  })
        buttons.append({ "title": "Check current price of stocks.", "payload": "/inform{\'opc\':  \'2\' }"  })
        dispatcher.utter_button_message("Choose from the list:", buttons)