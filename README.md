
# Website chơi cờ
Đây là một dự án mã nguồn mở cung cấp một ứng dụng chơi cờ vua trực tuyến. Dự án này sử dụng FastAPI, socket cho phía máy chủ và React cho phía giao diện.






## Tính năng

- Chơi cờ với máy: Người chơi có thể chọn chơi với máy với 3 mức độ dễ, khó, trung bình.
- Tạo phòng: Người chơi có thể tạo một phòng riêng để chơi cờ với bạn bè.
- Tham gia phòng: Người chơi có thể tham gia vào một phòng đã tồn tại để chơi cờ với người khác.
- Chat trong game: Người chơi có thể gửi tin nhắn cho đối thủ trong quá trình chơi.

## Cài đặt 

#### 1. Clone repository về máy
```bash
git clone https://github.com/Mirai3103/python-king-chess.git && cd python-king-chess && cd fastapi-server
```
#### 2. Tạo virtual environment và cài đặt các thư viện cần thiết
##### Đối với Windows
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
##### Đối với Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Chạy server
```bash
python main.py
```
#### 4. Chạy ứng dụng frontend
```bash
cd react-client && npm install && npm dev
```
### Chạy với docker
#### 1. Clone repository về máy
```bash
git clone https://github.com/Mirai3103/python-king-chess.git && cd python-king-chess && cd fastapi-server
```
#### 2. Run docker container
```bash
docker-compose up --build
```
## Demo

#### Màn hình chính
![alt text](https://cdn.discordapp.com/attachments/1109544174711218248/1235947446429941810/image.png?ex=66363942&is=6634e7c2&hm=54f4b064717e7dde27f499757595deb9f4ada73fcaafc5476a15e4c91085fff7&)

#### Chơi 2 người
![alt text](https://cdn.discordapp.com/attachments/979590301113020496/1236742408272875560/image.png?ex=66391d9f&is=6637cc1f&hm=a6aa0c6fc323d2e483a11d24378419c98c0cf2ae6b54948e63800875ac640a19&)

#### Chơi với máy

![alt text](https://cdn.discordapp.com/attachments/1109544174711218248/1235953875899514960/0503.gif?ex=66363f3e&is=6634edbe&hm=b215960da0b384b62826491b1e7c8f66c5dcf71bd859d266bb2844ba6a2125cd&)


## License
Licensed under the
[MIT](https://choosealicense.com/licenses/mit/)
 License

