# Основное задание:

1. Account URL: http://localhost:8001/api/swagger/

2. Hospital URL: http://localhost:8002/api/swagger/

3. Timetable URL: http://localhost:8003/api/swagger

4. Document URL: http://localhost:8004/api/swagger

# Дополнительное задание:

1. ElasticSearch URL: http://elasticsearch-service/

2. Kibana URL: http://kibana-service/

# Информация от участника
## Об особенностях данных json при отправке на сервер

### 1) POST /api/Authentication/Refresh/ 
Для данного URL POST запрос должен выглядеть следующим образом:
```json 
{
	"refresh": "string"
}
```

### 2) GET /api/History/Account/{id}/
Было разработано такое решение потому, что у пользователя с переданным id может быть несколько историй посещения врачей и данный формат ответа будет более корректным, чем тот, что представлен в ТЗ:

```json
{
    "История: ФИ пользователя": {
        "Номер истории": {
            "id": "int",
            "pacientId": "int",
            "hospitalId": "int",
            "doctorId": "int",
            "room": "stг",
            "date": "dateTime(ISO8601)",
            "data": "str"
        },
    }
}
```