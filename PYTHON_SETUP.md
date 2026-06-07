# Python Setup

Version 3.14.5 required.

1. [Python](https://www.python.org/) must be installed in your system.

2. [pip](https://pypi.org/project/pip/) must be installed in your system.

3. [pyenv](https://github.com/pyenv/pyenv) must be installed in your system.

4. Install the latest version of Python: `pyenv install 3.14.5`.

5. Run `pyenv versions` to see if it's installed.

6. Run `pyenv global 3.14.5` to set the latest version as global.

7. Open your `.zshrc` or `.bashrc` file and add next lines:

```bash
# python start
alias pip=pip3
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
# python end
```

This will alias `pip` command to `pip3` so you can just type `pip`.

It's also aliases `python` command to the global Python version you installed with `pyenv`, so you
can type `python` in order to exec commands.

8. Source file that you previously edited or restart your terminal and verify:

```bash
python --version # should show your installed version
pip --version # should show pip3 version
pyenv versions # should show installed python versions in your system
```
