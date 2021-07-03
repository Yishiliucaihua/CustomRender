from renderer import Renderer
from render_object_bracketTree import RenderObjectBracketTree

robt = RenderObjectBracketTree()
conf = {}
radius = 10
conf["r"] = radius
conf["margin_h"] = 2 * radius
conf["margin_v"] = 2 * radius

# output_dir must end with // or \
renderer = Renderer(robt, r".//bt3.txt", conf, r".//BT_Data//")
renderer.sort_command_list()
# renderer.draw("png")
renderer.draw_to_one_file("png", 2 * radius)
