---
title: Using R and the A* Algorithm to Cruise Around Minecraft
author: Michael Chow
date: '2018-06-05'
slug: r-and-astar-with-minecraft
categories: []
tags: []
draft: yes
---

In case you haven't heard, there are a bunch of cool ways you can interact with minecraft from R.
These include making a nice drawing of your mug, plotting a ggplot graph, and building mazes.

Recently at the NYC R conference, I had the chance to see David Smith demo building a maze, and then navigate it using the left-hand rule.
It was really cool!
By the end of the talk, as we stepped out of the maze and my gaze turned to the lofty minecraft peaks in the distance, a gentle thought stirred.

![](https://78.media.tumblr.com/cee821069e82c19d5550ddad02d596f7/tumblr_oj0k02nccx1skcw00o7_r1_400.gif)

I knew then that my heart belonged to finding the optimal path up one of those craggy slopes.

In this post, I'll quickly go through an R package I put together for using the A* algorithm, and how to apply it to minecraft.

## Using A* in R

The A* algorithm (pronounced "a star") is a search algorithm for finding the "shortest" path between two nodes in a graph.

The `astar` function requires specifying functions that answer four questions for a given node:

1. Is this the goal node?
2. Who are its neighbors?
3. How far is it from a neighbor?
4. (Approximately) how far is it from the goal?

While this often takes the shape of navigating between two points in space,
a lot of other problems can be solved by A* as well.
One interesting example is Word Latters.

## Word Latters

Word Latters involve two pieces:

1. words that differ by only one letter are neighbors (e.g. "cat" and "bat")
2. we want to find the path from one word to another (e.g. "cat" to "dog")

For example, the graph below shows some possible paths we could try for going from "cat" to "dog". The red path makes it in a few steps, whereas the blue path takes a roundabout way, that meets up with the shorter path.

<img src="/003-r-and-astar-1.png" style = "max-width: 500px; display: block; margin-left: auto; margin-right: auto;">

Below, I'll show how the A* algorithm can solve the problem of finding a path that takes the least number of steps.

First we install the `astar` package..

```r
remotes::install_github('machow/astar-r')
```

Next, we define the nodes in our graph, along with tools to see how far they are from eachother..


```r
library(astar)
words <- c(
  'cat', 'hat', 'bat', 'bet', 'cot', 'cut', 'bed', 'bud',
  'bot', 'bit', 'pat', 'sat', 'pit', 'put', 'sit', 'mit',
  'bog', 'bug', 'big', 'bag', 'cog', 'pig', 'hog', 'sag',
  'dig', 'dug', 'dog'
)

split <- function(s)               # breaks word into vector of letters
  unlist(strsplit(s, ""))

ltr_dist <- function(s1, s2)       # number of letters that differ
  sum(split(s1) != split(s2))
```

Then, we define four functions to answer each of the A* questions listed above.  In this case, I set all nodes connected as neighbors, but the distance between invalid nodes as infinite.



```r
# A* methods ----
is_goal_reached <- function(src, dst)     # should we stop?
  src == dst

neighbors <- function(node)               # find neighbors
  words[words != node]

edge_distance <- function(src, dst)       # how far is node from neighbor
  if (ltr_dist(src, dst) == 1) 1 else Inf

cost_estimate <- function(node, goal)     # estimate how far node is from goal
  as.numeric(ltr_dist(node, goal))        # best case estimate: min swaps left
```

Finally, we run the `astar` function with the starting and ending nodes..


```r
# Run ----
astar('cat', 'dog', 
      cost_estimate, edge_distance, neighbors, is_goal_reached
      )
```

```
[[1]]
[1] "cat"

[[2]]
[1] "cot"

[[3]]
[1] "cog"

[[4]]
[1] "dog"
```


## Cruising Around Minecraft

Navigating minecraft involves three separate pieces:

1. Coding A* to navigate a 3D space
2. Getting a chunk of blocks from minecraft to navigate
3. Placing blocks in minecraft as we go





