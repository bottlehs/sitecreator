#!/usr/bin/env python3
"""
서버 사전 점검 모듈
서버 설정 전에 필요한 사전 점검을 수행합니다.
"""

import paramiko
import re
import platform

def run_check_commands(hostname, username, password, commands):
    """점검 명령어들을 실행하고 결과를 반환"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        
        results = {}
        
        for command in commands:
            print(f"실행 중: {command}")
            stdin, stdout, stderr = ssh.exec_command(command)
            
            # 명령어 실행 완료 대기
            exit_status = stdout.channel.recv_exit_status()
            
            output = stdout.read().decode('utf-8', errors='ignore').strip()
            error = stderr.read().decode('utf-8', errors='ignore').strip()
            
            print(f"결과: {output}")
            if error:
                print(f"오류: {error}")
            
            results[command] = {
                'output': output,
                'error': error,
                'success': exit_status == 0,
                'exit_status': exit_status
            }
        
        ssh.close()
        return results
        
    except Exception as e:
        print(f"SSH 연결 오류: {e}")
        return {'error': str(e)}

def check_server_status(server_ip, server_password):
    """서버 상태 점검"""
    server_username = 'root'
    
    # 점검 명령어들
    check_commands = [
        'python3 --version',
        'python3 -m pip --version',
        'sudo netstat -tlnp | grep :5000 || echo "포트 5000 사용 중인 프로세스 없음"',
        'sudo systemctl list-units --type=service | grep flask || echo "기존 flask 서비스 없음"',
        'sudo nginx -t 2>/dev/null || echo "nginx 설정 파일 없음"',
        'df -h /root/ | tail -1',
        'free -h | grep Mem',
        'ls -la /root/project/ 2>/dev/null || echo "프로젝트 디렉토리 없음"',
        'sudo ufw status || echo "UFW 설정 없음"'
    ]
    
    print("=== 서버 사전 점검 시작 ===")
    print(f"로컬 OS: {platform.system()} {platform.release()}")
    print(f"서버: {server_ip}")
    print(f"사용자: {server_username}")
    
    results = run_check_commands(server_ip, server_username, server_password, check_commands)
    
    if 'error' in results:
        return False, f"SSH 연결 오류: {results['error']}"
    
    print("=== 점검 결과 분석 시작 ===")
    for i, cmd in enumerate(check_commands):
        result = results.get(cmd, {})
        print(f"명령어 {i+1}: {cmd}")
        print(f"  출력: {result.get('output', '')}")
        print(f"  오류: {result.get('error', '')}")
        print(f"  성공: {result.get('success', False)}")
        print("---")
    
    # 점검 결과 분석
    issues = []
    warnings = []
    
    # Python 버전 확인 (첫 번째 명령어)
    python_cmd = check_commands[0]  # 'python3 --version'
    python_result = results.get(python_cmd, {})
    python_output = python_result.get('output', '')
    python_success = python_result.get('success', False)
    
    print(f"Python 점검 결과: {python_output}")
    print(f"Python 실행 성공: {python_success}")
    
    if python_success and python_output:
        if 'Python 3' in python_output or 'Python' in python_output:
            version_match = re.search(r'Python (\d+)\.(\d+)', python_output)
            if version_match:
                major, minor = int(version_match.group(1)), int(version_match.group(2))
                if major < 3 or (major == 3 and minor < 6):
                    issues.append(f"Python 버전이 너무 낮습니다: {python_output}")
                else:
                    print(f"✅ Python 버전: {python_output}")
            else:
                print(f"✅ Python 설치됨: {python_output}")
        else:
            issues.append(f"Python 버전을 확인할 수 없습니다: {python_output}")
    else:
        error_msg = python_result.get('error', '')
        if error_msg:
            issues.append(f"Python 실행 오류: {error_msg}")
        else:
            issues.append("Python3가 설치되어 있지 않거나 실행할 수 없습니다")
    
    # 포트 5000 사용 확인 (세 번째 명령어)
    port_cmd = check_commands[2]
    port_output = results.get(port_cmd, {}).get('output', '')
    if '포트 5000 사용 중인 프로세스 없음' not in port_output and port_output.strip():
        warnings.append(f"포트 5000이 이미 사용 중입니다: {port_output}")
    else:
        print("✅ 포트 5000 사용 가능")
    
    # 기존 Flask 서비스 확인 (네 번째 명령어)
    flask_cmd = check_commands[3]
    flask_output = results.get(flask_cmd, {}).get('output', '')
    if '기존 flask 서비스 없음' not in flask_output and flask_output.strip():
        warnings.append(f"기존 Flask 서비스가 있습니다: {flask_output}")
    else:
        print("✅ 기존 Flask 서비스 없음")
    
    # 디스크 공간 확인 (여섯 번째 명령어)
    disk_cmd = check_commands[5]
    disk_output = results.get(disk_cmd, {}).get('output', '')
    if disk_output:
        # 디스크 사용률 추출 (예: "80%")
        usage_match = re.search(r'(\d+)%', disk_output)
        if usage_match:
            usage = int(usage_match.group(1))
            if usage > 90:
                issues.append(f"디스크 공간이 부족합니다: {disk_output}")
            elif usage > 80:
                warnings.append(f"디스크 공간이 부족할 수 있습니다: {disk_output}")
            else:
                print(f"✅ 디스크 공간: {disk_output}")
    
    # 메모리 확인 (일곱 번째 명령어)
    memory_cmd = check_commands[6]
    memory_output = results.get(memory_cmd, {}).get('output', '')
    if memory_output:
        print(f"✅ 메모리 상태: {memory_output}")
    
    # nginx 상태 확인 (다섯 번째 명령어)
    nginx_cmd = check_commands[4]
    nginx_output = results.get(nginx_cmd, {}).get('output', '')
    if 'nginx 설정 파일 없음' not in nginx_output and nginx_output.strip():
        if 'syntax is ok' in nginx_output.lower():
            print("✅ nginx 설정 정상")
        else:
            warnings.append(f"nginx 설정에 문제가 있을 수 있습니다: {nginx_output}")
    else:
        print("✅ nginx 설정 파일 없음 (새로 설치됨)")
    
    # UFW 상태 확인 (아홉 번째 명령어)
    ufw_cmd = check_commands[8]
    ufw_output = results.get(ufw_cmd, {}).get('output', '')
    if ufw_output and 'UFW 설정 없음' not in ufw_output:
        print(f"✅ UFW 상태: {ufw_output}")
    
    # 결과 요약
    if issues:
        error_msg = "❌ 심각한 문제 발견:\n" + "\n".join(f"• {issue}" for issue in issues)
        if warnings:
            error_msg += "\n\n⚠️ 경고사항:\n" + "\n".join(f"• {warning}" for warning in warnings)
        return False, error_msg
    
    if warnings:
        warning_msg = "⚠️ 경고사항이 있습니다:\n" + "\n".join(f"• {warning}" for warning in warnings)
        warning_msg += "\n\n계속 진행하시겠습니까?"
        return True, warning_msg
    
    success_msg = "✅ 모든 점검 항목이 정상입니다!\n\n점검 결과:\n"
    success_msg += f"• Python: {python_output}\n"
    success_msg += f"• 포트 5000: 사용 가능\n"
    success_msg += f"• 디스크: {disk_output}\n"
    success_msg += f"• 메모리: {memory_output}\n"
    success_msg += "• 기존 서비스: 충돌 없음"
    
    return True, success_msg

def auto_cleanup_server(server_ip, server_password):
    """서버 자동 정리"""
    server_username = 'root'
    
    cleanup_commands = [
        "sudo systemctl stop flask 2>/dev/null || echo '기존 flask 서비스 없음'",
        "sudo systemctl disable flask 2>/dev/null || echo '기존 flask 서비스 없음'",
        "sudo pkill -f 'gunicorn.*5000' 2>/dev/null || echo '기존 gunicorn 프로세스 없음'",
        "echo '서버 정리 완료'"
    ]
    
    print("=== 서버 자동 정리 시작 ===")
    results = run_check_commands(server_ip, server_username, server_password, cleanup_commands)
    
    if 'error' in results:
        return False, f"서버 정리 중 오류: {results['error']}"
    
    print("✅ 서버 정리 완료")
    return True, "서버 정리가 완료되었습니다."

if __name__ == "__main__":
    # 테스트용
    print("서버 점검 모듈 테스트")
