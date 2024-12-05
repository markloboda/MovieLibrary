# Movie Library

## Authors:
- Mark Loboda (ml7363@student.uni-lj.si)

## Description
The **Movie Library** application is a collection of movies designed to simplify the process of browsing for movies, adding them to a watchlist and marking them as already watched.
It addresses a problem of users struggling to keep track of movies they want to watch, forgetting which movies they've seen, and spending too much time deciding on which movie they want to watch.
The application Movie Library offers an interface for organizing and tracking movies.
The main goal of the project is to create a platform that improves **browsing for new movies**, **organizing already-watched movies**, and **creating watchlists of new movies**.

## Tools and technologies used
The main text and code editor used in the project is **Visual Studio Code**.
For version control and hosting of the project repository, I rely on **Git** and **GitHub**.
The main web framework used in developing the backend is a **Python-based web framework Flask**, which offers a lightweight and flexible foundation with extensive community support and documentation.
The application is containerized with **Docker** and orchestrated using **Kubernetes**.

## Architecture schema
![Architecture schema](assets/architecture-schema-dark.png)

## List of microservice functionalities
- **Login register microservice**
    - Creating a new user and adding it to the database of all users;
    - Logging into an existing user;
    - Forgot password option on existing user;
    - Remember me option to stay logged in.

- **Browse movies microservice**
    - Get recommended movies based on current already watched and watchlisted;
    - Browse all movies;
    - Sort movies by parameters;
    - Search for movies;
    - Add movies to watchlist and to already watched;
    - Filter movies by categories and parameters.

- **Watchlist & already watched microservice**
    - Browse movies added to watchlist and already watched list
    - Remove movies from watchlist and already watched list
    - Sort movies by date of added to each list and by other parameters;
    - Filter movies by categories and parameters.

## Use cases
1. A new user launches the web application for the first time and want's to register.
2. Existing user launches the web application and want's to login to his account.
3. Existing user launches the web application and want's to login to his account, but doesn't remember the password. He uses the forgot password functionality.
4. Existing user launches the web application and logs in to his account. While logging in, he checks the remember me functionality. After he successfully logs in, he goes to his watchlist and add a movie he watched yesterday to already watched. After, he goes into the browse movies tab and searches all recent comedy movies that have been published. He select one of the listed and adds it to his watchlist. After watching it, he goes into the watchlist and adds the movie to already watched.