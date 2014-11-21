pip install requests giphypop

in xchat:
/py load /path/to/xchat.py

then:
/gif some words

click on a gif, bam.

To get this auto-loaded in xchat, stick a file in ~/.xchat2/ (YMMV on other platforms), call it something like gif.py, and make the contents:
```python
__file__ = '/path/to/pygiphy/xchat.py'
execfile(__file__)
```
