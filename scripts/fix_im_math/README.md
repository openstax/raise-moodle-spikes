# Fix math in IM content

The content we receive from IM seems to be exports from Canvas where the math is generated as:

```html
<span><img class="equation_image" title="y" src="/equation_images/y" alt="LaTeX: y" data-equation-content="y"></span>
```

Before importing into Moodle, instances of this math need to be modified so that MathJax will render it using the underyling LaTeX:

```html
<span>\( y \)</span>
```

The `fix_im_math.py` script here can be used to automate that step:

```bash
$ pip install -r requirements.txt
$ python fix_im_math.py <path_to_catridge_extract>
```
