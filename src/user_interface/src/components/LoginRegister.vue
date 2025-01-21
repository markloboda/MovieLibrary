<template>
    <div>
        <h1>User Management</h1>

        <h2>Register</h2>
        <form @submit.prevent="register">
            <label for="registerEmail">Email:</label>
            <input type="email" id="registerEmail" v-model="registerData.email" required />
            <label for="registerPassword">Password:</label>
            <input type="password" id="registerPassword" v-model="registerData.password" required minlength="6" />
            <button type="submit">Register</button>
        </form>

        <h2>Login</h2>
        <form @submit.prevent="login">
            <label for="loginEmail">Email:</label>
            <input type="email" id="loginEmail" v-model="loginData.email" required />
            <label for="loginPassword">Password:</label>
            <input type="password" id="loginPassword" v-model="loginData.password" required />
            <button type="submit">Login</button>
        </form>

        <h3>Clear DB</h3>
        <button @click="clearDB">Clear DB</button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            url: "http://165.227.245.243/login-register",
            registerData: {
                email: "",
                password: "",
            },
            loginData: {
                email: "test@a.com",
                password: "123123",
            },
        };
    },
    methods: {
        async register() {
            if (this.registerData.password.length < 6) {
                alert("Password must be at least 6 characters long.");
                return;
            }

            try {
                const response = await fetch(`${this.url}/register`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(this.registerData),
                });

                if (response.ok) {
                    const result = await response.json();
                    alert(result.message);
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.message}`);
                }
            } catch (err) {
                console.error("Registration error:", err);
                alert("An unexpected error occurred.");
            }
        },
        async login() {
            try {
                const response = await fetch(`${this.url}/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(this.loginData),
                });

                if (response.ok) {
                    const result = await response.json();
                    alert(result.message);
                    localStorage.setItem("token", result.token);
                    window.location.href = "/browse_library.html";
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.message}`);
                }
            } catch (err) {
                console.error("Login error:", err);
                alert("An unexpected error occurred.");
            }
        },
        async clearDB() {
            try {
                const response = await fetch(`${this.url}/clearDB`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                });

                if (response.ok) {
                    const result = await response.json();
                    alert(result.message);
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.message}`);
                }
            } catch (err) {
                console.error("Clear DB error:", err);
                alert("An unexpected error occurred.");
            }
        },
    },
};
</script>

<style scoped></style>