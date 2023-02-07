from datetime import date
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import ast
import sys
from checkinputdata import Check
import chromedriver_binary


# настройки для webdriver
def settings_for_driver():    
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=800,800')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# функция авторизации на сайте и сохранения cookies
def auth(driver):
    # авторизация через cookies
    try:
        driver.get('https://uslugi.mosreg.ru/zdrav/')
        with open(f'cookies/cookies.txt', 'r') as file_open:
            all_cookies = ast.literal_eval(file_open.read()[1:-1])
        for cookie in all_cookies:
            driver.add_cookie(cookie)
        driver.get('https://uslugi.mosreg.ru/zdrav/')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "// a[contains(text(),\'Записаться на прием')]")))
        print('\033[0;92m---Вход на сайт выполнен через cookies---\033[00m')
        return True
    except Exception as e:
        print('\033[1;31m---Вход на сайт через cookies не удался---\033[00m')
        print(e)
    # авторизация через данные полиса и сохранение ccokies
    try:
        print('\033[0;92mВведите номер полиса (16 цифр) и дату рождения (например, 02.03.2004)!\033[00m')
        while True:
            try:
                npol = input('Введите номер полиса: ')
                int(npol)
                birthday = input('Введите дату рождения: ')
                day = int(birthday.split('.')[0])
                month = int(birthday.split('.')[1])
                year = int(birthday.split('.')[2])
                if (31 < day or day < 1) or (12 < month or month < 1) or (year < 1900 or year > 2100):
                    print('\033[1;31mНеверный ввод. Попробуйте заново!\033[00m')
                else:
                    break
            except Exception as e:
                print('\033[1;31mНеверный ввод. Попробуйте заново!\033[00m')
                print(e)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'nPol'))).send_keys(npol)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'birthday'))).send_keys(birthday)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'b-btn.b-btn--red.b-registry-form__btn.c-registry-form__btn'))).click()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "// a[contains(text(),\'Записаться на прием')]")))
        cookies = driver.get_cookies()
        with open(f'cookies/cookies.txt', 'w') as file:
            file.write(str(cookies))
        print('\033[0;92m---Вход выполнен через ввод данных полиса. Cookies записаны---\033[00m')
        return True
    except:
        print('\033[1;31m---Вход через ввод данных полиса не удался---\033[00m')
        pass
    print('\033[1;31m---Попробуйте осуществить вход заново! Проверьте заранее вводимые данные!---\033[00m')
    sys.exit()

# функция отправки сообщений в Telegram
async def teleg_message(app, message_for_TG, TG_nickname):
    async with app:
        await app.send_message(f'@{TG_nickname}', message_for_TG)

# функция генерации списка дат
def generate_dates_list(today, amount):
    list_of_days = []
    for i in range(amount):
        timedelta = datetime.timedelta(days=i)
        print(f'{i}: {(today + timedelta).strftime("%d.%m.%Y")}')
        list_of_days.append(today + timedelta)
    return list_of_days

