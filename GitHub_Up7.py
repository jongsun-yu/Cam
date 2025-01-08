from github import Github

# GitHub 토큰으로 로그인
g = Github("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")

# 저장소 및 파일 정보 설정
repo_name = "jongsun-yu/Cam"
file_path = "a01.jpg"
commit_message = "2025년01월08일 수요일"
branch = "main"
file_name_in_repo = "a01.jpg"

# 파일 열기 및 바이너리 데이터 읽기
with open(file_path, "rb") as file:
    content = file.read()

# 저장소 가져오기
repo = g.get_repo(repo_name)

try:
    # 파일이 존재하는지 확인하고 덮어쓰기
    contents = repo.get_contents(file_name_in_repo, ref=branch)
    sha = contents.sha
    repo.update_file(
        path=file_name_in_repo,
        message=commit_message,
        content=content,
        sha=sha,
        branch=branch
    )
    print("파일 덮어쓰기 완료")
except Exception as e:
    if "404" in str(e):
        # 파일이 존재하지 않으면 새 파일 생성
        repo.create_file(
            path=file_name_in_repo,
            message=commit_message,
            content=content,
            branch=branch
        )
        print("새 파일 생성 완료")
    else:
        print(f"오류 발생: {e}")
