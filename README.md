
# The Vivid Schemer

## Example

```
>>> from vivid_schemer import Repl
>>> repl = Repl()
>>> repl.read('(car (quote (a b c)))')
>>> repl.top()
(car
  (quote
    (a b c)))
>>> repl.eval()
>>> repl.top()
What is '(car (quote (a b c)))'?
(car
  (quote
    (a b c)))
>>> repl.eval()
>>> repl.top()
What is the car of l where l is (a b c)
(car
  ===> (list): (a b c)
  (quote
    (a b c)))
>>> repl.eval()
a
>>> repl.top()
===> (atom): a
(car
  ===> (list): (a b c)
  (quote
    because a is the first S-expression of this non-empty list.
    (a b c)))
```

