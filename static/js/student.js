(async function() {
  const calendarEl = document.getElementById('calendar');
  const popup = document.getElementById('popup');

  // Получаем CSRF токен из cookie
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrfToken = getCookie('csrftoken');

  // Загружаем группы ученика с API
  async function loadStudentGroups() {
    try {
      const res = await axios.get('/api/student-groups/', {
        withCredentials: true,
        headers: { 'X-CSRFToken': csrfToken }
      });

      const groups = res.data.map(g => ({
        name: g.name,
        teacher: g.teacher,
        color: g.color,
        day_of_week: g.day_of_week,
        start_time: g.start_time
      }));

      console.log('Группы ученика:', groups);
      renderCalendar(groups);
    } catch (err) {
      console.error('Ошибка загрузки групп ученика:', err.response || err);
    }
  }

  // Преобразуем день недели в число для JS Date (0 = Воскресенье)
  const dayMap = { 'Sun': 0, 'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6 };

  function renderCalendar(groups) {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();
    const firstDay = new Date(year, month, 1).getDay(); // 0=ВС
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Очистка календаря
    calendarEl.innerHTML = '';

    // Пустые ячейки до первого дня
    for (let i = 0; i < firstDay; i++) {
      calendarEl.appendChild(document.createElement('div'));
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const cell = document.createElement('div');
      cell.className = 'day';
      cell.textContent = day;

      const cellDay = new Date(year, month, day).getDay();

      const dayGroups = groups.filter(g => dayMap[g.day_of_week] === cellDay);
      if (dayGroups.length) {
        cell.classList.add('has-class');
        cell.style.backgroundColor = dayGroups[0].color; // берём цвет первой группы
        cell.addEventListener('click', () => {
          const info = dayGroups.map(g => `
            <strong>${g.name}</strong><br>
            ${g.teacher}<br>
            ${g.start_time}
          `).join('<hr>');
          popup.innerHTML = info;
          popup.style.display = 'block';
          popup.style.top = cell.offsetTop + 70 + 'px';
          popup.style.left = cell.offsetLeft + 'px';
        });
      }

      calendarEl.appendChild(cell);
    }

    document.body.addEventListener('click', e => {
      if (!e.target.classList.contains('day')) popup.style.display = 'none';
    });
  }

  // Запуск
  loadStudentGroups();
})();