# Conner's Retime Tool (CRT)

CRT is a tool that aids speedrunners and moderators in finding the accurate time of a speedrun with or without loads. 

## Installation

1. Navigate to the [releases](https://github.com/connerglover/Conners-Retime-Tool/releases/) page, here is every binary of CRT.
2. Locate your desired binary, the version is indicated by the title of each release, as every binary is named the same.
3. Once the binary has been located, click on its name to download it. Once the download has finished, open the file.
4. Get a PySimpleGUI License (For Free) and input it into the software. (Because I refuse to pay for PySimpleGUI, until I redo the GUI, this is required.)

## Help Development

- [Translate](https://forms.gle/7R2og1FAcXDrfr7c9)
- [Feature Request](https://forms.gle/gxr8dVEU5buHSYmN6) 
- [Report Bugs](https://forms.gle/YniGotPDvy4Cb2v57)

## Usage

To use CRT refer to the following step-by-step tutorial.

1. Set the framerate. If you're on Youtube, then you can right-click the YouTube video player and click "Stats for nerd" at "Current / Optimal Res" where a resolution is visible, the resolution will be followed by @XX, the XX is the video's framerate, input that into the input box called "FPS."
2. Get the frame of the start of your speedrun. If you're on YouTube then you can right-click on the video player and press "Copy Debug Info". You can then paste this into the frame section, by either pressing the "Paste" button next to the input or clicking inside the text box and pasting with [Ctrl + V]. CRT will parse the debug info into a frame Do the same for the end of the speedrun.
3. Find the loads. If your speedrun doesn't have any loads you should be good to go. Otherwise, you must locate the start and end of the load the same way you did for the last step. Once you've gathered those, click the "Add Load" button. You should get a confirmation if everything was done right.
4. Editing/Removing Loads. If you've made the mistake of inputting an incorrect load, simply press the "Edit Loads" button. In this menu you will be able to edit any load, just click the edit button right next to the load causing a new menu to open. In the menu, you just have to edit the time as you would set it initially. Press "Save" to save your new load or press "Discard Changes" to discard.
5. Getting the mod note and the time. This should be the easiest part of them all, if you'd like to get the mod note, you just simply press on "Copy Mod Note", this will set your clipboard to the mod note. The time is displayed right below it, clicking on the times will copy them to your clipboard.

## Credits

- Menzo - French & Polish Translation
- Cris - Spanish Translation

## License
```
MIT License

Copyright (c) 2024 Conner Glover

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.```
