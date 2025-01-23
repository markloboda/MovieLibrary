# Watchlist Service
Used to manage a user's watchlist of movies.

## Endpoints

### `POST /add-movie`
Add a movie to the user's watchlist.

#### Request Body
```json
Included token with user_id
{
  "added_date": "unix timestamp",
  "imdb_id": "string",
  "poster": "string",
  "title": "string",
  "type": "string",
  "year": "string"
}
```

#### Response
- **201 Created**
```json
{
  "message": "Movie {title} added to watchlist."
}
```

- **401 Unauthorized**
```json
{
  "message": "Token is missing or invalid."
}
```

- **409 Conflict**
```json
{
  "message": "Movie {title} is already in watchlist."
}
```

### `POST /remove-movie`
Remove a movie from the user's watchlist.

#### Request Body
Included token with user_id
```json
{
  "imdb_id": "string"
}
```

#### Response
- **200 OK**
```json
{
  "message": "Movie {title} removed from watchlist."
}
```

- **401 Unauthorized**
```json
{
  "message": "Token is invalid."
}
```
```json
{
  "message": "Token is missing."
}
```