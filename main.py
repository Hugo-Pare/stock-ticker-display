#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time

import yfinance as yf
import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_live_price, get_quote_table

# Input : sudo python3 main.py --led-cols=64 --led-rows=32 --led-gpio-mapping=adafruit-hat --led-slowdown-gpio=2

class RunText(SampleBase):

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font1 = graphics.Font()
        font2 = graphics.Font()
        font1.LoadFont("fonts/10x20.bdf")
        font2.LoadFont("fonts/8x13.bdf")

        ### Colors ###
        # White - (255, 255, 255)
        # Green - (0, 153, 0)
        # Red - (255, 0, 0)
        # Blue - (0, 0, 255)

        textColorWhite = graphics.Color(255, 255, 255)
        textColorGreen = graphics.Color(0, 153, 0)
        textColorRed = graphics.Color(255, 0, 0)
        textColorBlue = graphics.Color(0, 0, 255)

        ticker = "BTC-USD"
        pos = offscreen_canvas.width
        index = "S&P/TSX"
        count = 5

        ### Lines to display ###
        textLine1 = ticker + " " + str(f"{get_stock_values(ticker):,}")
        textLine2 = "S&P/TSX " + str(f"{get_index_values('^GSPTSE'):,}")

        while True:
            offscreen_canvas.Clear()
            line1 = graphics.DrawText(offscreen_canvas, font1, pos, 14, textColorGreen, textLine1)
            line2 = graphics.DrawText(offscreen_canvas, font2, pos, 30, textColorWhite, textLine2)
            pos -= 5
            count -= 1

            # Change this to biggest of line1/line2
            if (pos + line1 < 0):
                pos = offscreen_canvas.width

            # Updating stock prices
            if(count == 0):
                textLine1 = ticker + " " + str(f"{get_stock_values(ticker):,}")
                textLine2 = "S&P/TSX " + str(f"{get_index_values('^GSPTSE'):,}")
                count += 5

            time.sleep(0.005)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


def get_stock_values(ticker):

    ### fetching API ###

    live_price = si.get_live_price(ticker) 

    return round(live_price, 2)

# Important indices : S&P/TSX - DOW - S&P 500 - NASDAQ
def get_index_values(ticker):

    ### fetching API ###
    table = si.get_quote_table(ticker)

    live_price = si.get_live_price(ticker) 
    #print(table["Previous Close"])

    return round(live_price)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()