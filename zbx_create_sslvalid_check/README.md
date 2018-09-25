Current status: Ready to implement in Jenkins

Описание

Скрипт для проверки срока ssl сертификат. По мимо проверки сразу же создается триггер, который сработает за 20 дней (Приоритет 3 - average), за 5 дней (high) и за 3 дня (disaster) до окончания срока ssl сертификат.

Запуск

```
python  zbx_create_sslvalid_check/zbx_create_sslvalid_check.py --prname "southbridge.ru" --domain "southbridge.ru" --delay 1d
```

Где:
* --prname имя проекта в zabbix, в котором будет создана данная проверка
* --domain имя  домена при обращение на который будет отдаваться необходимый ssl сертификат
* --delay интервал запуска проверки. По умолчанию 1 день. 
