"""Database management for Mirra Cookies"""
import sqlite3
import json
from datetime import datetime
from config.settings import AppConfig
import os

class DatabaseConnection:
    def __init__(self, db_path=AppConfig.DATABASE_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                order_number TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                items JSON NOT NULL,
                total REAL NOT NULL,
                discount REAL DEFAULT 0,
                address TEXT NOT NULL,
                payment_method TEXT NOT NULL,
                status TEXT DEFAULT 'Processando 🔄',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Reviews table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                product_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Password recovery table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS password_recovery (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                used BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Cupons/Discounts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_cupons (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                cupom_code TEXT NOT NULL,
                used_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Audit log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                action TEXT NOT NULL,
                details JSON,
                ip_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, email, password_hash, name):
        """Create new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)',
                (email, password_hash, name)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND is_active = 1', (email,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def update_password(self, user_id, password_hash):
        """Update user password"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (password_hash, user_id)
        )
        conn.commit()
        conn.close()
    
    def create_recovery_code(self, user_id, code, expires_at):
        """Create password recovery code"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO password_recovery (user_id, code, expires_at) VALUES (?, ?, ?)',
            (user_id, code, expires_at)
        )
        conn.commit()
        conn.close()
    
    def verify_recovery_code(self, user_id, code):
        """Verify recovery code"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT * FROM password_recovery 
               WHERE user_id = ? AND code = ? AND used = 0 AND expires_at > CURRENT_TIMESTAMP''',
            (user_id, code)
        )
        recovery = cursor.fetchone()
        conn.close()
        return recovery
    
    def mark_recovery_as_used(self, recovery_id):
        """Mark recovery code as used"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE password_recovery SET used = 1 WHERE id = ?', (recovery_id,))
        conn.commit()
        conn.close()
    
    def create_order(self, user_id, order_number, items, total, discount, address, payment_method):
        """Create order"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO orders (user_id, order_number, items, total, discount, address, payment_method)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (user_id, order_number, json.dumps(items), total, discount, address, payment_method)
        )
        conn.commit()
        conn.close()
    
    def get_user_orders(self, user_id):
        """Get all orders for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC',
            (user_id,)
        )
        orders = cursor.fetchall()
        conn.close()
        return orders
    
    def add_review(self, product_id, user_id, rating, text):
        """Add product review"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO reviews (product_id, user_id, rating, text) VALUES (?, ?, ?, ?)',
            (product_id, user_id, rating, text)
        )
        conn.commit()
        conn.close()
    
    def get_product_reviews(self, product_id):
        """Get all reviews for product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT r.*, u.name FROM reviews r
               JOIN users u ON r.user_id = u.id
               WHERE r.product_id = ? ORDER BY r.created_at DESC''',
            (product_id,)
        )
        reviews = cursor.fetchall()
        conn.close()
        return reviews
    
    def log_cupom_usage(self, user_id, cupom_code):
        """Log cupom usagem"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO user_cupons (user_id, cupom_code, used_at) VALUES (?, ?, CURRENT_TIMESTAMP)',
            (user_id, cupom_code)
        )
        conn.commit()
        conn.close()
    
    def get_last_cupom_usage(self, user_id, cupom_code):
        """Get last cupom usage date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT used_at FROM user_cupons 
               WHERE user_id = ? AND cupom_code = ? AND used_at IS NOT NULL
               ORDER BY used_at DESC LIMIT 1''',
            (user_id, cupom_code)
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def add_audit_log(self, user_id, action, details, ip_address=None):
        """Add audit log entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO audit_log (user_id, action, details, ip_address) VALUES (?, ?, ?, ?)',
            (user_id, action, json.dumps(details) if isinstance(details, dict) else details, ip_address)
        )
        conn.commit()
        conn.close()
    
    def get_all_users(self):
        """Get all users (admin)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, name, created_at FROM users WHERE is_active = 1 ORDER BY created_at DESC')
        users = cursor.fetchall()
        conn.close()
        return users
    
    def get_all_orders(self):
        """Get all orders (admin)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT o.*, u.name, u.email FROM orders o
               JOIN users u ON o.user_id = u.id
               ORDER BY o.created_at DESC''')
        orders = cursor.fetchall()
        conn.close()
        return orders

# Global database instance
db = DatabaseConnection()
