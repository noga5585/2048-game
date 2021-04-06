import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
import random
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.Qt import Qt

qtCreatorFile = "gameWindow.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Menu(QMainWindow):
    def __init__(self):
        """
            Builder of menu window.
        """
        super(Menu, self).__init__()
        loadUi('menu.ui', self)
        self.show()
        self.start_button.clicked.connect(self.start_game)  # event.
        self.help_button.clicked.connect(self.help)  # event.
        self.exit_button.clicked.connect(self.exit)  # event.

    def start_game(self):
        """
        Opens the game window and closes that window.
        :return:The game window.
        """
        self.w = Game()
        self.w.show()
        self.hide()

    def help(self):
        self.w = Help()
        self.w.show()
        self.hide()

    def exit(self):
        sys.exit(app.exec_())


class Help(QMainWindow):
    def __init__(self):
        """
            Builder of help window.
        """
        super(Help, self).__init__()
        loadUi('help.ui', self)
        self.show()
        self.back_to_menu.clicked.connect(self.back_menu)  # event.

    def back_menu(self):
        self.w = Menu()
        self.w.show()
        self.hide()


class Game(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
            Builder of the game window.
        """
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        super(Game, self).__init__()
        loadUi('gameWindow.ui', self)
        self.labels = [[self.cell_1, self.cell_2, self.cell_3, self.cell_4], [self.cell_5, self.cell_6, self.cell_7, self.cell_8], [self.cell_9, self.cell_10, self.cell_11, self.cell_12]
            , [self.cell_13, self.cell_14, self.cell_15, self.cell_16]]  # list of the cells.
        self.newGame.clicked.connect(self.reset_board)  # event.
        self.menu_button.clicked.connect(self.back_menu)  # event.
        self.theBestScore = 0
        self.reset_board()

    def reset_board(self):
        """
        Initializes the game board.
        :return: None
        """
        self.gameFinish = False
        self.playerLose = False
        self.data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  # Stores the board data
        self.add_new_number()
        self.add_new_number()
        self.score.setText("0")
        self.bestScore.setText(str(self.theBestScore))
        self.theScore = 0
        self.draw_new_board()

    def back_menu(self):
        self.w = Menu()
        self.w.show()
        self.hide()

    def which_number(self, argument):
        """
        :param argument: The number that should be displayed on the board.
        :return: The image path that should be displayed.
        """
        numbers = {
            2: "imgs/number2.jpeg",
            4: "imgs/number4.jpeg",
            8: "imgs/number8.jpeg",
            16: "imgs/number16.jpeg",
            32: "imgs/number32.jpeg",
            64: "imgs/number64.jpeg",
            128: "imgs/number128.jpeg",
            256: "imgs/number256.jpeg",
            512: "imgs/number512.jpeg",
            1024: "imgs/number1024.jpeg",
            2048: "imgs/number2048.jpeg",
            }
        return numbers.get(argument)

    def add_new_number(self):
        """
        Adds number 2 or 4 to the board instead of a random blank.
        :return: None
        """
        count = 0
        nums = [2,4]
        while count != 1:  # There is a selected cell
            row = random.randint(0, len(self.data) - 1)
            col = random.randint(0, len(self.data[0]) - 1)
            if self.data[row][col] != 0:  # This is not an empty cell
                continue
            numberToFil = random.choice(nums)  # Randomly selects 2 or 4
            self.data[row][col] = numberToFil
            self.labels[row][col].setPixmap(QtGui.QPixmap(self.which_number (self.data[row][col])))
            count += 1

    def draw_new_board(self):
        """
        Deletes the images of all the numbers present in the cells. Name the new images according to the new data.
        :return: None
        """
        for i in range(4):
            for j in range(4):
                self.labels[i][j].setPixmap(QtGui.QPixmap("imgs/empy.jpeg"))
        for x in range(4):
            for y in range(4):
                if self.data[x][y] != 0:
                    self.labels[x][y].setPixmap(QtGui.QPixmap(self.which_number (self.data[x][y])))

    def compress_to_left(self):
        """
        Moves the entire board to the left.
        :return:True if the board has changed after the move else return False
        """
        changed = False
        new_mat = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for i in range(4):
            pos = 0
            for j in range(4):
                if self.data[i][j] != 0:
                    new_mat[i][pos] = self.data[i][j]
                    if j != pos:
                        changed = True
                    pos += 1
        self.data = new_mat
        return changed

    def merge(self):
        """
        Merge the adjacent cells with the same value, adding a score.
        :return: True if the board has changed after the move else return False
        """
        changed = False
        for i in range(4):
            for j in range(4):
                if j < 3 and self.data[i][j] == self.data[i][j + 1] and self.data[i][j] != 0:
                    self.theScore = self.theScore + self.data[i][j]*2  # add to score
                    self.data[i][j] = self.data[i][j] * 2  # change the data.
                    self.data[i][j + 1] = 0
                    changed = True
                if i < 3 and self.data[i][j] == self.data[i + 1][j] and self.data[i][j] != 0:
                    self.theScore = self.theScore + (self.data[i][j]*2)
                    self.data[i][j] = self.data[i][j] * 2
                    self.data[i][j + 1] = 0
                    changed = True

        self.compress_to_left()  # Move all cells to the left after merging
        self.change_score()
        return changed

    def change_score(self):
        """
        change the score
        :return: None
        """
        self.score.setText(str(self.theScore))
        if self.theScore > self.theBestScore:
            self.theBestScore = self.theScore
            self.bestScore.setText(str(self.theBestScore))

    def reverse(self):
        """
        Inverts all the data in the matrix in exactly the reverse order.
        :return: None
        """
        new_mat =[]
        for i in range(4):
            new_mat.append([])
            for j in range(4):
                new_mat[i].append(self.data[i][3 - j])
        self.data = new_mat

    def transpose(self):
        """
        Replaces the matrix. Everything that was in position (i,j) becomes in position (j,i).
        :return:
        """
        new_mat = []
        for i in range(4):
            new_mat.append([])
            for j in range(4):
                new_mat[i].append(self.data[j][i])
        self.data = new_mat

    def check_status(self):
        """
        Checks if the player has won or lost or can still continue to play.
        :return: None
        """
        there_is_empty_cell = False
        for i in range(4):
            for j in range(4):
                if j < 3 and self.data[i][j] == self.data[i][j + 1] and self.data[i][j] != 0:
                    there_is_empty_cell = True
                if i < 3 and self.data[i][j] == self.data[i + 1][j] and self.data[i][j] != 0:
                    there_is_empty_cell = True
                if self.data[i][j] == 0:
                    there_is_empty_cell = True
                if self.data[i][j] == 2048:
                    self.gameFinish = True
                    self.game_over()
        if not there_is_empty_cell:
            self.gameFinish = True
            self.game_over()

    def game_over(self):
        """
        Shows a lose screen
        :return: None
        """
        self.w = GameOver()
        self.w.show()
        self.hide()

    def keyPressEvent(self, e):
        """
        event that checks which key is pressed
        :param e: the key that was pressed
        :return: None
        """
        if self.gameFinish:
            return
        if e.key() == Qt.Key_A:  # LEFT
            self.move("left")
        if e.key() == Qt.Key_D:  # right
            self.move("right")
        if e.key() == Qt.Key_W:  # up
            self.move("up")
        if e.key() == Qt.Key_S:  # down
            self.move("down")

    def move(self, direction):
        """
        Checks where the player wants to move, if the move was possible.
        :param direction: Where the player wants to move
        :return: None
        """
        self.check_status()
        changed = False
        if direction == "left":
            changed = self.move_left()
        if direction == "right":
            changed = self.move_right()
        if direction == "up":
            changed = self.move_up()
        if direction == "down":
            changed = self.move_down()

        if changed:
            self.add_new_number()
            self.draw_new_board()
            self.check_status()

    def move_left(self):
        """
        Moves the board to the left
        :return: If there was a change in the data on the board after the move
        """
        changed = self.compress_to_left()
        changed2 = self.merge()
        return changed or changed2

    def move_right(self):
        """
        Moves the board to the right
        :return: If there was a change in the data on the board after the move
        """
        self.reverse()
        changed = self.compress_to_left()
        changed2 = self.merge()
        self.reverse()

        return changed or changed2

    def move_up(self):
        """
        Moves the board to the up
        :return: If there was a change in the data on the board after the move
        """
        self.transpose()
        changed = self.compress_to_left()
        changed2 = self.merge()
        self.transpose()
        return changed or changed2

    def move_down(self):
        """
        Moves the board to the down
        :return: If there was a change in the data on the board after the move
        """
        self.transpose()
        self.reverse()
        changed = self.compress_to_left()
        changed2 = self.merge()
        self.reverse()
        self.transpose()
        return changed or changed2


class GameOver(QMainWindow):
    def __init__(self):
        """
            Builder of help window.
        """
        super(GameOver, self).__init__()
        loadUi('gameOver.ui', self)
        self.show()
        self.play_again.clicked.connect(self.play)  # event.
        self.back.clicked.connect(self.back_menu)  # event.
        self.exit.clicked.connect(self.exit1)  # event.

    def back_menu(self):
        """
        close this window, open menu window
        :return: None
        """
        self.w = Menu()
        self.w.show()
        self.hide()

    def play(self):
        """
        close this window, open game window
        :return: None
        """
        self.w = Game()
        self.w.show()
        self.hide()

    def exit1(self):
        """
        close this window.
        :return: None
        """
        sys.exit(app.exec_())



if __name__ == '__main__':

    app = QApplication(sys.argv)
    widget = Menu()
    widget.show()
    sys.exit(app.exec_())
