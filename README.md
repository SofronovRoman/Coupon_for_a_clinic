## Скрипт позволяет отлеживать наличие талонов на заданную дату/период с задаваемой периодичностью к врачам Московской области, запись к которым осуществляется через сайт [https://uslugi.mosreg.ru/zdrav/](https://uslugi.mosreg.ru/zdrav/), и в случае необходимости оповещать о результатах в Telegram через клиента (не через бота).

## ⬇️ Подготовка
```ruby
$ git clone https://github.com/SofronovRoman/Coupon_for_a_clinic.git
$ cd Coupon_for_a_clinic
$ python3 -m pip install -r requirements.txt
```

## Конфигурация
Установите [Chrome](https://www.google.com/intl/ru/chrome/), если он у вас еще не установлен.
Если необходимо оповещение в Telegram о результатах работы скрипта, то необходимо в папку "TG_session" поместить файл Telegram-сессии клиента с расширением ".session". Если необходимо создание файла Telegram-сессии, то следуйте инструкции на [https://core.telegram.org/api/obtaining_api_id](https://core.telegram.org/api/obtaining_api_id). После получения api_id и api_hash сессию также можно создать с использованием скрипта в "TG_session\create_session.py". При использовании данного скрипта файл Telegram-сессии создается в папке "TG_session". При первом использовании скрипта вход на сайт будет осуществлен по данным полиса с сохранением файла "cookies\cookies.txt", дальнейший вход будет осуществляться с использованием файла cookies.

## Использование
```ruby
$ python3 main.py
```

## Docker
Для запуска скрипта в Docker-контейнере используйте файл "Dockerfile" для создания Docker-образа.
