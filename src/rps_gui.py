import sys
import os
from rps_logic import RPSGame
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QStackedWidget,
    QSpacerItem,
    QSizePolicy
)
# Get absolute path to the project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

def image_path(filename):
    return os.path.join(IMAGE_DIR, filename)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game_logic = None

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.menu_screen = MenuScreen(self)  # Creates the Menu Screen

        self.game_screen = GameScreen(self)  # Creates the Game Screen

        self.result_screen = ResultScreen(self)  # Creates the result Screen

        self.stacked_widget.addWidget(self.menu_screen)  # Index 0
        self.stacked_widget.addWidget(self.game_screen)  # Index 1
        self.stacked_widget.addWidget(self.result_screen)  # Index 2

        self.stacked_widget.setCurrentIndex(0)  # Show menu screen first
        self.setWindowTitle("Rock Paper Scissors")
        self.setFixedSize(500, 600)
        self.setWindowIcon(QIcon(image_path("rps.png")))

        self.setStyleSheet("background-color: #f0f4f8;")

# Utilized in Menu Screen
    # Function that starts the game
    def start_game(self):
        best_of = self.menu_screen.mode_dropdown.currentData()  # takes the gamemode selection from dropdown menu option
        self.game_logic = RPSGame(best_of)  # Creates the RPSGame instance using the gamemode selection
        self.stacked_widget.setCurrentIndex(1)  # Switches to the Game Screen
        self.update_game_screen()  # Updates the UI of the game screen to its intial state

# Utilized in game Screen
    # Function that processes the player choice and runs the logic to play a round.
    def play_turn(self, player_choice):
        if not self.game_logic:  # Checks if the game object is created
            return

        # Gets the result of the round
        result = self.game_logic.play_turn(player_choice)
        # Update UI labels based on result
        self.update_game_screen(result)

        if result['is_over']:
            QTimer.singleShot(1200, lambda: self.show_result(self.game_logic.get_winner()))  # Show result after delay of 1.5 seconds

    # Function that allows the Game Screen to be updated
    def update_game_screen(self, result=None):
        if not result:
            # initial call (when game starts)
            current_round = self.game_logic.player_score + self.game_logic.computer_score + 1  # Sets current round to 1
            total_rounds = self.game_logic.rounds_to_win * 2 - 1  # Gets the maximum number of rounds
            self.game_screen.title_label.setText(f"Round {current_round} of {total_rounds}, Choose your move")
            self.game_screen.result_label.setText("Make your move!")
            self.game_screen.score_label.setText(f"Score — You: 0 | Computer: 0")
        else:
            current_round = self.game_logic.player_score + self.game_logic.computer_score  # Sets current round
            total_rounds = self.game_logic.rounds_to_win * 2 - 1  # Gets the maximum number of rounds

            # Update title
            self.game_screen.title_label.setText(f"Round {current_round + 1} of {total_rounds}, Choose your move")

            # Update result text
            # This checks the key 'winner' to see who won the round
            # Result Text is updated accordingly to display who won
            if result['winner'] == 'player':
                result_text = f"You won! You picked {result['player']}, computer picked {result['computer']}."
            elif result['winner'] == 'computer':
                result_text = f"You lost! You picked {result['player']}, computer picked {result['computer']}."
            else:
                result_text = f"It's a tie! Both picked {result['player']}."

            self.game_screen.result_label.setText(result_text)

            # Update scores
            self.game_screen.score_label.setText(f"Score — You: {result['player_score']} | Computer: {result['computer_score']}")

# Utilized in Game Screen and Result Screen
    # Returns back to Menu Screen
    def return_to_menu(self):
        self.stacked_widget.setCurrentIndex(0)

    # Updates the Result Screen to Display Proper Result
    def show_result(self, winner: str):
        if winner == "You":
            self.result_screen.result_label.setText("You Won!")
            self.result_screen.result_label.setStyleSheet("color: #2e7d32;")  # Green
            image_file = "trophy-removebg-preview.png"
        else:
            self.result_screen.result_label.setText("Computer Won!")
            self.result_screen.result_label.setStyleSheet("color: #c62828;")  # Red
            image_file = "paper-cartoon-illustration-with-crying-gesture-vector.jpg"
        # Sets the image to display the corresponding image to whether the user or computer won
        self.result_screen.image_label.setPixmap(QPixmap(image_path(image_file)).scaled(750, 500, Qt.KeepAspectRatio))
        self.stacked_widget.setCurrentIndex(2)

class MenuScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()  # Create vertical layout
        layout.setAlignment(Qt.AlignCenter)  # Center all widgets
        layout.setSpacing(20)  # Space between widgets

        # Title
        title = QLabel("Welcome to Rock Paper Scissors!")
        title.setFont(QFont("Roboto", 20))
        title.setGeometry(0, 0, 500, 100)
        title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        title.setStyleSheet("color: #2c3e50;"
                            "font-weight: bold;")

        # Image
        image_label = QLabel()
        pixmap = QPixmap(image_path("titleimage-removebg-preview.png")).scaled(250, 250, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # Gamemode Selection
        mode_label = QLabel("Select Game Mode:")
        mode_label.setFont(QFont("Arial", 14))
        mode_label.setAlignment(Qt.AlignCenter)
        mode_label.setStyleSheet("color: #16a085")

        self.mode_dropdown = QComboBox()
        self.mode_dropdown.addItem("Best of 1", 1)  # Best of 1 Gamemode
        self.mode_dropdown.addItem("Best of 3", 3)  # Best of 3 Gamemode
        self.mode_dropdown.addItem("Best of 5", 5)  # Best of 5 Gamemode
        self.mode_dropdown.setFixedWidth(100)
        self.mode_dropdown.setStyleSheet("""
                    QComboBox {
                        background-color: white;
                        border: 1px solid #ccc;
                        padding: 4px;
                        font-size: 14px;
                    }
                """)

        # Centering the Dropdown
        dropdown_container = QHBoxLayout()
        dropdown_container.setAlignment(Qt.AlignCenter)
        dropdown_container.addWidget(self.mode_dropdown)

        # Start Button
        self.start_button = QPushButton("Start Game")
        self.start_button.setFixedWidth(200)
        self.start_button.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        font-weight: bold;
                        padding: 10px;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)

        # Centering the Dropdown
        button_container = QHBoxLayout()
        button_container.setAlignment(Qt.AlignCenter)
        button_container.addWidget(self.start_button)

        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(image_label)
        layout.addWidget(mode_label)
        layout.addLayout(dropdown_container)
        layout.addLayout(button_container)
        self.setLayout(layout)
        # Connect button to main window's method directly
        self.start_button.clicked.connect(self.window().start_game)


class GameScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout()  # Create vertical layout
        main_layout.setAlignment(Qt.AlignCenter)  # Center all widgets
        main_layout.setSpacing(20)  # Space between widgets

        # Title for Displaying Info
        self.title_label = QLabel("")  # Placeholder for displaying current round info
        self.title_label.setFont(QFont("Roboto", 20))
        self.title_label.setGeometry(0, 0, 500, 100)
        self.title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title_label.setStyleSheet("color: #2c3e50;" "font-weight: bold;")
        main_layout.addWidget(self.title_label)

        # Move Buttons
        # Create a horizontal layout
        button_row = QHBoxLayout()
        button_row.setSpacing(20)

        # Rock Button
        self.rock_button = QPushButton()
        self.rock_button.setIcon(QIcon(image_path("rock-removebg-preview.png")))  # Path to image
        self.rock_button.setCursor(Qt.PointingHandCursor)  # Makes it clear it’s clickable
        self.rock_button.setIconSize(QSize(100, 100))  # Size of the icon
        self.rock_button.setFixedSize(120, 120)  # Size of the button itself (optional)

        # Paper Button
        self.paper_button = QPushButton()
        self.paper_button.setIcon(QIcon(image_path("paper-removebg-preview.png")))
        self.paper_button.setCursor(Qt.PointingHandCursor)  # Makes it clear it’s clickable
        self.paper_button.setIconSize(QSize(100, 100))
        self.paper_button.setFixedSize(120, 120)

        # Scissors Button
        self.scissors_button = QPushButton()
        self.scissors_button.setIcon(QIcon(image_path("scissors-removebg-preview.png")))
        self.scissors_button.setCursor(Qt.PointingHandCursor)  # Makes it clear it’s clickable
        self.scissors_button.setIconSize(QSize(100, 100))
        self.scissors_button.setFixedSize(120, 120)

        # Aligning Buttons in Row and Vertically Alignment
        button_row.setAlignment(Qt.AlignCenter)
        button_row.addWidget(self.rock_button)
        button_row.addWidget(self.paper_button)
        button_row.addWidget(self.scissors_button)
        main_layout.addLayout(button_row)

        # Result Label
        self.result_label = QLabel("Result: ")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Roboto", 10, QFont.Bold))
        self.result_label.setStyleSheet("""
            color: #2980b9;
            background-color: #ecf0f1;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #d0d7de;
        """)
        main_layout.addWidget(self.result_label)

        # Score Label
        self.score_label = QLabel("Score — You: 0 | Computer: 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setFont(QFont("Roboto", 14))
        self.score_label.setStyleSheet("""
            color: #f0f4f8;                
            background-color: #2e3a59;    
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #1f2a45; 
        """)
        main_layout.addWidget(self.score_label)

        # Return to Menu Button Button
        self.return_button = QPushButton("Return to Main Menu")
        self.return_button.setFont(QFont("Roboto", 13))
        self.return_button.setCursor(Qt.PointingHandCursor)  # Makes it clear it’s clickable
        self.return_button.setStyleSheet("""
            color: #f0f4f8;                     
            background-color: #2e3a59;          
            border: 2px solid #16a085;          
            border-radius: 8px;                 
            padding: 10px 20px;            
            transition: background-color 0.3s ease;
        """)
        main_layout.addWidget(self.return_button)

        self.setLayout(main_layout)

        # Game Flow Button Connections that Allow for Buttons to Properly Update the Screen and Run Through the Gameplay
        self.rock_button.clicked.connect(lambda: self.window().play_turn('rock'))
        self.paper_button.clicked.connect(lambda: self.window().play_turn('paper'))
        self.scissors_button.clicked.connect(lambda: self.window().play_turn('scissors'))
        self.return_button.clicked.connect(self.window().return_to_menu)


class ResultScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #f4f4f4;")

        self.result_label = QLabel("You Won!")  # Placeholder Result
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.result_label.setStyleSheet("color: #2e7d32;")  # Win has green font
        self.layout.addWidget(self.result_label)

        self.image_label = QLabel()  # Creates an image label that will be updated depending on the result.
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        # Space between widgets
        self.layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Return to Menu Button Button
        self.return_button = QPushButton("Return to Main Menu")
        self.return_button.setFont(QFont("Roboto", 13))
        self.return_button.setCursor(Qt.PointingHandCursor)  # Makes it clear it’s clickable
        self.return_button.setStyleSheet("""
                    color: #f0f4f8;                     
                    background-color: #2e3a59;          
                    border: 2px solid #16a085;          
                    border-radius: 8px;                 
                    padding: 10px 20px;            
                    transition: background-color 0.3s ease;
                """)
        self.layout.addWidget(self.return_button, alignment=Qt.AlignCenter)
        self.return_button.clicked.connect(self.window().return_to_menu)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
