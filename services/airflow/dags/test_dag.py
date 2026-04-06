from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Аргументы по умолчанию
default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Создаем DAG
with DAG(
    'test_dag',
    default_args=default_args,
    description='Простой тестовый DAG',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['example'],
) as dag:

    # Задача 1: печатает дату
    print_date = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    # Задача 2: приветствие
    def print_hello():
        print("Привет от Airflow!")
        return "Hello!"

    hello_task = PythonOperator(
        task_id='hello_task',
        python_callable=print_hello,
    )

    # Задача 3: спим 5 секунд
    sleep_task = BashOperator(
        task_id='sleep_5_seconds',
        bash_command='sleep 5',
    )

    # Задача 4: финальная
    final_task = BashOperator(
        task_id='final_task',
        bash_command='echo "DAG выполнен успешно!"',
    )

    # Устанавливаем последовательность выполнения
    print_date >> hello_task >> sleep_task >> final_task