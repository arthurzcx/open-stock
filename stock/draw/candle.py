# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/04/05
# @version 1.0
# @desc: Draw candle.

import mplfinance as mpf
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets, QtGui

class Candle(QtWidgets.QDialog):
    """ Class to draw candle.
    """
    my_color = mpf.make_marketcolors(up='r',
                                                down='g',
                                                edge='inherit',
                                                wick='inherit',
                                                volume='inherit'
                                                )
    my_style = mpf.make_mpf_style(marketcolors=my_color,
                                                figcolor='(0.82,0.83, 0.85)',
                                                gridcolor='(0.82,0.83, 0.85)')

    title_font = {
                'size':     '16',
                'color':    'black',
                'weight':   'bold',
                'va':       'bottom',
                'ha':       'center'}

    large_red_font = {#'fontname': 'Arial',
                    'size':     '24',
                    'color':    'red',
                    'weight':   'bold',
                    'va':       'bottom'}

    large_green_font = {#'fontname': 'Arial',
                        'size':     '24',
                        'color':    'green',
                        'weight':   'bold',
                        'va':       'bottom'}

    small_red_font = {#'fontname': 'Arial',
                    'size':     '12',
                    'color':    'red',
                    'weight':   'bold',
                    'va':       'bottom'}

    small_green_font = {#'fontname': 'Arial',
                        'size':     '12',
                        'color':    'green',
                        'weight':   'bold',
                        'va':       'bottom'}

    normal_label_font = {#'fontname': 'pingfang HK',
                        'size':     '12',
                        'color':    'black',
                        'va':       'bottom',
                        'ha':       'right'}

    normal_font = {#'fontname': 'Arial',
                'size':     '12',
                'color':    'black',
                'va':       'bottom',
                'ha':       'left'}


    def __init__(self, df, parent=None):
        super(Candle, self).__init__(parent)

        if 'date' in df.columns:
            df.set_index(['date'], inplace=True)

        if 'volumn' in df.columns:
            df.rename(columns={'volumn':'volume'}, inplace=True)
        
        print(df.columns)

        self.df = df
        self.macd()

        self.fig = mpf.figure(style=self.my_style,
                                        figsize=(12,8),
                                        facecolor=(0.82,0.83,0.85))
        self.canvas = FigureCanvas(self.fig)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # mouse
        self.pressed = False
        self.x_press = None

        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)

        self.ax1 = self.fig.add_axes([0.06, 0.25, 0.88, 0.60])
        self.ax2 = self.fig.add_axes([0.06, 0.15, 0.88, 0.10], sharex=self.ax1)
        self.ax3 = self.fig.add_axes([0.06, 0.05, 0.88, 0.10], sharex=self.ax1)        

        self.ax1.set_ylabel("price")
        self.ax2.set_ylabel("volume")
        self.ax3.set_ylabel("macd")

        self.range_draw = 100
        self.idx_draw = [-self.range_draw, -1]

        self.fig.text(0.45, 0.95, df.iloc[0]['code'] + " " + df.iloc[0]['name'], **self.title_font)

    def macd(self):
        self.df['MACD-H'] = self.df['close'].ewm(span=12, adjust=False).mean()
        self.df['MACD-S'] = self.df['close'].ewm(span=26, adjust=False).mean()
        DIF = self.df['MACD-H'] - self.df['MACD-S']
        DEA = DIF.ewm(span=9, adjust=False).mean()
        self.df['MACD'] = 2*(DIF-DEA)

    def refresh(self, idx_draw=None):
        if idx_draw is None:
            idx_draw = self.idx_draw
        
        if idx_draw[1] > -1:
            idx_draw[1] = -1
        if idx_draw[0] < -self.df.shape[0]:
            idx_draw[0] = -self.df.shape[0]

        df = self.df.iloc[idx_draw[0]:idx_draw[1]]

        latest = df.iloc[-1]
        self.fig.text(0.05, 0.90, "Date: %s"%(latest.name.date()))
        self.fig.text(0.05, 0.86, "Unit: RMB")

        self.fig.text(0.2, 0.90, "Open: %.2f"%(latest['open']), **self.small_red_font)
        self.fig.text(0.2, 0.86, "Close: %.2f"%(latest['close']), **self.small_red_font)

        self.fig.text(0.35, 0.90, "High: %.2f"%(latest['high']), **self.small_red_font)
        self.fig.text(0.35, 0.86, "Low: %.2f"%(latest['low']), **self.small_red_font)

        ap = []

        # MACD
        ap.append(mpf.make_addplot(df[['MACD-H', 'MACD-S']], ax=self.ax3))
        bar_red = np.where(df['MACD'] > 0, df['MACD'], 0)
        bar_green = np.where(df['MACD'] <= 0, df['MACD'], 0)
        ap.append(mpf.make_addplot(bar_red, type='bar', color='red', ax=self.ax3))
        ap.append(mpf.make_addplot(bar_green, type='bar', color='green', ax=self.ax3))

        mpf.plot(df,
                        style=self.my_style,
                        type='candle',
                        ax = self.ax1,
                        volume=self.ax2,
                        addplot=ap,
                        warn_too_much_data=2000,
                        mav=[5,15,30])       
        # self.fig.show() 
        self.canvas.draw()

    def on_press(self, event):
        
        if not event.inaxes == self.ax1:
            return
        
        if event.button != 1:
            return
        
        self.pressed = True
        self.x_press = event.xdata
    
    def on_release(self, event):
        self.pressed =False
        if event.xdata is None or self.x_press is None:
            return

        dx = int(event.xdata -self.x_press)
        self.idx_draw[0] -= dx
        if self.idx_draw[0] <= -len(self.df):
            self.idx_draw[0] = -len(self.df)
        elif self.idx_draw[0] >= -self.range_draw:
            self.idx_draw[0] = -self.range_draw
        
        self.idx_draw[1]= self.idx_draw[0] + self.range_draw - 1

    def on_motion(self, event):
        if not self.pressed:
            return
        
        if not event.inaxes == self.ax1:
            return
        
        dx = int(event.xdata -self.x_press)
        self.idx_draw[0] -= dx
        if self.idx_draw[0] <= -len(self.df):
            self.idx_draw[0] = -len(self.df)
        elif self.idx_draw[0] >= -self.range_draw:
            self.idx_draw[0] = -self.range_draw
        
        self.idx_draw[1]= self.idx_draw[0] + self.range_draw - 1

        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        self.refresh(self.idx_draw)

    def on_scroll(self, event):
        if event.inaxes != self.ax1:
            return
        
        scale = 1.0
        if event.button == 'down':
            scale = 0.8
        elif event.button == 'up':
            scale = 1.25
        
        self.range_draw = int(self.range_draw*scale)

        if self.range_draw < 30:
            self.range_draw = 30
        if self.range_draw > self.df.shape[0]:
            self.range_draw = self.df.shape[0]
        
        self.idx_draw[0] = self.idx_draw[1] - (self.range_draw - 1)

        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.refresh(self.idx_draw)
