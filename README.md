# API Performance Monitor

A Flask-based application to monitor and analyze API performance metrics with a modern UI/UX.

## Features

- Real-time API monitoring
- Response time tracking
- Status code monitoring
- Performance dashboards
- Error tracking and reporting
- Data visualization with charts

## Technologies Used

- Python (Flask)
- SQLite (Database)
- Bootstrap 5 (Frontend Framework)
- Chart.js (Data Visualization)
- HTML/CSS/JavaScript

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd api-performance-monitor
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Application Structure

- `/templates` - HTML templates
- `/static` - CSS, JavaScript, and other static assets
- `app.py` - Main Flask application
- `api_monitor.db` - SQLite database (created automatically)

## UI Components

### 1. Overview Page
- Summary metrics (total APIs, average response time, uptime, errors)
- Response time trends chart
- Status distribution chart
- Recent API activity table

### 2. API Monitor Page
- Test API endpoints manually
- Add new APIs to monitor
- View monitored APIs with their status
- Perform actions (test, edit, delete)

### 3. Performance Dashboard
- Detailed performance metrics
- Filtering capabilities
- Response time distribution
- Error rate trends
- Uptime monitoring
- Detailed performance data table

## API Endpoints

- `GET /` - Overview page
- `GET /monitor` - API monitoring page
- `GET /dashboard` - Performance dashboard
- `POST /api/test` - Test an API endpoint
- `GET /api/metrics` - Retrieve performance metrics

## Database Schema

The application uses SQLite with a single table:

```sql
CREATE TABLE api_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    response_time REAL,
    status_code INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT
);
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License.