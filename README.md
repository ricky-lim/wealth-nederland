# Wealth of Nederland
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ricky-lim/wealth-nederland/master?filepath=notebooks%2Fwealth_of_nederland.ipynb)


A dashboard application to explore income data from opendata.cbs.nl.

Avaiable at http://wealth-of-nederland.herokuapp.com

Details on how to deploy voila-based notebook on heroku, please refer [here](https://github.com/martinRenou/voila-heroku).

## Setup

```
make create_environment

# Activate the virtual environment, `conda activate wealth-nederland`
make requirements

# Add dataset
make data
```

### Development

```
make dev_requirements

# Create ipykernel for jupyter
make kernel

# Lint `src` and `notebooks`
make lint

# Run test
make test
```

## References

- Nederland map is from https://www.webuildinternet.com/articles/2015-07-19-geojson-data-of-the-netherlands/provinces.geojson
- Income data with id: `71103ENG` from `opendata.cbs.nl`