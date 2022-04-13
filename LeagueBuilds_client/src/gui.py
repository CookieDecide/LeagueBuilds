from kivy.config import Config

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '1000')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.lang import Builder

import sorting
from models.statics_db import RUNES, RUNEKEYS, SUMMONER, CHAMPIONS

import time
from lcu import get_champion, get_rune, get_summ, get_skills

Window.clearcolor = (1, 1, 1, 1)

Builder.load_string("""
<Tooltip>:
    size_hint: None, None
    size: self.texture_size[0]+5, self.texture_size[1]+5
    canvas.before:
        Color:
            rgb: 0.2, 0.2, 0.2
        Rectangle:
            size: self.size
            pos: self.pos          
""")

class Tooltip(Label):
    pass

class ImageButton(ButtonBehavior, AsyncImage):

    tooltip = None

    def __init__(self, tooltext, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.tooltip = Tooltip(text=tooltext)

        #self.size_hint_x = None
        #self.size_hint_y = None
        #self.width = 64
        #self.height = 64
        self.allow_stretch = True

        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        self.tooltip.pos = pos
        Clock.unschedule(self.display_tooltip) # cancel scheduled event since I moved the cursor
        self.close_tooltip() # close if it's opened
        if self.collide_point(*self.to_widget(*pos)):
            Clock.schedule_once(self.display_tooltip, 1)

    def close_tooltip(self, *args):
        Window.remove_widget(self.tooltip)

    def display_tooltip(self, *args):
        Window.add_widget(self.tooltip)

class SpellTitle(GridLayout):
    cols=1
    def __init__(self, champion, **kwargs):
        super(SpellTitle, self).__init__(**kwargs)
        label = Label(text="Spells",font_size ='40sp',color=(0,0,0))
        self.add_widget(label)
        self.add_widget(SpellWindow(champion=champion))

class SpellWindow(GridLayout):
    cols=5
    def __init__(self, champion, **kwargs):
        super(SpellWindow, self).__init__(**kwargs)
        icon = 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/passive/' + CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_passive
        self.add_widget(ImageButton(source=icon,tooltext="Passive"))
        icon = 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_q
        self.add_widget(ImageButton(source=icon,tooltext="Q"))
        icon = 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_w
        self.add_widget(ImageButton(source=icon,tooltext="W"))
        icon = 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_e
        self.add_widget(ImageButton(source=icon,tooltext="E"))
        icon = 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_r
        self.add_widget(ImageButton(source=icon,tooltext="R"))

class SpellOrderTitle(GridLayout):
    cols=1
    def __init__(self, champion, skills, **kwargs):
        super(SpellOrderTitle, self).__init__(**kwargs)
        label = Label(text="Spellorder",font_size ='40sp',color=(0,0,0))
        self.add_widget(label)
        self.add_widget(SpellOrderWindow(skills=skills, champion=champion))

class SpellOrderWindow(GridLayout):
    cols=7
    def __init__(self, champion, skills, **kwargs):
        super(SpellOrderWindow, self).__init__(**kwargs)
        dict = {1:CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_q, 2:CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_w, 3:CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_e, 4:CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_r}
        spell_key = {1: 'Q', 2: 'W', 3: 'E', 4: 'R'}

        layout_1 = GridLayout(cols=1)
        layout_1.add_widget(Label(text=spell_key[skills[0]],font_size ='30sp',color=(0,0,0)))
        icon = 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[0]]
        layout_1.add_widget(ImageButton(source=icon,tooltext=str(skills[0])))
        self.add_widget(layout_1)

        icon = 'https://cdn-icons-png.flaticon.com/512/66/66831.png'
        self.add_widget(ImageButton(source=icon,tooltext=""))

        layout_2 = GridLayout(cols=1)
        layout_2.add_widget(Label(text=spell_key[skills[1]],font_size ='30sp',color=(0,0,0)))
        icon = 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[1]]
        layout_2.add_widget(ImageButton(source=icon,tooltext=str(skills[1])))
        self.add_widget(layout_2)

        icon = 'https://cdn-icons-png.flaticon.com/512/66/66831.png'
        self.add_widget(ImageButton(source=icon,tooltext=""))

        layout_3 = GridLayout(cols=1)
        layout_3.add_widget(Label(text=spell_key[skills[2]],font_size ='30sp',color=(0,0,0)))
        icon = 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[2]]
        layout_3.add_widget(ImageButton(source=icon,tooltext=str(skills[2])))
        self.add_widget(layout_3)

        icon = 'https://cdn-icons-png.flaticon.com/512/66/66831.png'
        self.add_widget(ImageButton(source=icon,tooltext=""))

        layout_4 = GridLayout(cols=1)
        layout_4.add_widget(Label(text=spell_key[skills[3]],font_size ='30sp',color=(0,0,0)))
        icon = 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[3]]
        layout_4.add_widget(ImageButton(source=icon,tooltext=str(skills[3])))
        self.add_widget(layout_4)

class SummonerTitle(GridLayout):
    cols=1
    def __init__(self, summ, **kwargs):
        super(SummonerTitle, self).__init__(**kwargs)
        label = Label(text="Summoner spells",font_size ='40sp',color=(0,0,0))
        self.add_widget(label)
        self.add_widget(SummonerWindow(summ=summ))

