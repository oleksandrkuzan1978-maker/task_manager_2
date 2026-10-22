if __package__:
    from .bootstrap import setup_django
else:
    from bootstrap import setup_django

setup_django()

# 1. Импортируем модель User и класс Count
from django.db.models import Count
from django.contrib.auth import get_user_model

print('\n--- ЗА ДЗ: ЗАДАНИЕ 6: Количество задач для каждого пользователя ---')

# 3. Напишите запрос, который получит количество задач для каждого пользователя.
# 4. С помощью values_list указываем, что хотим работать только с конкретными полями.
User = get_user_model()
count_of_tasks_to_user = User.objects.annotate(
    count_of_tasks=Count('tasks__id')
).values_list('username', 'count_of_tasks')

# Выведем SQL-запрос в консоль для наглядности (как на слайде решения)
print("Сгенерированный SQL-запрос:")
print(count_of_tasks_to_user.query)
print("-" * 50)

# 5. Выведите как результат никнейм разработчика и количество прикреплённых задач
for username, count_of_tasks in count_of_tasks_to_user:
    print(f"Developer - {username} | Count of tasks: {count_of_tasks}")
