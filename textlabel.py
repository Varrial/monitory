from kivy.uix.label import Label
from services.read import getData


class TextLabel(Label):
    font = getData("RozmiarTekstu")
    pass
