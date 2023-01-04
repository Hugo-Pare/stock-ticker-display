#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import yfinance as yf
import asyncio

# Input :  sudo python3 main.py --led-cols=64 --led-rows=32 --led-gpio-mapping=adafruit-hat --led-slowdown-gpio=2 --led-pwm-bits=2

class RunText(SampleBase):

    # tickers = ["AAPL", "INTC", "MSFT", "TSLA"]
    # indices_ticker = ["^GSPTSE", "^DJI", "^GSPC", "^IXIC"]
    # indices_name = ["S&P/TSX", "DOW", "S&P 500", "NASDAQ"]
    index = "S&P/TSX"
    global ticker 
    ticker = "BTC-USD"

    ### Lines to display ###
    global textLine1
    global colorLine1
    global textLine2 
    global colorLine2

    def update_values(self, ticker):
        ## fetching API async ###
        stats = yf.Ticker(ticker).stats()

        live_price = stats['price']['regularMarketPrice']
        previous_close = stats['price']['regularMarketPreviousClose']

        if(round(live_price) == round(previous_close)):
            # No change or closed market
            colorLine1 = "white"
            return ticker + " " + str(f"{round(live_price, 2):,}")
        
        elif(round(live_price) > round(previous_close)):
            # Up
            difference = round(live_price) - round(previous_close)
            colorLine1 = "green"
            return ticker + " " + str(f"{round(previous_close, 2):,}") + " +" + str(f"{round(difference):,}")

        else:
            # Down
            difference = round(previous_close) - round(live_price)
            colorLine1 = "red"
            return ticker + " " + str(f"{round(previous_close, 2):,}") + " -" + str(f"{round(difference):,}")

    def get_color_stock(self):
        return colorLine1

    def get_index_values(ticker):
        ### fetching API ###
        stats = yf.Ticker(ticker).stats()

        live_price = stats['price']['regularMarketPrice'] 
        previous_close = stats['price']['regularMarketPreviousClose']

        if(round(live_price) == round(previous_close)):
            # No change or closed market
            return index + " " + str(f"{round(live_price):,}")
        
        elif(round(live_price) > round(previous_close)):
            # Up
            difference = round(live_price) - round(previous_close)
            return index + " " + str(f"{round(previous_close):,}") + " +" + str(f"{round(difference):,}")

        else:
            # Down
            difference = round(previous_close) - round(live_price)
            return index + " " + str(f"{round(previous_close):,}") + " -" + str(f"{round(difference):,}")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font1 = graphics.Font()
        font2 = graphics.Font()
        font1.LoadFont("fonts/10x20.bdf")
        font2.LoadFont("fonts/8x13.bdf")

        textLine1 = self.update_values(ticker)
        colorLine1 = self.get_index_values()

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

        while True:
            offscreen_canvas.Clear()
            line1 = graphics.DrawText(offscreen_canvas, font1, pos, 14, colorLine1, textLine1)
            line2 = graphics.DrawText(offscreen_canvas, font2, pos, 30, textColorWhite, textLine2)
            pos -= 1

            # Change this to biggest of line1/line2
            if (pos + line1 < 0):
                pos = offscreen_canvas.width
                # Updating stock prices
                textLine1 = self.update_values(ticker)
                colorLine1 = self.get_index_values()

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()