class SummonerWindow(GridLayout):
    cols=2
    def __init__(self, summ, **kwargs):
        super(SummonerWindow, self).__init__(**kwargs)
        icon = 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + SUMMONER.get(SUMMONER.key == summ[0]).id + '.png'
        self.add_widget(ImageButton(source=icon,tooltext=str(summ[0])))
        icon = 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + SUMMONER.get(SUMMONER.key == summ[1]).id + '.png'
        self.add_widget(ImageButton(source=icon,tooltext=str(summ[1])))

class RuneTitle(GridLayout):
    cols=1
    def __init__(self, rune, **kwargs):
        super(RuneTitle, self).__init__(**kwargs)
        label = Label(text="Runes",font_size ='40sp',color=(0,0,0))
        self.add_widget(label)
        self.add_widget(RuneWindow(rune=rune, size_hint_y=3))

class RuneWindow(GridLayout):
    cols=2
    def __init__(self, rune, **kwargs):
        super(RuneWindow, self).__init__(**kwargs)
        self.add_widget(MainPerksWindow(rune=rune))
        self.add_widget(SubPerksWindow(rune=rune))

class MainPerksWindow(GridLayout):
    cols=1
    def __init__(self, rune, **kwargs):
        super(MainPerksWindow, self).__init__(**kwargs)
        icon = 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNEKEYS.get(RUNEKEYS.id == rune['primaryStyle']).icon
        self.add_widget(ImageButton(source=icon,tooltext=str(rune['primaryStyle'])))

        icon = 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNES.get(RUNES.id == rune['primaryPerk1']).icon
        self.add_widget(ImageButton(source=icon,tooltext=str(rune['primaryPerk1'])))
        icon = 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNES.get(RUNES.id == rune['primaryPerk2']).icon
        self.add_widget(ImageButton(source=icon,tooltext=str(rune['primaryPerk2'])))
        icon = 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNES.get(RUNES.id == rune['primaryPerk3']).icon
        self.add_widget(ImageButton(source=icon,tooltext=str(rune['primaryPerk3'])))
        icon = 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNES.get(RUNES.id == rune['primaryPerk4']).icon
        self.add_widget(ImageButton(source=icon,tooltext=str(rune['primaryPerk4'])))

class SubPerksWindow(GridLayout):
    cols=1
    def __init__(self, rune, **kwargs):
        super(SubPerksWindow, self).__init__(**kwargs)
        self.add_widget(SubPerks(rune=rune))
        self.add_widget(StatPerks(rune=rune))

class SubPerks(GridLayout):
    cols=1
    def __init__(self, rune, **kwargs):
        super(SubPerks, self).__init__(**kwargs)
        icon = 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNEKEYS.get(RUNEKEYS.id == rune['subStyle']).icon
        self.add_widget(ImageButton(source=icon,tooltext=str(rune['subStyle'])))

        icon = 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNES.get(RUNES.id == rune['subPerk1']).icon
        self.add_widget(ImageButton(source=icon,tooltext=str(rune['subPerk1'])))
        icon = 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNES.get(RUNES.id == rune['subPerk2']).icon
        self.add_widget(ImageButton(source=icon,tooltext=str(rune['subPerk2'])))

class StatPerks(GridLayout):
    cols=1
    def __init__(self, rune, **kwargs):
        super(StatPerks, self).__init__(**kwargs)
        dict = {5001:'StatModsHealthScalingIcon.png', 5002:'StatModsArmorIcon.png', 5003:'StatModsMagicResIcon.png', 5005:'StatModsAttackSpeedIcon.png', 5007:'StatModsCDRScalingIcon.png', 5008:'StatModsAdaptiveForceIcon.png'}
        icon = 'https://ddragon.leagueoflegends.com/cdn/img/perk-images/StatMods/' + dict[rune['offense']]
        self.add_widget(ImageButton(source=icon,tooltext=str(rune['offense'])))
        icon = 'https://ddragon.leagueoflegends.com/cdn/img/perk-images/StatMods/' + dict[rune['flex']]
        self.add_widget(ImageButton(source=icon,tooltext=str(rune['flex'])))
        icon = 'https://ddragon.leagueoflegends.com/cdn/img/perk-images/StatMods/' + dict[rune['defense']]
        self.add_widget(ImageButton(source=icon,tooltext=str(rune['defense'])))

class MainWindow(GridLayout):
    cols=1
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.add_widget(Label(text="Waiting for champion...",font_size ='40sp',color=(0,0,0)))
        self.event = Clock.create_trigger(self._rebuild)
        Clock.schedule_interval(self.tick, 20)

    def tick(self, *args):
        print('event')
        self.event()

    def _rebuild(self, *args):
        print('clock')
        self.clear_widgets()
        champion = get_champion()
        rune = get_rune()
        summ = get_summ()
        skills = get_skills()
        if (champion!=0 and rune and summ.all() and skills):
            self.add_widget(SpellTitle(champion=champion))
            self.add_widget(SpellOrderTitle(skills=skills, champion=champion))
            self.add_widget(SummonerTitle(summ=summ))
            self.add_widget(RuneTitle(rune=rune, size_hint_y=3))
        else:
            self.add_widget(Label(text="Waiting for champion...",font_size ='40sp',color=(0,0,0)))

class LeagueBuildsApp(App):
    def build(self):
        return MainWindow()