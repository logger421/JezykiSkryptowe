#!/bin/zsh

GAMEPLAY_CHOICE_REGEX='^[0-9]$'
GAMEPLAY_COMP_CHOICE_REGEX='^[1-9]$'
MENU_CHOICE_REGEX='^[0-4]$'
SAVE_AND_EXIT=false
USER1_SYMBOL=X
USER2_SYMBOL=O

SAVES_DIR="$(dirname $0)/saves"
echo "Saves dir: $SAVES_DIR"

STATE=([1]=1 [2]=2 [3]=3 [4]=4 [5]=5 [6]=6 [7]=7 [8]=8 [9]=9)

menu() {
  echo "  ================================="
  echo "  # What you would like to do?"
  echo "  # 0. Exit"
  echo "  # 1. Player vs player tour game"
  echo "  # 2. Player vs computer tour game"
  echo "  # 3. Load previously saved game"
  echo "  ================================="
  printf "  Enter your choice: "
  read -r MENU_CHOICE
  if ! [[ $MENU_CHOICE =~ $MENU_CHOICE_REGEX ]]; then
    echo "Invalid input"
    menu
  fi
}

draw_game() {
  echo "\n===================="
  echo "# USER1: ${USER1_SYMBOL}, USER2: ${USER2_SYMBOL}"
  echo "===================="
  echo " -------------"
  echo " | ${STATE[7]} | ${STATE[8]} | ${STATE[9]} |"
  echo " |---+---+---|"
  echo " | ${STATE[4]} | ${STATE[5]} | ${STATE[6]} |"
  echo " |---+---+---|"
  echo " | ${STATE[1]} | ${STATE[2]} | ${STATE[3]} |"
  echo " -------------"
}

# This will save state to file
save() {
  # Creat dir for saves
  if [ ! -d "$SAVES_DIR" ]; then
    mkdir $SAVES_DIR
    echo "Created directory $SAVES_DIR"
  fi
  FILE_TIMESTAMP=$(date +%s)
}

# This will load state of game from selected save
load() {
  if [ ! -d "SAVES_DIR" ]; then
      echo "$SAVES_DIR doesn't exists, so there are no saves to load!"
  else
    echo 'Choose file to load data:'
    ls -l "$SAVES_DIR"
    printf "Enter filename: "
    read -r SAVE_FILENAME
  fi
}

end_game() {
  local WINNER_SYMBOL=$1
  echo "======================"
  echo "The winner is: "
  if [[ $WINNER_SYMBOL == $USER1_SYMBOL && $USER2 != "COMPUTER" ]]; then
    printf "USER1"
  else
    printf "USER2"
  fi

  if [[ $WINNER_SYMBOL == $USER1_SYMBOL && $USER2 == "COMPUTER" ]]; then
    printf "USER1"
  else
    printf "COMPUTER"
  fi
  echo "======================"
  exit 0
}

check_vertical_lines() {
  for i in 1 2 3; do
      NEXT=$(($i + 3))
      NEXTNEXT=$(($NEXT + 3))
      WINNER_SYMBOL=${STATE[$i]}
      [[ ${STATE[$i]} == ${STATE[$NEXT]} ]] && [[ ${STATE[$NEXT]} == ${STATE[$NEXTNEXT]} ]] && end_game $WINNER_SYMBOL
  done
}

check_horizontal_lines() {
  for i in 1 4 7; do
    NEXT=$(($i + 1))
    NEXTNEXT=$(($NEXT + 1))
    WINNER_SYMBOL=${STATE[$i]}
    [[ ${STATE[$i]} == ${STATE[$NEXT]} ]] && [[ ${STATE[$NEXT]} == ${STATE[$NEXTNEXT]} ]] && end_game $WINNER_SYMBOL
  done
}

check_diagonal_lines() {
  WINNER_SYMBOL=${STATE[5]}
  [[ ${STATE[1]} == ${STATE[5]} ]] && [[ ${STATE[5]} == ${STATE[9]} ]] && end_game $WINNER_SYMBOL
  [[ ${STATE[7]} == ${STATE[5]} ]] && [[ ${STATE[5]} == ${STATE[3]} ]] && end_game $WINNER_SYMBOL
}

# This will check if game ended and who won
check_winner() {
  check_diagonal_lines
  check_vertical_lines
  check_horizontal_lines
}

player_move() {
  printf "Enter your choice $2 [1-9] or press 0 to save and exit: "
  read -r CHOICE

  # check if input is valid
  if ! [[ $CHOICE =~ $GAMEPLAY_CHOICE_REGEX ]]; then
    echo "Invalid input"
    player_move $1 $2
  fi

  # check if user pressed 0 then save and exit to main menu
  if [[ $CHOICE == 0 ]]; then
    save
    SAVE_AND_EXIT=true
    return 0
  fi

  # check if selected value was not selected
  if ! [[ ${STATE[$CHOICE]} =~ $GAMEPLAY_CHOICE_REGEX ]]; then
    echo "Already occupied"
    player_move $1 $2
  fi
  STATE[$CHOICE]=$1
}

computer_move() {
  COMPUTER_CHOICE=$(($RANDOM % 9 + 1))
  [[ ! ${STATE[$COMPUTER_CHOICE]} =~ $GAMEPLAY_COMP_CHOICE_REGEX ]] && computer_move
  STATE[$COMPUTER_CHOICE]=$USER2_SYMBOL
}

# player vs player gameplay
vs_player() {
  while true; do
    player_move $USER1_SYMBOL 'USER1'
    if $SAVE_AND_EXIT; then
      SAVE_AND_EXIT=false
      echo "Game saved. Exiting."
      break
    fi
    draw_game
    check_winner
    player_move $USER2_SYMBOL 'USER2'
    if $SAVE_AND_EXIT; then
      echo "Game saved. Exiting."
      SAVE_AND_EXIT=false
      break
    fi
    draw_game
    check_winner
  done
}

# player vs machine gameplay
vs_computer() {
  while true; do
    player_move $USER1_SYMBOL 'USER1'
    draw_game
    check_winner
    computer_move
    draw_game
    check_winner
  done
}

while true; do
  menu
  if [[ $MENU_CHOICE == 0 ]]; then
      exit 0
  fi
  if [[ $MENU_CHOICE == 1 ]]; then
    USER2="USER2"
    draw_game
    vs_player
  fi
  if [[ $MENU_CHOICE == 2 ]]; then
    USER2="COMPUTER"
    draw_game
    vs_computer
    exit 0
  fi
  if [[ $MENU_CHOICE == 3 ]]; then
    load
    exit 0
  fi
done