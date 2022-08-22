Sudoku-Potato
Description

    A double Sudoku game with Gui


    The main program is created by C, and the Gui is created using Python and Pyqt6, and with Gui based on Modern-GUI-PyDracula.


    Thankfully, all the icons used are from font-awesome.

Introduction

    To play this game, you should choose the Level you want firstly.There are 5 default levels: Easy, Middle,Hard, Difficult, and Hell, which mean 20 holes, 40 holes... to 100 holes for you to finish. Also, you can choose Personalize to define the holes you want.However, as the Sudoku only has 153 holes, putting the right number is recommended(1,153). After that you can press the start button to init the sudoku.Tips: too many holes may cause that the sudoku has no unique ans, in this case the tip button is not recommended, which may disturb your process to finish this game. O:,sorry for that, the tip button can provide a possible answer in the sudoku, but try not to depend on it.And, the restart button will turn time to 0, and make the sudoku to the last time press the start button, the stop button can stop the time when you get in trouble eating, toilet or something else(Mention: this is not for you to cheat). When you are sure that you finish the sudoku, press the submit button will send the data to background using DPLL algorithm to check whether your answer is right.

Further Knowledge

    One hole can add several numbers to help you figure out the final answer if you make sure that every hole has only 1 number when you press the submit button, or you will lose this game.


    Arrow keys can help when you from one hole to another instead of click

Remain to Do

    The sudoku is created by using an algorithm to create an original sudoku and randomly remove several holes. So I can not promise that the sudoku is absolutely solvable. So if you find it impossible to put next number, use the tip button or put one number you like in one hole to figure out whether you are that lucky.

Others

    You can change theme in left box pressing the Adjustments button. And to see the source code of the gui, you can press the share button, if you want to see other project of mine, the more button will help.


    MIT License


    Created by: Potato(Zhu Xincai)
