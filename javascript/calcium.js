var CalciumSprite = function(x, y, frames, frame_index) {
	this.x = x;
	this.y = y;
	this.frames = frames;
	this.frame_index = frame_index || 0;
};

CalciumSprite.prototype.get_pixels = function () {
	return this.frames[this.frame_index];
};

CalciumSprite.prototype.next_frame = function () {
	this.frame_index += 1;
	if (this.frame_index >= this.frames.length) {
		this.frame_index = 0;
	}
};

CalciumSprite.prototype.last_frame = function () {
	this.frame_index -= 1;
	if (this.frame_index < 0) {
		this.frame_index = this.frames.length - 1;
	}
};

var CalciumScreen = function(width, height, fps) {
	this.width = width;
	this.height = height || width;
	this.fps = fps || 60;
	this.clear_color = 3;
	this.lines = [];
	this.clear();
};

CalciumScreen.LEVELS = [ '█', '▓', '▒', '░', ' ' ];

CalciumScreen.prototype.clear = function () {
	this.lines = [];
	var line;
	for (var li=0; li < this.height; li++) {
		line = [];
		for (var ci=0; ci < this.width; ci++) {
			line.push(CalciumScreen.LEVELS[this.clear_color]);
		}
		this.lines.push(line);
	}
};

CalciumScreen.prototype.toString = function () {
	var r = '';
	for (var li=0; li < this.height; li++) {
		for (var ci=0; ci < this.width; ci++) {
			r += this.lines[li][ci] + this.lines[li][ci];
		}
		r += '\n';
	}
	return r;
};

CalciumScreen.prototype.set_pixel = function (x, y, level) {
	if (x < 0 || x >= this.width) {
		return;
	}
	if (y < 0 || y >= this.height) {
		return;
	}
	if (level > 4) {
		console.warn('Calcium: invalid level value');
		return;
	}
	this.lines[y][x] = CalciumScreen.LEVELS[level];
};

CalciumScreen.prototype.plot = function (sprite) {
	var pixels = sprite.get_pixels();
	var length = pixels.length;
	for (var pi = 0; pi < length; pi += 3) {
		this.set_pixel(
			sprite.x + pixels[pi],
			sprite.y + pixels[pi + 1],
			pixels[pi + 2]
		);
	}
};

CalciumScreen.prototype.mainloop = function (func) {
	setInterval(function() {
		func();
	}, 1000 / this.fps);
};

CalciumScreen.prototype.draw = function (elem) {
	elem.innerHTML = this.toString();
};