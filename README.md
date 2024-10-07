# Основное задание:

1. Account URL: http://localhost:8001/api/swagger/

2. Hospital URL: http://localhost:8002/api/swagger/

3. Timetable URL: http://localhost:8083/ui-swagger

4. Document URL: http://localhost:8084/ui-swagger

# Дополнительное задание:

1. ElasticSearch URL: http://elasticsearch-service/

2. Kibana URL: http://kibana-service/

# Информация от участника
## Об особенностях данных json при отправке на сервер

#### 1) POST http://127.0.0.1:8000/api/Authentication/Refresh/ 
Для данного URL POST запрос должен выглядеть следующим образом:
```json 
{
	"refresh": "string"
}
```

#### 2) GET /api/Timetable/Hospital/{id}/
К данному запросу сделано следующее описание:
> <strong>описание:</strong> Получение расписания больницы по Id
> <strong>параметры:</strong>
```json
{
 	"from": "string(ISO8601)",
 	"to": "string(ISO8601)"
}
```
> <strong>ограничения:</strong> Только авторизованные пользователи 

И в связи с этим возникает вопрос: 
```txt
Почему json должен возвращать только одно расписание(from и to),
а не список расписаний, так как больница может иметь множество расписаний,
а не только одно?
``` 
Данное описание можно интерпретировать для себя по разному. К примеру, можно вернуть только первую запись больницы, но в таком случае будет не понятно, какая именно запись была возвращена. А можно пойти другим путем, но в таком случае ответ сервера будет немного вида изменен, а именно:
```json
{
	"Название больницы": {
		"Номер расписания": {
			"from": "string(ISO8601)",
			"to": "string(ISO8601)"
		},
		. . .
	}
}
```
И в таком случае, json будет выглядеть более корректно. Поскольку в ТЗ есть следующие слова:
>"Если у вас возникли вопросы по заданию, то решите его на
свое усмотрение, а мы оценим ваше решение. Если ваше
решение отличается от задания, то обязательно напишите все
изменения в файл Readme.md."

Я решил сделать более корректный и понятный ответ сервера

#### 3) GET /api/Timetable/Doctor/{id}/
В данном GET запросе описание было тоже весьма сомнительным, так как просилось вернуть только ОДНО какое-то расписание, без каких-либо уточнений. В связи с этим, я подумал, что намного эффективнее будет улучшить ответ сервера. Пример успешного возврата сервера выглядит следующим образом:
```json
{
    "Номер расписания": {
        "from": "2024-10-06T18:33:31Z",
        "to": "2024-10-06T18:33:32Z"
    },
	. . .
}
```