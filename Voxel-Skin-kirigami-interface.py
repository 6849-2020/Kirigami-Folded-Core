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

# /////////////////////////////////////////////////////Parameters///////////////////////////////////////////////////////

pitch = 74.4 #(mm)
rivet_distance = pitch * 0.153629032258065 #Relation taken from cad as every material shrink a specific length ideally isotropically after injection molding
rivet_diameter = 2.5
#Maybe use this guy as an imput?
items = 5 # numbers of voxels in a row
angle = 77 #degrees
centerwidth = 6
outerwidth = 14
hinge = 15

# /////////////////////////////////////////////////////PFunctions///////////////////////////////////////////////////////

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

def corrugate_lines(base, upper, angle, outerwidth, centerwidth):
    '''
    Given the baseline, analize if the local slope is positive or negative and draw the slotted line in consecuence

    :return:
    '''
    angle = math.radians(angle)
    upper_copy = rs.CopyObject(upper, translation=(0,pitch/2,0))
    slope_value = slope(base, upper_curve)
    lx0, ly0, lz0 =  rs.CurveStartPoint(base)


    p0 = rs.AddPoint((lx0 + pitch/2, ly0 , lz0))


    p0 = (rs.PointCoordinates(p0))
    p1 = [p0[0] + rivet_distance+rivet_diameter, p0[1], p0[2]]
    p2 = [p0[0] + pitch - rivet_distance-rivet_diameter, p0[1], p0[2]]
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
        parameter = domain[1] / 2
        h1, h2 = rs.SplitCurve(h, parameter)


        domain1 = rs.CurveDomain(h1)
        parameter1 = domain1[1] / 1.005
        h1f, h1s = rs.SplitCurve(h1, parameter1)

        h1 = h1f





        pathsim =(rs.AddLine(p0s, (p0s[0],p0s[1]- centerwidth, p0s[2] )))
        pathout =(rs.AddLine(p0s, (p0s[0],p0s[1] + outerwidth, p0s[2] )))

        #Poniendo un punto en medio y dandole offset

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


        b_off = rs.CopyObject(b, translation=(0,outerwidth,0))
        d_off = rs.CopyObject(d, translation=(0,outerwidth,0))
        g_off= rs.CopyObject(g, translation=(0,-centerwidth,0))
        i_off= rs.CopyObject(i, translation=(0,-centerwidth,0))


        sim1 = rs.JoinSurfaces((F,G,H1,), delete_input = True)
        sim2 = rs.JoinSurfaces((H2,I,J), delete_input = True)
        out = rs.JoinSurfaces((A,B,C,D,E), delete_input = True)
        # Creating the rivets

        rivet1_base = rs.AddCircle((lx0+rivet_distance, ly0 + pitch/2, lz0), rivet_diameter/2)
        rivet2_base = rs.AddCircle((lx0+pitch/2, ly0 + rivet_distance, lz0), rivet_diameter/2)
        rivet3_base = rs.AddCircle((lx0+ pitch - rivet_distance, ly0 + pitch/2, lz0), rivet_diameter/2)
        rivet4_base = rs.AddCircle((lx0+ 1.5* pitch , ly0 + rivet_distance, lz0), rivet_diameter/2)



        rivet1 = rs.ExtrudeCurve(rivet1_base, rs.AddLine((0,0,0), (0,0,5)))
        rivet2 = rs.ExtrudeCurve(rivet2_base, rs.AddLine((0,0,0), (0,0,5)))
        rivet3 = rs.ExtrudeCurve(rivet3_base, rs.AddLine((0,0,0), (0,0,5)))
        rivet4 = rs.ExtrudeCurve(rivet4_base, rs.AddLine((0,0,0), (0,0,5)))

        #Cutting them with corrugated surfaces.

        sim1 = rs.SplitBrep(sim1 ,rivet1 , delete_input=True)
        rs.DeleteObject(sim1[1])
        sim2 = rs.SplitBrep(sim2 ,rivet3 , delete_input=True)
        rs.DeleteObject(sim2[1])
        out = rs.SplitBrep(out ,rivet2 , delete_input=True)
        out = rs.SplitBrep(out[1], rivet4, delete_input=True)
        rs.DeleteObject(out[1])


        for el in [rivet1, rivet2, rivet3,rivet4, rivet1_base, rivet2_base, rivet3_base, rivet4_base]:
            rs.DeleteObject(el)



        return sim1, sim2, out ,b_off, d_off, g_off, i_off

    else:

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



        domain = rs.CurveDomain(c)
        parameter = domain[1] / 2
        c1, c2 = rs.SplitCurve(c, parameter)


        domain1 = rs.CurveDomain(c1)
        parameter1 = domain1[1] / 1.005
        c1f, c1s = rs.SplitCurve(c1, parameter1)

        c1 = c1f






        pathsim =(rs.AddLine(p0s, (p0s[0],p0s[1]- centerwidth, p0s[2] )))
        pathout =(rs.AddLine(p0s, (p0s[0],p0s[1] + outerwidth, p0s[2] )))

        #Poniendo un punto en medio y dandole offset


        A = rs.ExtrudeCurve(a, pathout)
        B = rs.ExtrudeCurve(b, pathout)
        C1 = rs.ExtrudeCurve(c1, pathout)
        C2 = rs.ExtrudeCurve(c2, pathout)
        D = rs.ExtrudeCurve(d, pathout)
        E = rs.ExtrudeCurve(e, pathout)
        F = rs.ExtrudeCurve(f, pathsim)
        G = rs.ExtrudeCurve(g, pathsim)
        H = rs.ExtrudeCurve(h, pathsim)
        I = rs.ExtrudeCurve(i, pathsim)
        J = rs.ExtrudeCurve(j, pathsim)


        b_off = rs.CopyObject(b, translation=(0,outerwidth,0))
        d_off = rs.CopyObject(d, translation=(0,outerwidth,0))
        g_off= rs.CopyObject(g, translation=(0,-centerwidth,0))
        i_off= rs.CopyObject(i, translation=(0,-centerwidth,0))


        sim = rs.JoinSurfaces((F,G,H,I,J), delete_input = True)
        out1 = rs.JoinSurfaces((A,B,C1), delete_input = True)
        out2 = rs.JoinSurfaces((C2,D,E), delete_input = True)

        # Creating the rivets

        rivet1_base = rs.AddCircle((lx0 + rivet_distance, ly0 + pitch / 2, lz0), rivet_diameter / 2)
        rivet2_base = rs.AddCircle((lx0 + pitch / 2, ly0 + rivet_distance, lz0), rivet_diameter / 2)
        rivet3_base = rs.AddCircle((lx0 + pitch - rivet_distance, ly0 + pitch / 2, lz0-1), rivet_diameter / 2)
        rivet4_base = rs.AddCircle((lx0 + 1.5 * pitch, ly0 + rivet_distance, lz0), rivet_diameter / 2)

        rivet1 = rs.ExtrudeCurve(rivet1_base, rs.AddLine((0, 0, 0), (0, 0, 5)))
        rivet2 = rs.ExtrudeCurve(rivet2_base, rs.AddLine((0, 0, 0), (0, 0, 5)))
        rivet3 = rs.ExtrudeCurve(rivet3_base, rs.AddLine((0, 0, 0), (0, 0, 15)))
        rivet4 = rs.ExtrudeCurve(rivet4_base, rs.AddLine((0, 0, 0), (0, 0, 5)))

        # Cutting them with corrugated surfaces.

        sim = rs.SplitBrep(sim, rivet1, delete_input=True)
        sim = rs.SplitBrep(sim[0], rivet3, delete_input=True)
        rs.DeleteObject(sim[1])
        out1 = rs.SplitBrep(out1, rivet2, delete_input=True)
        rs.DeleteObject(out1[0])
        out2 = rs.SplitBrep(out2, rivet4, delete_input=True)
        rs.DeleteObject(out2[1])

        for el in [rivet1, rivet2, rivet3, rivet4, rivet1_base, rivet2_base, rivet3_base, rivet4_base]:
            rs.DeleteObject(el)

        return out1, out2, sim ,b_off, d_off, g_off, i_off

