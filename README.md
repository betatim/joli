# joli -- pretty notebooks

> "c’est du joli!"


```
pip install joli
joli notebook.ipynb
```

joli let's you lint your notebooks and it formats your code with `black`.

You can lint the code in your notebook but so far you can't lint the whole
notebook. Examples of lint in a notebook:

* cells executed out of order
* a mixture of executed and unexecuted cells
* too much code compared to narrative text


## Goal

The goal of joli is to provide feedback to humans and editors about lint in a
notebook. Notebook frontends should be able to implement the notebook equivalent
of putting little wiggly underlines under your code, but for notebooks.

The experience of running `joli a-notebook-file.ipynb` in a terminal should be
similar to running a linter/code formatter like `pep8` or `prettier` on a code
file.


## Developing

Checkout this repository and run `pip install -e.`. Try
`joli examples/out-of-order.ipynb` you should see some errors.
