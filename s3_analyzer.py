import hashlib
import boto3
import os

def compute_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def store_file_hash_locally(file_key, hash_value):
    hash_dir = os.path.join(os.path.dirname(__file__), '..', 'hashes')
    if not os.path.exists(hash_dir):
        os.makedirs(hash_dir)
    
    hash_file_path = os.path.join(hash_dir, f'{file_key}.hash')
    with open(hash_file_path, 'w') as hash_file:
        hash_file.write(hash_value)

def read_stored_hash(file_key):
    hash_file_path = f'hashes/{file_key}.hash'
    with open(hash_file_path, 'r') as hash_file:
        return hash_file.read().strip()

def upload_file_to_s3(bucket_name, file_path, file_key):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, file_key)

def download_file_from_s3(bucket_name, file_key, download_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, file_key, download_path)

def check_file_corruption(bucket_name, file_key, original_hash):
    download_path = f'{file_key}'
    download_file_from_s3(bucket_name, file_key, download_path)
    
    computed_hash = compute_file_hash(download_path)
    return computed_hash == original_hash

def analyze_s3_file(bucket_name, file_path, file_key):
    # Step 1: Compute hash of the local file
    original_hash = compute_file_hash(file_path)
    store_file_hash_locally(file_key, original_hash)
    
    # Step 2: Upload the file to S3
    upload_file_to_s3(bucket_name, file_path, file_key)
    
    # Step 3: Check file corruption
    if not check_file_corruption(bucket_name, file_key, original_hash):
        return False  # Bad file
    return True  # Good file
