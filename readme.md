# BG Analyzer

Basic image processing used to analyse games on : [bgstudio](https://heroes.backgammonstudio.com/)

Some values are hardcoded for mac 15", it might work with some other screens but it's not tested yet.

Layout is then sent to [bgblitz](http://www.bgblitz.com/) which sends back the bests moves.
We only display top-1.

# installation
```
git clone https://github.com/Sylv-Lej/bg-analyser.git
pip install -r requirements.txt
cd bg-analyser-main
```

# run

Open [bgblitz](http://www.bgblitz.com/) and head to a game.

Put the terminal in the right of the screen (where score is displayed) then launch the python app

```
cd app/src
python main.py
```
