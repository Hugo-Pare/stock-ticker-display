#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("fonts/9x15.bdf")
        ### Modified section ###

        # Input : sudo python3 main.py --led-cols=64 --led-gpio-mapping=adafruit-hat --text="Hello, world!"

        ### Colors ###
        # White - (255, 255, 255)
        # Green - (0, 153, 0)
        # Red - (255, 0, 0)

        textColor = graphics.Color(255, 255, 255)
        textColorUp = graphics.Color(0, 153, 0)
        textColorDown = graphics.Color(255, 0, 0)

        #pos = offscreen_canvas.width
        pos = 0 
        textLine1 = "Invesco QQQ Trust (QQQ)"
        textLine2 = "211.89 (-18.44%)"

        line1 = graphics.DrawText(offscreen_canvas, font, pos, 12, textColor, textLine1)
        line2 = graphics.DrawText(offscreen_canvas, font, pos, 0, textColorDown, textLine2)

        while True:
            # offscreen_canvas.Clear()
        
            # pos -= 1

            # # Change this to biggest of line1/line2
            # if (pos + line1 < 0):
            #     pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()