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

        print(name)
        print(data)

        content = get_content(name, data)
        file_path = get_filepath(name)
        print(content)
        
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
        print(f"서버 설정 중 오류 발생: {e}")
        return False


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


# 사전 점검 명령어들
pre_check_commands = [
    "echo '=== 서버 사전 점검 시작 ==='",
    "python3 --version",
    "python3 -m pip --version",
    "echo '=== 포트 5000 사용 중인 프로세스 확인 ==='",
    "sudo netstat -tlnp | grep :5000 || echo '포트 5000 사용 중인 프로세스 없음'",
    "echo '=== 기존 nginx 설정 확인 ==='",
    "sudo nginx -t 2>/dev/null || echo 'nginx 설정 파일 없음'",
    "echo '=== 기존 systemd 서비스 확인 ==='",
    "sudo systemctl list-units --type=service | grep flask || echo '기존 flask 서비스 없음'",
    "echo '=== 디스크 공간 확인 ==='",
    "df -h /root/",
    "echo '=== 기존 프로젝트 디렉토리 확인 ==='",
    "ls -la /root/project/ 2>/dev/null || echo '프로젝트 디렉토리 없음'",
    "echo '=== 사전 점검 완료 ==='",
]

init_commands = [
    "apt-get update",
    "apt-get install curl nginx letsencrypt certbot python3-certbot-nginx -y",
    "apt-get install python3 python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools -y",
    "apt-get install python3-venv -y",
    "apt-get install unzip",
    "mkdir -p /root/static",
    "cd /root/project && rm -rf venv && python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt",
    "cp -r /root/static /root/project/",
    "cp -r /root/white.html /root/project/templates/",
    """
cat <<EOT> /root/project/wsgi.py
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
    'systemctl daemon-reload',
    'sudo systemctl restart flask',
    'sudo service nginx restart',
]

# 서비스 검증 명령어들
verification_commands = [
    "echo '=== 서비스 상태 확인 ==='",
    "sudo systemctl status flask --no-pager",
    "echo '=== 포트 5000 리스닝 확인 ==='",
    "sudo netstat -tlnp | grep :5000",
    "echo '=== nginx 상태 확인 ==='",
    "sudo systemctl status nginx --no-pager",
    "echo '=== Flask 로그 확인 ==='",
    "sudo journalctl -u flask --no-pager -n 10",
    "echo '=== 검증 완료 ==='",
]

def server_control(domain, server, server_pass):
    server_username = 'root'
    data = {
        'domain': domain,
        'black': '',
        'black_link': '',
    }
    
    # 1단계: 사전 점검
    print("=== 1단계: 서버 사전 점검 ===")
    run_commands(server, server_username, server_pass, pre_check_commands)
    
    # 2단계: 기존 서비스 정리 (필요시)
    print("=== 2단계: 기존 서비스 정리 ===")
    cleanup_commands = [
        "sudo systemctl stop flask 2>/dev/null || echo '기존 flask 서비스 없음'",
        "sudo systemctl disable flask 2>/dev/null || echo '기존 flask 서비스 없음'",
        "sudo pkill -f 'gunicorn.*5000' 2>/dev/null || echo '기존 gunicorn 프로세스 없음'",
    ]
    run_commands(server, server_username, server_pass, cleanup_commands)
    
    # 3단계: 서버 설정
    print("=== 3단계: 서버 설정 ===")
    run_commands(server, server_username, server_pass, init_commands)
    edit_config(server, server_username, server_pass, 'nginx', data)
    edit_config(server, server_username, server_pass, 'config', data)
    run_commands(server, server_username, server_pass, project_start_commands)
    
    # 4단계: 서비스 검증
    print("=== 4단계: 서비스 검증 ===")
    run_commands(server, server_username, server_pass, verification_commands)
    
    print("성공: 세팅 완료")
