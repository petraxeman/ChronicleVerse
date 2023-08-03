from kivymd.uix.textfield.textfield import MDTextField
from kivy.metrics import dp


class MDTextFieldFuncIcon(MDTextField):
    def __init__(self, *args, **kwargs):
        super(MDTextFieldFuncIcon, self).__init__(*args, **kwargs)
        self.register_event_type('on_icon_press')
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.icon_right:
                icon_x = (self.width + self.x) - (self._icon_right_label.texture_size[1]) - dp(8)
                icon_y = self.center[1] - self._icon_right_label.texture_size[1] / 2
                if self.mode == "rectangle":
                    icon_y -= dp(4)
                elif self.mode != 'fill':
                    icon_y += dp(8)
                if touch.pos[0] > icon_x and touch.pos[1] > icon_y:
                    self.dispatch('on_icon_press', self)
        return super(MDTextFieldFuncIcon, self).on_touch_down(touch)
    
    def on_icon_press(self, *args):
        pass
