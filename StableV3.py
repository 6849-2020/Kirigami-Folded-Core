import rhinoscriptsyntax as rs
import math

'''
This tool generates a Kirigami modified Miura inspired core with some new features that provides more materiability.
The development of this tool as a detailed strategy explanation lives here:

https://alfonso.pages.cba.mit.edu/geometric-folding-algorithms/index.html

The tool will ask the user to select an upper surface, a lower surface, a starting point and the number of voxels to
fill.

It will evaluate locally the upper surface step by step, decide if it is a positive slope or a negative slope and
according to that it will generate the cell. At the same time, every time the cell has been finished, it will read it
and will generate the unfolded drawing.

Any question related to the project contact me at aprubio [at] mit [dot] edu

'''

# Parameters

pitch = 75 #(mm)
rivet_distance = 14.3
rivet_diameter = 2.5
#Maybe use this guy as an imput?
items = 5 # numbers of voxels in a row
angle = 70 #degrees
centerwidth = 6
outerwidth = 14
#Functions

def slope(line, upper):
    '''

    Given the base line and the top line, this function returns True if is positive and False if is negative.

    '''
    points =  rs.DivideCurve(line, 4)
    intersections = []
    lengths = []

    for point in points:
        locline = rs.AddLine(point, (point[0], point[1], 100000))
        intersection = rs.CurveCurveIntersection(locline, upper, tolerance=-1)
        lengths.append(rs.Distance(point,(intersection[0][1])))
    #print(lengths)

    if lengths[1]<lengths[3]:  # Defining if the slope is positive or negative. It will return True if its positive and False if its negative
        return True
    else:
        return False


def baselines(cell_range):

    point1,point2, point3, point4


def corrugate_lines(base, upper, angle, outerwidth, centerwidth):
    '''

    :return:
    '''
    angle = math.radians(angle)
    upper_copy = rs.CopyObject(upper, translation=(0,pitch/2,0))
    slope_value = slope(base, upper_curve)
    lx0, ly0, lz0 =  rs.CurveStartPoint(base)


    p0 = rs.AddPoint((lx0 + pitch/2, ly0 , lz0))


    p0 = (rs.PointCoordinates(p0))
    p1 = [p0[0] + rivet_distance, p0[1], p0[2]]
    p2 = [p0[0] + pitch - rivet_distance, p0[1], p0[2]]
    p3 = [p0[0] + pitch, p0[1], p0[2]]

    p0s = [p0[0] - pitch / 2, p0[1] + pitch/2, p0[2]]
    p1s = [p1[0] - pitch / 2, p1[1] + pitch / 2, p1[2]]
    p2s = [p2[0] - pitch / 2, p2[1] + pitch / 2, p2[2]]
    p3s = [p3[0] - pitch / 2, p3[1] + pitch / 2, p3[2]]



    if slope_value == True :
        a = rs.AddLine(p0, p1)
        b = rs.AddLine(p1, (p1[0]+400*math.cos(angle), p1[1], p1[2]+400*math.sin(angle)))
        d = rs.AddLine(p2, (p2[0] - 400 * math.cos(angle), p2[1], p2[2] + 400 * math.sin(angle)))
        c = rs.AddLine((rs.CurveCurveIntersection(b,upper)[0][1]), (rs.CurveCurveIntersection(d,upper)[0][1]))
        e = rs.AddLine(p2,p3)

        b = rs.AddLine(p1, rs.CurveCurveIntersection(b , upper)[0][1])
        d = rs.AddLine(rs.CurveCurveIntersection(d ,upper)[0][1] , p2)

        f = rs.AddLine(p0s, p1s)
        g = rs.AddLine(p1s, (p1s[0]+400*math.cos(angle), p1s[1], p1s[2]+400*math.sin(angle)))
        i = rs.AddLine(p2s, (p2s[0] - 400 * math.cos(angle), p2s[1], p2s[2] + 400 * math.sin(angle)))
        h = rs.AddLine((rs.CurveCurveIntersection(g,upper_copy)[0][1]), (rs.CurveCurveIntersection(i,upper_copy)[0][1]))
        j = rs.AddLine(p2s,p3s)

        g = rs.AddLine(p1s, rs.CurveCurveIntersection(g , upper_copy)[0][1])
        i = rs.AddLine(rs.CurveCurveIntersection(i ,upper_copy)[0][1] , p2s)

        domain = rs.CurveDomain(h)
        parameter = domain[1] / 2.0
        h1, h2 = rs.SplitCurve(h, parameter)

        pathsim =(rs.AddLine(p0s, (p0s[0],p0s[1]- centerwidth, p0s[2] )))
        pathout =(rs.AddLine(p0s, (p0s[0],p0s[1] + outerwidth, p0s[2] )))

        A = rs.ExtrudeCurve(a, pathout)
        B = rs.ExtrudeCurve(b, pathout)
        C = rs.ExtrudeCurve(c, pathout)
        D = rs.ExtrudeCurve(d, pathout)
        E = rs.ExtrudeCurve(e, pathout)
        F = rs.ExtrudeCurve(f, pathsim)
        G = rs.ExtrudeCurve(g, pathsim)
        H1 = rs.ExtrudeCurve(h1, pathsim)
        H2 = rs.ExtrudeCurve(h2, pathsim)
        I = rs.ExtrudeCurve(i, pathsim)
        J = rs.ExtrudeCurve(j, pathsim)
        











    return None











# Reading Curves and Origin.

upper_curve = rs.GetObject("Click Upper Line")
origin = rs.GetObject("Select Origin")
orx, ory, orz = rs.PointCoordinates(origin)





#Drawing the pitch cells lines
cells_range = []

for i in range(items):
    line = rs.AddLine((orx + i*1.5 *pitch, ory, orz), (orx +i* 1.5 *pitch + 1.5* pitch, ory, orz ))
    cells_range.append(line)











corrugate_lines(cells_range[0], upper_curve, angle, outerwidth, centerwidth)