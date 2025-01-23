<template>
  <div class="signin">
    <div v-if="notificationMessage" class="notification">{{ notificationMessage }}</div>
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
      apiUrl: "/service/login-register",
      notificationMessage: "",
      registerData: {
        email: "",
        password: "",
      },
      loginData: {
        email: "test@a.com",
        password: "123123",
      }
    };
  },
  methods: {
    openBrowseLibrary() {
      this.$router.push("/");
    },
    setNotification(message) {
      this.notificationMessage = message;
      setTimeout(() => {
        this.notificationMessage = "";
      }, 5000); // Clear the message after 5 seconds
    },
    async register() {
      if (this.registerData.password.length < 6) {
        let message = "Password must be at least 6 characters long.";
        alert(message);
        this.setNotification(message);
        return;
      }
      try {
        const response = await fetch(`${this.apiUrl}/register`, {
          method: "POST",
          body: JSON.stringify(this.registerData),
          headers: { "Content-Type": "application/json" },
        });
        if (response.ok) {
          let message = `User registered successfully!`;
          alert(message);
          this.setNotification(message);

          // login after registration
          this.loginData.email = this.registerData.email;
          this.loginData.password = this.registerData.password;
          this.login();
        } else {
          const error = await response.json();
          alert(`Error: ${error.message}`);

          if (response.status === 409) {
            // Email already exists.
            let message = "Email already exists.";
            this.setNotification(message);
            alert(message);
          } else {
            let message = "An unexpected error occurred while registring.";
            this.setNotification(message);
            alert(message);
          }
        }
      } catch (err) {
        let message = "An unexpected error occurred while registring.";
        this.setNotification(message);
        alert(message);
        console.error("Register error:", err);
      }
    },
    async login() {
      try {
        const response = await fetch(`${this.apiUrl}/login`, {
          method: "POST",
          credentials: "include",
          body: JSON.stringify(this.loginData),
          headers: { "Content-Type": "application/json" },
        });
        if (response.ok) {
          let successfull = await this.checkToken();
          if (successfull) {
            let message = "Logged in successfully!";
            this.setNotification(message);
            alert(message);
            this.openBrowseLibrary();
          }
        }
        else if (response.status === 401) {
          let message = "Invalid email or password.";
          this.setNotification(message);
          alert(message);
        }
        else {
          const error = await response.json();
          alert(`Error: ${error.message}`);
        }
      } catch (err) {
        let message = "An unexpected error occurred while logging in.";
        alert(message);
        this.setNotification(message);
        console.error("Login error:", err);
      }
    },
    async checkToken() {
      try {
        localStorage.removeItem("activeUser");
        const response = await fetch(`${this.apiUrl}/check-token`, {
          method: "GET",
          credentials: "include",
        });
        if (response.ok) {
          alert("Token is valid!");
          const result = await response.json();
          localStorage.setItem("activeUser", result["email"]);
          return true;
        } else {
          const error = await response.json();
          alert(`Error: ${error.message}`);
        }
      } catch (err) {
        console.error("Check token error:", err);
        alert("An unexpected error occurred while checking token.");
      }

      return false;
    },
  },
};
</script>

<style scoped>
.signin {
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
  padding-top: 5px;
  padding-bottom: 5px;
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
