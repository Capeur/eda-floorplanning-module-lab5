# B*-tree floorplan representation

**Module id:** module02-03-bstar-tree
**Lab:** bstar-tree
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — B*-tree floorplan representation

Five blocks, one frame, and a tree that says where each block goes. Can you build the picture from the tree alone? By the end, you will, and you will find the tightest picture of all.

## Slide 2 — Five blocks

![The five blocks A to E on squared paper](assets/blocks-1.png)

A chip is made of large rectangular parts, called blocks. Ours has five blocks, named A to E. They are drawn on squared paper, so you can count each width and height.

## Slide 3 — The outline

![The five blocks next to the empty outline, ten wide and eight tall](assets/blocks.png)

A floorplan says where each block sits on the chip. Every block must stay inside a frame called the outline. Our outline is ten squares wide and eight squares tall. The tighter the blocks are packed, the smaller the chip can be.

## Slide 4 — A tree as a recipe

![The B*-tree: A is the root, with a left child and a right child](assets/tree-golden.png)

Writing down every position is slow, so we use a recipe instead: a B-star tree. Each block is one node of the tree. The top node, A, is called the root. Each node can have two children: a left child and a right child.

## Slide 5 — The root goes in the corner

![A placed in the lower-left corner; x counts to the right, y counts up](assets/rule-1.png)

The root goes in the lower-left corner of the outline. From that corner, x counts squares to the right, and y counts squares up.

## Slide 6 — Left is next door, right is upstairs

![A left child goes next door, a right child goes upstairs](assets/rule.png)

A left child goes next door, right against its parent's right side. A right child goes upstairs, on top of its parent, with the same left edge. The names sound backwards, so remember: left means next door, right means upstairs. In the tree, a solid line means next door, and a dashed line means upstairs.

## Slide 7 — Where does B go?

