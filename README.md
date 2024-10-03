# Основное задание:

1. Account URL: http://localhost:8001/api/swagger/

2. Hospital URL: http://localhost:8082/ui-swagger

3. Timetable URL: http://localhost:8083/ui-swagger

4. Document URL: http://localhost:8084/ui-swagger

# Дополнительное задание:

1. ElasticSearch URL: http://elasticsearch-service/

2. Kibana URL: http://kibana-service/

# Информация от участника
## Об особенностях данных json при отправке на сервер
1) http://127.0.0.1:8000/api/Authentication/Refresh/ 
Для данного URL POST запрос должен выглядеть следующим образом:
```json 
{
	"refresh": "string" // Refresh token, который был получен при входе в аккаунт
}
```
