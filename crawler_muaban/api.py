import os
from dotenv import load_dotenv
from pathlib import Path

import google.generativeai as genai

load_dotenv(dotenv_path=Path('./.env'))
GOOGLE_API_KEY = os.getenv('API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')


def extract_description(description):
    prompt = f"Ta có thông tin rao bán nhà bằng tiếng Việt như sau: \
        {description} \n \
        Hãy trích xuất thông tin trên và trả về 8 trường thông tin dưới đây. \
        Danh sách các trường: num_bedroom, \
        num_diningroom, num_kitchen, num_toilet, num_floor (nếu là nhà trọ thì có mấy tầng), \
        current_floor (phòng trọ ở tầng mấy), direction (hướng nhà, 1 trong 4 giá trị Đông/Tây/Nam/Bắc), \
        street_width (số thực, theo mét). \
        Trường nào không xuất hiện thì để là 0.\
        Trường direction không xuất hiện thì để là rỗng.\
        Các trường thông tin ngăn cách bởi dấu phẩy.\
        Ví dụ: \"0,0,1,1,0,0,Đông,0\", hoặc \"1,0,1,1,0,0,,0\" nếu không có direction."

    response = model.generate_content(prompt)
    return response.text


str = "Cho nữ thuê phòng khép kín tại phố Dương Văn Bé, cạnh Time City, quận Hai Bà trưng, diện tích 20 m2/1 phòng, nhà mới xây thiết bị mới hiện đại vào ở ngay. Cạnh trường, chợ, tiện đi lại, có sân để xe. Giá 3 triệu/tháng."

extract_description(str)
