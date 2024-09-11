import random  # Import random for shuffle


# Create Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []
        self.played = []
        self.sum = 0
        self.alive = 1

    # Defines print string for Player
    def __str__(self):
        return self.name


# Create Card class
class Card:
    # Defines card ranks and suits
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['clubs', 'diamonds', 'hearts', 'spades']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.symbols = {  # Defines suit Unicode symbols
            'spades': "\u001b[34m\u2660\u001b[0m",
            'clubs': "\u001b[34m\u2663\u001b[0m",
            'diamonds': "\u001b[31m\u2666\u001b[0m",
            'hearts': "\u001b[31m\u2665\u001b[0m"
        }
        self.card_values = {  # Defines card values based on rank
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        self.value = self.card_values[rank]
        self.symbol = self.symbols[suit]

    # Defines print string for Cards - Makes them look nicer
    def __str__(self):
        card_str = ""
        if len(self.rank) <= 1:  # For all cards other than 10
            card_str += '┌─────────┐\n'
            card_str += f'| {self.rank}       |\n'
            card_str += '|         |\n'
            card_str += f'|    {self.symbol}    |\n'
            card_str += '|         |\n'
            card_str += f'|      {self.rank}  |\n'
            card_str += '└─────────┘\n'
        else:  # For the "10" cards as it breaks other layout
            card_str += '┌─────────┐\n'
            card_str += f'| {self.rank}      |\n'
            card_str += '|         |\n'
            card_str += f'|    {self.symbol}    |\n'
            card_str += '|         |\n'
            card_str += f'|      {self.rank} |\n'
            card_str += '└─────────┘\n'
        return card_str


players = []
# Create deck from Card class
deck = [Card(rank, suit) for suit in Card.suits for rank in Card.ranks]


# Define the shuffle deck function
def shuffle_deck():
    for i in range(7):  # shuffles deck 7 times (out of nostalgia from childhood)
        random.shuffle(deck)


# Define the deal function, taking players as a property
def deal(players):
    while len(deck) > 0:  # While there are cards in the deck
        for player in players:
            if len(deck) > 0:
                card = deck.pop()  # Removes card from deck
                player.deck.append(card)  # Adds it to the player's deck


# Define the play function, taking the player property
def play(player):
    if len(player.deck) > 0:
        card = player.deck.pop()  # Removes 1 card from player's deck
        print(f'{player.name} revealed')
        print(card)
        player.played.append(card)  # Adds it to played cards
    else:
        print(f'\n{player.name} is out of cards\n')


# Define the give_up function, taking the player property
def give_up(player):
    print(f'\n{player.name} has given up.\n')
    player.played.extend(player.deck)  # Adds all cards from player.deck to player.played
    player.deck.clear()  # Removes all entries from player.deck
    player.alive = 0  # This is referenced later setting player.sum to 0 forcing a loss


# Define the forfeit_or_continue function, taking the player property
def forfeit_or_coninue(player):
    if len(players) > 0:
        if player.name == "AI":
            play(player)
        else:
            # Requests input from user, asking if they want to reveal a card, or forfeit.
            choice = input(
                f"\n{player.name} would you like to (R) Reveal a card or (F) Forfeit? (Defaults to R): \n").strip().upper()
            if choice == "" or choice == "R":
                play(player)
            elif choice == "F":
                give_up(player)
            else:  # Calls the play function as it was the "default" option
                print("Invalid choice. Defaulting to (R) Reveal.")
                play(player)


# Define the hand_value function, taking the cards property
def hand_value(cards):
    total = 0
    for card in cards:
        total += card.value  # Sums total value of cards
    print(f'Hand Value = {total}\n\n')
    return total  # Returns the total


# Define the normal_round function, taking the players property
def normal_round(players):
    for player in players:
        if len(player.deck) > 0:  # If they have cards in their deck
            forfeit_or_coninue(player)
            if player.alive == 0:  # This means the player forfeited
                player.sum = 0
            else:
                player.sum = hand_value(player.played)
        else:  # If they have no cards
            print(f'\n\n{player.name} has no more cards and has been eleminated.')
            print('Better luck next time!\n\n')
            players.remove(player)  # Removes the player from the players list


# Define the war function, taking the players property
def war(players):
    print('\n\n************   War!   ************\n\n')
    for player in players:
        for i in range(4): # Causes this to repeat 4 times
            play(player)
        player.sum = hand_value(player.played)


# Define the winning_hand function, taking the players property
def winning_hand(players):
    top = 0  # Initializes the top variable and sets to 0
    winning_players = players  # Creates the winner list and sets it to the players
    winners = len(winning_players)  # sets winners to the number of players
    while winners > 1:  # As long as there isn't a clear winner
        temp_winner = []
        for player in winning_players:
            sum_hand = player.sum
            if sum_hand > top:
                top = sum_hand
                temp_winner.clear()
                temp_winner.append(player)  # places player in the winner list
            elif sum_hand == top and player not in temp_winner:  # If sum ties winner
                temp_winner.append(player)  # Add player to winner if not already in list
        winning_players = temp_winner
        winners = len(winning_players)  # Updates winners to either reset or leave the loop
        if winners > 1:
            war(winning_players)
    winner = winning_players[0]  # Sets the winner to the entry in the list
    print(f'{winner.name} has won the round!')
    return winner


# Defines the add_cards function, taking the winner and players properties
def add_cards(winner, players):
    for player in players:
        winner.deck.extend(player.played)  # Add played cards to the winners deck
        player.played.clear()  # Clears played cards
        random.shuffle(winner.deck)  # Shuffle the winners deck with the new cards


def cards_remaining(players):  # print total cards in each deck
    print('\n\n******** Round Over ********')
    for player in players:
        print(f'{player.name} has {len(player.deck)} cards left')
    print('****************************\n\n')


def celebrate(players):
    winner = players[0]
    if winner.name == "AI":  # Prints Doom message
        print(''' 
                               ________________
                          ____/ (  (    )   )  \\___
                         /( (  (  )   _    ))  )   )\\
                       ((     (   )(    )  )   (   )  )
                     ((/  ( _(   )   (   _) ) (  () )  )
                    ( (  ( (_)   ((    (   )  .((_ ) .  )_
                   ( (  )    (      (  )    )   ) . ) (   )
                  (  (   (  (   ) (  _  ( _) ).  ) . ) ) ( )
                  ( (  (   ) (  )   (  ))     ) _)(   )  )  )
                 ( (  ( \\ ) (    (_  ( ) ( )  )   ) )  )) ( )
                  (  (   (  (   (_ ( ) ( _    )  ) (  )  )   )
                 ( (  ( (  (  )     (_  )  ) )  _)   ) _( ( )
                  ((  (   )(    (     _    )   _) _(_ (  (_ )
                   (_((__(_(__(( ( ( |  ) ) ) )_))__))_)___)
                   ((__)        \\\\||lll|l||///          \\_))
                            (   /(/ (  )  ) )\\   )
                          (    ( ( ( | | ) ) )\\   )
                           (   /(| / ( )) ) ) )) )
                         (     ( ((((_(|)_)))))     )
                          (      ||\\(|(|)|/||     )
                        (        |(||(||)||||        )
                          (     //|/l|||)|\\\\ \\     )
                        (/ / //  /|//||||\\\\  \\ \\  \\ _)
  ''')
        print('Humanity is lost, AI has taken over the world. Welcome your new robot overlords.')
    else:  # Prints Celebration Message
        print('''
                                   .''.
       .''.      .        *''*    :_\/_:     .
      :_\/_:   _\\(/_  .:.*_\/_*   : /\\ :  .'.:.'.
  .''.: /\\ :   ./)\\   ':'* /\\ * :  '..'.  -=:o:=-
 :_\/_:'.:::.    ' *''*    * '.\\'/.' _\\(/_'.':'.'
 : /\\ : :::::     *_\\/_*     -= o =-  /)\\    '  *
  '..'  ':::'     * /\\ *     .'/.\'.   '
      *            *..*         :
        *
        *
        *
    ''')
        print(f'Congratulations {winner}, you have won the war!')  # Congrats


# Defines the print welcome function
def print_welcome():  # Prints the welcome message and rules for the game
    print("╔═══════════════════════════════════════════╗")
    print("║     *****    Welcome to War.    *****     ║")
    print("║───────────────────────────────────────────║")
    print("║                  Rules:                   ║")
    print("║  1. Each player will take turns revealing ║")
    print("║     cards.                                ║")
    print("║  2. The player with the highest card      ║")
    print("║     value wins the round and takes all    ║")
    print("║     the played cards.                     ║")
    print("║  3. If there's a tie, the players enter   ║")
    print("║     'War'.                                ║")
    print("║  4. In 'War', each tied player reveals    ║")
    print("║     four additional cards.                ║")
    print("║  5. The player with the highest total     ║")
    print("║     value of all revealed cards wins the  ║")
    print("║     'War' round.                          ║")
    print("║  6. The game continues until only one     ║")
    print("║     player has cards left.                ║")
    print("║  7. The last player with cards            ║")
    print("║     is the winner!                        ║")
    print("╚═══════════════════════════════════════════╝")


print_welcome()
num_players = 0  # Initializes the number of players

while True:  # Creates a loop until the correct number of players is entered
    try:
        num_players = int(input('How many players will be playing? (1-4): '))
        if 1 <= num_players <= 4:
            break
        else:  # If a number other than 1-4 is given
            print('Invalid input.')
    except ValueError:  # If something other than a number is entered
        print('Invalid input.')

if num_players == 1:  # If only one player, create an AI player to go against
    while True:
        player_name = input('Enter your name: ')
        if player_name.strip().upper() == "AI":  # Reserved for the computer
            print('Sorry, that name is reserved, try another.')
        else:  # Add player and move on
            player = Player(player_name)
            players.append(player)
            break  # Ends loop
    AI = Player("AI")  # Creates AI player
    players.append(AI)  # Adds AI to players list
    print(f'\n\nWelcome {player} to War. Your opponent is an')
    print('advanced AI threatening the world. Good luck!')
else:  # If more than one player
    for i in range(num_players):  # Asks each player for their name
        while True:  # Create Loop until player name is established
            player_name = input(f'Enter name for player {i + 1}: ')
            if player_name.strip().upper() == "AI":  # Reserved for the computer
                print('Sorry, that name is reserved, try another.')
            elif any(player_name == player.name for player in players):  # already used
                print('Sorry, that name is already taken, try another.')
            else:  # Add player and move on
                player = Player(player_name)
                players.append(player)
                break  # Ends loop
    print("\n\nWelcome to War players:", end=" ")
    for player in players:
        print(player.name, end=". ")  # Adds player's names to the message
    print('Who will come out on top?')
    print('Who will fall on the battlefield? It\'s time to find out.')

shuffle_deck()  # Shuffles the deck
deal(players)  # Deals the deck to each player
active_players = []  # Initializes the active_players list
while True:  # Creates the play loop
    # Determines how many players are left
    for player in players:
        if len(player.deck) > 0:  # checks for each player
            active_players.append(player)  # Adds to active_players
    # As long as 2 players are left
    while len(active_players) > 1:
        normal_round(active_players)  # Reveal card
        winner = winning_hand(active_players)  # Determine winner
        add_cards(winner, active_players)  # Add played cards to winner's hand
        cards_remaining(active_players)  # Prints card count for reamining players
    break  # When only 1 player left, ends loop

celebrate(active_players)  # Prints ASCII art for winner
