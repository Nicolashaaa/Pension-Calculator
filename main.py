from tkinter import *
from tkinter import ttk
import subprocess

# Глобальные переменные для отслеживания состояния интерфейса
age_calculated = False
disability_calculated = False


def calculate_pension_from_c_program(gender, income, insurance_record, retirement_age, radio_choice):
    try:
        # Запуск программы на C и передача данных через стандартный ввод (stdin)
        process = subprocess.Popen(
            ["./Individual work_age - Copy.exe"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

        # Формирование строки с входными данными для программы на C
        input_data = f"{gender} {income} {insurance_record} {retirement_age} {radio_choice}"

        # Передача данных в стандартный ввод (stdin) программы на C
        output, _ = process.communicate(input=input_data)

        # Преобразование вывода программы на C в число (результат пенсии)
        pension = float(output.strip())
        return pension

    except FileNotFoundError:
        print("Ошибка: Файл программы на C не найден")
        return None
    except ValueError:
        print("Ошибка: Неверный формат данных из программы на C")
        return None


def calculate_by_age():
    global age_calculated, disability_calculated

    # Очищаем текущее окно
    clear_interface()

    # Добавляем текст "You are OLD" по центру
    def show_tooltip(widget, message):
        # Функция для отображения подсказки при наведении курсора на виджет
        widget.bind("<Enter>", lambda e: tooltip.configure(text=message))
        widget.bind("<Leave>", lambda e: tooltip.configure(text=""))

    def submit_form():
        # Считываем значения из полей ввода
        gender_input = entry_vars["Gender"].get().strip()  # Получаем значение и удаляем лишние пробелы

        # Оставляем только первую букву
        if gender_input:
            gender = gender_input[0].upper()  # Берем первую букву и переводим в верхний регистр
        else:
            gender = ''

        # Проверяем правильность ввода для поля Gender
        if gender not in ['M', 'F']:
            print("Ошибка: Неправильно введены данные для поля Gender. Введите 'M' для мужского или 'F' для женского.")
            return  # Прекращаем выполнение функции в случае неправильного ввода
        try:
            monthly_income = float(entry_vars["Monthly Income"].get())  # Получаем значение и преобразуем во float
        except ValueError:
            monthly_income = 0.0  # Обработка ошибки ввода, если не удалось преобразовать в число

        try:
            insurance_record = float(entry_vars["Insurance record"].get())  # Получаем значение и преобразуем во float
        except ValueError:
            insurance_record = 0.0  # Обработка ошибки ввода, если не удалось преобразовать в число

        try:
            retirement_age = float(entry_vars["Retirement age"].get())  # Получаем значение и преобразуем во float
        except ValueError:
            retirement_age = 0.0  # Обработка ошибки ввода, если не удалось преобразовать в число

        # Считываем выбор галочки
        radio_choice = -1  # Инициализируем переменную для выбора галочки

        # Перебираем варианты галочек и ищем выбранный
        for i, option in enumerate(radio_options):
            if radio_var.get() == option:
                radio_choice = i + 1  # Индексация начинается с 0, поэтому добавляем 1 для получения числового значения
                break

        # Вывод полученных данных для проверки
        print("Gender:", gender)
        print("Monthly Income:", monthly_income)
        print("Insurance record:", insurance_record)
        print("Retirement age:", retirement_age)
        print("Radio Choice:", radio_choice)

        pension_result = calculate_pension_from_c_program(gender, monthly_income, insurance_record, retirement_age, radio_choice)
        print(f"Your pension is {pension_result:.2f} lei")

        clear_interface()

        root.title("Pension Result")

        label = Label(root, text=f"Your pension is {pension_result:.2f} lei", font=("Helvetica", 16))
        label.pack(padx=20, pady=20)

        reset_button = ttk.Button(root, text="Reset", command=reset_interface)
        reset_button.pack(side=BOTTOM, anchor="se", padx=10, pady=10)



        # Здесь можно дальше обрабатывать или сохранять полученные данные

    # Создаем основное окно


    # Организуем основной контейнер
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack()

    # Подсказка для полей ввода
    tooltip = ttk.Label(root, text="", font=("Helvetica", 10), foreground="gray")
    tooltip.pack()

    # Создаем метки с полями ввода
    fields = {
        "Gender": "Male or Female",
        "Monthly Income": "Your fixed income per month",
        "Insurance record": "Is calculated by summing up all insurance periods",
        "Retirement age": "Actual age at retirement"
    }

    entry_vars = {}

    row_index = 0
    for field, message in fields.items():
        label = ttk.Label(main_frame, text=field + ":")
        label.grid(row=row_index, column=0, padx=10, pady=5, sticky=W)

        entry_var = StringVar()
        entry = ttk.Entry(main_frame, textvariable=entry_var, width=30)
        entry.grid(row=row_index, column=1, padx=10, pady=5, sticky=W)

        entry_vars[field] = entry_var

        # Показываем подсказку при наведении курсора на поле ввода
        show_tooltip(entry, message)

        row_index += 1

    # Создаем разделитель
    separator = ttk.Separator(main_frame, orient="horizontal")
    separator.grid(row=row_index, columnspan=2, pady=10, sticky="ew")
    row_index += 1

    # Подсказка для галочек
    tooltip_radio = ttk.Label(root, text="", font=("Helvetica", 10), foreground="gray")
    tooltip_radio.pack()

    # Создаем галочки (radio buttons)
    radio_var = StringVar()
    radio_options = [
        "for agricultural workers, labourers (I-II qualification category) and unskilled auxiliary personnel",
        "for medium-skilled workers (III-IV qualification category)",
        "for highly qualified workers (V-VIII qualification category) and specialists with specialised secondary education",
        "for professionals with higher education",
        "for executives at the level of structural subdivision",
        "for heads of enterprises and their deputies"
    ]

    for i, option in enumerate(radio_options):
        radio = ttk.Radiobutton(main_frame, text=option, variable=radio_var, value=option)
        radio.grid(row=row_index + i, column=0, columnspan=2, padx=10, pady=5, sticky=W)

        # Показываем подсказку при наведении курсора на галочку
        show_tooltip(radio, f"Select: {option}")

    # Кнопка отправки формы
    submit_button = ttk.Button(main_frame, text="Submit", command=submit_form)
    submit_button.grid(row=row_index + len(radio_options), columnspan=2, pady=20)

    reset_button = ttk.Button(root, text="Reset", command=reset_interface)
    reset_button.pack(side=BOTTOM, anchor="se", padx=10, pady=10)

def disability_calculate_pension_from_c_program(disability_determination, insurance_record, monthly_income,  radio_choice):
    try:
        # Запуск программы на C и передача данных через стандартный ввод (stdin)
        process = subprocess.Popen(
            ["./Individual work_disability - Copy.exe"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

        # Формирование строки с входными данными для программы на C
        input_data = f"{disability_determination} {insurance_record} {monthly_income} {radio_choice}"

        # Передача данных в стандартный ввод (stdin) программы на C
        output, _ = process.communicate(input=input_data)

        # Преобразование вывода программы на C в число (результат пенсии)
        pension = float(output.strip())
        return pension

    except FileNotFoundError:
        print("Ошибка: Файл программы на C не найден")
        return None
    except ValueError:
        print("Ошибка: Неверный формат данных из программы на C")
        return None


def calculate_by_disability():
    global age_calculated, disability_calculated

    # Очищаем текущее окно
    clear_interface()

    def show_tooltip(widget, message):
        # Функция для отображения подсказки при наведении курсора на виджет
        widget.bind("<Enter>", lambda e: tooltip.configure(text=message))
        widget.bind("<Leave>", lambda e: tooltip.configure(text=""))

    def submit_form():
        try:
            disability_determination = float(entry_vars[
                                                 "Age at the date of disability determination"].get())  # Получаем значение и преобразуем во float
        except ValueError:
            disability_determination = 0.0  # Обработка ошибки ввода, если не удалось преобразовать в число

        try:
            monthly_income = float(entry_vars["Monthly Income"].get())  # Получаем значение и преобразуем во float
        except ValueError:
            monthly_income = 0.0  # Обработка ошибки ввода, если не удалось преобразовать в число

        try:
            insurance_record = float(entry_vars["Insurance record"].get())  # Получаем значение и преобразуем во float
        except ValueError:
            insurance_record = 0.0  # Обработка ошибки ввода, если не удалось преобразовать в число
        radio_choice = -1  # Инициализируем переменную для выбора галочки

        # Перебираем варианты галочек и ищем выбранный
        for i, option in enumerate(radio_options):
            if radio_var.get() == option:
                radio_choice = i + 1  # Индексация начинается с 0, поэтому добавляем 1 для получения числового значения
                break

        print("Age at the date of disability determination:", disability_determination)
        print("Monthly Income:", monthly_income)
        print("Insurance record:", insurance_record)
        print("Radio Choice:", radio_choice)

        pension_result = disability_calculate_pension_from_c_program(disability_determination, insurance_record, monthly_income, radio_choice)
        print(f"Your pension is {pension_result:.2f} lei")

        clear_interface()

        root.title("Pension Result")

        label = Label(root, text=f"Your pension is {pension_result:.2f} lei", font=("Helvetica", 16))
        label.pack(padx=20, pady=20)

        reset_button = ttk.Button(root, text="Reset", command=reset_interface)
        reset_button.pack(side=BOTTOM, anchor="se", padx=10, pady=10)



    # Организуем основной контейнер
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack()

    # Подсказка для полей ввода
    tooltip = ttk.Label(root, text="", font=("Helvetica", 10), foreground="gray")
    tooltip.pack()

    # Создаем метки с полями ввода и поля ввода
    fields = {
        "Age at the date of disability determination": "The age of the initial establishment of the disability",
        "Insurance record": "Is calculated by summing up all insurance periods",
        "Monthly Income": "Your fixed income per month"
    }

    entry_vars = {}

    row_index = 0
    for field, message in fields.items():
        label = ttk.Label(main_frame, text=field + ":")
        label.grid(row=row_index, column=0, padx=10, pady=5, sticky=W)

        entry_var = StringVar()
        entry = ttk.Entry(main_frame, textvariable=entry_var, width=30)
        entry.grid(row=row_index, column=1, padx=10, pady=5, sticky=W)

        entry_vars[field] = entry_var

        # Показываем подсказку при наведении курсора на поле ввода
        show_tooltip(entry, message)

        row_index += 1

    # Создаем разделитель
    separator = ttk.Separator(main_frame, orient="horizontal")
    separator.grid(row=row_index, columnspan=2, pady=10, sticky="ew")
    row_index += 1

    # Подсказка для галочек
    tooltip_radio = ttk.Label(root, text="", font=("Helvetica", 10), foreground="gray")
    tooltip_radio.pack()

    # Создаем галочки (radio buttons)
    radio_var = StringVar()
    radio_options = [
        "1 - Severe disability group",
        "2 - Accented disability group",
        "3 - Medium disability group"
    ]

    for i, option in enumerate(radio_options):
        radio = ttk.Radiobutton(main_frame, text=option, variable=radio_var, value=option)
        radio.grid(row=row_index + i, column=0, columnspan=2, padx=10, pady=5, sticky=W)

        # Показываем подсказку при наведении курсора на галочку
        show_tooltip(radio, f"Select: {option}")

    # Кнопка отправки формы
    submit_button = ttk.Button(main_frame, text="Submit", command=submit_form)
    submit_button.grid(row=row_index + len(radio_options), columnspan=2, pady=20)

    reset_button = ttk.Button(root, text="Reset", command=reset_interface)
    reset_button.pack(side=BOTTOM, anchor="se", padx=10, pady=10)

def clear_interface():
    for widget in root.winfo_children():
        widget.destroy()


def reset_interface():
    clear_interface()

    title_label = ttk.Label(root, text="Pension Calculator", font=("Roboto", 28))
    title_label.pack(pady=(100, 0))

    # Восстанавливаем кнопки "Calculate by Age" и "Calculate by Disability" при необходимости
    age_button = ttk.Button(root, text="Calculate by Age", command=calculate_by_age)
    age_button.pack(side=LEFT, padx=(200, 10), pady=(250, 10))

    disability_button = ttk.Button(root, text="Calculate by Disability", command=calculate_by_disability)
    disability_button.pack(side=RIGHT, padx=(10, 200), pady=(250, 10))


# Создаем основное окно
root = Tk()
root.title("PensionCalculator")
root.geometry("800x600")






title_label = ttk.Label(root, text="Pension Calculator", font=("Roboto", 28))
title_label.pack(pady=(100, 0))

age_button = ttk.Button(root, text="Calculate by Age", command=calculate_by_age)
age_button.pack(side=LEFT, padx=(200 , 10), pady=(250, 10))

disability_button = ttk.Button(root, text="Calculate by Disability", command=calculate_by_disability)
disability_button.pack(side=RIGHT, padx=(10 , 200),  pady=(250, 10))

root.mainloop()
