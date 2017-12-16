from bokeh.client import push_session
from bokeh.embed import autoload_server, components
from bokeh.plotting import figure, curdoc, show, output_file
import numpy as np



def run(dataList):
''' 
This function takes in a dataList from server side and construct an image for display. 
It returns the script and div for javascript use. 
'''
	y = np.arange(1, len(dataList)+1)
	p = figure(title="line graph", x_axis_label='x', y_axis_label='y')
	p.line(dataList, y, legend="Temp.", line_width=2)
	script, div = components(p)
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


















