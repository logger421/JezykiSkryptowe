## Chatbot project
This project is rasa based chatbot, it's main purpose is taking orders from user and helping him
with checking if restaurant is open and what restaurant could offer to him.


### Requirements

1. A chatbot with the trained ability to handle at least 3 ways to phrase those intents.
2. Information about opening hours and menu items should be fetched from the configuration file.
3. Chatbot needs to process the order and confirm purchased meals, as well as additional requests.
4. Chatbot needs to confirm when the meal will be available as a pick-up in the restaurant.
5. Integrate it with one of the platforms mentioned in Chabots_Integration notebook.
6. (optional) Chatbot should ask and confirm the delivery address instead of pick-up option.

### TODO
- [x] Integration with discord should work correctly
- [ ] Small refactoring
- [ ] Bot should work for public channels, currently it's working on private chat. It could be creation problem.
- [ ] Discord messages formatting should be added, for now all is flattened during snd/rec.