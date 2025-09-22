================================================================================
                            SHOPLITEV - E-COMMERCE PLATFORM
================================================================================

OVERVIEW
--------
ShopLiteV is a full-stack e-commerce platform built with Django (frontend) and 
FastAPI (backend API). It features a complete shopping cart system, user 
authentication, product management, and order processing.

TECHNOLOGY STACK
----------------
- Frontend: Django 5.2.5 (Python web framework)
- Backend API: FastAPI (Python API framework)
- Database: SQLite (default), PostgreSQL (optional)
- ORM: Django ORM + SQLAlchemy
- Frontend: HTML, CSS, Bootstrap
- Python: 3.13.7

PROJECT STRUCTURE
-----------------
ShopLiteV/
├── ecommerce/              # Django project settings
├── shop/                   # Main shop app (products, orders, checkout)
├── cart/                   # Shopping cart functionality
├── accounts/               # User authentication
├── static/                 # CSS, JS, images
├── media/                  # User uploaded files
├── templates/              # HTML templates
├── main.py                 # FastAPI application
├── database.py             # Database configuration
├── schemas.py              # Pydantic models for FastAPI
├── models.py               # SQLAlchemy models
├── manage.py               # Django management script
└── db.sqlite3              # SQLite database

PREREQUISITES
-------------
1. Python 3.8 or higher
2. pip (Python package installer)
3. Git (optional, for version control)

INSTALLATION & SETUP
--------------------

1. CLONE OR DOWNLOAD THE PROJECT
   ------------------------------
   - If using Git: git clone <repository-url>
   - Or download and extract the project folder

2. NAVIGATE TO PROJECT DIRECTORY
   ------------------------------
   cd ShopLiteV

3. CREATE VIRTUAL ENVIRONMENT (RECOMMENDED)
   -----------------------------------------
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate

4. INSTALL REQUIRED PACKAGES
   -------------------------
   pip install django==5.2.5
   pip install fastapi
   pip install uvicorn
   pip install sqlalchemy
   pip install python-dotenv
   pip install pydantic

   # Optional: For PostgreSQL support
   pip install psycopg2-binary

5. SET UP ENVIRONMENT VARIABLES (OPTIONAL)
   ----------------------------------------
   Create a .env file in the project root:
   DATABASE_URL=sqlite:///./shoplite.db
   # For PostgreSQL: DATABASE_URL=postgresql://user:password@localhost/shoplite

DATABASE SETUP
--------------

1. RUN DJANGO MIGRATIONS
   ----------------------
   python manage.py makemigrations
   python manage.py migrate

2. CREATE SUPERUSER (ADMIN ACCOUNT)
   ---------------------------------
   python manage.py createsuperuser
   Follow prompts to create admin username, email, and password

3. LOAD SAMPLE DATA (OPTIONAL)
   ----------------------------
   python manage.py loaddata fixtures/sample_data.json

RUNNING THE APPLICATION
-----------------------

OPTION 1: RUN DJANGO SERVER ONLY (FRONTEND)
--------------------------------------------
python manage.py runserver
- Open browser: http://localhost:8000
- Admin panel: http://localhost:8000/admin

OPTION 2: RUN BOTH DJANGO AND FASTAPI (FULL STACK)
---------------------------------------------------
Terminal 1 (Django):
python manage.py runserver

Terminal 2 (FastAPI):
uvicorn main:app --reload
- Django: http://localhost:8000
- FastAPI: http://localhost:8001
- FastAPI Docs: http://localhost:8001/docs

USAGE INSTRUCTIONS
------------------

1. ACCESSING THE APPLICATION
   -------------------------
   - Open web browser
   - Navigate to http://localhost:8000
   - Register a new account or use admin credentials

2. BROWSING PRODUCTS
   ------------------
   - View product list on homepage
   - Click on products for detailed view
   - Use category filters if available

3. SHOPPING CART
   --------------
   - Add items to cart from product pages
   - View cart summary at /cart/summary/
   - Update quantities or remove items
   - Proceed to checkout

