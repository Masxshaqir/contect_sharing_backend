# Content Sharing Platform

This project is a content-sharing platform developed using Django Rest Framework (DRF) for the backend and React.js for the frontend. The platform allows users to register, log in, create posts, comment on posts, and vote on posts. The platform also supports following users and managing friendships.

## Features

### User Management
- **Registration**: Users can register with their email and create a profile.
- **Login/Logout**: Users can log in and out of their accounts.
- **Profile Management**: Users can update their profile information.
- **Friendship**: Users can add or remove friends and follow other users.

### Content Management
- **Post Creation**: Users can create posts with titles, content, images, and hashtags.
- **Comments**: Users can comment on posts.
- **Voting**: Users can vote on posts.
- **Hashtags**: Posts can include hashtags, and users can filter posts by hashtags.

## API Endpoints

### Accounts (`/accounts/`)
- `POST /register/`: Register a new user.
- `POST /login/`: Log in a user.
- `POST /logout/`: Log out a user.
- `POST /get_profile/`: Get the profile of the logged-in user.
- `POST /add_friend/`: Add a friend by email.
- `GET /get_all_users/`: Get a list of all users excluding the logged-in user.
- `GET /get_following_users/`: Get a list of users followed by the logged-in user.
- `PUT /update_profile/`: Update the profile of the logged-in user.
- `DELETE /delete_friend/`: Remove a friend by email.

### Posts (`/posts/`)
- `POST /add_post/`: Add a new post.
- `GET /get_all_posts/`: Retrieve all posts.
- `PUT /update_post/`: Update an existing post.
- `DELETE /delete_post/`: Delete a post.
- `POST /add_comment/`: Add a comment to a post.
- `PUT /update_comment/`: Update an existing comment.
- `DELETE /delete_comment/`: Delete a comment.
- `POST /add_update_vote/`: Add or update a vote on a post.
- `POST /get_votes/`: Get all votes for a post.
- `GET /get_all_hashtags/`: Get a list of all unique hashtags.
- `GET /post_filter_list/`: Filter and search posts by various criteria.

## Setup and Installation

### Backend

1. Clone the repository:

    ```bash
    git clone [<repository-url>](https://github.com/Masxshaqir/contect_sharing_backend.git)
    cd content_sharing
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```



## Usage

After setting up the project, you can access the platform by navigating to `http://localhost:8000/` in your web browser. Use the admin panel at `http://localhost:8000/admin/` to manage users, posts, comments, and other data.

## Technologies Used
- **Backend**: Django, Django Rest Framework
- **Frontend**: React.js
- **Database**: SQLite (default, can be changed to PostgreSQL, MySQL, etc.)
- **Authentication**: Token-based authentication with Django Rest Framework's authtoken.

## Contributing

If you'd like to contribute to this project, please fork the repository and use a feature branch. Pull requests are warmly welcome.
