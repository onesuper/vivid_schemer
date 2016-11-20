
# The Vivid Schemer

## Introduction


The Vivid Schemer is inspired by [The Little Schemer](http://www.amazon.com/The-Little-Schemer-4th-Edition/dp/0262560992).
It uses the metaphor of Q&As to illustrate the concepts of programming, such as recursion, combination, and
sub-problem. It is based on a small subset of [scheme programming language](https://en.wikipedia.org/wiki/Scheme_%28programming_language%29).


It is intended to provide a [learnable programming](http://worrydream.com/LearnableProgramming/)
 environment in which people can 'see' and understand the behavior of code.


Currently, The Vivid Schemer provides two command-line tool. `repl` has not difference with an ordinary lisp *read-eval-print* loop, **except** it does allow you to see each step of evaluation and the whole story about it. `cli.py` is an interactive version for The Little Schemer.


![](screenshot.gif)


## Lessons Learned

The former (deprecated) web interface can be visited at [http://vivid.chengyichao.info](http://vivid.chengyichao.info). As you can see, though it claims to be interative, the interaction is awkward. It is like an old man rambling about his old days. And one can not just interrupt it and ask:

* What states have I changed?
* Which peice of the code did the magic stuff?


Actually, context matters. The execution flow and should be associated with the code and the scope of vairables. Otherwise one can still be overwhelmed by the recursive calls.


## Caveat

* This tool is not for production. Do not use it when you are in a hurry.
* The Vivid Schemer is NOT a notebook-like system like [Jupyter](http://jupyter.org/) because such systems do not exhibit the execution flow of a program.
