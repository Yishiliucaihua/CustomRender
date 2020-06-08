from render_object import RenderObject
import math


# Node of tree
class BracketTreeNode:
	def __init__(self, label):
		self.children = []
		self.label = label
		# Contains the position of node when draw node
		self.info = {}

	def add_child(self, child):
		self.children.append(child)

	def set(self, info: dict):
		for (k, v) in info.items():
			self.info[k] = v

	def get(self, key: str):
		return self.info[key]


# You can modify this implementation and call to control the display of label
def get_text_size(r):
	return r * 6


def modify_label(root, d: dict):
	for child in root.children:
		modify_label(child, d)
	if d.get(root.label) is None:
		d[root.label] = 0
	lab = root.label
	root.label = r"$\mathrm{" + lab + r"}_" + str(d[lab]) + r"$"
	d[lab] = d[lab] + 1


class RenderObjectBracketTree(RenderObject):
	l_b = "{"
	r_b = "}"
	# Used to control the size of figure
	scale = 0.08

	def __init__(self):
		super().__init__()
		self.type_id = "bracket_tree_object"
		self.roots = []
		# Used to control axes length
		self.h = -1
		self.v = -1

	def parse_from_file(self, file_path: str):
		with open(file_path, "r") as file:
			content = file.readlines()
			self.roots.clear()

			for k in range(len(content)):
				line = content[k].strip()
				stack = []
				start_i = -1

				for i in range(len(line)):
					if line[i:i + 1] == RenderObjectBracketTree.l_b:
						if start_i != -1:
							stack.append(line[start_i:i])
						stack.append(RenderObjectBracketTree.l_b)
						start_i = i + 1
					elif line[i:i + 1] == RenderObjectBracketTree.r_b:
						if start_i != -1:
							stack.append(line[start_i:i])
						t_l_b = -1
						label = -1
						children = []

						c = 0
						while len(stack) > 0 and c < 2:
							if isinstance(stack[len(stack) - 1], str):
								c = c + 1
								s = stack.pop()
								if label != -1:
									t_l_b = s
								else:
									label = s
							else:
								children.append(stack.pop())

						if t_l_b != RenderObjectBracketTree.l_b:
							print("error: parse " + file_path + ", line" + str(i + 1) + " -> bracket not matched")
							return False

						node = BracketTreeNode(label)
						for child in reversed(children):
							node.add_child(child)
						stack.append(node)
						start_i = -1
				if len(stack) != 1:
					print("error: parse " + file_path + ", line" + str(i + 1) + " -> can't match full content")
					return False

				d = {}
				modify_label(node, d)
				self.roots.append(node)

	def gen_command(self, root: BracketTreeNode, cur_v, cur_h, r, margin_v, margin_h, commands):
		root.set({"v": cur_v})
		for child in root.children:
			cur_h = self.gen_command(child, cur_v + r + margin_v, cur_h, r, margin_v, margin_h, commands)

		if len(root.children) == 0:
			root.set({"h": cur_h})
			e_h = cur_h
		else:
			s_h = root.children[0].get("h")
			e_h = root.children[len(root.children) - 1].get("h")
			root.set({"h": ((s_h + e_h) / 2)})

		self.v = max(self.v, root.get("v"))

		for child in root.children:
			# Avoid line intersect with circle
			rh = root.get("h")
			rv = root.get("v")
			ch = child.get("h")
			cv = child.get("v")

			d_h = math.fabs(rh - ch)
			d_v = math.fabs(rv - cv)

			if d_h == 0:
				diff_h = 0
				diff_v = r
			else:
				theta = math.atan(d_v / d_h)
				diff_h = r * math.cos(theta)
				diff_v = r * math.sin(theta)

			if rh > ch:
				rh = rh - diff_h
				ch = ch + diff_h
			else:
				rh = rh + diff_h
				ch = ch - diff_h

			if rv > cv:
				rv = rv - diff_v
				cv = cv + diff_v
			else:
				rv = rv + diff_v
				cv = cv - diff_v

			command = "line: " + str(rh) + "," + str(rv) + ","
			command = command + str(ch) + "," + str(cv)
			commands.append(command)

		commands.append("circle:" + str(root.get("h")) + "," + str(root.get("v")) + "," + str(r))
		command = "text: " + str(root.get("h")) + "," + str(root.get("v")) + ","
		command = command + root.label + "," + str(get_text_size(r))
		commands.append(command)
		return e_h + margin_h + r * 2

	def gen_command_list(self, config: dict):
		r = config["r"]
		# In bottom level of tree, two brother node will gap margin_h
		# Two consequent level will gap margin_v
		margin_h = config["margin_h"]
		margin_v = config["margin_v"]
		self.command_list.clear()

		for root in self.roots:
			commands = []
			self.h = -1
			self.v = -1
			self.gen_command(root, r, r, r, margin_v, margin_h, commands)
			self.info.append((self.v + r, root.get("h") * 2))
			self.command_list.append(commands)
