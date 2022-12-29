#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time

import yfinance as yf
import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_live_price, get_quote_table

# Input :  sudo python3 main.py --led-cols=64 --led-rows=32 --led-gpio-mapping=adafruit-hat --led-slowdown-gpio=2 --led-show-refresh --led-pwm-bits=2

count = 0
text1 = ""
text2 = ""

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
        
        pos = offscreen_canvas.width

        tickers = ["AAPL", "INTC", "MSFT", "TSLA"]
        ticker = "KO"
        indices_ticker = ["^GSPTSE", "^DJI", "^GSPC", "^IXIC"]
        indices_name = ["S&P/TSX", "DOW", "S&P 500", "NASDAQ"]
        index = "S&P/TSX"

        ### Lines to display ###
        textLine1 = ticker + " " + str(f"{get_stock_values(ticker):,}")
        get_index_values('^GSPTSE')
        textLine2 = index + " " + text2

        while True:
            offscreen_canvas.Clear()
            line1 = graphics.DrawText(offscreen_canvas, font1, pos, 14, textColorGreen, textLine1)
            line2 = graphics.DrawText(offscreen_canvas, font2, pos, 30, textColorWhite, textLine2)
            pos -= 2

            # Change this to biggest of line1/line2
            if (pos + line1 < 0):
                pos = offscreen_canvas.width

            # Updating stock prices
            textLine1 = ticker + " " + str(f"{get_stock_values(ticker):,}")
            #textLine2 = "S&P/TSX " + get_index_values('^GSPTSE')
            get_index_values('^GSPTSE')

            time.sleep(0.005)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

def get_stock_values(ticker):
    ### fetching API ###

    live_price = si.get_live_price(ticker) 

    return round(live_price, 2)

# Important indices : S&P/TSX - DOW - S&P 500 - NASDAQ
def get_index_values(ticker):
    ### fetching API ###
    live_price = si.get_live_price(ticker) 
    previous_close = yf.Ticker(ticker).info['regularMarketPreviousClose']

    if(count == 0):
        print("refresh data")

        if(round(live_price) == round(previous_close)):
            # No change or closed market
            text2 = str(f"{round(live_price):,}")
        
        elif(round(live_price) > round(previous_close)):
            # Up
            difference = round(live_price) - round(previous_close)
            text2 = str(f"{round(previous_close):,}") + " +" + str(f"{round(difference):,}")

        else:
            # Down
            difference = round(previous_close) - round(live_price)
            text2 = str(f"{round(previous_close):,}") + " -" + str(f"{round(difference):,}")

        count += 5

    else:
        count -= 1

    

    


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()