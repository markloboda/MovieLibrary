const url = "http://127.0.0.1:57929";

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    if (password.length < 6) {
        alert("Password must be at least 6 characters long.");
        return;
    }

    const response = await fetch(`${url}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            "email": email,
            "password": password
        })
    });
    if (response.ok) {
        const result = await response.json();
        alert(result.message);
    } else {
        const error = await response.json();
        alert(`Error: ${error.message}`);
    }
});

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const response = await fetch(`${url}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "email": email,
            "password": password
        })
    });
    if (response.ok) {
        const result = await response.json();
        alert(result.message);
    } else {
        const error = await response.json();
        alert(`Error: ${error.message}`);
    }
});

document.getElementById('fetchUsers').addEventListener('click', async () => {
    const response = await fetch(`${url}/users`);
    const users = await response.json();
    const usersList = document.getElementById('usersList');
    usersList.innerHTML = '';
    users.forEach(user => {
        const li = document.createElement('li');
        li.textContent = user.email;
        usersList.appendChild(li);
    });
});