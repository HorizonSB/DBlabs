import datetime
import tkinter
from tkinter import ttk
import psycopg2
from tkinter import *
from config import host, user, password, db_name

connection = None
cursor = None
role = None


def login():
    login_string = login_entry.get()
    password_string = password_entry.get()
    if login_string:
        global connection
        connection = psycopg2.connect(
            host=host,
            user=login_string,
            password=password_string,
            database=db_name
        )
        connection.autocommit = True;
        global cursor
        cursor = connection.cursor()
        hide_login_window()
        show_manager_selection_menu()
        print(f'Login {login_string}')
    else:
        error_window = Toplevel()
        error_window.geometry('50x50')
        newlabel = Label(error_window, text="Ошибка")
        newlabel.pack()
        print('Ошибка авторизации')


def test():
    cursor.execute("SELECT * FROM task;")
    Label(window, text=cursor.fetchone()).grid(row=6, column=1)


def show_all_tasks():
    window = Toplevel()
    window.geometry('1850x300')
    window.title('Задания')
    cursor.execute('SELECT count(*) from task;')
    number_of_rows = cursor.fetchone()

    cursor.execute("SELECT * FROM task;")
    tasks = cursor.fetchall()

    # определяем столбцы
    columns = (
        'task_id', 'deadline', 'assignment_date', 'task_description', 'priority', 'status', 'executor_employee_id',
        'author_employee_id', 'contract_id')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.grid(row=0, column=0, sticky="nsew")
    # определяем заголовки
    tree.heading('task_id', text='ID Задания')
    tree.heading('deadline', text='Дедлайн')
    tree.heading('assignment_date', text='Дата назначения')
    tree.heading('task_description', text='Описание')
    tree.heading('priority', text='Приоритет')
    tree.heading('status', text='Статус')
    tree.heading('executor_employee_id', text='ID исполнителя')
    tree.heading('author_employee_id', text='ID автора')
    tree.heading('contract_id', text='ID контракта')

    # добавляем данные
    for task in tasks:
        tree.insert("", END, values=task)

    # добавляем вертикальную прокрутку
    scrollbar = ttk.Scrollbar(window, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")


def create_task():
    create_task_window = Toplevel()
    create_task_window.geometry('320x230')
    create_task_window.title('Создание задания')
    # task_id_entry = Entry(create_task_window)
    # task_id_entry.grid(row=0, column=1)
    deadline_entry = Entry(create_task_window)
    deadline_entry.grid(row=1, column=1)
    assignment_date_entry = Entry(create_task_window)
    assignment_date_entry.grid(row=2, column=1)
    description_entry = Entry(create_task_window)
    description_entry.grid(row=3, column=1)
    priority_entry = Entry(create_task_window)
    priority_entry.grid(row=4, column=1)
    # status_entry = Entry(create_task_window)
    # status_entry.grid(row=5, column=1)
    executor_entry = Entry(create_task_window)
    executor_entry.grid(row=6, column=1)
    # author_entry = Entry(create_task_window)
    # author_entry.grid(row=7, column=1)
    # contract_id_entry = Entry(create_task_window)
    # contract_id_entry.grid(row=8, column=1)
    # Label(create_task_window, text='task_id').grid(row=0, column=0)
    Label(create_task_window, text='Дедлайн').grid(row=1, column=0)
    Label(create_task_window, text='Дата назначения').grid(row=2, column=0)
    Label(create_task_window, text='Описание задания').grid(row=3, column=0)
    Label(create_task_window, text='Приоритет').grid(row=4, column=0)
    # Label(create_task_window, text='Статус').grid(row=5, column=0)
    Label(create_task_window, text='Исполнитель').grid(row=6, column=0)
    # Label(create_task_window, text='Автор').grid(row=7, column=0)
    # Label(create_task_window, text='contract_id').grid(row=8, column=0)
    submit_task_button = Button(create_task_window, text='Готово', command=submit_task())
    submit_task_button.grid(row=10, column=0, columnspan=2, sticky='we')


def submit_task():
    # task_id = task_id_entry.get()
    # print(task_id)
    # cursor.execute(f"""INSERT INTO task(task_id,
    # deadline,
    # assignment_date,
    # task_description,
    # priority, status,
    # executor_employee_id,
    # author_employee_id,
    #  "contract_id ")
    # VALUES ({int(task_id_entry)},
    #  '{datetime.date()}',
    #  '{datetime.date()}',
    #  '{description_entry}',
    #   {int(priority_entry)},
    #  '{status_entry}',
    #   {int(executor_entry)},
    #   {int(author_entry)},
    #   {int(contract_id_entry)})""")
    pass


def show_employee():
    # создание нового окна
    window = Toplevel()
    window.title("Сотрудники")
    window.geometry("1350x300")

    # считаем количество строк
    cursor.execute('SELECT count(*) from employee;')
    number_of_rows = cursor.fetchone()

    cursor.execute("SELECT * FROM employee;")
    employees = cursor.fetchall()

    # определяем столбцы
    columns = ('employee_id', 'phone_number', 'job_title', 'first_name', 'last_name', 'email', 'username', 'password')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.grid(row=0, column=0, sticky="nsew")
    # определяем заголовки
    tree.heading('employee_id', text='ID Сотрудника')
    tree.heading('phone_number', text='Телефон')
    tree.heading('job_title', text='Роль')
    tree.heading('first_name', text='Имя')
    tree.heading('last_name', text='Фамилия')
    tree.heading('email', text='Email')
    tree.heading('username', text='Username')
    tree.heading('password', text='Password')

    for employee in employees:
        tree.insert("", END, values=employee)

    # добавляем вертикальную прокрутку
    scrollbar = ttk.Scrollbar(window, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")


def hide_login_window():
    main_label.grid_remove()
    login_label.grid_remove()
    password_label.grid_remove()
    login_entry.grid_remove()
    password_entry.grid_remove()
    entry_button.grid_remove()
    register_button.grid_remove()
    # manager_choice.grid_remove()
    # employee_choice.grid_remove()
    # test_button.grid_remove()


def select_role():
    global role
    role = role_selection.get()
    print(role)


def show_manager_selection_menu():
    window.title('Менеджер')
    button_show_employee = Button(text='Показать сотрудников', command=show_employee)
    button_show_employee.grid(row=0, column=0, sticky='we')
    button_show_tasks = Button(text='Показать задания', command=show_all_tasks)
    button_show_tasks.grid(row=0, column=1, sticky='we')
    button_create_task = Button(text='Создать задание', command=create_task)
    button_create_task.grid(row=0, column=2, sticky='we')
    button_create_report_of_tasks = Button(text='Отчет по задачам', command=create_report_of_tasks)
    button_create_report_of_tasks.grid(row=1, column=0, sticky='we')
    button_create_report_of_employees = Button(text='Отчет по сотрудникам', command=create_report_of_employees)
    button_create_report_of_employees.grid(row=1, column=1, sticky='we')


def create_report_of_tasks():
    cursor.execute('SELECT tasks_to_json();')
    success_window = Toplevel()
    success_window.geometry('200x50')
    Label(success_window, text='Отчет по задачам сохранен').pack()
    print('Отчет по задачам сохранен')
    pass


def create_report_of_employees():
    cursor.execute('SELECT employee_to_json();')
    success_window = Toplevel()
    success_window.geometry('200x50')
    Label(success_window, text='Отчет по сотрудникам сохранен').pack()
    print('Отчет по сотрудникам сохранен')
    pass


def show_employee_selection_menu():
    button_show_my_tasks = Button(text='Мои задачи', command=show_my_tasks)
    window.title('Сотрудник')
    button_show_my_tasks.grid(row=0, column=0)


def show_my_tasks():
    window = Toplevel()
    window.geometry('1850x300')
    window.title('Задания')
    global connection
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    global cursor
    cursor = connection.cursor()
    cursor.execute('SELECT count(*) from task;')
    number_of_rows = cursor.fetchone()

    cursor.execute('SELECT * FROM task WHERE executor_employee_id = 111 OR author_employee_id = 111;')
    tasks = cursor.fetchall()

    # определяем столбцы
    columns = (
        'task_id', 'deadline', 'assignment_date', 'task_description', 'priority', 'status', 'executor_employee_id',
        'author_employee_id', 'contract_id')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.grid(row=0, column=0, sticky="nsew")
    # определяем заголовки
    tree.heading('task_id', text='ID Задания')
    tree.heading('deadline', text='Дедлайн')
    tree.heading('assignment_date', text='Дата назначения')
    tree.heading('task_description', text='Описание')
    tree.heading('priority', text='Приоритет')
    tree.heading('status', text='Статус')
    tree.heading('executor_employee_id', text='ID исполнителя')
    tree.heading('author_employee_id', text='ID автора')
    tree.heading('contract_id', text='ID контракта')

    # добавляем данные
    for task in tasks:
        tree.insert("", END, values=task)

    # добавляем вертикальную прокрутку
    scrollbar = ttk.Scrollbar(window, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")
    print(cursor.fetchall())
    pass


def show_current_user():
    cursor.execute('SELECT current_user;')
    print(cursor.fetchone())
    pass


def registration():
    registration_window = Toplevel()
    registration_window.geometry('400x200')
    registration_window.title('Регистрация')

    global connection
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    connection.autocommit = True;
    global cursor
    cursor = connection.cursor()
    cursor.execute('SELECT current_user;')
    print(cursor.fetchone())

    Label(registration_window, text='Имя').grid(row=0, column=0)
    name_entry = Entry(registration_window)
    name_entry.grid(row=0, column=1)
    Label(registration_window, text='Фамилия').grid(row=1, column=0)
    last_name_entry = Entry(registration_window)
    last_name_entry.grid(row=1, column=1)
    Label(registration_window, text='Номер телефона').grid(row=3, column=0)
    phone_number_entry = Entry(registration_window)
    phone_number_entry.grid(row=3, column=1)
    Label(registration_window, text='Email').grid(row=4, column=0)
    email_entry = Entry(registration_window)
    email_entry.grid(row=4, column=1)
    Label(registration_window, text='Логин').grid(row=5, column=0)
    login_entry = Entry(registration_window)
    login_entry.grid(row=5, column=1)
    Label(registration_window, text='Пароль').grid(row=6, column=0)
    password_entry = Entry(registration_window)
    password_entry.grid(row=6, column=1)

    manager_choice = tkinter.Radiobutton(registration_window,
                                         text='Менеджер',
                                         variable=role_selection,
                                         value='manager',
                                         command=select_role)
    employee_choice = tkinter.Radiobutton(registration_window,
                                          text='Сотрудник',
                                          variable=role_selection,
                                          value='employee',
                                          command=select_role)
    employee_choice.grid(row=7, column=1, sticky='we')
    manager_choice.grid(row=7, column=0, sticky='we')

    submit_button = Button(registration_window, text='Готово')
    submit_button.grid(row=10, column=0, columnspan=2, sticky='we')

    pass


widght = 600
height = 500
window = Tk()
window.title('lab7-8')
window.geometry(f'{widght}x{height}')

main_label = Label(window, text='Авторизация', font='bold')
main_label.grid(row=0, column=0, columnspan=2, sticky='we')

login_label = Label(window, text='Логин')
login_label.grid(row=1, column=0, sticky='we')

password_label = Label(window, text='Пароль')
password_label.grid(row=2, column=0, sticky='we')

login_entry = Entry(window)
login_entry.grid(row=1, column=1, sticky='we')

password_entry = Entry(window)
password_entry.grid(row=2, column=1, sticky='we')

entry_button = Button(text='Вход', command=login)
entry_button.grid(row=4, column=0, columnspan=2, sticky='we')

register_button = Button(text='Регистрация', command=registration)
register_button.grid(row=5, column=0, columnspan=2, sticky='we')

role_selection = tkinter.StringVar()

# test_button = Button(text='Тест', command=show_current_user)
# test_button.grid(row=6, column=0, columnspan=2, sticky='we')

window.mainloop()

cursor.close()
connection.close()
print("[INFO] PostgresSQL connection closed")
