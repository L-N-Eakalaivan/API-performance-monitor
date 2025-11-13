from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import requests
import time
from datetime import datetime
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import shutil

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize database
def init_db():
    conn = sqlite3.connect('api_monitor.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS api_metrics
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  url TEXT NOT NULL,
                  response_time REAL,
                  status_code INTEGER,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  error_message TEXT)''')
    
    # Create table for monitored APIs
    c.execute('''CREATE TABLE IF NOT EXISTS monitored_apis
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  url TEXT NOT NULL,
                  check_interval INTEGER DEFAULT 5,
                  alert_email TEXT,
                  last_checked DATETIME,
                  is_active BOOLEAN DEFAULT 1)''')
    
    conn.commit()
    conn.close()

# Function to send email alerts
def send_email_alert(to_email, api_url, error_message):
    # This is a placeholder - in a real implementation, you would configure
    # actual SMTP settings
    try:
        # Example SMTP configuration (commented out for security)
        # smtp_server = "smtp.gmail.com"
        # port = 587
        # sender_email = "your_email@gmail.com"
        # password = "your_password"
        # 
        # server = smtplib.SMTP(smtp_server, port)
        # server.starttls()
        # server.login(sender_email, password)
        # 
        # message = MIMEMultipart()
        # message["From"] = sender_email
        # message["To"] = to_email
        # message["Subject"] = f"API Monitor Alert: {api_url}"
        # 
        # body = f"API monitoring detected an error:\nURL: {api_url}\nError: {error_message}"
        # message.attach(MIMEText(body, "plain"))
        # 
        # server.sendmail(sender_email, to_email, message.as_string())
        # server.quit()
        
        print(f"Alert email would be sent to {to_email} for API {api_url} with error: {error_message}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/monitor')
def monitor():
    return render_template('monitor.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/api/test', methods=['POST'])
def test_api():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Save to metrics database
        conn = sqlite3.connect('api_monitor.db')
        c = conn.cursor()
        c.execute("INSERT INTO api_metrics (url, response_time, status_code) VALUES (?, ?, ?)",
                  (url, response_time, response.status_code))
        conn.commit()
        
        # Update last_checked timestamp for this API in monitored_apis table
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("UPDATE monitored_apis SET last_checked = ? WHERE url = ?", 
                  (current_time, url))
        conn.commit()
        conn.close()
        
        return jsonify({
            'url': url,
            'response_time': response_time,
            'status_code': response.status_code,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        # Save error to database
        conn = sqlite3.connect('api_monitor.db')
        c = conn.cursor()
        c.execute("INSERT INTO api_metrics (url, error_message) VALUES (?, ?)",
                  (url, str(e)))
        
        # Update last_checked timestamp even for failed requests
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("UPDATE monitored_apis SET last_checked = ? WHERE url = ?", 
                  (current_time, url))
        conn.commit()
        conn.close()
        
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics')
def get_metrics():
    conn = sqlite3.connect('api_monitor.db')
    c = conn.cursor()
    c.execute("SELECT * FROM api_metrics ORDER BY timestamp DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    
    metrics = []
    for row in rows:
        metrics.append({
            'id': row[0],
            'url': row[1],
            'response_time': row[2],
            'status_code': row[3],
            'timestamp': row[4],
            'error_message': row[5]
        })
    
    return jsonify(metrics)

@app.route('/api/monitored-apis', methods=['GET'])
def get_monitored_apis():
    conn = sqlite3.connect('api_monitor.db')
    c = conn.cursor()
    c.execute("SELECT * FROM monitored_apis WHERE is_active = 1")
    rows = c.fetchall()
    conn.close()
    
    apis = []
    for row in rows:
        apis.append({
            'id': row[0],
            'url': row[1],
            'check_interval': row[2],
            'alert_email': row[3],
            'last_checked': row[4],
            'is_active': row[5]
        })
    
    return jsonify(apis)

@app.route('/api/monitored-apis', methods=['POST'])
def add_monitored_api():
    data = request.get_json()
    url = data.get('url')
    check_interval = data.get('check_interval', 5)
    alert_email = data.get('alert_email', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    conn = sqlite3.connect('api_monitor.db')
    c = conn.cursor()
    c.execute("INSERT INTO monitored_apis (url, check_interval, alert_email) VALUES (?, ?, ?)",
              (url, check_interval, alert_email))
    api_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': api_id, 'url': url, 'check_interval': check_interval, 'alert_email': alert_email}), 201

@app.route('/api/monitored-apis/<int:api_id>', methods=['DELETE'])
def delete_monitored_api(api_id):
    conn = sqlite3.connect('api_monitor.db')
    c = conn.cursor()
    c.execute("UPDATE monitored_apis SET is_active = 0 WHERE id = ?", (api_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/export-metrics')
def export_metrics():
    conn = sqlite3.connect('api_monitor.db')
    c = conn.cursor()
    c.execute("SELECT * FROM api_metrics ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    
    # Format data as CSV with proper timestamp formatting for Excel
    csv_data = "ID,URL,Response Time,Status Code,Timestamp,Error Message\n"
    for row in rows:
        # Format timestamp to be Excel-friendly (ISO format)
        timestamp = row[4] if row[4] else ""
        if timestamp:
            try:
                # Parse the timestamp and format it properly
                dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                # Format as ISO 8601 which Excel can understand
                formatted_timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                # If parsing fails, use the original timestamp
                formatted_timestamp = str(timestamp)
        else:
            formatted_timestamp = ""
        
        # Escape any commas, quotes, or newlines in the data
        def escape_csv_field(field):
            if field is None:
                return ""
            field_str = str(field)
            if ',' in field_str or '"' in field_str or '\n' in field_str:
                # Escape quotes by doubling them
                field_str = field_str.replace('"', '""')
                # Enclose in quotes
                field_str = f'"{field_str}"'
            return field_str
        
        # Format each field properly
        id_field = escape_csv_field(row[0])
        url_field = escape_csv_field(row[1])
        response_time_field = escape_csv_field(row[2])
        status_code_field = escape_csv_field(row[3])
        timestamp_field = escape_csv_field(formatted_timestamp)
        error_message_field = escape_csv_field(row[5])
        
        csv_data += f"{id_field},{url_field},{response_time_field},{status_code_field},{timestamp_field},{error_message_field}\n"
    
    return csv_data, 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=api_metrics.csv'}

@app.route('/api/backup-database')
def backup_database():
    try:
        # Create a backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'api_monitor_backup_{timestamp}.db'
        backup_filepath = os.path.join('backups', backup_filename)
        
        # Create backups directory if it doesn't exist
        os.makedirs('backups', exist_ok=True)
        
        # Copy the database file
        shutil.copy2('api_monitor.db', backup_filepath)
        
        # Return the backup file for download
        return send_file(backup_filepath, as_attachment=True, download_name=backup_filename)
    except Exception as e:
        return jsonify({'error': f'Backup failed: {str(e)}'}), 500

@app.route('/api/clear-metrics', methods=['POST'])
def clear_metrics():
    try:
        # Connect to database and clear metrics data
        conn = sqlite3.connect('api_monitor.db')
        c = conn.cursor()
        c.execute("DELETE FROM api_metrics")
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Metrics data cleared successfully'})
    except Exception as e:
        return jsonify({'error': f'Failed to clear metrics data: {str(e)}'}), 500

if __name__ == '__main__':
    # Create static and templates directories if they don't exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    
    init_db()
    app.run(debug=True)