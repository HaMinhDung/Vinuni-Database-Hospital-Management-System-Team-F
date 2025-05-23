Bước 0: cd be
Bước 1: Tải Requirement (lỗi thì tải tiếp, thêm thư viện vào requirement)
Bước 2: Chạy db vào MySql
Bước 3: kết nối MySQL: ./db/Connection.py: điền mật khẩu, tài khoản vô

Kết nối xong check bằng main.py: test các chức năng như admin
login.py: đăng nhập (tài khoản mật khẩu check bảng User), đăng nhập bằng các role khác nhau (Doctor/Patient): test các chức năng của User
p_sign_up: Test chức năng tạo user, hồ sơ bệnh nhân mới, không có bác sĩ vì bác sĩ sẽ do thằng admin thêm

Bước 4: python server.py, kết nối với server frontend

Note: trong frontend.tsx là check nếu là bác sĩ, bệnh nhân bằng cách check row trong bảng userProfile, nếu có thông tin bên cột nào thì là doctor/patient, nếu cả 2 là null là admin

