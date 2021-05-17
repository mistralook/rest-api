# REST API
### Автор работы: Львов Ярослав

### Начало работы
В body POST запроса /database?merge=1 передать данные по валютам относительно курса доллара в json формате. 
Пример: 
```
{
    RUR: 74,
    EUR: 0.82,
    YEN: 109.19
}
```
### Конвертация
* GET /convert?from=RUR&to=USD&amount=42 
* Ответ: ```{amount: $(converted_amount)}```.

### Хранилище данных
#### json(redis w.i.p)

### Тесты
#### W.I.P

### Docker
#### W.I.P