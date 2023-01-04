#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import yfinance as yf
import asyncio

# Input :  sudo python3 main.py --led-cols=64 --led-rows=32 --led-gpio-mapping=adafruit-hat --led-slowdown-gpio=2 --led-pwm-bits=2

# tickers = ["AAPL", "INTC", "MSFT", "TSLA"]
# indices_ticker = ["^GSPTSE", "^DJI", "^GSPC", "^IXIC"]
# indices_name = ["S&P/TSX", "DOW", "S&P 500", "NASDAQ"]
index = "S&P/TSX"
ticker = "BTC-USD"

def update_values(ticker):
    ## fetching API async ###
    stats = yf.Ticker(ticker).stats()

    live_price = stats['price']['regularMarketPrice']
    rounded_price = round(live_price, 2)
    textLine1 = ticker + " " + str(f"{rounded_price:,}")


# Important indices : S&P/TSX - DOW - S&P 500 - NASDAQ
def get_index_values(ticker):
    ### fetching API ###
    stats = yf.Ticker(ticker).stats()

    live_price = stats['price']['regularMarketPrice'] 
    previous_close = stats['price']['regularMarketPreviousClose']

    print(previous_close)

    if(round(live_price) == round(previous_close)):
        # No change or closed market
        return str(f"{round(live_price):,}")
    
    elif(round(live_price) > round(previous_close)):
        # Up
        difference = round(live_price) - round(previous_close)
        return str(f"{round(previous_close):,}") + " +" + str(f"{round(difference):,}")

    else:
        # Down
        difference = round(previous_close) - round(live_price)
        return str(f"{round(previous_close):,}") + " -" + str(f"{round(difference):,}")

### Lines to display ###
# textLine1 = ticker + " " + str(f"{get_stock_values(ticker):,}")
textLine1 = ""
textLine2 = index + " " + get_index_values('^GSPTSE')

class RunText(SampleBase):

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font1 = graphics.Font()
        font2 = graphics.Font()
        font1.LoadFont("fonts/10x20.bdf")
        font2.LoadFont("fonts/8x13.bdf")

        update_values(ticker)
        time.sleep(5)
        print(textLine1)

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
            line1 = graphics.DrawText(offscreen_canvas, font1, pos, 14, textColorGreen, textLine1)
            line2 = graphics.DrawText(offscreen_canvas, font2, pos, 30, textColorWhite, textLine2)
            pos -= 1

            # Change this to biggest of line1/line2
            if (pos + line1 < 0):
                pos = offscreen_canvas.width
                update_values(ticker)

            # Updating stock prices
            # textLine1 = ticker + " " + str(f"{get_stock_values(ticker):,}")
            # textLine2 = "S&P/TSX " + get_index_values('^GSPTSE')

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()