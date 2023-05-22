# CloudOffice


설치 필요 라이브러리 목록

- pip install comtypes
- pip install reportlab



알아서 작업하고 변동하항 확실하게 작성할 것






5.6 bjpark21 : 회원가입, 로그인 작업


1.authentication - forms.py 수정 (Emp-models.py 맞춰서)

2.회원가입 시스템 변경

  -회원가입 후 로그인 바로 안되게 설정
  
  -관리자가 관리자 페이지에서 권한부여하면 로그인이 가능하게
  
3.관리자 페이지(http://127.0.0.1:8000/admin/)

  -로그인 후 회원가입한 아이디 권한 변경

4. gitignore 추가
   
   - 이후 최초 커밋 시 superuser(admin) 계정 새로 만들어야 함
   - admin 페이지에서 admin 계정 정보 포함하는 Employee 객체 생성해둘 것
