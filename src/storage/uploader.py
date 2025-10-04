import paramiko
import boto3
import logging

def upload_scp(local_path, remote_config):
    ssh = paramiko.Transport((remote_config["host"], 22))
    ssh.connect(username=remote_config["user"])
    sftp = paramiko.SFTPClient.from_transport(ssh)
    sftp.put(local_path, remote_config["path"] + local_path.split("/")[-1])
    sftp.close()
    ssh.close()
    logging.info(f"Uploaded {local_path} to {remote_config['host']}")

def upload_s3(local_path, aws_config):
    s3 = boto3.client("s3", region_name=aws_config["region"])
    s3.upload_file(local_path, aws_config["bucket"], local_path.split("/")[-1])
    logging.info(f"Uploaded {local_path} to S3 bucket {aws_config['bucket']}")
