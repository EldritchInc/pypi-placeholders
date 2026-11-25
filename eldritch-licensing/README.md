# eldritch-licensing (placeholder)

`eldritch-licensing` is not distributed on PyPI. This package holds the name
for Eldritch, Inc., so that nothing else can be installed under it.

eldritch-licensing checks the licence an
[Azathoth](https://github.com/EldritchInc/azathoth) remote with
azathoth-team runs under. It comes with azathoth-team, which Eldritch, Inc.
licenses to teams. To get it, write to us at
[eldritchinc.com/workwithus](https://eldritchinc.com/workwithus/).

## If you installed this

Run `eldritch-licensing`. It lists Python and the Azathoth packages
installed beside it; include those lines when you write. It reads nothing
but the versions of Python packages installed in its environment: it reaches
no network, runs no program, and reads and writes no file of its own. It
always exits with status 1, so a script that expected the real package stops
there.

Importing `eldritch_licensing` raises `ImportError`, saying the same.

To remove it:

```bash
python -m pip uninstall eldritch-licensing
```

The source of this placeholder is at
[github.com/EldritchInc/pypi-placeholders](https://github.com/EldritchInc/pypi-placeholders).
