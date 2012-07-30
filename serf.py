import boto.ec2
import requests
import time
import ssh

AWS_ACCESS_KEY_ID = "AKIAIZHHHKUHKBOUIJKA"
AWS_SECRET_ACCESS_KEY = "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"
AMI_IMAGE_ID = "ami-606ee150"
AWS_KEY_PAIR_NAME = "ec2"
AWS_SECURITY_GROUP_ID = "sg-aa8b1a9a"
KING_URL = "http://localhost:5000"
KEY_FILE = "/home/nick/Downloads/ec2.pem"

conn = None

def create(id, username, region='us-west-2'):
    make_connection(region)
    instance = create_instance(id, username)
    if instance is None:
        print "Something failed!"
        return

    resp = create_new_user(id, username, instance.public_dns_name)
    
    if resp is False:
        terminate_instance(instance.id)
        status = 'errored'
    else:
        stop_instance(id, username, instance.id)
        status = 'completed'
        
    payload = {
            'id': id,
            'username': username,
            'instance': instance.id,
            'dns_name': instance.public_dns_name,
            'state': status,
    }

    try:
        requests.post(KING_URL+"/command/"+str(id), data=payload)
    except Exception as e:
        print e
        print payload


def make_connection(region):
    regions = boto.ec2.regions(aws_access_key_id=AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    for r in regions:
        if region in r.name:
            global conn
            conn = r.connect(aws_access_key_id=AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            break
    else:
        print "No matching region found"
        return

    return conn


def create_instance():
    reservation = conn.run_instances(AMI_IMAGE_ID, key_name=AWS_KEY_PAIR_NAME,
            security_group_ids=[AWS_SECURITY_GROUP_ID],
            instance_type='t1.micro')

    instance = reservation.instances[0]

    while instance.state != 'running':
        print 'Waiting on instance start...'
        time.sleep(10)
        instance.update()
    
    time.sleep(90)
    
    return instance


def stop_instance(instance_id):
    conn.stop_instances([instance_id])

    while instance.state != 'stoppped':
        print 'Waiting on instance stop...'
        time.sleep(10)
        instance.update()


def terminate_instance(instance_id):
    conn.terminate_instances([instance_id])

    while instance.state != 'terminated':
        print 'Waiting on instance termination...'
        time.sleep(10)
        instance.update()


def create_new_user(username, url):
    client = ssh.SSHClient()
    privkey = ssh.RSAKey.from_private_key_file(KEY_FILE)
    client.set_missing_host_key_policy(ssh.AutoAddPolicy())

    try:
        client.connect(url, username='ubuntu', pkey=privkey)
        print "Connected!"
        exec_string = 'casperjs --name=%s /opt/two-face/troublemaker.js' % username
        stdin, stdout, stderr = client.exec_command(exec_string)

        print stdout.read()
        print stderr.read()
        return True
    
    except Exception as e:
        print e
        return False
