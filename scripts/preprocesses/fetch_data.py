from ftplib import FTP
import os
import dotenv

dotenv.load_dotenv()  # Load environment variables from .env file

HOST = os.getenv('FTP_HOST', "")
USER = os.getenv('FTP_USER', "")
PASS = os.getenv('FTP_PASS', "")

LOCAL_DIR = os.getenv('LOCAL_DIR', 'data/raw/')
REMOTE_DIR = os.getenv('REMOTE_DIR', '/csv')

PREFIX = {
    'CRMLSListing',
    'CRMLSSold'
}

os.makedirs(LOCAL_DIR, exist_ok=True)

ftp = FTP(HOST)
ftp.login(USER, PASS)
ftp.cwd(REMOTE_DIR)

filenames = ftp.nlst()

print(f"Found {len(filenames)} items")

for filename in filenames:
    if filename.endswith('.csv') and any(filename.startswith(prefix) for prefix in PREFIX):
        local_path = os.path.join(LOCAL_DIR, filename)
        try:
            with open(local_path, 'wb') as f:
                ftp.retrbinary(f'RETR {filename}', f.write)
            print(f"Downloaded: {filename}")
        except Exception as e:
            if os.path.exists(local_path):
                os.remove(local_path)
            print(f"Skipped {filename}: {e}")

ftp.quit()