from renderer import Renderer
from render_object_bipartiteGraph import RenderObjectBipartiteGraph

robt = RenderObjectBipartiteGraph()
conf = {}
radius = 10
conf["r"] = radius
conf["v_start_h"] = 1.5 * radius
conf["u_start_h"] = 0
conf["gap_h"] = radius
conf["gap_v"] = radius * 5
conf["margin_h"] = 1 * radius
conf["margin_v"] = 1 * radius

# output_dir must end with // or \
renderer = Renderer(robt, r".//bg1.txt", conf, r".//BG_Data//")
renderer.sort_command_list()
renderer.draw("eps")
