#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import yfinance as yf
import asyncio

# Input :  sudo python3 main.py --led-cols=64 --led-rows=32 --led-gpio-mapping=adafruit-hat --led-slowdown-gpio=2 --led-pwm-bits=2

class RunText(SampleBase):

    global stock_tickers
    global indices_tickers
    global indices_names

    stock_tickers = ["AAPL", "AMZN", "GOOGL", "INTC", "MSFT", "NVDA", "SCHD", "TSLA", "QQQ", "ENB.TO", "SU.TO", "RY.TO"]
    indices_tickers = ["^DJI", "^GSPC", "^IXIC", "^GSPTSE"]
    indices_names = ["DOW JONES", "S&P 500", "NASDAQ", "S&P/TSX"]

    ### Lines to display ###
    global infoLine1
    global infoLine2

    def update_values(self, ticker):
        ## fetching API async ###
        stats = yf.Ticker(ticker).stats()

        live_price = stats['price']['regularMarketPrice']
        previous_close = stats['price']['regularMarketPreviousClose']

        print(live_price)

        if(round(live_price, 2) == round(previous_close, 2)):
            # No change or closed market
            return [ticker + " " + str(f"{round(live_price, 2):,.2f}"), 0]
        
        elif(round(live_price, 2) > round(previous_close, 2)):
            # Up
            difference = round(live_price, 2) - round(previous_close, 2)
            return [ticker + " " + str(f"{round(live_price, 2):,.2f}") + " +" + str(f"{round(difference, 2):,.2f}"), 1]

        else:
            # Down
            difference = round(previous_close, 2) - round(live_price, 2)
            return [ticker + " " + str(f"{round(live_price, 2):,.2f}") + " -" + str(f"{round(difference, 2):,.2f}"), 2]

    def get_index_values(self, ticker, num):
        index = num % len(indices_tickers)

        ### fetching API ###
        stats = yf.Ticker(ticker).stats()

        live_price = stats['price']['regularMarketPrice'] 
        previous_close = stats['price']['regularMarketPreviousClose']

        if(round(live_price) == round(previous_close)):
            # No change or closed market
            return [indices_names[index] + " " + str(f"{round(live_price):,}"), 0]
        
        elif(round(live_price) > round(previous_close)):
            # Up
            difference = round(live_price) - round(previous_close)
            return [indices_names[index] + " " + str(f"{round(live_price):,}") + " +" + str(f"{round(difference):,}"), 1]

        else:
            # Down
            difference = round(previous_close) - round(live_price)
            return [indices_names[index] + " " + str(f"{round(live_price):,}") + " -" + str(f"{round(difference):,}"), 2]

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font1 = graphics.Font()
        font2 = graphics.Font()
        font1.LoadFont("fonts/10x20.bdf")
        font2.LoadFont("fonts/8x13.bdf")
        counter1 = 0
        counter2 = 0

        infoLine1 = self.update_values(stock_tickers[counter1])
        infoLine2 = self.get_index_values(indices_tickers[counter2], counter2)

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
        textLine2 = infoLine2[0]
        colorLine1 = textColors[infoLine1[1]]

        while True:
            offscreen_canvas.Clear()
            line1 = graphics.DrawText(offscreen_canvas, font1, pos, 14, colorLine1, textLine1)
            line2 = graphics.DrawText(offscreen_canvas, font2, pos, 30, textColorWhite, textLine2)
            pos -= 1

            # Can also do (pos + line1 + 64 < 0)
            if (pos + line1 < 0):
                pos = offscreen_canvas.width
                # Updating stock prices
                counter1 += 1
                counter2 += 1
                infoLine1 = self.update_values(stock_tickers[counter1 % len(stock_tickers)])
                infoLine2 = self.get_index_values(indices_tickers[counter2 % len(indices_tickers)], counter2)

                textLine1 = infoLine1[0]
                textLine2 = infoLine2[0]
                colorLine1 = textColors[infoLine1[1]]

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()