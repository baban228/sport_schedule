# Nutrition API Endpoints

| Метод | URL | Описание | Тело запроса (POST) | Ответ |
|-------|-----|----------|-------------------|-------|
| **GET** | `/api/nutrition/products/` | Список всех продуктов | — | Список продуктов |
| **GET** | `/api/nutrition/products/?search=<query>` | Поиск продуктов по имени | — | Список продуктов с фильтром |
| **POST** | `/api/nutrition/products/` | Добавить новый продукт | `{ "name": "Курица", "calories": 165, "protein": 31, "fat": 3.6, "carbs": 0 }` | Созданный продукт |
| **GET** | `/api/nutrition/meals/` | Список всех приемов пищи пользователя | — | Список meals с MealItems |
| **POST** | `/api/nutrition/meals/` | Добавить новый прием пищи | `{ "meal_type": "lunch", "date": "2026-04-05" }` | Созданный meal |
| **GET** | `/api/nutrition/meals/today/` | Все приемы пищи за сегодня | — | Список сегодняшних meals с MealItems |
| **GET** | `/api/nutrition/meal-items/` | Список всех элементов еды | — | Список MealItems |
| **POST** | `/api/nutrition/meal-items/` | Добавить элемент еды в прием пищи | `{ "meal": 1, "product": 2, "weight": 150 }` | Созданный MealItem |
| **GET** | `/api/nutrition/nutrition-stats/today/` | Итоговая статистика за сегодня (КБЖУ) | — | `{ "calories": 247.5, "protein": 46.5, "fat": 5.4, "carbs": 0 }` |
| **GET** | `/api/nutrition/nutrition-stats/week/` | Статистика за последние 7 дней (для графика) | — | `[ { "date": "2026-04-01", "calories": 1800, "protein": 120, "fat": 60, "carbs": 200 }, ... ]` |

### Примечания
- Все запросы требуют аутентификации (только авторизованные пользователи).
- POST-запросы автоматически связывают объекты с текущим пользователем (`request.user`).
- Статистика за неделю возвращается в порядке от старого дня к сего