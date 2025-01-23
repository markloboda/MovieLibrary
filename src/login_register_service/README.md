# Login register service
This microservice handles authentication of users (user creation, logging in, logging out, confirming authentication).

## End Points

### POST /register
Registers a new user.

#### Request Body
```json
{
    "email": "email",
    "password": "password"
}
```

#### Response
- **201 Created**
```json
{
    "message": "User {email} created."
}
```

- **409 Conflict**
```json
{
    "message": "User {email} already exists."
}
```

### POST /login
Logs in a user.

#### Request Body
```json
{
    "email": "email",
    "password": "password"
}
```

#### Response
- **200 OK**
```json
{
    "message": "User {email} logged in."
}
```

- **401 Unauthorized**
```json
{
    "message": "Invalid credentials."
}
```

### POST /logout
Logs out a user.

#### Request Body
Cookie with "user_id"

#### Response
- **200 OK**
```json
{
    "message": "Logout successful."
}
```

- **401 Unauthorized**
```json
{
    "message": "Token is missing."
}
```

### POST /check-token
Checks if a token is valid.

#### Request Body
Cookie with "user_id"

#### Response
- **200 OK**
```json
{
  "user_id": "user.id",
   "email": "user.email"
}
```

- **401 Unauthorized**
```json
{
    "message": "Token is missing."
}
```
```json
{
    "message": "Token has expired."
}
```
```json
{
    "message": "Token is invalid."
}
```


