CSV-to-WikiData
===============

## Install pywikibot (no PyPI package yet...):

```bash
git clone --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git pywikibot-core
cd pywikibot-core
sudo python setup.py install
```

**NOTE:**
This script currently uses a not yet merged feature of pywikibot in order to use unit-less quantities.
See https://gerrit.wikimedia.org/r/#/c/132629 for details

### Development

If you want to help with the development, you should clone this repository and install the requirements:

    pip install -r requirements.txt

After that, it is recommended to install the `flake8` pre-commit-hook:

    flake8 --install-hook
