import requests
import sys

BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/login/"
API_URL = f"{BASE_URL}/api/nutrition/products/"
USER, PASS = "test", "123456789"

def get_csrf(session):
    r = session.get(LOGIN_URL)
    return session.cookies.get('csrftoken')

def login(session, csrf):
    r = session.post(LOGIN_URL, headers={'X-CSRFToken': csrf}, data={
        'username': USER, 'password': PASS, 'csrfmiddlewaretoken': csrf
    }, allow_redirects=True)
    return 'login' not in r.url.lower() and r.status_code == 200

def run_tests(session, csrf):
    cases = [
        {"name": "", "calories": 100, "protein": 0, "fat": 0, "carbs": 0},
        {"name": "Test", "protein": 0, "fat": 0, "carbs": 0},  # no calories
        {"name": "Test", "calories": -10, "protein": 0, "fat": 0, "carbs": 0},
        {"name": "Test", "calories": "abc", "protein": 0, "fat": 0, "carbs": 0},
        {"name": "A"*300, "calories": 100, "protein": 0, "fat": 0, "carbs": 0},
        {"name": "Test'; DROP TABLE--", "calories": 100, "protein": 0, "fat": 0, "carbs": 0},
        {"name": "Apple", "calories": 52, "protein": 0.3, "fat": 0.2, "carbs": 14},  
    ]
    
    stats = {}
    for data in cases:
        r = session.post(API_URL, headers={'X-CSRFToken': csrf, 'Content-Type': 'application/json'}, json=data)
        stats[r.status_code] = stats.get(r.status_code, 0) + 1
    return stats

if __name__ == "__main__":
    s = requests.Session()
    csrf = get_csrf(s)
    if not csrf or not login(s, csrf):
        print("❌ Ошибка: не удалось авторизоваться")
        sys.exit(1)
    
    results = run_tests(s, get_csrf(s))
    
    total = sum(results.values())
    success = results.get(201, 0) + results.get(200, 0)
    errors = total - success
    
    print("\n" + "═"*40)
    print("Тесты завершены")
    print(f"Всего запросов: {total}")
    print(f"Успешных (200/201): {success}")
    print(f"Отклонено/ошибок: {errors}")
    print(f"Детализация по статусам: {dict(sorted(results.items()))}")
    print("═"*40)