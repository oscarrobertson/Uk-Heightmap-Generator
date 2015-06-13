# Uk-Heightmap-Generator

Uses Terrain 50 OS data to generate 16 bit PNGs

TO USE THIS CODE IN THE CURRENT STATE:

- You need to download the "data" folder and the "main.py" file. Place the file and folder in the same directory.
- Ensure you have Python 2.7 installed
- Find the coordinates (lower left of a square) you want using a website like this http://www.gridreferencefinder.com (the X and Y co-ordinates)
- Decide how big a square you want (measured in metres, CS uses 18km size maps generally so 18000)
- Decide how large you want the output png to be (measured in pixels, CS uses 1081)
- Input these four values into the program, this can be done by changing the numbers on lines 191,192,193 and 195 to what you want.
- Run main.py (if you edit using idle this can be done by pressing f5) and you'll get the output file in the same directory.
