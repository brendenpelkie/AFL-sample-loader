import numpy as np
import pandas as pd
import xarray as xr
from math import sqrt

import plotly.graph_objects as go
import plotly.express as px

import ipywidgets
from ipywidgets import Dropdown,Layout,Label,Button,Checkbox,VBox,HBox,Text
import pickle

import NistoRoboto.prepare 
from NistoRoboto.shared.units import units

from NistoRoboto.prepare.StockBuilderWidget import StockBuilderWidget
from NistoRoboto.prepare.SweepBuilderWidget import SweepBuilderWidget
from NistoRoboto.prepare.DeckBuilderWidget import DeckBuilderWidget


class PrepareWidget:
    def __init__(self):
        self.data_model = PrepareWidget_Model()
        self.data_view = PrepareWidget_View()
        self.deck_builder = DeckBuilderWidget()
        self.stock_builder = None
        self.sweep_builder = None
        
    def SweepBuilder_reset_cb(self,event):
        deck = self.stock_builder.add_stocks_to_deck()
        self.sweep_builder = SweepBuilderWidget(deck)
        widget = self.sweep_builder.start()
        
        self.data_view.SweepBuilder_Container.children = [
            self.data_view.reset_SweepBuilder_button,
            widget
        ]
    def StockBuilder_reset_cb(self,event):
        deck = self.deck_builder.build_deck_object()
        self.stock_builder = StockBuilderWidget(deck)
        widget = self.stock_builder.start()
        
        self.data_view.StockBuilder_Container.children = [
            self.data_view.reset_StockBuilder_button,
            widget
        ]
    def start(self):
        widget = self.data_view.start( self.deck_builder.start() )
        
        self.data_view.reset_StockBuilder_button.on_click(self.StockBuilder_reset_cb)
        self.data_view.reset_SweepBuilder_button.on_click(self.SweepBuilder_reset_cb)
        return widget
        
    
class PrepareWidget_Model:
    pass
    
class PrepareWidget_View:
    def start(self,deck_builder_widget):
        
        self.tabs = ipywidgets.Tab()
        
        self.reset_StockBuilder_button = Button(description='Reset StockBuilder')
        self.reset_SweepBuilder_button = Button(description='Reset SweepBuilder')
        self.StockBuilder_Container = VBox([self.reset_StockBuilder_button])
        self.SweepBuilder_Container = VBox([self.reset_SweepBuilder_button])
        self.tabs.children = [deck_builder_widget,self.StockBuilder_Container,self.SweepBuilder_Container]
        self.tabs.set_title(0,'Deck Setup')
        self.tabs.set_title(1,'Stock Setup')
        self.tabs.set_title(2,'Sweep Setup')
        return self.tabs