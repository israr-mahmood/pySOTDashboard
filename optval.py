from bokeh.client import push_session
from bokeh.embed import autoload_server, components
from bokeh.plotting import figure, curdoc, show, output_file
import numpy as np
# from scatter import scatter

class optval:
	def __init__(self):
		# self.x = [1, 2, 3, 4, 5]
		self.x = np.array([])		# an array of same size of self.y, value from 1 to ...
		self.y = np.array([3,4,6,8,2])		# optimal value

	def addData(self, newdata):
		self.y = np.append(self.y, newdata)
		self.x = np.arange(len(self.y))
		# graph = scatter()
		# script, div = graph.run()
		# emit('appendgraphdiv', div)
		# emit('appendgraphscript', script)
	def plotArr(self):
		p = figure(title="simple line example", x_axis_label='time', y_axis_label='optval')
		p.line(self.x, self.y, legend="Temp.", line_width=2)
		script, div = components(p)
		print script
		return script, div


# 1. the client is connected:
		# add the data and plot it again
# 2. get a new data, the client is not connected 
		# append the data 
# 3. the experiment is on, the server is connected,
		# just plot the graph 

