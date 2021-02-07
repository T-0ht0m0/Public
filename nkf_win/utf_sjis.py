import subprocess
import time

print("文字化けするファイルを入れてください")
print("ドラッグ&ドロップしてください")
path = input().rstrip()
p = subprocess.Popen(["nkf", "-g", path],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in iter(p.stdout.readline, b""):
    line_str = str(line.rstrip()).lstrip("b")
    print("現在の文字コード：", line_str)
if line_str == "\'UTF-8\'":
    print("\'Shift_JIS\'に変換します")
    ans = 1
elif line_str == "\'Shift_JIS\'":
    print("\'UTF-8\'に変換します")
    ans = 2
else:
    print(f"現在の文字コードは{line_str}です")
    print("操作を選んでください\n")
    print("1: \'Shift_JIS\'に変換します（Windows向け）")
    print("2: \'UTF-8\'に変換します（Mac, Linux向け）")
    print("3: 終了")
    ans = 0
    while ans not in {1, 2, 3}:
        print("1,2,3 から選んでください")
        try:
            ans = int(input())
        except:
            # print("goodbye")
            ans = 0
if ans == 1:
    subprocess.Popen(["nkf", "-s", "--overwrite", path],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
elif ans == 2:
    subprocess.Popen(["nkf", "-w", "--overwrite", path],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
else:
    pass

if ans != 3:
    print("変換しました")
t = 5
for i in range(t):
    print("\r"+str(t-i)+"秒後、自動的に終了します", end="")
    time.sleep(1)
