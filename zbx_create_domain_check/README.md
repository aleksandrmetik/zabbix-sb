## Описание

Current status: Ready to implement in Jenkins

Скрипт для проверки срока делегирования домена. По мимо сомой проверки сразу же создается триггер, который сработает за 20 дней (average) и за 5 дней (high), и за 3 дня (disaster) до окончания срока делегирования домена.
Проверка выполняется раз в сутки

## Запуск

```
python zbx_create_domain_check/domain_check.py --prname "southbridge.ru" --domain "southbridge.ru"
```

Где:
* --prname имя проекта в zabbix, в котором будет создана данная проверка
* --domain url домена который будет проверяться 
