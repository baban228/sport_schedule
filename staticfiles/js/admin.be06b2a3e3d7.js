function showGroupForm() {
    document.getElementById('group-form').style.display = 'block';
}

// Загрузка всех групп
async function loadGroups() {
    try {
        const res = await axios.get('/api/groups/', {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        });
        const tbody = document.querySelector('#groups-table tbody');
        tbody.innerHTML = '';
        res.data.forEach(group => {
            tbody.innerHTML += `
                <tr>
                    <td>${group.name}</td>
                    <td>${group.teacher}</td>
                    <td>${group.students.join(', ')}</td>
                </tr>
            `;
        });
    } catch (err) {
        console.error(err);
    }
}

// Создание группы
async function createGroup() {
    const name = document.getElementById('group-name').value;
    const teacher = document.getElementById('group-teacher').value;
    const students = document.getElementById('group-students').value.split(',').map(s => s.trim());

    try {
        await axios.post('/api/groups/', { name, teacher, students }, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        });
        loadGroups();
        document.getElementById('group-form').style.display = 'none';
    } catch (err) {
        console.error(err);
    }
}

window.onload = loadGroups;