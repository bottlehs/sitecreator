import paramiko
import os



def get_content(name, data):
    domain = data["domain"] or ''
    black = data['black'] or ''
    black_link = data['black_link'] or ''
    contents = {
        "nginx": f'''
server {{
        listen 80 default_server;
        listen [::]:80 default_server;

        server_name www.{domain} {domain};
        
        location / {{
            include proxy_params;
            proxy_pass http://localhost:5000;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }}
}}
''',
        "config": f'''
[site]
SITE = {domain}
BLACK= {black}
BLACK_LIST = {black_link}
'''
    }
    return contents[name]


def get_filepath(name):
    content = {
        "nginx": "/etc/nginx/sites-enabled/default",
        "config": "/root/project/config.ini"
    }
    return content[name]


def edit_config(hostname, username, password, name, data):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname, username=username, password=password)

        content = get_content(name, data)
        file_path = get_filepath(name)
        
        # 임시 파일에 내용을 저장한 후 이동
        temp_file = f"/tmp/{name}_config"
        command = f"sudo bash -c 'cat > {temp_file} << \"EOF\"\n{content}\nEOF\nmv {temp_file} {file_path}'"

        print(command)

        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode()
        error = stderr.read().decode()

        print(f"결과: {output}")

        if error:
            print(f"에러: {error}")

        ssh.close()

    except Exception as e:
        print(f"에러: {e}")


def upload_server(local_path, remote_path, hostname, username, password, item_name=''):
    def upload_folder_recursive(local_folder_path, ec2_folder_path):
        for item in os.listdir(local_folder_path):
            local_item_path = os.path.join(local_folder_path, item)
            ec2_item_path = ec2_folder_path + '/' + item

            if os.path.isfile(local_item_path):
                sftp.put(local_item_path, ec2_item_path)
            elif os.path.isdir(local_item_path):
                try:
                    sftp.mkdir(ec2_item_path)
                except IOError:
                    pass
                upload_folder_recursive(local_item_path, ec2_item_path)

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        sftp = ssh.open_sftp()

        if os.path.isfile(local_path):
            remote_path = remote_path + '/' + item_name
            print(remote_path)
            sftp.put(local_path, remote_path)
        else:
            sftp.mkdir(remote_path + '/' + item_name)
            upload_folder_recursive(local_path, remote_path + '/' + item_name)

        sftp.close()
        ssh.close()

        return True

    except Exception as e:
        print(f"에러 ㅅㅂ: {e}")
        exit()


def run_commands(hostname, username, password, commands):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname, username=username, password=password)

        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            # print(f"{command}: {output}")

            if (error):
                print(f"ERROR!-{command}: {output}")
        ssh.close()

    except Exception as e:
        print(f"에러: {e}")


def get_folders_in_path(_path):
    folders = []
    for item in os.listdir(_path):
        if os.path.isdir(os.path.join(_path, item)):
            folders.append(item)
    return folders


init_commands = [
    "apt-get update",
    "apt-get install curl nginx letsencrypt certbot python3-certbot-nginx -y",
    "apt-get install python3 python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools -y",
    "apt-get install python3-venv -y",
    "apt-get install unzip",
    "mkdir -p /root/static",
    "cd /root/project && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt",
    "cp -r /root/static /root/project/",
    "cp -r /root/white.html /root/project/templates/",
    """
cat <<EOT> /root/project/wsgi.py
from flaskapp import app

if __name__ == "__main__":
    app.run()
EOT
    """,
    """
    cat <<EOT> /etc/systemd/system/flask.service
[Unit]
Description=Gunicorn instance to serve Flask
After=network.target
[Service]
User=root
Group=www-data
WorkingDirectory=/root/project
Environment="PATH=/root/project/venv/bin"
ExecStart=/root/project/venv/bin/gunicorn --bind 0.0.0.0:5000 --pythonpath /root/project wsgi:app
[Install]
WantedBy=multi-user.target
EOT
""",
    "chown -R root:www-data /root/project",
    "chmod -R 775 /root/project",
    "systemctl daemon-reload",
    "systemctl start flask",
    "systemctl enable flask",
    "sudo ufw allow 'Nginx HTTP'",
    "sudo ufw allow ssh",
    "sudo ufw allow 'Nginx Full'",
]

project_start_commands = [
    'sudo systemctl restart flask',
]

def black_server_control(domain, links,  server, server_pass):
    server_username = 'root'
    data = {
        'domain': domain,
        'black': '',
        'black_link': links,
    }
    edit_config(server, server_username, server_pass, 'config', data)
    run_commands(server, server_username, server_pass, project_start_commands)
    print("성공: 세팅 완료")