4. CHECKOUT PROCESS
   -----------------
   - Review cart items
   - Fill in shipping information
   - Place order
   - Receive order confirmation

5. ADMIN FUNCTIONS
   ---------------
   - Access admin panel at /admin/
   - Manage products, categories, orders
   - View user accounts and order history

API ENDPOINTS (FASTAPI)
-----------------------
- GET / - Welcome message
- GET /items - List all items
- POST /items - Create new item
- PUT /items/{item_id} - Update item
- DELETE /items/{item_id} - Delete item
- GET /orders - List all orders
- POST /orders - Create new order
- GET /sales - List all sales
- POST /sales - Create new sale

API Documentation: http://localhost:8001/docs

CONFIGURATION
-------------

1. DJANGO SETTINGS
   ---------------
   - File: ecommerce/settings.py
   - DEBUG: Set to False for production
   - ALLOWED_HOSTS: Add your domain for production
   - SECRET_KEY: Change for production

2. DATABASE CONFIGURATION
   ----------------------
   - Default: SQLite (db.sqlite3)
   - For PostgreSQL: Update DATABASE_URL in .env
   - Run migrations after database change

3. STATIC FILES
   ------------
   - Collect static files: python manage.py collectstatic
   - Static files served from /static/ directory

TROUBLESHOOTING
---------------

COMMON ISSUES:

1. "NoReverseMatch" Error
   ----------------------
   - Check URL patterns in urls.py files
   - Ensure all referenced URLs exist
   - Verify namespace usage in templates

2. Database Errors
   ---------------
   - Run migrations: python manage.py migrate
   - Check database file permissions
   - Verify DATABASE_URL configuration

3. Static Files Not Loading
   ------------------------
   - Run: python manage.py collectstatic
   - Check STATIC_URL and STATIC_ROOT settings
   - Verify file paths in templates

4. Module Import Errors
   --------------------
   - Ensure virtual environment is activated
   - Install missing packages with pip
   - Check Python path and PYTHONPATH

5. Port Already in Use
   -------------------
   - Change port: python manage.py runserver 8001
   - Kill existing process using the port
   - Check for other running Django instances

6. FastAPI Connection Issues
   -------------------------
   - Ensure FastAPI server is running
   - Check FASTAPI_BASE_URL in Django settings
   - Verify network connectivity

PERFORMANCE OPTIMIZATION
------------------------

1. PRODUCTION SETTINGS
   -------------------
   - Set DEBUG = False
   - Use production database (PostgreSQL)
   - Configure proper ALLOWED_HOSTS
   - Set up proper logging

2. STATIC FILES
   ------------
   - Use CDN for static files
   - Enable gzip compression
   - Optimize images and CSS

3. DATABASE
   ---------
   - Use database connection pooling
   - Add proper indexes
   - Regular database maintenance

DEVELOPMENT NOTES
-----------------

1. CODE STRUCTURE
   --------------
   - Django apps: shop, cart, accounts
   - Models: Product, Category, Order, OrderItem
   - Views: Product listing, cart management, checkout
   - Templates: Bootstrap-based responsive design

2. CUSTOM MANAGEMENT COMMANDS
   --------------------------
   - python manage.py manage_inventory
   - python manage.py sync_to_fastapi

3. TESTING
   --------
   - Run tests: python manage.py test
   - Test individual apps: python manage.py test shop

SUPPORT & MAINTENANCE
---------------------

1. LOGS
   ----
   - Django logs: Check console output
   - FastAPI logs: Check uvicorn output
   - Database logs: Check SQLite/PostgreSQL logs

2. BACKUP
   -------
   - Regular database backups
   - Backup media files
   - Version control for code

3. UPDATES
   --------
   - Keep dependencies updated
   - Test after updates
   - Follow Django/FastAPI release notes

CONTACT & SUPPORT
-----------------
For technical support or questions about this application, please refer to:
- Django Documentation: https://docs.djangoproject.com/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Project repository issues section

================================================================================
                            END OF README
================================================================================