def facets(b,d,g,i, hinge, angle, upper):
    pb = rs.CurveStartPoint(b)
    pd = rs.CurveEndPoint(d)
    pg = rs.CurveStartPoint(g)
    pi = rs.CurveEndPoint(i)

    FrontLine = rs.AddLine(pb, pg)
    RearLine = rs.AddLine(pd, pi)

    front_domain =rs.CurveDomain(FrontLine)
    rear_domain =rs.CurveDomain(RearLine)

    tf = front_domain[1]/2
    tr = rear_domain[1] / 2

    pf = rs.EvaluateCurve(FrontLine, tf)
    pr = rs.EvaluateCurve(RearLine, tr)

    pf = [pf[0]-hinge, pf[1], pf[2]]
    pr = [pr[0]-hinge, pr[1], pr[2]]

    rs.AddPoint(pf)
    rs.AddPoint(pr)

    front = rs.JoinCurves((rs.AddLine(pg, pf), rs.AddLine(pf,pb)), delete_input = True)
    rear = rs.JoinCurves((rs.AddLine(pd, pr), rs.AddLine(pr,pi)), delete_input = True)

    upper = rs.ExtrudeCurve(upper, rs.AddLine((0,0,0), (0,75,0)))

    front_path = rs.AddLine((0,0,0), (500*math.cos(math.radians(angle)), 0, 500 * math.sin(math.radians(angle))))
    front_shield = rs.ExtrudeCurve(front, front_path)

    rear_path = rs.AddLine((0,0,0), (-500*math.cos(math.radians(angle)), 0, 500 * math.sin(math.radians(angle))))
    rear_shield = rs.ExtrudeCurve(rear, rear_path)

    frontsplit = rs.SplitBrep(front_shield ,upper , delete_input=True)
    rearsplit = rs.SplitBrep(rear_shield ,upper , delete_input=True)

    rs.DeleteObject(frontsplit[0])
    rs.DeleteObject(rearsplit[0])




    return None

# /////////////////////////////////Reading Curves and Origin and calling functions./////////////////////////////////////


upper_curve = rs.GetObject("Click Upper Line")
origin = rs.GetObject("Select Origin")
orx, ory, orz = rs.PointCoordinates(origin)


#Drawing the pitch cells lines

cells_range = []

for i in range(items):
    line = rs.AddLine((orx + i*1.5 *pitch, ory, orz), (orx +i* 1.5 *pitch + 1.5* pitch, ory, orz ))
    cells_range.append(line)

corrdata =  corrugate_lines(cells_range[0], upper_curve, angle, outerwidth, centerwidth)
b,d,g,i = corrdata[3],corrdata[4], corrdata[5], corrdata[6]
facets(b,d,g,i, hinge, angle, upper_curve)
simetric(a,b,c,d,e)
