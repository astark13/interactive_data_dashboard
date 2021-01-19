from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN           # CDN = Content Delivery Network

start=datetime.datetime(2015,3,1)
end=datetime.datetime(2016,3,10)
df=data.DataReader(name="GOOG",data_source="yahoo",start=start,end=end)

#print(df)
#print(df.index[df.Close > df.Open])   # the index for the dataframe is represented by the "Date"
                                      # this data set refers to the days in which the stock price increased

def inc_dec(c, o):
    if c > o:
        value="Increase"
    elif c < o:
        value="Decrease"
    else:
        value="Equal"
    return  value

# Adds a new column "Status" to the dataframe that show if the stock increased or decreased
df["Status"]=[inc_dec(c,o) for c,o in zip(df.Close,df.Open)]   
df["Middle"]=(df.Open+df.Close)/2
df["Height"]=abs(df.Close-df.Open)

#print(df)

#dates_increase=df.index[df.Close > df.Open]
#dates_decrease=df.index[df.Close < df.Open]

#"sizing_mode" - graph fits to window size
p=figure(x_axis_type='datetime',width=1000,height=300,sizing_mode="scale_width")
p.title.text="Candlestick Chart"
p.grid.grid_line_alpha=0.3     # sets the intensity of gridlines; "0" means invisible

hours_12=12*60*60*1000     # turns hours to miliseconds

#(x axis highest point, y axis highest point, x axis lowest point, y axis lowest point,)
# it's important to have the "p.segment" line of code before the "p.rect"\
# if we don't want a line going through the rectangles --> layer order!!!
p.segment(df.index, df.High, df.index, df.Low, line_color="black")

#(x axis rect. center, y axis rect. center, width of rect., height of rect.)
p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"], 
    hours_12,df.Height[df.Status=="Increase"], fill_color="#CCFFFF", line_color="black")   

p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"], 
    hours_12,df.Height[df.Status=="Decrease"], fill_color="#FF3333", line_color="black")

output_file("CS.html")  # saves the file locally
show(p)                 # displays the file "CS.html" in the default webbrowser

######################################################################
# !!! Following lines are useful when deploying the app with Flask!!!#
######################################################################

# print(components(p))     # contains the javascript and html code for the graph, in form of a tuple
# print(type(components(p)))  # it's a tuple
# print(len(components(p)))   # the length of the tuple is 2 (javascript, html)

#script1, div1 = components(p)
#cdn_js=CDN.js_files          # the output is a list containing links for javascript
#cdn_css=CDN.css_files        # the output is a list containing links for css

#print(type((cdn_js)[0]))     #returns a list
#print(cdn_css)

#print(script1)    # displays the javascript for the graph
#print(div1)       # displays the html code for the graph