from bokeh.client import push_session
from bokeh.embed import autoload_server, components
from bokeh.plotting import figure, curdoc, show, output_file

# figure() function auto-adds the figure to curdoc()


#script = autoload_server("https://demo.bokehplots.com/apps/sliders")

# prepare some data


class scatter:
	def __init__(self):
		self.x = [1, 2, 3, 4, 5]
		self.y = [6, 7, 2, 4, 5]			# optimal value

		# taking in input x, y, and a curve for the opt sol (y list)

	def run(self):
		p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
		p.line(self.x, self.y, legend="Temp.", line_width=2)
		script, div = components(p)
		print script
		return script, div


# # options for colors 
# x = [1, 2, 3, 4, 5]
# y = [6, 7, 2, 4, 5]

# # output to static HTML file
# output_file("lines.html")

# # create a new plot with a title and axis labels
# p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

# # add a line renderer with legend and line thickness
# p.line(x, y, legend="Temp.", line_width=2)

# # show the results
# #script, div = components(p)
# script, div = components(p)

## 


















