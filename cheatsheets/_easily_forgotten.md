# Easily Forgotten

The basic things you *know* but blank on mid-problem. Not tricks, just the
"wait, how do I… again?" moments.

**Add to this list whenever you look something up twice.**

---

## The ones that started this list

```python
len(string_a)        # length of anything: str, list, dict, set, tuple
str(x)               # convert anything to a string
```

---

## Length and size: it's always `len()`

```python
len("hello")         # 5
len([1, 2, 3])       # 3
len({"a": 1})        # 1 (number of keys)
len(set())           # 0
```
Not `.length`, not `.size()`, not `.count()`. Python has **one** function
for all of them.

---

## Converting between types

```python
str(42)              # '42'        anything -> string
int("42")            # 42          string -> integer
int(3.9)             # 3           float -> int (TRUNCATES, doesn't round)
float("3.5")         # 3.5
list("abc")          # ['a', 'b', 'c']   string -> list of characters
list((1, 2))         # [1, 2]            tuple -> list
tuple([1, 2])        # (1, 2)            list -> tuple (so it can be a dict key)
set([1, 1, 2])       # {1, 2}            list -> set (drops duplicates)
''.join(['a', 'b'])  # 'ab'              list of strings -> string
bool(0), bool("")    # False, False      empty / zero is falsy
ord('a'), chr(97)    # 97, 'a'           character <-> number
```

**The one that trips people:** `str(123)` → `'123'`, and `list(str(123))` →
`['1', '2', '3']`. That's the quick way to get the digits of a number.

```python
[int(d) for d in str(123)]      # [1, 2, 3]  digits of a number
int(''.join(['1', '2', '3']))   # 123        digits back to a number
```

---

## Checking what something is

```python
type(x)                   # <class 'int'>
isinstance(x, int)        # True / False (prefer this for checks)
x is None                 # use `is` for None, not ==
```

---

## Python spelling (if you've used other languages)

| You might type | Python wants |
|---|---|
| `true` / `false` / `null` | `True` / `False` / `None` |
| `&&` / `\|\|` / `!` | `and` / `or` / `not` |
| `else if` | `elif` |
| `i++` | `i += 1` |
| `x.length` | `len(x)` |
| `2 ^ 3` for power | `2 ** 3` (`^` is **XOR**: `2 ^ 3 == 1`) |
| `// comment` | `# comment` |
| `a ? b : c` | `b if a else c` |

---

## Division

```python
7 / 2       # 3.5   always a float
7 // 2      # 3     integer (floor) division
7 % 2       # 1     remainder
2 ** 10     # 1024  power
```

---

## Lists: the easily mixed-up pairs

```python
a.append(4)          # add ONE item to the end
a.extend([4, 5])     # add EACH item from another list
a + [4, 5]           # new list; a itself doesn't change

a.sort()             # sorts a IN PLACE, returns None
b = sorted(a)        # returns a NEW sorted list

a.pop()              # remove and RETURN the last item
a.pop(i)             # remove and return the item at index i
a.remove(x)          # remove the first item EQUAL to x (no return)
del a[i]             # delete by index (no return)

a.index(x)           # position of x (ValueError if missing)
x in a               # True / False (O(n) on a list)
a.count(x)           # how many times x appears

a[-1]                # last item
a[::-1]              # reversed copy
```

**Classic bug:** `a = a.sort()` sets `a` to `None`. `.sort()` returns
nothing. Use `a.sort()` on its own line, or `a = sorted(a)`.

---

## Strings: the ones people blank on

```python
s.split()                  # "a b c" -> ['a', 'b', 'c']
'-'.join(parts)            # the SEPARATOR comes first, then .join(list)
s.find('x')                # index, or -1 if missing (safe)
s.index('x')               # index, or ValueError if missing
s.strip()                  # remove whitespace from both ends
s.lower(), s.upper()
s.isdigit(), s.isalpha(), s.isalnum()
s.replace('a', 'b')        # returns a NEW string
s[i]                       # a single character (strings index like lists)
```

**Strings are immutable.** `s[0] = 'x'` is an error, and `s.replace(...)`
doesn't change `s`. Assign the result: `s = s.replace('a', 'b')`.

---

## Cleaning and filtering strings

Almost every "clean up this string" task uses **one template**:

```python
''.join( <what to keep it as>  for c in s  if <keep this char?> )
#          transform             loop          filter
```

The `if` decides what gets **dropped**, and the part before `for` decides what
each kept character **becomes**. Once that's familiar, the recipes below are
just variations on it.

```python
s = "A man, a plan, a canal: Panama!"

# Keep only letters and digits (drops spaces, commas, punctuation)
''.join(c for c in s if c.isalnum())           # 'AmanaplanacanalPanama'

# ...and lowercase at the same time. This is Valid Palindrome's prep step.
''.join(c.lower() for c in s if c.isalnum())   # 'amanaplanacanalpanama'

# Only letters / only digits
''.join(c for c in "a1b2c3" if c.isalpha())    # 'abc'
''.join(c for c in "a1b2c3" if c.isdigit())    # '123'

# Drop specific characters
''.join(c for c in s if c not in ",.:!?")      # 'A man a plan a canal Panama'
```

