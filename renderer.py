import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import Circle, PathPatch
import os

from render_object import RenderObject
from render_object_bracketTree import RenderObjectBracketTree

draw_offset_info_size = 1


# To implement other primitives, you should implement new method like this,
# and you should change parameters of all draw_xxx like method when needed,
# they must have same form
def draw_line(pl: list, ax):
	if len(pl) != 4 + draw_offset_info_size:
		print("error: the parameters of draw line wasn't correct")
	vertices = [(float(pl[0]) + float(pl[4]), float(pl[1])), (float(pl[2]) + float(pl[4]), float(pl[3]))]
	codes = [Path.MOVETO, Path.LINETO]
	path = Path(vertices, codes)
	patch = PathPatch(path, lw=2)
	ax.add_patch(patch)


def draw_circle(pl: list, ax):
	if len(pl) != 3 + draw_offset_info_size:
		print("error: the parameters of draw circle wasn't correct")
	x = float(pl[0]) + float(pl[3])
	y = float(pl[1])
	c = Circle((x, y), float(pl[2]), facecolor="white", linewidth=3, alpha=0.7, edgecolor="black")
	ax.add_patch(c)


def draw_text(pl: list, ax):
	if len(pl) != 4 + draw_offset_info_size:
		print("error: the parameters of draw text wasn't correct")
	x = float(pl[0]) + float(pl[4])
	y = float(pl[1])
	ax.text(x, y, pl[2], style="normal", horizontalalignment="center", verticalalignment="center", size=int(pl[3]))


class Renderer:
	def __init__(self, ro: RenderObject, file_path: str, config: dict, output_dir: str):
		self.render_object = ro

		exists = os.path.exists(output_dir)
		if not exists:
			os.makedirs(output_dir)

		(_, f_t) = os.path.split(file_path)
		(file_prefix, _) = os.path.splitext(f_t)
		s_dir = os.path.join(output_dir, file_prefix)
		exists = os.path.exists(s_dir)
		if not exists:
			os.makedirs(s_dir)
		self.s_dir = s_dir

		ro.parse_from_file(file_path)
		ro.gen_command_list(config)
		self.fig = None
		self.ax = None

	# The function_map can be used to "remove"(due to overlap) unwanted things, the number is the priority of elements
	function_map = {"line": 0, "circle": 1, "text": 2}
	function_list = [draw_line, draw_circle, draw_text]

	def sort_command_list(self):
		for commands in self.render_object.command_list:
			cs = len(commands)

			for i in range(cs):
				for j in range(i + 1, cs):
					ki = str(commands[i]).split(":")[0]
					kj = str(commands[j]).split(":")[0]
					if Renderer.function_map[ki] < Renderer.function_map[kj]:
						temp = commands[i]
						commands[i] = commands[j]
						commands[j] = temp

	def draw(self, fmt):
		n = min(len(self.render_object.command_list), len(self.render_object.info))
		for i in range(n):
			print("processing: " + str(i))
			h = self.render_object.info[i][1]
			v = self.render_object.info[i][0]
			s = RenderObjectBracketTree.scale
			self.fig, self.ax = plt.subplots(figsize=(h * s, v * s))
			self.ax.set_xlim(0, h)
			self.ax.set_ylim(0, v)

			for command in self.render_object.command_list[i]:
				cs = str(command).split(":")
				if len(cs) == 2:
					f = Renderer.function_map.get(cs[0])
					if f is None:
						print("error: command " + cs[0] + " not found")
					else:
						pl = cs[1].split(",")
						pl.append(str(0))
						Renderer.function_list[f](pl, self.ax)
				else:
					print("error: the parameters of " + cs[0] + " wasn't correct")

			self.ax.xaxis.set_ticks_position("top")
			self.ax.invert_yaxis()
			plt.axis("equal")
			self.ax.axis("off")
			self.ax.xaxis.set_major_locator(plt.NullLocator())
			self.ax.yaxis.set_major_locator(plt.NullLocator())
			plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
			# to avoid losing primitives in corner
			plt.margins(0.01, 0.01)
			self.fig.savefig(os.path.join(self.s_dir, str(i) + "." + fmt), dpi=600, format=fmt)
			plt.close(self.fig)

	def draw_to_one_file(self, fmt, gap):
		n = min(len(self.render_object.command_list), len(self.render_object.info))
		total_h = 0
		total_v = 0

		for i in range(n):
			h = self.render_object.info[i][1]
			v = self.render_object.info[i][0]
			total_h = total_h + h + gap
			total_v = max(total_v, v)

		if n > 0:
			total_h = total_h - gap

		s = RenderObjectBracketTree.scale
		self.fig, self.ax = plt.subplots(figsize=(total_h * s, total_v * s))
		self.ax.set_xlim(0, total_h)
		self.ax.set_ylim(0, total_v)

		offset_h = 0
		for i in range(n):
			print("processing: " + str(i))
			for command in self.render_object.command_list[i]:
				cs = str(command).split(":")
				if len(cs) == 2:
					f = Renderer.function_map.get(cs[0])
					if f is None:
						print("error: command " + cs[0] + " not found")
					else:
						pl = cs[1].split(",")
						pl.append(str(offset_h))
						Renderer.function_list[f](pl, self.ax)
				else:
					print("error: the parameters of " + cs[0] + " wasn't correct")

			h = self.render_object.info[i][1]
			offset_h = offset_h + h + gap

		self.ax.xaxis.set_ticks_position("top")
		self.ax.invert_yaxis()
		plt.axis("equal")
		self.ax.axis("off")
		self.ax.xaxis.set_major_locator(plt.NullLocator())
		self.ax.yaxis.set_major_locator(plt.NullLocator())
		plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
		# to avoid losing primitives in corner
		plt.margins(0.01, 0.01)
		self.fig.savefig(os.path.join(self.s_dir, str(n) + "." + fmt), dpi=600, format=fmt)
		plt.close(self.fig)
