def get_wall_direction(x1, y1, h1, w1, x2_wall, y2_wall, h2_wall, w2_wall):
    answer = []

    box_left = x1
    box_right = x1 + w1
    box_top = y1
    box_bottom = y1 + h1

    wall_left = x2_wall
    wall_right = x2_wall + w2_wall
    wall_top = y2_wall
    wall_bottom = y2_wall + h2_wall

    if (box_right >= wall_left) and (wall_right >= box_left) and (box_bottom >= wall_top) and (wall_bottom >= box_top):

        if box_left >= wall_left:
            answer.append("LEFT")
        elif box_left < wall_left:
            answer.append("RIGHT")

        if box_top >= wall_top:
            answer.append("TOP")
        elif box_top >= wall_top:
            answer.append("BOTTOM")

        print "horiz: %d, vert: %d" % (box_left - wall_left, box_top - wall_top)

    return answer


def is_point_inside_rect(x, y, rect):

    left = rect[0]
    right = rect[0] + rect[2]
    top = rect[1]
    bottom = rect[1] + rect[3]

    if (x > left) and (x < right) and (y > top) and (y < bottom):
        return True
    else:
        return False


def frange(x, y, jump):
    x += 0.0
    y += 0.0
    jump += 0.0
    while x < y:
        yield x
        x += jump


def do_rects_intersect(x1, y1, h1, w1, x2, y2, h2, w2, gap=0):
    answer = True
    if (x1 + w1 + gap < x2) or (x2 + w2 + gap < x1) or (y1 + h1 + gap < y2) or (y2 + h2 + gap < y1):
        answer = False
    return answer


def is_overlapping(x, y, hei, wid, interactables, gap):
    x1 = x
    y1 = y
    h1 = hei
    w1 = wid

    answer = False
    for block in interactables:

        x2 = block.xpos
        y2 = block.ypos
        h2 = block.height
        w2 = block.width

        answer = do_rects_intersect(x1, y1, h1, w1, x2, y2, h2, w2, gap)

        if answer:
            break

    return answer