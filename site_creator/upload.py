import paramiko
import os


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
            
            # 원격 디렉토리가 존재하지 않으면 생성
            remote_dir = os.path.dirname(remote_path)
            if remote_dir and remote_dir != '/':
                try:
                    sftp.mkdir(remote_dir)
                    print(f"📁 원격 디렉토리 생성: {remote_dir}")
                except:
                    pass  # 이미 존재하면 무시
            
            sftp.put(local_path, remote_path)
        else:
            # 기존 디렉토리가 있으면 SSH로 삭제
            try:
                stdin, stdout, stderr = ssh.exec_command(f'rm -rf {remote_path}/{item_name}')
                stdout.read()  # 명령 완료 대기
                print(f"🗑️ 기존 디렉토리 삭제: {remote_path}/{item_name}")
            except:
                pass  # 삭제 실패해도 계속 진행
            
            # 새 디렉토리 생성
            sftp.mkdir(remote_path + '/' + item_name)
            upload_folder_recursive(local_path, remote_path + '/' + item_name)

        sftp.close()
        ssh.close()

        return True

    except Exception as e:
        import traceback
        print(f"❌ 업로드 중 오류 발생: {e}")
        print(f"📁 로컬 경로: {local_path}")
        print(f"📁 원격 경로: {remote_path}")
        print(f"🌐 서버: {hostname}")
        print(f"🔍 상세 오류 정보:")
        traceback.print_exc()
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



def upload(path, domain, server, server_pass):
    project = os.path.join(os.getcwd(), 'page_default')
    server_path = '/root'
    server_username = 'root'
    
    print(f"📁 템플릿 경로: {path}")
    print(f"📁 프로젝트 경로: {project}")
    
    if len(path) and len(domain) and len(server) and len(server_pass):
        # 필요한 파일들 확인
        white_html_path = os.path.join(path, 'white.html')
        static_path = os.path.join(path, 'static')
        static_zip_path = os.path.join(path, 'static.zip')
        
        print(f"📄 white.html 존재: {os.path.exists(white_html_path)}")
        print(f"📁 static 폴더 존재: {os.path.exists(static_path)}")
        print(f"📦 static.zip 존재: {os.path.exists(static_zip_path)}")
        print(f"📁 page_default 존재: {os.path.exists(project)}")
        
        if (os.path.exists(project) and os.path.exists(white_html_path)):
            print("🚀 프로젝트 업로드 시작...")
            print(f"📤 업로드 대상: {project} -> {server_path}/project")
            upload_result = upload_server(project, server_path, server, server_username, server_pass, 'project')

            if upload_result is True:
                print("📄 white.html 업로드 시작...")
                print(f"📤 업로드 대상: {white_html_path} -> {server_path}/project/templates/white.html")
                upload_result2 = upload_server(white_html_path, f"{server_path}/project/templates", server, server_username, server_pass, 'white.html')
                
                if upload_result2:
                    # static.zip이 있으면 업로드, 없으면 static 폴더를 zip으로 만들어서 업로드
                    if os.path.exists(static_zip_path):
                        print("📦 static.zip 업로드 및 압축 해제 시작...")
                        print(f"📤 업로드 대상: {static_zip_path} -> {server_path}/project/static.zip")
                        upload_result3 = upload_server(static_zip_path, f"{server_path}/project", server, server_username, server_pass, 'static.zip')
                        if upload_result3:
                            print("📁 static.zip 압축 해제 중...")
                            # 기존 SSH 연결을 사용하여 압축 해제
                            try:
                                import paramiko
                                ssh_temp = paramiko.SSHClient()
                                ssh_temp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                ssh_temp.connect(server, username=server_username, password=server_pass)
                                stdin, stdout, stderr = ssh_temp.exec_command(f'cd {server_path}/project && unzip -o static.zip -d static/ && rm static.zip')
                                stdout.read()  # 명령 완료 대기
                                ssh_temp.close()
                                print("✅ static.zip 압축 해제 완료")
                            except Exception as e:
                                print(f"⚠️ 압축 해제 중 오류: {e}")
                    elif os.path.exists(static_path):
                        print("📁 static 폴더를 zip으로 압축 후 업로드...")
                        import shutil
                        zip_path = os.path.join(path, 'static.zip')
                        shutil.make_archive(os.path.join(path, 'static'), 'zip', static_path)
                        print(f"📤 업로드 대상: {zip_path} -> {server_path}/project/static.zip")
                        upload_result3 = upload_server(zip_path, f"{server_path}/project", server, server_username, server_pass, 'static.zip')
                        if upload_result3:
                            print("📁 static.zip 압축 해제 중...")
                            # 기존 SSH 연결을 사용하여 압축 해제
                            try:
                                import paramiko
                                ssh_temp = paramiko.SSHClient()
                                ssh_temp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                ssh_temp.connect(server, username=server_username, password=server_pass)
                                stdin, stdout, stderr = ssh_temp.exec_command(f'cd {server_path}/project && unzip -o static.zip -d static/ && rm static.zip')
                                stdout.read()  # 명령 완료 대기
                                ssh_temp.close()
                                print("✅ static.zip 압축 해제 완료")
                            except Exception as e:
                                print(f"⚠️ 압축 해제 중 오류: {e}")
                    else:
                        print("⚠️ static 폴더가 없어서 static.zip 업로드를 건너뜁니다.")
                        upload_result3 = True
                    
                    if upload_result3:
                        print("✅ 업로드 성공")
                    else:
                        print("❌ static.zip 업로드 실패")
                else:
                    print("❌ white.html 업로드 실패")
            else:
                print("❌ 프로젝트 업로드 실패")
        else:
            missing_files = []
            if not os.path.exists(project):
                missing_files.append("page_default 폴더")
            if not os.path.exists(white_html_path):
                missing_files.append("white.html 파일")
            
            print(f"❌ 필요한 파일이 없습니다: {', '.join(missing_files)}")
            print("💡 해결 방법: 먼저 '폴더 정리' 버튼을 클릭하세요.")
    else:
        print("❌ 입력값 확인 필요 (도메인, 서버 IP, 비밀번호)")