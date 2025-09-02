#!/usr/bin/env python
"""
Setup script for Shahin Auto Service Django project
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_mysql():
    """Check if MySQL is available"""
    try:
        result = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MySQL detected")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  MySQL not found. Please install MySQL 8.0+")
    return False

def create_env_file():
    """Create .env file from example"""
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            with open('env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✅ .env file created from example")
        else:
            print("⚠️  env.example not found, creating basic .env file")
            with open('.env', 'w') as f:
                f.write("SECRET_KEY=your-secret-key-here\nDEBUG=True\n")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up Shahin Auto Service Django Project")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check MySQL
    check_mysql()
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists('venv'):
        if not run_command('python -m venv venv', 'Creating virtual environment'):
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists")
    
    # Activate virtual environment and install requirements
    if os.name == 'nt':  # Windows
        activate_cmd = 'venv\\Scripts\\activate'
        pip_cmd = 'venv\\Scripts\\pip'
    else:  # Unix/Linux/Mac
        activate_cmd = 'source venv/bin/activate'
        pip_cmd = 'venv/bin/pip'
    
    if not run_command(f'{pip_cmd} install --upgrade pip', 'Upgrading pip'):
        sys.exit(1)
    
    if not run_command(f'{pip_cmd} install -r requirements.txt', 'Installing requirements'):
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Create necessary directories
    directories = ['media', 'media/lectures', 'media/services', 'media/site', 'staticfiles']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Created necessary directories")
    
    # Run Django commands
    django_cmd = 'venv\\Scripts\\python' if os.name == 'nt' else 'venv/bin/python'
    
    if not run_command(f'{django_cmd} manage.py makemigrations', 'Creating migrations'):
        print("⚠️  Migrations creation failed, continuing...")
    
    if not run_command(f'{django_cmd} manage.py migrate', 'Running migrations'):
        print("⚠️  Migrations failed, please check your database settings")
    
    if not run_command(f'{django_cmd} manage.py create_sample_data', 'Creating sample data'):
        print("⚠️  Sample data creation failed, continuing...")
    
    if not run_command(f'{django_cmd} manage.py collectstatic --noinput', 'Collecting static files'):
        print("⚠️  Static files collection failed, continuing...")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your database credentials")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Run the server: python manage.py runserver")
    print("4. Visit http://localhost:8000")
    print("\n🔧 Admin access:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n📚 For more information, see README.md")

if __name__ == '__main__':
    main()
