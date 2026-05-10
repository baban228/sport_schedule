(function() {
    const tableBody = document.querySelector('#teacher-groups-table tbody');
    if (!tableBody) return;

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

    async function loadTeacherGroupsFixed() {
        try {
            const res = await axios.get('/api/teacher-groups/', {
                withCredentials: true,
                headers: { 'X-CSRFToken': csrfToken }
            });

            console.log('Groups loaded (Fixed):', res.data);
            tableBody.innerHTML = '';

            if (!res.data || res.data.length === 0) {
                 tableBody.innerHTML = `
                    <tr>
                        <td colspan="4" class="text-center py-4 text-white-50">
                            У вас пока нет назначенных групп
                        </td>
                    </tr>`;
                 return;
            }

            res.data.forEach(group => {
                let studentsText = '-';
                if (group.students && Array.isArray(group.students) && group.students.length > 0) {
                    studentsText = group.students.map(s => s.username).join(', ');
                }

                const daysMap = {
                    'Mon': 'Понедельник', 'Tue': 'Вторник', 'Wed': 'Среда',
                    'Thu': 'Четверг', 'Fri': 'Пятница', 'Sat': 'Суббота', 'Sun': 'Воскресенье'
                };
                const dayDisplay = daysMap[group.day_of_week] || group.day_of_week || '-';

                const timeDisplay = group.start_time || '-';

                const rowHtml = `
                    <tr>
                        <td class="fw-bold" style="color: white;">${group.name}</td>
                        <td>${studentsText}</td>
                        <td>${dayDisplay}</td>
                        <td>${timeDisplay}</td>
                    </tr>
                `;

                tableBody.insertAdjacentHTML('beforeend', rowHtml);
            });
        } catch (err) {
            console.error('Error loading teacher groups:', err);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center py-4 text-danger">
                        <i class="fas fa-exclamation-triangle me-2"></i>Ошибка загрузки данных
                    </td>
                </tr>`;
        }
    }

    window.addEventListener('load', () => {

        setTimeout(loadTeacherGroupsFixed, 100);
    });

})();