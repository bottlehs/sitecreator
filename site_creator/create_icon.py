#!/usr/bin/env python3
"""
Windows용 ICO 아이콘 파일 생성 스크립트
PIL을 사용하여 간단한 아이콘 생성
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("❌ PIL(Pillow) 라이브러리가 필요합니다.")
    print("💡 pip install Pillow로 설치해주세요.")
    exit(1)

def create_simple_icon():
    """간단한 아이콘 생성"""
    # 256x256 크기의 아이콘 생성
    size = 256
    icon = Image.new('RGBA', (size, size), (0, 120, 215, 255))  # Windows 블루
    
    # 그리기 객체 생성
    draw = ImageDraw.Draw(icon)
    
    # 중앙에 "SC" 텍스트 그리기
    try:
        # 폰트 크기 계산
        font_size = size // 4
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # 폰트를 찾을 수 없으면 기본 폰트 사용
        font = ImageFont.load_default()
    
    # 텍스트 크기 계산
    text = "SC"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 텍스트를 중앙에 배치
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # 흰색 텍스트 그리기
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # 원형 테두리 그리기
    draw.ellipse([10, 10, size-10, size-10], outline=(255, 255, 255, 255), width=5)
    
    return icon

def save_ico(icon, filename="icon.ico"):
    """ICO 파일로 저장"""
    # 여러 크기로 리사이즈
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    resized_icons = []
    
    for size in sizes:
        resized = icon.resize(size, Image.Resampling.LANCZOS)
        resized_icons.append(resized)
    
    # ICO 파일로 저장
    resized_icons[0].save(filename, format='ICO', sizes=[(icon.width, icon.height) for icon in resized_icons])
    print(f"✅ 아이콘 파일 생성 완료: {filename}")

def main():
    """메인 함수"""
    print("🎨 Windows용 ICO 아이콘 생성기")
    print("=" * 40)
    
    try:
        # 아이콘 생성
        print("🔧 아이콘 생성 중...")
        icon = create_simple_icon()
        
        # ICO 파일로 저장
        print("💾 ICO 파일로 저장 중...")
        save_ico(icon)
        
        print("\n🎉 아이콘 생성이 완료되었습니다!")
        print("💡 이제 build_windows_only.py를 실행하여 EXE 파일을 생성할 수 있습니다.")
        
    except Exception as e:
        print(f"❌ 아이콘 생성 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
