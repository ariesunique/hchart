# H-Charts

Simple charting web application. Upload data in csv format. The application will generate a beautiful table and chart.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Make sure you have python (and pip) installed on your system.

### Installing

1. Clone this repository

```
git clone https://github.com/ariesunique/hchart.git
```

2. Create a virtual environment.

```
python -m venv hchart-env
source hchart-env/bin/activate
pip install --upgrade pip
```

3. Install the dependencies.

```
cd hchart
pip install -r requirements.txt
```

4. Create a .env file for local development.

As per [the Twelve Factor App](https://12factor.net/config) methodology, it is preferable to store application settins as environment variables rather than in config files. 
However, for convenience a .env file can be used for local development. This should not be used on a production server. 
The settings specifed in this file will be read by settings.py and passed to the flask application. The [Environs package](https://pypi.org/project/environs/)
will copy any config vars found into environment variables.


```
cp .env.example .env
```

5. **Run the application**

```
./run.sh
```

## Running the tests

Several initial tests are provided. There are definitely more tests that can be added.

The tests can be run from the tests directory.

```
cd tests
pytest
```


## Deployment

This could be deployed on Heroku.

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [Plotly](https://plotly.com/python/) - Graphing library
* [Pandas](https://pandas.pydata.org/) - Data analysis
* [Bootstrap](https://getbootstrap.com/) - User Interface
* [PyTest](https://docs.pytest.org/en/latest/) - Testing framework


## Acknowledgments

* Thanks [PurpleBooth](https://github.com/PurpleBooth) for the useful Readme template
