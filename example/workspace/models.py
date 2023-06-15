
from dataclasses import dataclass
import mysql.connector

@dataclass
class Vulnerability:
    id: int = None
    name: str = None
    description: str = None
    severity: str = None
    date_added: str = None

class VulnerabilityDAO:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='vulnerabilities'
        )
        self.cursor = self.conn.cursor()

    def search_vulnerabilities(self, search_query):
        query = "SELECT * FROM vulnerabilities"
        if search_query:
            query += f" WHERE name LIKE '%{search_query}%' OR description LIKE '%{search_query}%'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        vulnerabilities = []
        for row in result:
            vulnerability = Vulnerability(id=row[0], name=row[1], description=row[2], severity=row[3], date_added=row[4])
            vulnerabilities.append(vulnerability)
        return vulnerabilities

    def add_vulnerability(self, vulnerability):
        query = "INSERT INTO vulnerabilities (name, description, severity) VALUES (%s, %s, %s)"
        values = (vulnerability.name, vulnerability.description, vulnerability.severity)
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_vulnerability(self, vulnerability_id):
        query = "SELECT * FROM vulnerabilities WHERE id = %s"
        values = (vulnerability_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        vulnerability = Vulnerability(id=result[0], name=result[1], description=result[2], severity=result[3], date_added=result[4])
        return vulnerability

    def update_vulnerability(self, vulnerability):
        query = "UPDATE vulnerabilities SET name = %s, description = %s, severity = %s WHERE id = %s"
        values = (vulnerability.name, vulnerability.description, vulnerability.severity, vulnerability.id)
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_vulnerability(self, vulnerability_id):
        query = "DELETE FROM vulnerabilities WHERE id = %s"
        values = (vulnerability_id,)
        self.cursor.execute(query, values)
        self.conn.commit()