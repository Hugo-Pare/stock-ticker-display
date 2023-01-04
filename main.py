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
    global index 
    index = "S&P/TSX"
    global ticker 
    ticker = "KO"
    global ticker2
    ticker2 = "^GSPTSE"

    ### Lines to display ###
    global infoLine1
    global infoLine2

    def update_values(self, ticker):
        ## fetching API async ###
        stats = yf.Ticker(ticker).stats()

        live_price = stats['price']['regularMarketPrice']
        previous_close = stats['price']['regularMarketPreviousClose']
        print(previous_close)

        if(round(live_price, 2) == round(previous_close, 2)):
            # No change or closed market
            return [ticker + " " + str(f"{round(live_price, 2):,}"), 0]
        
        elif(round(live_price, 2) > round(previous_close, 2)):
            # Up
            difference = round(live_price) - round(previous_close)
            return [ticker + " " + str(f"{round(previous_close, 2):,}") + " +" + str(f"{round(difference, 2):,}"), 1]

        else:
            # Down
            difference = round(previous_close, 2) - round(live_price, 2)
            return [ticker + " " + str(f"{round(previous_close, 2):,}") + " -" + str(f"{round(difference, 2):,}"), 2]

    def get_index_values(self, ticker2):
        ### fetching API ###
        stats = yf.Ticker(ticker2).stats()

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

        infoLine1 = self.update_values(ticker)
        infoLine2 = self.get_index_values(ticker2)

        ### Colors ###
        # White - (255, 255, 255)
        # Green - (0, 153, 0)
        # Red - (255, 0, 0)
        # Blue - (0, 0, 255)

        textColorWhite = graphics.Color(255, 255, 255)
        textColorGreen = graphics.Color(0, 153, 0)
        textColorRed = graphics.Color(255, 0, 0)
        textColorBlue = graphics.Color(0, 0, 255)
        textColors = [textColorWhite, textColorGreen, textColorRed, textColorBlue]
        
        pos = offscreen_canvas.width

        textLine1 = infoLine1[0]
        textLine2 = infoLine2
        colorLine1 = textColors[infoLine1[1]]

        while True:
            offscreen_canvas.Clear()
            line1 = graphics.DrawText(offscreen_canvas, font1, pos, 14, colorLine1, textLine1)
            line2 = graphics.DrawText(offscreen_canvas, font2, pos, 30, textColorWhite, textLine2)
            pos -= 1

            # Change this to biggest of line1/line2
            if (pos + line1 < 0):
                pos = offscreen_canvas.width
                # Updating stock prices
                infoLine1 = self.update_values(ticker)
                infoLine2 = self.get_index_values(ticker2)

                textLine1 = infoLine1[0]
                colorLine1 = textColors[infoLine1[1]]

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()