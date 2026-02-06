# Stock Data ETL Pipeline

## Project Overview

This project is an end-to-end Data Engineering pipeline that fetches daily stock market data from the Yahoo Finance API, processes it using Python, engineers financial features, and loads the transformed data into a PostgreSQL database.

The primary aim of this project is to demonstrate core Data Engineering concepts including API ingestion, data transformation, database design, and ETL pipeline development using modular and reusable code.

---

## Features

- Fetches real-time stock price data from Yahoo Finance API  
- Parses raw JSON responses into structured tabular data  
- Cleans and validates financial time-series data  
- Engineers quantitative features such as:
  - Daily returns  
  - Log returns  
  - Rolling volatility  
  - Moving averages  
- Loads transformed data into PostgreSQL  
- Implements modular, object-oriented ETL design  
- Config-driven architecture for easy extensibility  
- One-command execution pipeline  

---

## Project Architecture

The project follows a modular ETL architecture.

### Folder Structure

```bash
stock_pipeline/
│
├── src/
│   ├── ingestion/
│   │   ├── stock_fetcher.py
│   │   └── stock_parser.py
│   ├── transformation/
│   │   └── stock_transformer.py
│   ├── db/
│   │   └── db_loader.py
│   ├── pipeline/
│   │   └── etl_pipeline.py
│   └── utils/
│       ├── config.py
│       └── logger.py
│
├── data/
│   └── raw/
│
├── requirements.txt
└── main.py
```

---

## Technologies Used

- **Python** – Core programming language  
- **Pandas** – Data manipulation  
- **Requests** – API interaction  
- **PostgreSQL** – Data storage  
- **SQLAlchemy** – Database connection  
- **Object-Oriented Programming (OOP)**  
- **Logging & Config Management**

---

## Data Pipeline Flow

1. **Extract**  
   - Fetches daily stock price data using Yahoo Finance API  
   - Stores raw API responses for audit and reproducibility  

2. **Transform**  
   - Converts JSON to structured DataFrame  
   - Cleans missing values  
   - Generates financial analytics features  

3. **Load**  
   - Stores processed data in PostgreSQL  
   - Uses normalized schema with indexing  
   - Ensures data integrity via constraints  

---

## Database Design

### Tables

**stocks**

| Column    | Type    | Description      |
|----------|---------|------------------|
| stock_id | SERIAL  | Primary Key      |
| symbol   | VARCHAR | Unique Stock Code|

**daily_prices**

| Column         | Description          |
|----------------|----------------------|
| stock_id       | Foreign Key          |
| date           | Trading date         |
| open           | Opening price        |
| high           | High price           |
| low            | Low price            |
| close          | Closing price        |
| volume         | Traded volume        |
| daily_return   | Simple return        |
| log_return     | Log return           |
| volatility_20d | Rolling volatility   |
| ma_20d         | 20-day moving avg    |
| ma_50d         | 50-day moving avg    |

---

## How to Run the Project

### 1. Clone Repository

```bash
git clone https://github.com/augustusHarts/Stock-Data-ETL-Pipeline.git
cd stock_pipeline
```

### 2. Create Virtual Environment

```bash
python -m venv etlenv
source etlenv/bin/activate   # Mac/Linux
etlenv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database

1. Create a PostgreSQL database:

```
stock_pipeline
```

2. Update database credentials in the configuration file:

```
src/utils/config.py
```

Add your local PostgreSQL connection details such as:

- host  
- username  
- password  
- database name  

---

### 5. Run the Pipeline

```bash
python main.py
```

---

## Output

- Raw API responses are stored in:

```
data/raw/
```

- Transformed and cleaned data is loaded into PostgreSQL tables:

```
stocks  
daily_prices
```

---

## Future Enhancements

Planned improvements:

- Automate pipeline using Apache Airflow  
- Add Docker support  
- Implement incremental data loading  
- Add unit tests  
- Build analytics dashboard on top of processed data  

---

## About

This project was built as a portfolio project to showcase foundational Data Engineering and Python development skills.
