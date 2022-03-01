import os
from tabnanny import check
from turtle import update
from github import Github

from database import DB
from automation import Automation

class VersionUpdate:
    def __init__(self):
        with open(r"D:\Master\PythonWorkspace\NYNOA\git_token.txt", "r") as git_file:
            self.git_token = git_file.readline()

    def checkVersion(self):
        print("업데이트를 확인합니다.")
        # os.system() 으로 cmd에서 디렉토리 이동을 해도 이동이 되지 않았다. -> os.chdir() 함수를 통해 이동하니 이동됨.
        # os.system("D:")
        # os.system("cd D:\\Master\\PythonWorkspace\\NYNOA")
        os.chdir("D:\\Master\\PythonWorkspace\\NYNOA")
        # res = os.system("git log -1 --pretty=format:'%s'")    # return value: 0 -> 정상작동
        cur_version = os.popen("git log -1 --pretty=format:'%s'").read().strip("'")  # 변수 담기

        try:
            g = Github(self.git_token)        
            repo = g.get_repo("dldudals0728/operate_automation")
            branch = repo.get_branch("main")
        except:
            print("git token 이 최신상태가 아닙니다. 관리자에게 문의해주세요!")
            return

        update_version = branch.commit.commit.message
        if cur_version == update_version:
            print("현재 프로그램이 최신상태 입니다.")

        else:
            print("업데이트 내역이 존재합니다.")
        
        print(cur_version)
        print(update_version)


if __name__ == "__main__":
    checker = VersionUpdate()
    checker.checkVersion()