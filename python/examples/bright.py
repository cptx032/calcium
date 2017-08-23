# coding: utf-8

import sys
sys.path.extend(['..', '.'])
import calcium
import arcade

tk = calcium.import_tkinter()
top = tk.Tk()
top.bind('<Escape>', lambda evt: top.destroy(), '+')
label = tk.Label(top, font=('arial', 2))
label.pack()

screen = calcium.CalciumScreen(64)
sprite_1 = calcium.CalciumSprite(32, 32, animations={'run': [[0, 0, 0],]})
sprite_2 = sprite_1.clone()
sprite_2.animations['run'] = [[0,0,2],]
sprite_2.x += 1
world = arcade.ArcadeWorld()
world.add(sprite_1)
world.add(sprite_2)

def _loop():
	screen.clear()
	world.draw(screen)
	label['text'] = str(screen)
	top.after(int(1000 / 60), _loop)
_loop()
top.mainloop()
