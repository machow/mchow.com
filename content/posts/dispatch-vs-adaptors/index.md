---
title: 'Python patterns: single dispatch vs adapters'
author: Michael Chow
date: '2024-07-12'
slug: dispatch-vs-adaptors
freeze: true
---


<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous" data-relocate-top="true"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


Often, library developers need to perform the same set of actions over classes from different libraries. For example, a person might want their library to be able to handle DataFrames from both the Pandas and Polars libraries.

In general there are two common approaches to this:

-   **adapters**: create new data (i.e. a class) in order to perform new actions
-   **single dispatch**: create new actions (i.e. functions) directly for existing data

In my experience, adapters seem to be the most common. Often, when implementing single dispatch, people will ask why I am not using an adapter. This post is an attempt to explain why: adapters are a special case of single dispatch, with a tricky layer of data added.

> (What I am calling single dispatch here is single [generic function](https://peps.python.org/pep-0443) dispatch.)

## The challenge: define new actions over DataFrames

Suppose you are building a data tool in python, and want to be able support both Pandas and Polars DataFrames.

``` python
import pandas as pd
import polars as pl

df_pandas = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
df_polars = pl.from_pandas(df_pandas)
```

These two types of DataFrames have many similarities, but also a devilish number of tiny differences.

For example, both have a `.columns` property that reports similar information (column names), but they each return different types of things.

``` python
df_pandas.columns  # a pd.Index object
df_polars.columns  # a list of strings
```

    ['x', 'y']

In practice, it's not hard to turn both results into a list, but some layer of logic is needed to handle operating on either type of DataFrame.

## Adapters: new classes with new actions (methods)

A common approach in Python is to use the adapter pattern.
Adapters are classes that wrap the data, with methods for performing new actions on that data.

For example, you could create a `.columns()` method to return the column names of either DataFrame as a list.

``` python
class PandasAdapter:
    def __init__(self, data: pd.DataFrame):
        self._d = data

    def columns(self) -> list[str]:
        # must make columns a list
        return list(self._d.columns)


class PolarsAdapter:
    def __init__(self, data: pl.DataFrame):
        self._d = data

    def columns(self) -> list[str]:
        # similar to pandas, but columns already a list
        return self._d.columns


pd_adapter = PandasAdapter(df_pandas)
pl_adapter = PolarsAdapter(df_polars)

# both return ["x", "y"]
pd_adapter.columns()
pl_adapter.columns()
```

    ['x', 'y']

### Dilemma 1: actions that produce DataFrames

One challenge with adapters is that you need to keep wrapping the original data. For example, if you wanted to add a `subset_rows()` method---which creates a new DataFrame with fewer rows---that new DataFrame result will need to be wrapped in an adapter.

``` python
from typing_extensions import Self


class PandasAdapter:
    ...

    def subset_rows(self, rows: list[int]) -> Self:
        return self.__class__(self._d.iloc[rows])


class PolarsAdapter:
    ...

    def subset_rows(self, rows: list[int]) -> Self:
        return self.__class__(self._d[rows])
```

Now that `.subset_rows()` returns an adapter, you can use the `.columns()` method on it.

``` python
PandasAdapter(df_pandas).subset_rows([1]).columns()
```

    ['x', 'y']

This is fine, but quickly spirals out of control:

-   **Adapting DataFrame parts**: each column of a DataFrame is a series. If you want to adapt the Series, now you need to return a `PolarsSeriesAdapter`, etc..
-   **Adapting adapters**: notice how we used DataFrame methods in our adapter code. If someone wanted to use DataFrame methods and your adapter methods, it quickly becomes a nightmare.

The second piece is a nightmare worth talking about.

### Dilemma 2: adapters of adapters of adapters

Suppose 2 libraries wrote DataFrame adapters. In order use them, you would basically have to juggle..

-   wrapping the data in adapter1 to call its methods.
-   unwrapping the data
-   wrapping the data in adapter2 to call its methods.

This feels wrong because adapters don't functionally add any new data. They appear as new data in order to create new actions.

## Single dispatch: new actions only

By contrast, generic functions do what adapters do (add new actions), but are just regular functions. The most common form of generic function dispatch is single dispatch, where the first argument to a function is used to determine which implementation to use.

For example, here is the `.columns()` method reimplemented using python's built in `singledispatch` decorator.

``` python
from functools import singledispatch

# columns ----


@singledispatch
def columns(data):
    raise TypeError(f"Unsupported type: {type(data)}")


@columns.register
def _(data: pd.DataFrame) -> list[str]:
    return list(data.columns)


@columns.register
def _(data: pl.DataFrame) -> list[str]:
    return data.columns


columns(df_pandas)
columns(df_polars)
```

    ['x', 'y']

``` python
@singledispatch
def subset_rows(data, rows: list[int]):
    raise TypeError(f"Unsupported type: {type(data)}")


@subset_rows.register
def _(data: pd.DataFrame, rows: list[int]) -> pd.DataFrame:
    return data.iloc[rows]


@subset_rows.register
def _(data: pl.DataFrame, rows: list[int]) -> pl.DataFrame:
    return data[rows]
```

``` python
columns(subset_rows(df_pandas, [1]))
```

    ['x', 'y']

### You can still create adapters with singledispatch

There's an exciting twist: adapters are a special case of single dispatch.

Recall that..

-   singledispatch creates new actions on existing classes
-   an adapter creates a new class (in order to create new actions)

Adapters are single dispatch over a new class. More specifically, they are what's called generic method dispatch, since the first argument (`self`) is the class that determines the specific method to call (e.g. `PandasAdapter.columns()` vs `PolarsAdapter.columns()`).

It's quick for single dispatch (using generic functions) to implement the same actions an adapter might have. For example, here is `columns()` re-implemented over the `PandasAdapter`.

``` python
@columns.register
def _(data: PandasAdapter) -> list[str]:
    return list(data._d.columns)


@subset_rows.register
def _(data: PandasAdapter, rows: list[int]) -> PandasAdapter:
    return data._d.iloc[rows]


columns(subset_rows(PandasAdapter(df_pandas), [1]))
```

    ['x', 'y']

The big difference between adapters and singledispatch is that you can't go the other way: Python's singledispatch can do what adapters do, but adapters can't restrict themselves to what singledispatch does (since they do something extra--create a new piece of class data).

To really drive this point home, the code below registers the adapter methods directly to a new single dispatch function, `subset_rows2()`:

``` python
@singledispatch
def subset_rows2(data, rows):
    raise TypeError()


subset_rows2.register(PandasAdapter, PandasAdapter.subset_rows)
subset_rows2.register(PolarsAdapter, PolarsAdapter.subset_rows)

subset_rows2(PandasAdapter(df_pandas), [1])
```

    <__main__.PandasAdapter at 0x111dab9d0>

Note that the big challenge is there's no way to undo the wrapping: whereas the single dispatch functions were written to operate on DataFrames directly, the adapter methods expect a DataFrame wrapped in something.

Another way to say this is that the single dispatch functions could be DataFrame methods if they wanted to be:

``` python
pd.DataFrame.subset_rows = subset_rows

df_pandas.subset_rows([1])
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | x   | y   |
|-----|-----|-----|
| 1   | 2   | 4   |

</div>

## Should I never use adapters?

Adapters in Python have one big benefit: they can use [method chaining](https://stackoverflow.com/a/41817688). For user-facing interaces this can be really helpful! Often when people ask about adapters though, they're using them for back-of-shop activities. In this case, I think adapters are less useful.

Another useful place for an adapter is when it needs to hold data. For example, if `PandasAdapter` needed to hold options, or state. In this case, you could still use `singledispatch` to separate `PandasAdapter` data (e.g. its options and state) from its actions (e.g. the singledispatch functions that operate on it).

Finally, many programming decisions are social in nature. If people are more likely to use (or contribute to) an adapter, then it makes sense to use one.

## Wrapping up

Adapters and single (generic function) dispatch are two ways to add new actions to existing data. While single dispatch gets away with implementing functions directly, adapters add a new type of data: a class wrapping the original data.

For more on the joys and challenges of single (generic function) dispatch, see:

-   [databackend](https://github.com/machow/databackend): a library for using singledispatch with optional dependencies.
-   [Single dispatch for democratizing data science tools](https://mchow.com/posts/2020-02-24-single-dispatch-data-science/): more on single dispatch.
-   [python docs on singledispatch](https://docs.python.org/3/library/functools.html#functools.singledispatch)