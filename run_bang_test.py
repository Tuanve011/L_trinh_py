import sys
import io
import os
import subprocess
import importlib.util
import math

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

EXAMS = {
    "de1": (os.environ.get("DE1_FOLDER", "De1_BaiLam"), "bang_test_de1.py"),
    "de2": (os.environ.get("DE2_FOLDER", "De2_BaiLam"), "bang_test_de2.py"),
}

def load_tests(path):
    spec = importlib.util.spec_from_file_location("bang_" + os.path.basename(path), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.tests

def run_program(path, text):
    r = subprocess.run([sys.executable, "-X", "utf8", path], input=text, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10)
    return r.returncode, r.stdout, r.stderr

def run_exam(key):
    folder, table = EXAMS[key]
    tests = load_tests(os.path.join(HERE, table))
    print(f"=== {key.upper()} ({folder}) ===")
    
    scores = {}
    for cau, cases in tests.items():
        path = os.path.join(ROOT, folder, cau.lower() + ".py")
        ok = 0
        for i, case in enumerate(cases, 1):
            try:
                code, out, err = run_program(path, case["input"])
                missing = [exp for exp in case.get("expected", []) if exp not in out]
                
                # Check approximate floats if specified
                approx_ok = True
                for prefix, value in case.get("approx", []):
                    found = None
                    for line in out.splitlines():
                        if prefix in line:
                            tail = line.rsplit(prefix, 1)[1].strip()
                            try:
                                found = float(tail)
                            except ValueError:
                                found = None
                            break
                    if found is None or not math.isclose(found, value, rel_tol=1e-5, abs_tol=1e-5):
                        approx_ok = False
                        break

                if code == 0 and not missing and approx_ok:
                    ok += 1
            except Exception:
                pass
        
        score_per_case = 2.0 / len(cases) if len(cases) > 0 else 0
        cau_score = round(ok * score_per_case, 2)
        scores[cau] = (cau_score, ok, len(cases))
        print(f"  {cau}: {ok}/{len(cases)} test cases passed -> Điểm: {cau_score}/2.0")
    
    total_exam_score = round(sum(s[0] for s in scores.values()), 2)
    print(f"  ==> TỔNG ĐIỂM {key.upper()}: {total_exam_score}/10.0\n")
    return scores, total_exam_score

def main():
    for k in EXAMS:
        run_exam(k)

if __name__ == "__main__":
    main()
