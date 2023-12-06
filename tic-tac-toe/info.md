## Tic-tac-toe
This is a simple implementation of bash tic-tac-toe game.
### Possible game scenarios: 
- User can play vs another player.
- User can play vs computer (`random generator 1-9`).
- User can save current game state and load it later.

> *NOTE*
> 
> To save and load files if not existing in project directory `/saves` dir will
> be created. To load save file user will be prompted to enter filename of 
> regarding save. Each save will have name `save_POSTFIX` where `POSTFIX` will be equal to
>seconds from UNIX epoch time.


TODO
- [x] Save should be saved and loaded correctly.
- [x] Loaded save should start correctly from next user tour.
- [x] After saving and starting new tour game state should be restarted.
- [ ] Refactor code to use less global variables