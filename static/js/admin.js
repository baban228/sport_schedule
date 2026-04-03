// admin.js
(function() {
    console.log('admin.js загружен');

    // Получаем CSRF токен
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
        console.log('CSRF токен admin:', cookieValue);
        return cookieValue;
    }

    const csrfToken = getCookie('csrftoken');

    // Показываем/скрываем форму добавления группы
    function toggleGroupForm() {
        const form = document.getElementById('group-form');
        if (!form) return;
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
        console.log('toggleGroupForm:', form.style.display);
    }
    window.toggleGroupForm = toggleGroupForm;

    // Загрузка всех групп
    async function loadGroups() {
        const tbody = document.querySelector('#groups-table tbody');
        if (!tbody) {
            console.warn('Таблица #groups-table не найдена, пропускаем loadGroups');
            return;
        }

        try {
            const res = await axios.get('/api/groups/', {
                withCredentials: true,
                headers: { 'X-CSRFToken': csrfToken }
            });

            console.log('Получены группы:', res.data);

            tbody.innerHTML = '';
            res.data.forEach(group => {
                const studentIds = group.students.join(', ');
                tbody.innerHTML += `
                    <tr>
                        <td>${group.name}</td>
                        <td>${group.teacher}</td>
                        <td>${studentIds}</td>
                        <td>${group.day_of_week || '-'}</td>
                        <td>${group.start_time || '-'}</td>
                    </tr>
                `;
            });
        } catch (err) {
            console.error('Ошибка загрузки групп:', err.response || err);
        }
    }

    // Создание новой группы
    async function createGroup() {
        const name = document.getElementById('group-name').value;
        const teacher = parseInt(document.getElementById('group-teacher').value);
        const students = document.getElementById('group-students').value
            .split(',')
            .map(s => parseInt(s.trim()))
            .filter(s => !isNaN(s));
        const day_of_week = document.getElementById('group-day').value;
        const start_time = document.getElementById('group-time').value;

        if (!name || isNaN(teacher) || !day_of_week || !start_time) {
            alert('Введите название, ID учителя, день недели и время начала!');
            return;
        }

        try {
            const res = await axios.post('/api/groups/', { name, teacher, students, day_of_week, start_time }, {
                withCredentials: true,
                headers: { 'X-CSRFToken': csrfToken }
            });
            console.log('Группа создана:', res.data);

            document.getElementById('group-name').value = '';
            document.getElementById('group-teacher').value = '';
            document.getElementById('group-students').value = '';
            document.getElementById('group-day').value = '';
            document.getElementById('group-time').value = '';
            const form = document.getElementById('group-form');
            if (form) form.style.display = 'none';

            loadGroups();
        } catch (err) {
            console.error('Ошибка создания группы:', err.response || err);
            alert('Не удалось создать группу: ' + (err.response?.status || 'Ошибка'));
        }
    }
    window.createGroup = createGroup;

    // Запуск после загрузки страницы
    window.addEventListener('DOMContentLoaded', () => {
        console.log('Страница admin загружена, запускаем loadGroups...');
        loadGroups();
    });

})();