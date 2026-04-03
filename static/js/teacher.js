(function() {
    console.log('teacher.js загружен');

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
        console.log('CSRF токен teacher:', cookieValue);
        return cookieValue;
    }

    const csrfToken = getCookie('csrftoken');

    // Загрузка групп для учителя
    async function loadTeacherGroups() {
        const tbody = document.querySelector('#teacher-groups-table tbody');
        if (!tbody) {
            console.warn('Таблица #teacher-groups-table не найдена, пропускаем loadTeacherGroups');
            return;
        }

        try {
            const res = await axios.get('/api/teacher-groups/', {
                withCredentials: true,
                headers: { 'X-CSRFToken': csrfToken }
            });

            console.log('Получены группы учителя:', res.data);

            tbody.innerHTML = '';
            res.data.forEach(group => {
                const students = group.students.map(s => s.username).join(', ');
                tbody.innerHTML += `
                    <tr>
                        <td>${group.name}</td>
                        <td>${group.teacher.username}</td>
                        <td>${students}</td>
                    </tr>
                `;
            });
        } catch (err) {
            console.error('Ошибка загрузки групп учителя:', err.response || err);
            alert('Не удалось загрузить группы');
        }
    }

    window.addEventListener('DOMContentLoaded', () => {
        console.log('Страница teacher загружена, запускаем loadTeacherGroups...');
        loadTeacherGroups();
    });
})();