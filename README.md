# pypi-placeholders

Placeholders that hold, on PyPI, the names Eldritch, Inc.'s private
packages are installed under. Neither private package is distributed on
PyPI; a placeholder keeps anyone else from publishing a package under its
name, which pip would otherwise take for the real one.

| Placeholder | Holds the name of | Source |
| --- | --- | --- |
| [`azathoth-team`](https://pypi.org/p/azathoth-team) | The team tier of [Azathoth](https://github.com/EldritchInc/azathoth) | `azathoth-team/` |
| [`eldritch-licensing`](https://pypi.org/p/eldritch-licensing) | The licences an Azathoth team remote runs under | `eldritch-licensing/` |

Teams get the real packages from Eldritch:
[eldritchinc.com/workwithus](https://eldritchinc.com/workwithus/).

## What a placeholder does

- Run under its product's name, it lists Python and the Azathoth packages
  installed beside it, says the product is not distributed on PyPI and
  where to ask for it, and exits with status 1, so a script that expected
  the real package stops there.
- Importing the package it holds raises `ImportError`, saying the same.
- It reads nothing but the versions of Python packages installed in its
  environment. It reaches no network, runs no program, reads and writes no
  file of its own, and runs nothing when installed: it is published as a
  wheel only. Tests hold it to the imports the report needs.
- It depends on nothing, adds no plugin to Azathoth, and its version,
  `0.0.1`, is below every release of the real package, so pip never takes
  it for the real one.

Both placeholders share one report module, byte for byte; each takes its
product from its own package's name.

## Developing

```bash
python -m venv .venv
source .venv/bin/activate
make install
make check
```

`make build` builds both wheels into `dist/`.

## Releasing

Each placeholder has a release workflow of its own,
`release-azathoth-team.yml` and `release-eldritch-licensing.yml`, since PyPI
trusts one workflow file to publish one new project. A tag naming the
product and its version runs that product's workflow, which tests, builds
its wheel alone, installs and runs it, and publishes it to PyPI from the
`pypi` environment with trusted publishing; no token is kept anywhere.

```bash
git tag azathoth-team-v0.0.1
git push origin azathoth-team-v0.0.1
git tag eldritch-licensing-v0.0.1
git push origin eldritch-licensing-v0.0.1
```

A version is published once: PyPI refuses it a second time, even after it
is deleted.

## Licence

MIT. See [LICENSE](https://github.com/EldritchInc/pypi-placeholders/blob/main/LICENSE).
