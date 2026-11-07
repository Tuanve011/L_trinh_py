# Câu 1 - Đề 2


def TongUocSo(n):
    """Tổng tất cả các ước số của n."""
    tong = 0
    for i in range(1, n + 1):
        if n % i == 0:
            tong += i
    return tong


def S(n):
    """S = 1 + 2^2 + 3^3 + ... + n^n"""
    s = 0
    for i in range(1, n + 1):
        s = s + (i ** i)
    return s


# a. Nhập n, nếu ngoài đoạn [1;99] thì nhập lại
n = int(input("Nhập giá trị 1<=n<=99: "))
while n < 1 or n > 99:
    n = int(input("Nhập lại giá trị 1<=n<=99: "))

# b.
print("Tổng các ước số là:", TongUocSo(n))

# c.
print("S =", S(n))
