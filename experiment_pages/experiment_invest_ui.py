from tkinter import *
from tkinter.ttk import *
from tk_models import *


class InvestigatorsUI(MouserPage):
    def __init__(self, parent:Tk, prev_page: Frame = None):
        super().__init__(parent, "Investigators", prev_page)