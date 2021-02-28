import pygame, os, sys
from pygame.locals import*

def text_on_button(surface, txt, rect, font, color=(255, 255, 255)):
    x = rect.x + rect.width / 2 - font.size(txt)[0] / 2
    y = rect.y + rect.height / 2 - font.size(txt)[1] / 2
    surface.blit(font.render(txt, True, color), (x, y))

class Label:
    # a Rect being drawn
    def __init__(self, surface, pos, txt, bg_clr=(0,0,0), txt_clr=(255,255,255), border=None, border_clr=(255,255,255),
               font="arial", font_size=36, width=None, height=None, side="left", picture=None):
        self.surface    = surface
        self.pos        = pos
        self.txt        = txt
        self.bg_clr     = bg_clr
        self.txt_clr    = txt_clr
        self.border     = border
        self.border_clr = border_clr
        self.font       = pygame.font.SysFont(font, font_size)
        self.width      = width
        self.height     = height
        self.side       = side
        self.picture    = picture

        if not self.width:
            self.width  = self.font.size(self.txt)[0]
        if not self.height:
            self.height = self.font.size(self.txt)[1]
        self.rect       = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        if self.side == "center":
            self.rect.centerx = self.pos[0]
        if self.side == 'right':
            self.rect.right = self.pos[0]+self.rect.width

    def draw(self, surf=None, pos=None):
        if surf == None:
            surf = self.surface
        if pos == None:
            pos = self.pos
        pygame.draw.rect(surf, self.bg_clr, (pos[0], pos[1], self.rect.width, self.rect.height))
        if self.border:
            pygame.draw.rect(surf, self.border_clr, (pos[0], pos[1], self.rect.width, self.rect.height), 2)
        if not self.picture:
            text_on_button(surf, self.txt, pygame.Rect(pos[0], pos[1], self.rect.width, self.rect.height), self.font, self.txt_clr)
        else:
            self.picture = pygame.transform.scale(self.picture, (32, 32))
            surf.blit(self.picture, (
            self.rect.centerx - self.picture.get_width() / 2, self.rect.centery - self.picture.get_height() / 2))

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

