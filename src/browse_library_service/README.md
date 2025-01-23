# Browse Library Service
Used to search for movies by title from an external API.

## Endpoints

### `GET /service/browse-library/search`

Search for movies by title.

#### Request Parameters:

| Parameter | Type   | Required | Description                  |
|-----------|--------|----------|------------------------------|
| `title`   | string | Yes      | The title of the movie to search for. |

#### Responses:

- **200 OK**
  ```json
  {
    "Response": "True",
    "Search": [
      {
        "Poster": "URL to poster image",
        "Title": "Movie Title",
        "Type": "movie",
        "Year": "2021",
        "imdbID": "tt1234567",
      }
    ],
    "totalResults": "100"
  }
  ```

- **400 Bad Request**
  ```json
  {
    "code":400,
    "message": "Title parameter is required",
    "status": "Bad Request"
  }
  ```

- **500 Internal Server Error**
  ```json
  {
    "code":500,
    "message": "Internal Server Error",
    "status": "Internal Server Error"
  }
  {
    "code":500,
    "message": "Title parameter is required",
    "status": "Internal Server Error"
  }
  ```