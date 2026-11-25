# azathoth-team (placeholder)

`azathoth-team` is not distributed on PyPI. This package holds the name for
Eldritch, Inc., so that nothing else can be installed under it.

azathoth-team is the team tier of
[Azathoth](https://github.com/EldritchInc/azathoth): each person on a remote
has an identity, roles, tokens and single sign-on of their own, and an audit
records what each did. Eldritch, Inc. licenses it to teams. To get it, write
to us at [eldritchinc.com/workwithus](https://eldritchinc.com/workwithus/).

## If you installed this

Run `azathoth-team`. It lists Python and the Azathoth packages installed
beside it; include those lines when you write. It reads nothing but the
versions of Python packages installed in its environment: it reaches no
network, runs no program, and reads and writes no file of its own. It always
exits with status 1, so a script that expected the real package stops there.

Importing `azathoth_team` raises `ImportError`, saying the same.

To remove it:

```bash
python -m pip uninstall azathoth-team
```

The source of this placeholder is at
[github.com/EldritchInc/pypi-placeholders](https://github.com/EldritchInc/pypi-placeholders).