![A is three wide and two tall; B is A's left child](assets/pause-b.png)

A is three squares wide and two squares tall. B is A's left child. Pause and guess: where does B's left edge go?

<!-- algorithm-walkthrough -->

## Slide 8 — B goes next door, at x = 3

![B goes next door, at x = 3](assets/steps/01-root.png)

B goes next door, at x equals three: A starts at zero, and A is three wide. Nothing is under B, so it rests on the floor, at y equals zero.

## Slide 9 — The walk: A, B, C, E, then D

![The walk: A, B, C, E, then D](assets/steps/02-left-chain.png)

We place the blocks one at a time, in a fixed walk order. Place a node, then everything down its left side, and only then its right child. So the walk goes A, B, C and E, and D comes last.

## Slide 10 — C and E go next door

![C and E go next door](assets/steps/03-right-d.png)

C is B's left child, so it goes next door to B, at x equals five. E is C's left child, so it lands next door to C, at x equals seven. The widths simply add up: three, plus two, plus two, makes seven.

## Slide 11 — D goes upstairs, on A

![D goes upstairs, on A](assets/steps/04-legal.png)

The left side is done, so the walk comes back to D, A's right child. D goes upstairs, so it starts at x equals zero, like A. It sits on top of A, at y equals two.

## Slide 12 — Five blocks placed

![Five blocks placed](assets/steps/05-takeaway.png)

All five blocks are placed, and every one is inside the outline. Pause and guess: if we swap A and C in the tree, does D still land at y equals two?

<!-- /algorithm-walkthrough -->

## Slide 13 — Swap A and C

![The tree with A and C swapped: C, B, A and E placed in a row](assets/lift-1.png)

No: D lands one square higher. Here is the tree with A and C swapped: C is the root, and A takes C's old place. C, B, A and E still go next door, one after the other.

## Slide 14 — The skyline

![The skyline of C, B, A and E, with D dropping from above](assets/lift-2.png)

Now picture the blocks as a city, seen from far away. The top edge of everything placed so far is the skyline. A new block drops from the sky, like a Tetris piece, until it touches the skyline.

## Slide 15 — D lands on B

![D stopped by B at y = 3, leaving a hole above C](assets/lift.png)

D is three wide, so it hangs over C and over part of B. B is three tall, so it stops D at y equals three. That leaves a hole of two empty squares above C.

## Slide 16 — The bounding box

![The first tree's bounding box: nine by three, twenty-seven squares](assets/golden-box-1.png)

So which floorplan is better? To compare, we draw the bounding box: the smallest rectangle around all the blocks. For the first tree, it is nine wide and three tall: twenty-seven squares.

## Slide 17 — Wasted space

![Twenty-three squares in blocks, four squares wasted](assets/golden-box.png)

The five blocks cover twenty-three squares. The other four squares in the box are empty: that is wasted space. Fewer wasted squares means a tighter floorplan.

## Slide 18 — One swap, a worse score

![The swapped tree: box nine by four, thirty-six squares, thirteen wasted](assets/lift-box.png)

The swapped tree needs a box nine by four: thirty-six squares, with thirteen wasted. So one swap of two names changed the picture and the score. Twenty-seven became thirty-six: the first tree is better.

## Slide 19 — One long row

![A tree where every child is a left child, next to the empty outline](assets/chain-1.png)

Now take a tree where every child is a left child. Pause and guess: will this long row fit inside the outline?

## Slide 20 — Every block next door

![A, B, C and D in a row: three, two, two and three make ten](assets/chain-2.png)

No, it will not fit. Every block goes next door: three, two, two and three make ten. The outline is already full, and E is still waiting.

## Slide 21 — Sticking out

![E sticks out of the outline: the row is twelve wide](assets/chain.png)

E lands at x equals ten, so the row is twelve squares wide. E sticks out of the outline by two squares. A floorplan is legal only when every block is inside the outline. So this row is not legal.

## Slide 22 — Never an overlap

![No overlap, but E sticks out: the only way a B*-tree can fail](assets/chain-check.png)

Notice that the blocks never overlap. Each block drops onto the skyline, so it can never land inside another one. With a B-star tree, sticking out is the only way to fail.

## Slide 23 — Turn one block

![D turned on its side: one wide and three tall, and the row fits](assets/turn.png)

We can turn a block on its side, so its width and height swap. Turn D, and it becomes one wide and three tall. Now the row is ten wide, so it fits exactly, and it is legal again.

## Slide 24 — Three small changes

Turning is one of three small changes. You can also swap two names in the tree, as we did with A and C. Or move a leaf, a block with no children, to a free spot in the tree. Each change gives a new floorplan, with a new score. Pause and guess: can any tree beat twenty-seven squares, and what is the smallest box?

## Slide 25 — The tightest floorplan

![One of the best trees, before its last block, B](assets/best-1.png)

Yes: many trees beat twenty-seven, and the best need only twenty-four squares. Here is one of the best trees. Its walk places A, D, C and E, and B comes last.

## Slide 26 — B is lifted by the skyline

![B lands on D at y = 1; the box is six by four, twenty-four squares](assets/best.png)

Under B, the skyline is the top of D, so B lands at y equals one. It fills the gap, and the box is six wide and four tall: twenty-four squares. Only one square is wasted.

## Slide 27 — Why not twenty-three?

Could a box of twenty-three squares, with nothing wasted, hold all five blocks? Twenty-three squares only make a rectangle one square thick. Block B is too thick for that, so twenty-four is the best possible.

## Slide 28 — Browser lab track

![Browser lab starter](assets/lab-starter.png)

Now build floorplans yourself. In the browser lab, you edit the tree and watch each block drop onto the skyline. The challenges check the tree you built. Lift D higher, make the long row fit, and reach twenty-four.

## Slide 29 — Implement track

![Real shell session](assets/real-shell.png)

If you like programming, write the packer in Python. The examples file gives the exact rules. Run the checker once to print every correct answer, then run it on your own file. It compares your packer with the right one on all five thousand and forty trees.

```bash
# print every correct answer
python3 examples/bstar_check.py --show

# check your own functions
python3 examples/bstar_check.py --impl my_bstar.py
```

## Slide 30 — Remember

Left child: next door. Right child: upstairs, with the same left edge. Walk the tree: the node, its whole left side, then its right child. Each block drops until it touches the skyline. Score a floorplan with its bounding box, and count the wasted squares. A tree never overlaps, but it can stick out, so check the outline.

## Slide 31 — Your turn

Pick a track: the browser lab, Python, or both. Tick each box of the checklist, then take the short quiz. Next comes the sequence pair: two lists of names instead of a tree. Pause and guess: can two lists describe our best floorplan, with twenty-four squares? Yes: two lists are enough. That's the sequence pair, in the next lab.
