
![img](/app/static/images/vinyl_vault_doc.png)

## What is VinylVault? 
**VinylVault** is a web-app designed to help users track and manage their music collections. 

It allows users to search for, add items to, and analyse their music collections.

The app provides an analytics dashboard with insights, including breakdowns by genre, decade, and more - including tailored music suggestions driven from their library. VinylVault uses data from the Spotify and LastFM APIs to power its ETL pipeline. 

Future updates will include integration with Discogs, allowing users to browse current listings for albums in their collection and receive additional recommendations, filtering by price and condition.

## Setup & Installation (MacOS)
### Prerequisites
Please ensure that the following software is installed:
- `psql`
- `Python 3`
## Running the program
1. Clone the repository.
- `git clone https://github.com/Leon-JS02/VinylVault`
2. Set up a virtual environment and enter the repository.
- `python3 -m venv venv`
- `source venv/bin/activate`
- `cd VinylVault`
3. Install requirements
- `pip3 install -r requirements.txt`
4. Initialise the database
- `bash schema/setup-db.sh`
5. Run the program
- `python3 app/main.py`
- [Access here](http://localhost:8080/)