# функция
def open_site(driver, dates_priema, app, input_flag, input_specialization_number, input_policlinic_number, text, TG_flag, TG_nickname):
    driver.get('https://uslugi.mosreg.ru/zdrav/')
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "// a[contains(text(),\'Записаться на прием')]"))).click()
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "// a[contains(text(),\'ПРОДОЛЖИТЬ ЗАПИСЬ НА ПРИЕМ')]"))).click()

    # Получаем список специализаций
    specialization_numbers = WebDriverWait(driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, "b-doctor-spec__text.b-doctor-spec__title"))

    # флаг выбора специализаций. Необходим, чтобы не вводить повторно специализацию при следующей итерации поиска
    if not input_flag:
        # выводим в консоль имеющиеся специализации
        for i in range(len(specialization_numbers)):
            print(f'{i}: {specialization_numbers[i].text}')
        # выбираем необходимую специализацию
        while True:
            input_specialization_number = input(f'Введите номер необходимой специализации [0-{len(specialization_numbers)-1}]: ')
            if Check.check_input_value(input_specialization_number, specialization_numbers):
                input_specialization_number = int(input_specialization_number)
                break
        print(f'\033[0;92mВыбранная специализация - {specialization_numbers[input_specialization_number].text}\033[00m')
    specialization = specialization_numbers[input_specialization_number].text
    specialization_numbers[input_specialization_number].click()
    # при выборе некоторых специализаций появляется окно-информация, закрываем его
    try:
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "// a[contains(text(),\'Закрыть окно')]"))).click()
    except:
        pass
    # получаем список медицинских организаций
    policlinic_numbers = WebDriverWait(driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, "b-clinic-item.b-clinic-item--open.lpu-item-with-doctors"))
    # флаг, аналогичный предыдущему флагу (см.выше)
    # аналогичные операции, только для мед .учреждений (см. выше)
    if not input_flag:
        for i in range(len(policlinic_numbers)):
            print(f'{i}: {policlinic_numbers[i].find_element(By.CLASS_NAME, "b-link-inner").text}')
        while True:
            input_policlinic_number = input(f'Введите номер необходимого медицинского учреждения [0-{len(policlinic_numbers)-1}]: ')
            if Check.check_input_value(input_policlinic_number, policlinic_numbers):
                break
        print(f'\033[0;92mВыбранное медицинское учреждение - {policlinic_numbers[int(input_policlinic_number)].find_element(By.CLASS_NAME, "b-link-inner").text}\033[00m')
    policlinic = policlinic_numbers[int(input_policlinic_number)].find_element(By.CLASS_NAME, "b-link-inner").text
    category_numbers = policlinic_numbers[int(input_policlinic_number)].find_elements(By.CLASS_NAME, 'b-doctor-table.clearfix')
    # флаг, аналогичный предыдущему флагу (см.выше)
    # аналогичные операции, только для отслеживаемой категории (см. выше)
    if not input_flag:
        list_of_names = []
        for i in range(len(category_numbers)):
            names = category_numbers[i].find_elements(By.CLASS_NAME, 'b-doctor-info__spec')
            for item in names:
                list_of_names.append(item.text)
        list_of_names = sorted(list(set(list_of_names)))
        for i in range(len(list_of_names)):
            print(f'{i}: {list_of_names[i]}')
        while True:
            input_names_number = input(f'Введите значение отслеживаемой категории [0-{len(list_of_names)-1}]: ')
            if Check.check_input_value(input_names_number, list_of_names):
                break
        text = list_of_names[int(input_names_number)]
        print(f'\033[0;92mОтслеживаемая категория - {text}\033[00m')

    k = 0
    doctor_index = []

    #  формируем список докторов, удовлетворяющих отслеживаемой категории
    for i in range(len(category_numbers)):
        list_of_doctors = category_numbers[i].text
        if list_of_doctors.find(text) >= 0:
            doctor_index.append(i)

    # для всех отслеживаемых дат
    for data_priema in dates_priema:
        # если отслеживаемая дата на следующей неделе, то необходимо переключить неделю
        if ((data_priema - datetime.date.today()).days > 6):
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'b-doc-record-header-nav__item.next.c-next-week'))).click()
        # считываем имена докторов и их даты приема
        for item in doctor_index:
            names = WebDriverWait(driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, "b-clinic-item.b-clinic-item--open.lpu-item-with-doctors"))[int(input_policlinic_number)].find_elements(By.CLASS_NAME, 'b-doctor-table.clearfix')
            list_of_dates = names[item].find_elements(By.CLASS_NAME, 'b-doctor-schedule__item.free-tickets.vi-background-invert-hf.c-step')
            # после возврата на страницу изменяется идентификаторы элементов страницы, приходится их обновлять (
            for j in range(len(list_of_dates)):
                names = WebDriverWait(driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, "b-clinic-item.b-clinic-item--open.lpu-item-with-doctors"))[int(input_policlinic_number)].find_elements(By.CLASS_NAME, 'b-doctor-table.clearfix')
                list_of_dates = names[item].find_elements(By.CLASS_NAME, 'b-doctor-schedule__item.free-tickets.vi-background-invert-hf.c-step')
                # берем конкретную дату
                date = names[item].find_elements(By.CLASS_NAME, 'b-doctor-schedule__item.free-tickets.vi-background-invert-hf.c-step')[j].text

                # сравниваем взятую дату с требуемой датой приема
                if date.find(data_priema.strftime("%d.%m")) >= 0:
                    amount = list_of_dates[j].find_element(By.CLASS_NAME, 'b-doctor-schedule__item-tickets')
                    number_of_talons = amount.text
                    name = names[item].find_element(By.CLASS_NAME, 'b-doctor-info__name').text
                    vremya_priema = list_of_dates[j].find_element(By.CLASS_NAME, 'b-doctor-schedule__item-time').text
                    date = list_of_dates[j].find_element(By.CLASS_NAME, 'b-doctor-schedule__date-mob').text
                    # если у доктора есть свободные талоны
                    if amount != 'ТАЛОНОВ 0':
                        k += 1
                        amount.click()
                        list_of_time = []
                        # получаем времена приема для необходимой даты
                        elements = WebDriverWait(driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, 'b-app-time__item.free-tickets.vi-background-invert-hf.c-step'))
                        for element in elements:
                            list_of_time.append(element.text)
                        list_of_time = ', '.join(list_of_time)
                        message = f'Дата: {data_priema.strftime("%d.%m.%Y")};{policlinic}:{specialization};Врач: {name};Время приема: {vremya_priema};{number_of_talons} ({list_of_time}). Дата проверки: {time.strftime("%d.%m.%Y %H:%M:%S")}'
                        message_for_TG = f'Дата: {data_priema.strftime("%d.%m.%Y")} \r\nМед. учреждение: {policlinic} \r\nСпециализация: {specialization} \r\nВрач: {name} \r\nВремя приема: {vremya_priema} \r\n{number_of_talons} ({list_of_time}). \r\nДата проверки: {time.strftime("%d.%m.%Y %H:%M:%S")}'
                        # выводим сообщение в консоль в случае положительного поиска
                        print(message)
                        # флаг, аналогичный указанным выше. Отправляем сообщение в Telegram
                        if TG_flag:
                            app.run(teleg_message(app, message_for_TG, TG_nickname))
                        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'b-gray-steps__nav__item.prev.icon-z4.c-prev-step.c-step'))).click()
                        try:
                            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "// a[contains(text(),\'Закрыть окно')]"))).click()
                        except:
                            pass
                        if ((data_priema - datetime.date.today()).days > 6):
                            WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located(
                                    (By.CLASS_NAME, 'b-doc-record-header-nav__item.next.c-next-week'))).click()
    print('-------')
    # если свободные талоны есть, то отпраляем в Telegram адрес сайта, для оперативной записи сразу с телефона
    if k != 0:
        if TG_flag:
            app.run(teleg_message(app, 'https://uslugi.mosreg.ru/zdrav/', TG_nickname))
    # если свободных талонов нет, то только в вконсоль выводим эту информацию
    else:
        print(f'\033[1;31mНа {data_priema.strftime("%d.%m.%Y")} талонов нет (дата проверки - {time.strftime("%d.%m.%Y %H:%M:%S")})\033[00m')
    # для того, чтобы повторно не вводить все выбранные категории, возвращаем их и используем в качестве аргументов функции при следующей итерации плиска
    return [input_specialization_number, input_policlinic_number, text]


