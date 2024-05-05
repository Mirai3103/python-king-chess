
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
![alt text](https://cdn.discordapp.com/attachments/1109544174711218248/1235947446429941810/image.png?ex=6638dc42&is=66378ac2&hm=ed755c0cc348825f5895351880fbd8ec1bf0ee2ca6d00dddc79fcf86aacf92f9&)

#### Chơi 2 người
![alt text](https://cdn.discordapp.com/attachments/979590301113020496/1236742408272875560/image.png?ex=66391d9f&is=6637cc1f&hm=a6aa0c6fc323d2e483a11d24378419c98c0cf2ae6b54948e63800875ac640a19&)

#### Chơi với máy
![alt text](https://cdn.discordapp.com/attachments/1109544174711218248/1235953225908224062/image.png?ex=6638e1a3&is=66379023&hm=0e8be0654a1a16057d65fd330479945025cfbe7a92c7587471fb30155f043e3f&)
![alt text](https://cdn.discordapp.com/attachments/1109544174711218248/1235953875899514960/0503.gif?ex=6638e23e&is=663790be&hm=9425cab7f3b702b5ec1a989ed1c834312a25cf1c7da5524802faf5d3d9486e5b&)


## License
Licensed under the
[MIT](https://choosealicense.com/licenses/mit/)
 License

