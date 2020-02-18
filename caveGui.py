from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label      import Label
from kivy.uix.textinput  import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from functools import partial

import lang

import cave


class LoginScreen(GridLayout):

    def __init__(self, myCollection, myCave, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Nom'))
        self.nom = TextInput(multiline=False)
        self.add_widget(self.nom)
        self.add_widget(Label(text='Cuvée'))
        self.cuvee = TextInput(multiline=False)
        self.add_widget(self.cuvee)

        self.add_widget(Label(text='Millesime'))
        #self.millesime = TextInput(multiline=False)
        #self.add_widget(self.millesime)
        dropdown = DropDown()
        for index in range(1980, 2020):
            btn = Button(text='Millesime %d' % index, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        millesime = Button(text='Millesime')
        millesime.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(millesime, 'text', x))
       # runTouchApp(millesime)
        self.add_widget(millesime)

        self.add_widget(Label(text='Prix'))
        self.prix = TextInput(multiline=False)
        self.add_widget(self.prix)
        addBottleBtn = Button(text='Ajouter')
        v = myCollection.addVigneron("Alain Ducasse")
        b = cave.Bottle("Chateau Ducasse", millesime=2010, vigneron=v)
        pos = cave.Position(1, 1, 1, 1)
        
        #addBottleBtn.bind(on_press=partial(myCollection.storeBottle, b, myCave, pos))
    
        self.add_widget(addBottleBtn)



class CaveGUI(App):

    def build(self):
        myCollection = cave.Collection()
        myCave = myCollection.createCave()
        self.title = lang.APPNAME
        return LoginScreen(myCollection, myCave)
