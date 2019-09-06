# Запуск

python app.py


Для запуска нужен модуль Flask
pip install Flask

# Rest Api

#### Для отправки файла и получения id, по которому можно будет получить json (POST)
http://localhost:5000/send_file
#### Для отправки файла и получения json ответа (GET)
http://localhost:5000/get_json_by_file

#### Для отправки id и получения json ответа (GET)
http://localhost:5000/get_json_by_id

#### Пример содержимого входного файла:
#0\n
1\r
2\r\n
#3\r
##4\n
##5\n
###6\n
###7\r
##8\n
##9\r
#10\r\n

#### Пример запроса:
curl -i -H "Content-Type: application/json" -X GET -d "{"""id""":6}" http://localhost:5000/get_json_by_id

#### Пример ответа:
{
    "lines": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], 
    "structure": [
        {
            "section": 0, 
            "content": [1, 2], 
            "subsections": []
        }, 
        {
            "section": 3, 
            "content": [], 
            "subsections": [
                {
                    "section": 4, 
                    "content": [], 
                    "subsections": []
                }, 
                {
                    "section": 5, 
                    "content": [], 
                    "subsections": [
                        {
                            "section": 6, 
                            "content": [], 
                            "subsections": []
                        }, 
                        {
                            "section": 7, 
                            "content": [], 
                            "subsections": []
                        }
                    ]
                }, 
                {
                    "section": 8, 
                    "content": [],
                    "subsections": []
                }, 
                {
                    "section": 9, 
                    "content": [], 
                    "subsections": []
                }
            ]
        }, 
        {
            "section": 10, 
            "content": [], 
            "subsections": []
        }
    ]
}
