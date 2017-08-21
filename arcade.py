# coding: utf-8
import calcium

class AABB(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	@property
	def nw(self):
		return [self.x, self.y]

	@property
	def sw(self):
		return [self.x, self.y + self.height]

	@property
	def ne(self):
		return [self.x + self.width, self.y]

	@property
	def se(self):
		return [self.x + self.width, self.y + self.height]

	# Touching in left
	def t_left(self, aabb):
		return AABB.point_inside(self.nw, aabb) or AABB.point_inside(self.sw, aabb)

	# Touching in right
	def t_right(self, aabb):
		return AABB.point_inside(self.ne, aabb) or AABB.point_inside(self.se, aabb)

	# Touching in down
	def t_down(self, aabb):
		return AABB.point_inside(self.sw, aabb) or AABB.point_inside(self.se, aabb)

	# Touching in up
	def t_up(self, aabb):
		return AABB.point_inside(self.nw, aabb) or AABB.point_inside(self.ne, aabb)

	def touching(self, aabb):
		return self.t_up(aabb) or self.t_down(aabb) or self.t_left(aabb) or self.t_right(aabb)

	@staticmethod
	def point_inside(xy, aabb):
		x, y = xy
		inx = x <= (aabb.x + aabb.width) and x >= aabb.x
		iny = y <= (aabb.y + aabb.height) and y >= aabb.y
		return inx and iny

	def clone(self):
		return AABB(self.x, self.y, self.width, self.height)


class ArcadeWorld(object):
	def __init__(self):
		self.aabbs = []

	def add(self, aabb):
		self.aabbs.append(aabb)
		aabb.world = self

class AABBSprite(AABB, calcium.CalciumSprite):
	def __init__(
			self, x, y,
			width, height, animations,
			frame_index=0, animation_key=None):
		self.world = None
		calcium.CalciumSprite.__init__(
			self, x, y, animations,
			frame_index, animation_key
		)
		AABB.__init__(self, x, y, width, height)

	def inc_x(self, value):
		if not value:
			return

		# verifying if is touching some other sprite
		touching = False
		touch_sprite = None
		for sprite in self.world.aabbs:
			if sprite != self:
				if value > 0:
					touching = self.t_right(sprite)
					if touching:
						touch_sprite = sprite
						break
				elif value < 0:
					touching = self.t_left(sprite)
					if touching:
						touch_sprite = sprite
						break

		if touching:
			print 'here'
			# adjusting the position to limit
			if value > 0:
				self.x = touch_sprite.x - self.width
			elif value < 0:
				self.x = touch_sprite.x + touch_sprite.width
		else:
			self.x += value

	def inc_y(self, value):
		if not value:
			return

		# verifying if is touching some other sprite
		touching = False
		touch_sprite = None
		for sprite in self.world.aabbs:
			if sprite != self:
				if value > 0:
					touching = self.t_down(sprite)
					if touching:
						touch_sprite = sprite
						break
				elif value < 0:
					touching = self.t_up(sprite)
					if touching:
						touch_sprite = sprite
						break

		if touching:
			# adjusting the position to limit
			if value > 0:
				self.y = touch_sprite.y - self.height
			elif value < 0:
				self.y = touch_sprite.y + touch_sprite.height
		else:
			self.y += value
