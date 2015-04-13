from spade import pyxf

#print spade.__file__
myXsb = pyxf.xsb('/home/adrian/Applications/XSB/bin/xsb')
myXsb.load("/home/adrian/project/cse537-project/project_4/search/prolog_scripts/maze.P")
myXsb.load("/home/adrian/project/cse537-project/project_4/search/prolog_scripts/bfs.P")
#result = myXsb.query("member(cell23,[cell23|start]).")
#print result
result = myXsb.query("append([a,b,c],[1,2,3],[a,b,c,1,2,3]).")
print result