class Button:
    # a Rect being drawn
    def __init__(self, surface, pos, txt, bg_clr=(0,0,0), txt_clr=(255, 255, 255), border_clr=(50,50,50), select_clr=(255,255,255),
                 font="arial", font_size=36, width=None, height=None, picture=None, side="left"):
        self.surface                = surface
        self.pos                    = pos
        self.txt                    = txt
        self.bg_clr                 = bg_clr
        self.txt_clr                = txt_clr
        self.border_clr             = border_clr
        self.original_border_clr    = border_clr
        self.select_clr             = select_clr
        self.font                   = pygame.font.SysFont(font, font_size)
        self.width                  = width
        self.height                 = height
        self.picture                = picture # wordt later omgezet naar 16x16
        self.side                   = side

        if self.width == None:
            self.width = self.font.size(self.txt)[0] + 10
        if self.height == None:
            self.height = self.font.size(self.txt)[1] + 8
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        if self.side == "center":
            self.rect.centerx = self.pos[0]
        if self.side == 'right':
            self.rect.right = self.pos[0]

    def draw(self):
        self.border_clr = self.original_border_clr
        if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            self.border_clr = self.select_clr
        pygame.draw.rect(self.surface, self.bg_clr, self.rect)
        pygame.draw.rect(self.surface, self.border_clr, self.rect, 2)
        if not self.picture:
            text_on_button(self.surface, self.txt, self.rect, self.font, self.txt_clr)
        else:
            self.picture = pygame.transform.scale(self.picture, (32,32))
            self.surface.blit(self.picture, (self.rect.centerx-self.picture.get_width()/2, self.rect.centery-self.picture.get_height()/2))

    def pressed(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            return True
        else:
            return False

class TextInput:
    """
    Copyright 2017, Silas Gyger, silasgyger@gmail.com, All rights reserved.
    Borrowed from https://github.com/Nearoo/pygame-text-input under the MIT license.

    This class lets the user input a piece of text, e.g. a name or a message.
    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    """
    def __init__(
            self,
            plot_surface,
            pos,
            initial_string="",
            font="arial",
            font_size=35,
            antialias=True,
            text_color=(0, 0, 0),
            cursor_color=(0, 0, 1),
            repeat_keys_initial_ms=400,
            repeat_keys_interval_ms=35,
            max_string_length=-1,
            password=False,
            width=None,
            height=None,
            bg_clr=(255,255,255)):
        """
        :param initial_string: Initial text to be displayed
        :param font_family: name or list of names for font (see pygame.font.match_font for precise format)
        :param font_size:  Size of font in pixels
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :param text_color: Color of text (duh)
        :param cursor_color: Color of cursor
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :param max_string_length: Allowed length of text
        """

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.max_string_length = max_string_length
        self.password = password
        self.input_string = initial_string  # Inputted text

        self.font_object = pygame.font.SysFont(font, font_size)

        # Text-surface will be created during the first update call:
        self.plot_surface = plot_surface
        self.pos = pos
        self.bg_clr = bg_clr
        if width != None:
            self.width = self.font_object.size("A")[0]*width
        else:
            self.width = self.font_object.size("A")[0]*15
        if height != None:
            self.height = height
        else:
            self.height = self.font_object.size("A")[1]
        self.surface = pygame.Surface((0,0))
        #self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size / 20 + 1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self.keyrepeat_counters:
                    if not event.key == K_RETURN: # Filters out return key, others can be added as necessary
                        self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == K_BACKSPACE:
                    self.input_string = (
                        self.input_string[:max(self.cursor_position - 1, 0)]
                        + self.input_string[self.cursor_position:]
                    )

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == K_DELETE:
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + self.input_string[self.cursor_position + 1:]
                    )

                elif event.key == K_RETURN:
                    return True

                elif event.key == K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == K_HOME:
                    self.cursor_position = 0

                elif len(self.input_string) < self.max_string_length or self.max_string_length == -1:
                    # If no special key is pressed, add unicode of key to input_string
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + event.unicode
                        + self.input_string[self.cursor_position:]
                    )
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = (
                    self.keyrepeat_intial_interval_ms
                    - self.keyrepeat_interval_ms
                )

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(KEYDOWN, key=event_key, unicode=event_unicode))

        # Re-render text surface:
        string = self.input_string
        if self.password:
            string = "*" * len(self.input_string)
        self.surface = self.font_object.render(string, self.antialias, self.text_color)

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
            self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

        self.clock.tick()
        return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0

    def draw(self):
        self.rect = pygame.Rect(self.pos[0]-3, self.pos[1], self.width+6, self.height)
        pygame.draw.rect(self.plot_surface, self.bg_clr, self.rect)
        pygame.draw.rect(self.plot_surface, self.text_color, self.rect, 1)
        self.plot_surface.blit(self.surface, self.pos)

    def pressed(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            return True
        else:
            return False

class CheckBox:
    # a Rect being drawn
    def __init__(self, surface, pos, txt=None, bg_clr=(0,0,0), txt_clr=(255, 255, 255), border_clr=(50,50,50), select_clr=(255,255,255),
                 font="arial", font_size=36, width=None, height=None, side="left", box_side="right", box_size=20):
        self.surface                = surface
        self.pos                    = pos
        self.txt                    = txt
        self.bg_clr                 = bg_clr
        self.txt_clr                = txt_clr
        self.border_clr             = border_clr
        self.original_border_clr    = border_clr
        self.select_clr             = select_clr
        self.font                   = pygame.font.SysFont(font, font_size)
        self.width                  = width
        self.height                 = height
        self.side                   = side
        self.box_side               = box_side
        self.box_size               = box_size
        self.selected               = False

        if self.txt == None:
            self.box_rect = pygame.Rect(self.pos[0], self.pos[1], self.box_size, self.box_size)
        else:
            if self.width == None:
                self.width = self.font.size(self.txt)[0] + 10
            if self.height == None:
                self.height = self.font.size(self.txt)[1] + 8

            if self.box_side == "right":
                self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
                self.box_rect = pygame.Rect(self.pos[0]+self.rect.width, self.pos[1]+(self.rect.height-self.box_size)//2, self.box_size, self.box_size)
            elif self.box_side == "left":
                self.box_rect = pygame.Rect(self.pos[0], self.pos[1]+(self.height-self.box_size)//2, self.box_size, self.box_size)
                self.rect = pygame.Rect(self.pos[0]+self.box_rect.width, self.pos[1], self.width, self.height)

    def draw(self):
        self.border_clr = self.original_border_clr
        if self.box_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            self.border_clr = self.select_clr
        pygame.draw.rect(self.surface, self.bg_clr, self.box_rect)
        if not self.selected:
            pygame.draw.rect(self.surface, self.border_clr, self.box_rect, 2)
        else:
            pygame.draw.rect(self.surface, self.select_clr, self.box_rect)
        if self.txt != None:
            text_on_button(self.surface, self.txt, self.rect, self.font, self.txt_clr)

    def pressed(self):
        if self.box_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            self.selected = not self.selected
            return True
        else:
            return False

class ScrolledBox:
    # a Surface
    def __init__(self, surface, pos, width, rows, items, bg_clr=(255,255,255), txt_clr=(255,255,255),
                 border_clr=(50,50,50), font="arial", font_size=36, checks=False, box_width=None, only_first=False):
        self.surface        = surface  #waarop het wordt getekend
        self.pos            = pos
        self.width          = width
        self.rows           = rows # het aantal kotjes gewild op veld
        self.items          = items
        self.bg_clr         = bg_clr
        self.txt_clr        = txt_clr
        self.border_clr     = border_clr
        self.font           = pygame.font.SysFont(font, font_size)
        self.checks         = checks
        if box_width == None:
            self.box_width  = [15 * self.font.size("A")[0]]*len(items)
        else:
            self.box_width  = []
            for i, item in enumerate(box_width):
                self.box_width.append(box_width[i] * self.font.size("A")[0])
        self.box_space      = sum(self.box_width)  #the space all the cols would take in
        self.only_first     = only_first

        self.view_rows      = 0
        self.enter_space    = self.font.size("A")[1]
        self.scroll_step    = self.font.size("A")[1]
        self.box_surface    = pygame.Surface((width, rows*self.enter_space))  #box zelf
        if self.checks:
            self.checkboxes = []
            for i in range(self.rows):
                #self.checkboxes.append(CheckBox(self.box_surface, (0, i*self.enter_space)))
                self.checkboxes.append(CheckBox(self.surface, (self.pos[0]-50, self.pos[1] + i * self.enter_space + 10)))



    def scroll(self, dir):
        if dir == "up" and self.view_rows*self.scroll_step < 0:
            self.view_rows += 1
        elif dir == "down" and self.view_rows*self.scroll_step > (len(self.items)-self.rows)*self.enter_space*-1:
            self.view_rows -= 1

    def draw(self):
        self.box_surface.fill(self.bg_clr)
        curr_rows = self.view_rows *self.scroll_step
        for i, obj in enumerate(self.items):
            if isinstance(obj, list):
                if self.only_first:
                    txt = obj[0]
                    Label(self.box_surface, (0, curr_rows), txt, txt_clr=self.txt_clr, bg_clr=self.bg_clr).draw()
                else:
                    for i, word in enumerate(obj):
                        txt = word
                        x_pos = sum(self.box_width[0:i])
                        Label(self.box_surface, (x_pos, curr_rows), txt, txt_clr=self.txt_clr, bg_clr=self.bg_clr).draw()
            else:
                txt = obj
                Label(self.box_surface, (0, curr_rows), txt, txt_clr=self.txt_clr, bg_clr=self.bg_clr).draw()
            if self.checks:
                for i in self.checkboxes:
                    i.draw()
            curr_rows += self.enter_space
        self.surface.blit(self.box_surface, self.pos)
