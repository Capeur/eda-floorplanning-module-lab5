# Demo narration (not the lab's script)

## Slide 1 — A tree is a recipe

Five boxes, one floor, and a tree that says where each box goes. The root, A, sits in the corner, at zero, zero. B is the left child of A, so B goes next door. C and E follow, next door each time. D is the right child of A, so D goes upstairs.

## Slide 2 — The skyline

Look at the orange line. That's the skyline, the top of everything placed so far. Each box falls until it touches the skyline. So D lands on A, at a height of two.

## Slide 3 — A taller neighbour

The dashed frame is the bounding box, twenty-seven squares. Now swap the names A and C. B is three tall, and it sticks out under D. So D stops at three, not two, and leaves a hole. The box grows to thirty-six.

## Slide 4 — Turn a box

Make every box a left child, and the row is twelve wide. It sticks out of the outline. Turn D on its side, and the row shrinks to ten. Now it fits.

## Slide 5 — Your turn

The best tree packs the boxes into twenty-four squares. Can a tree beat twenty-seven?
