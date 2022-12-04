#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time


class RunText(SampleBase):
    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("fonts/9x15.bdf")
        ### Modified section ###

        # Input : sudo python3 main.py --led-cols=64 --led-rows=32 --led-gpio-mapping=adafruit-hat --led-slowdown-gpio=2

        ### Colors ###
        # White - (255, 255, 255)
        # Green - (0, 153, 0)
        # Red - (255, 0, 0)
        # Blue - (0, 0, 255)

        textColor = graphics.Color(255, 255, 255)
        textColorUp = graphics.Color(0, 153, 0)
        textColorDown = graphics.Color(255, 0, 0)

        textColorBlue = graphics.Color(0, 0, 255)

        pos = offscreen_canvas.width
        textLine1 = "line 1"
        textLine2 = "line 2"

        while True:
            offscreen_canvas.Clear()
            line1 = graphics.DrawText(offscreen_canvas, font, pos, 12, textColorUp, textLine1)
            line2 = graphics.DrawText(offscreen_canvas, font, pos, 28, textColorBlue, textLine2)
            pos -= 1

            # Change this to biggest of line1/line2
            if (pos + line1 < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()