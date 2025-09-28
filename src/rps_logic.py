import random

class RPSGame:
    def __init__(self, gamemode):
        # Rounds to Win is basically the gamemode like best of 5 divided by 2 which is 2 plus 1 which is 3
        self.rounds_to_win = gamemode // 2 + 1
        self.player_score = 0  # Sets initial player score to 0
        self.computer_score = 0  # Sets initial computer score to 0

    def total_rounds(self):
        return self.rounds_to_win * 2 - 1  # Gets the total possible number of rounds

    def current_round(self):
        return self.player_score + self.computer_score + 1  # calculates currents round by adding both scores

    # Play turn function that takes in a player choice of either rock, paper, or scissors
    def play_turn(self, player_choice):
        computer_choice = random.choice(['rock', 'paper', 'scissors'])  # Gets a random choice for the computer
        winner = self.determine_winner(player_choice, computer_choice)  # Calls a function to determine winner

        # Increments the score for who won
        if winner == 'player':
            self.player_score += 1
        elif winner == 'computer':
            self.computer_score += 1

        # Returns all necessary components like each choice, winner of the round, score, and if the game is over
        return {
            'player': player_choice,
            'computer': computer_choice,
            'winner': winner,
            'player_score': self.player_score,
            'computer_score': self.computer_score,
            'is_over': self.is_over()
        }

    # Function used to check both choices and see who won
    def determine_winner(self, player, computer):
        if player == computer:
            return 'tie'
        elif (player == 'rock' and computer == 'scissors') or \
             (player == 'paper' and computer == 'rock') or \
             (player == 'scissors' and computer == 'paper'):
            return 'player'
        else:
            return 'computer'

    # Function to check if the overall game is over
    def is_over(self):
        return self.player_score == self.rounds_to_win or self.computer_score == self.rounds_to_win

    # Function used to get the winner
    def get_winner(self):
        if self.player_score > self.computer_score:
            return "You"
        else:
            return "Computer"
