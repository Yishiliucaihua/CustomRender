class RenderObject:
	def __init__(self):
		self.type_id = "render_object"
		# contains all draw commands
		self.command_list = []
		# contains canvas data, such as width and height
		self.info = []

	def parse_from_file(self, file_path: str):
		pass

	def gen_command_list(self, config: dict):
		pass