def main():
    print('\033[0;92mВыберите дату, на которую желаете отследить наличие талонов! \033[00m')
    today = date.today()
    list_of_days = generate_dates_list(today, amount=14)
    print(f'{len(list_of_days)}: На любые доступные даты')
    while True:
        input_day_number = input(f'Выберите дату из предложенных [0-{len(list_of_days)}]: ')
        if input_day_number == '14':
            dates_priema = list_of_days
            print(f'\033[0;92mВыбранная дата - На любые доступные даты \033[00m')
            break
        else:
            if Check.check_input_value(input_day_number, list_of_days):
                dates_priema = [list_of_days[int(input_day_number)]]
                print(f'\033[0;92mВыбранная дата - {list_of_days[int(input_day_number)].strftime("%d.%m.%Y")} \033[00m')
                break

    print('\033[0;92mВведите значение задержки между запросами о наличии талонов в минутах! Например, 5. В таком случае проврека будет проводиться каждые 5 минут \033[00m')
    while True:
        delay = input('Введите значение задержки, мин: ')
        if Check.check_delay(delay):
            delay = int(delay)
            break
    while True:
        TG_flag = input('Направлять информацию о талонах в случае их наличия в Telegram [Y/N]: ')
        TG_nickname = None
        if Check.check_TG_flag(TG_flag) == 'y':
            if Check.check_telegram_session():
                path = Check.check_telegram_session()[:-8]
                TG_flag = True
                TG_nickname = input('Введите nickname Telegram (значение после символа @): ')
                from pyrogram import Client
                app = Client(path)
                break
            else:
                print('\033[1;31mОтсутствует файл Telegram-сессии. Поместите файл Telegram-сессии в папку "TG_session" и попробуйте заново!\033[00m')
        elif Check.check_TG_flag(TG_flag) == 'n':
            TG_flag = False
            app = None
            break
        else:
            print('\033[1;31mНеверный ввод. Попробуйте заново!\033[00m')
    driver = settings_for_driver()
    if auth(driver):
        input_flag = False
        input_values = open_site(driver, dates_priema, app, input_flag, input_specialization_number=None, input_policlinic_number=None, text=None, TG_flag=TG_flag, TG_nickname=TG_nickname)
        input_specialization_number, input_policlinic_number, text = input_values[0], input_values[1], input_values[2]
        input_flag = True
        while True:
            try:
                time.sleep(delay*60)
                # если скрипт работает больше суток, обновляется список актуальных дат в режиме "На любые доступные даты"
                if today != date.today() and input_day_number == '14':
                    list_of_days = generate_dates_list(today, amount=14)
                open_site(driver, dates_priema, app, input_flag, input_specialization_number, input_policlinic_number, text, TG_flag, TG_nickname)
            except Exception as e:
                print('\033[1;31m---Скрипт аварийно завершил выполнение---\033[00m')
                print(e)
                pass


if __name__ == '__main__':
    main()


