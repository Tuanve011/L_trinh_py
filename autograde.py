import sys
import io
import os
import subprocess

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def main():
    print("==================================================")
    print("          BẮT ĐẦU CHẤM BÀI TỰ ĐỘNG (AUTOGRADE)      ")
    print("==================================================\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    run_bang_script = os.path.join(base_dir, 'test_de', 'run_bang_test.py')

    if os.path.exists(run_bang_script):
        res = subprocess.run([sys.executable, run_bang_script], cwd=base_dir, capture_output=True, text=True, encoding='utf-8', errors='replace')
        print(res.stdout)
        if res.stderr:
            print("Chi tiết cảnh báo:", res.stderr)

    print("==================================================")
    print("              ĐÃ HOÀN THÀNH AUTOGRADE             ")
    print("==================================================")

if __name__ == '__main__':
    main()
