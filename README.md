# Source Management

This application aims to facilitate operations such as inserting, viewing, updating, and deleting sources. It categorizes sources into two types—index and profile—and further classifies them under two categories: organization and person. Additionally, sources can be associated with multiple jurisdictions, allowing for advanced filtering based on source type, category, jurisdiction, and name. A unique feature of the application is its ability to assess and assign credibility scores to both the sources themselves and their individual data attributes. These credibility scores are crucial for filtering and retrieving sources. The request also includes the need for creating a MySQL database script and a system architecture diagram to support these functionalities.

## Prerequisites

Before using this Source Management, ensure you have the following:

- Python 3.111
- MySQL 8
- Docker

## Usage

1. Clone this repository to your local machine.

```bash
  git clone git@github.com:FocalIDT/source-management.git
  cd source-management
```

2. Install the requirements

```
    pip3 install -r requirements.txt
```

3. Create `.env` file using `env.example` file and Set The Values

4. Run the main.py file

```
    python3 main.py
```

5. Insert database metadata with Make File using `init_db.sql` file

- Set database related values in Make File

```
    make init_db
```

6. Run with Docker

```
    docker build -t source-management .
    docker run -t source-management
```

7. Run With Make File

Please Update `dev.sh` file variable with appropriate Values. 

```
    make build env=dev
    make deploy env=dev
```

## Source Management

This Service Can Manage Following Features

- Sources
- Clients
- DataAttributes Of Sources and Credibility

## Tech Stack

Python3, Docker, MySQL

## License

This Source Management is licensed under the following License details.

[FOCALID](https://focalid.tech/)

## Contact

If you have any questions or need further assistance, you can reach out to

## Authors

- [Chalith Wickramathilaka](https://github.com/chalithaw)
- [Prasad Kumara](https://github.com/contactpkumara)