### Spaces

```python
"a b  c".replace(" ", "")          # 'abc'     removes spaces only
''.join("a b\tc\n".split())        # 'abc'     removes ALL whitespace
' '.join("a   b    c".split())     # 'a b c'   collapses runs to one space
"  hi  ".strip()                   # 'hi'      only the two ends
```

`.split()` with **no argument** splits on any run of whitespace and drops the
empty pieces. That's why `''.join(s.split())` and `' '.join(s.split())` work.
`.split(' ')` doesn't do this: `"a  b".split(' ')` gives `['a', '', 'b']`.

### Case

```python
s.lower()          # 'a man, a plan, a canal: panama!'
s.upper()          # 'A MAN, A PLAN, A CANAL: PANAMA!'
"hello world".title()        # 'Hello World'
"hello world".capitalize()   # 'Hello world'   first letter only
"Hi".swapcase()              # 'hI'
c.islower(), c.isupper()     # check one character
a.lower() == b.lower()       # compare ignoring case
```

### The check methods, and what counts

| Method | True for | Example |
|---|---|---|
| `c.isalnum()` | letter **or** digit | `'a'`, `'7'` |
| `c.isalpha()` | letter | `'a'`, `'Z'` |
| `c.isdigit()` | digit | `'7'` |
| `c.isspace()` | space, tab, newline | `' '`, `'\t'` |
| `c.islower()` / `c.isupper()` | lowercase / uppercase letter | `'a'` / `'A'` |

On a whole string they check **every** character: `"abc1".isalnum()` is
`True`, and `"ab c".isalnum()` is `False` because of the space. On an empty
string they all return `False`.

### Checking without building a new string

```python
any(c.isdigit() for c in s)        # does it contain a digit?
all(c.isalpha() for c in s)        # is it letters only?
sum(c.isupper() for c in s)        # how many capitals (True counts as 1)
```

### Words

```python
' '.join(reversed(s.split()))      # reverse word order: 'b a' from 'a b'
' '.join(w[::-1] for w in s.split())   # reverse each word, keep order
[w for w in s.split() if len(w) > 3]   # words longer than 3 letters
```

### Handy constants

```python
import string
string.ascii_lowercase     # 'abcdefghijklmnopqrstuvwxyz'
string.ascii_uppercase     # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
string.digits              # '0123456789'
string.punctuation         # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
```

### Putting it together: the palindrome check

```python
cleaned = ''.join(c.lower() for c in s if c.isalnum())
cleaned == cleaned[::-1]           # True for "A man, a plan, a canal: Panama!"
```

This builds a new string, so it uses O(n) extra space. It's correct, and a
good first answer. An interviewer may then ask for O(1) space, which means two
pointers skipping non-alphanumeric characters as they go (Module 02).

---

## Dicts

```python
d[k]                 # KeyError if missing
d.get(k)             # None if missing
d.get(k, 0)          # 0 if missing
k in d               # checks KEYS, not values
d.keys(), d.values(), d.items()
for k, v in d.items(): ...
del d[k]
d.pop(k, None)       # remove, no error if missing
```

---

## Loops

```python
for i in range(n):              # 0 .. n-1
for i in range(a, b):           # a .. b-1  (b is EXCLUDED)
for i in range(n - 1, -1, -1):  # n-1 down to 0
for i, x in enumerate(a):       # index AND value
for x, y in zip(a, b):          # two lists side by side
```

`range(a, b)` never includes `b`. Neither does the slice `a[i:j]`, which
stops before `j`. Same rule everywhere.

---

## Numbers

```python
abs(-5)              # 5
round(2.567, 2)      # 2.57
max(a), min(a), sum(a)
max(3, 7)            # works on plain values too
float('inf')         # a value bigger than any number
import math
math.sqrt(16)        # 4.0
math.ceil(2.1)       # 3   round up
math.floor(2.9)      # 2   round down
```

---

## Default arguments: never a list or dict

```python
def add(x, items=[]):      # WRONG: the same list is shared by every call
    items.append(x)
    return items

add(1)    # [1]
add(2)    # [1, 2]   <- the 1 is still there

def add(x, items=None):    # right: make a fresh list inside
    if items is None:
        items = []
    items.append(x)
    return items
```

A default value is created **once**, when the function is defined, not on each
call. That's harmless for numbers and strings, and a bug for lists, dicts, and
sets. It bites in recursive helpers like `def dfs(node, path=[])`.

---

## My additions

<!-- Whenever you look something up twice, put it here. One line each. -->

-

---

Related: [`_python.md`](_python.md) for interview idioms ·
[`00_complexity.md`](00_complexity.md) for what each operation costs ·
[← back to the repo](../README.md)
