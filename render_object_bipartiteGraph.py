from render_object import RenderObject


# You can modify this implementation and call to control the display of label
def get_text_size(r):
	return int(r * 6)


class RenderObjectBipartiteGraph(RenderObject):
	# Used to control the size of figure
	scale = 0.08

	def __init__(self):
		super().__init__()
		self.type_id = "bipartite_graph_object"
		self.us = []
		self.ls = []
		self.um = {}
		self.lm = {}
		self.es = []
		# Used to control axes length
		self.h = -1
		self.v = -1

	def parse_from_file(self, file_path: str):
		with open(file_path, "r") as file:
			content = file.readlines()
			self.us = []
			self.ls = []
			self.um = {}
			self.lm = {}
			self.es = []
			self.h = -1
			self.v = -1

			# U
			line = content[0].strip().replace("[", "").replace("]", "").replace("'", "")
			tu = line.split(",")
			for _u in tu:
				td = {}
				self.um[_u.strip()] = td
				self.us.append([_u.strip(), td])
			# L
			line = content[1].strip().replace("[", "").replace("]", "").replace("'", "")
			tl = line.split(",")
			for _l in tl:
				td = {}
				self.lm[_l.strip()] = td
				self.ls.append([_l.strip(), td])
			# Edges
			line = content[2].strip().replace("[", "").replace("]", "").replace("'", "")
			te = line.split("),")
			for _e in te:
				_e = _e.replace("(", "").replace(")", "")
				_e = _e.split(",")
				self.es.append([_e[0].strip(), _e[1].strip(), _e[2].strip()])

	def gen_command(self, vsh, ush, r, gap_h, gap_v, commands):
		# U
		cur_v = 0
		cur_h = ush
		for _u in self.us:
			_u[1]["cp_h"] = cur_h
			_u[1]["cp_v"] = cur_v + r
			commands.append("circle: " + str(cur_h) + "," + str(cur_v) + "," + str(r))
			command = "text: " + str(cur_h) + "," + str(cur_v) + ","
			command = command + _u[0] + "," + str(get_text_size(r))
			commands.append(command)
			cur_h = cur_h + gap_h + 2 * r
		# L
		cur_v = 0 + gap_v
		cur_h = vsh
		for _l in self.ls:
			_l[1]["cp_h"] = cur_h
			_l[1]["cp_v"] = cur_v - r
			commands.append("circle: " + str(cur_h) + "," + str(cur_v) + "," + str(r))
			command = "text: " + str(cur_h) + "," + str(cur_v) + ","
			command = command + _l[0] + "," + str(get_text_size(r))
			commands.append(command)
			cur_h = cur_h + gap_h + 2 * r
		# E
		for e in self.es:
			u_h = self.um[e[0]]["cp_h"]
			u_v = self.um[e[0]]["cp_v"]
			l_h = self.lm[e[1]]["cp_h"]
			l_v = self.lm[e[1]]["cp_v"]
			command = "line: " + str(u_h) + "," + str(u_v) + ","
			command = command + str(l_h) + "," + str(l_v) + "," + str(e[2])
			commands.append(command)

		self.v = gap_v + 2 * r
		self.h = cur_h + 2 * r

	def gen_command_list(self, config: dict):
		r = config["r"]
		gap_h = config["gap_h"]
		gap_v = config["gap_v"]
		margin_h = config["margin_h"]
		margin_v = config["margin_v"]
		vsh = config["v_start_h"]
		ush = config["u_start_h"]
		self.command_list.clear()

		self.h = -1
		self.v = -1
		commands = []
		self.gen_command(vsh, ush, r, gap_h, gap_v, commands)
		self.command_list.append(commands)
		self.info.append((self.v + margin_v, self.h + margin_h))
