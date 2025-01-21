<template>
    <div class="login-register">
        <div class="form-container">
            <h2>Register</h2>
            <form @submit.prevent="register">
                <div class="form-group">
                    <label for="registerEmail">Email:</label>
                    <input type="email" id="registerEmail" v-model="registerData.email" required />
                </div>
                <div class="form-group">
                    <label for="registerPassword">Password:</label>
                    <input type="password" id="registerPassword" v-model="registerData.password" required />
                </div>
                <button type="submit" class="btn">Register</button>
            </form>
        </div>

        <div class="form-container">
            <h2>Login</h2>
            <form @submit.prevent="login">
                <div class="form-group">
                    <label for="loginEmail">Email:</label>
                    <input type="email" id="loginEmail" v-model="loginData.email" required />
                </div>
                <div class="form-group">
                    <label for="loginPassword">Password:</label>
                    <input type="password" id="loginPassword" v-model="loginData.password" required />
                </div>
                <button type="submit" class="btn">Login</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            url: "http://165.227.245.243/service/login-register",
            registerData: {
                email: "",
                password: "",
            },
            loginData: {
                email: "",
                password: "",
            },
            userData: {
                user_id: 0,
                email: "",
            }
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
                    body: JSON.stringify(this.registerData),
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
                console.error("Registration error:", err);
                alert("An unexpected error occurred.");
            }
        },
        async login() {
            try {
                const response = await fetch(`${this.url}/login`, {
                    method: "POST",
                    credentials: 'include',
                    body: JSON.stringify(this.loginData),
                    headers: { "Content-Type": "application/json" },
                });

                if (response.ok) {
                    alert("Login successful");
                    this.checkToken();

                    // Redirect to the home page
                    // this.$router.push("/");
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.message}`);
                }
            } catch (err) {
                console.error("Login error:", err);
                alert("An unexpected error occurred.");
            }
        },
        async checkToken() {
            try {
                const response = await fetch(`${this.url}/check-token`, {
                    method: "GET",
                    credentials: 'include'
                });

                if (response.ok) {
                    const result = await response.json();
                    this.userData = result;
                    alert("User data:", this.userData);
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.message}`);
                }
            } catch (err) {
                console.error("Check token error:", err);
            }
        }
    },
};
</script>

<style scoped>
.login-register {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}

.form-container {
    width: 100%;
    max-width: 400px;
    margin-bottom: 20px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.form-group input {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.btn {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.btn:hover {
    background-color: #0056b3;
}
</style>