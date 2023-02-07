import os


class Check:
    @staticmethod
    def check_data_priema(data_priema):
        try:
            day = data_priema.split('.')[0]
            len_day = len(day)
            day = int(day)
            month = data_priema.split('.')[1]
            len_month = len(month)
            month = int(month)
            if (31 < day or day < 1) or (12 < month or month < 1) or (len_day != 2) or (len_month != 2):
                print('\033[1;31mНеверный ввод. Проверьте вводимые данные и следуйте формату, указанному в примере! \033[00m')
            else:
                return True
        except:
            print('\033[1;31mНеверный ввод. Проверьте вводимые данные и следуйте формату, указанному в примере! \033[00m')

    @staticmethod
    def check_delay(delay):
        try:
            delay = int(delay)
            return True
        except:
            print('\033[1;31mНеверный ввод. Попробуйте заново!\033[00m')

    @staticmethod
    def check_TG_flag(TG_flag):
        if TG_flag.lower() == 'y':
            return 'y'
        elif TG_flag.lower() == 'n':
            return 'n'

    @staticmethod
    def check_input_value(input_value, checked_list):
        try:
            input_value = int(input_value)
            if (input_value > len(checked_list)-1) or (input_value < 0):
                print('\033[1;31mНеверный ввод. Попробуйте заново! \033[00m')
            else:
                return True
        except:
            print('\033[1;31mНеверный ввод. Попробуйте заново! \033[00m')
            pass

    @staticmethod
    def check_telegram_session():
        file_list = os.listdir('TG_session')
        for file in file_list:
            if file.endswith('.session'):
                return os.path.join('TG_session', file)

