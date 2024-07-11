from s3_analyzer import analyze_s3_file
from traffic_monitor import check_server_capacity
from alarm_service import send_alarm

BUCKET_NAME = 'ibm-storage-bucket'
FILE_PATH = '../files/sample-file.txt'
FILE_KEY = 'sample-file'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:992382716502:ibm-topic'

def main():
    if analyze_s3_file(BUCKET_NAME, FILE_PATH, FILE_KEY):
        send_alarm('File Upload and Integrity Check',
                   f'The file {FILE_KEY} has been uploaded and integrity check passed.',
                   SNS_TOPIC_ARN)
    else:
        send_alarm('File Corruption/Vulnerability Detected',
                   f'The file {FILE_KEY} is corrupted or vulnerable.',
                   SNS_TOPIC_ARN)

    if not check_server_capacity():
        send_alarm('Server Capacity Alert',
                   'Server capacity has reached 75%. Consider scaling up.',
                   SNS_TOPIC_ARN)

if __name__ == '__main__':
    main()
