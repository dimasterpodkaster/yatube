# YaTube - Social Network Project

## Overview

This project is a social networking platform built with Django, allowing users to create and share posts, follow other users, and engage with content through comments and subscriptions. The application includes user authentication, pagination, caching, and error handling for a smooth user experience.

## Features

### Public Views

- **index**: Displays a paginated list of all posts, cached for 20 seconds.
- **group\_posts**: Displays posts related to a specific group.
- **profile**: Displays a user's profile, their posts, and follower statistics.
- **post\_view**: Displays a specific post along with comments.
- **view\_image**: Displays an image attached to a post.

### Authentication-Required Views

- **new\_post**: Allows logged-in users to create a new post.
- **post\_edit**: Allows the author of a post to edit it.
- **add\_comment**: Enables users to add comments to posts.
- **follow\_index**: Shows posts from users that the logged-in user follows.
- **profile\_follow**: Allows users to follow another user.
- **profile\_unfollow**: Allows users to unfollow another user.

### Error Handlers

- **page\_not\_found (404)**: Renders a custom 404 page.
- **server\_error (500)**: Renders a custom 500 page.

## Pagination

All post listings (index, group posts, profile posts, follow index) are paginated to display 10 posts per page.

## Caching

The `index` view is cached using Django's `cache_page` decorator.

## Authentication

All post-creation, editing, commenting, and following actions require user authentication. The `login_required` decorator ensures only authenticated users can perform these actions.

## Dependencies

- Django framework
- Django authentication system
- Django pagination
- Django ORM for database interactions

## Installation and Setup

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <project_directory>
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
5. Run the development server:
   ```sh
   python manage.py runserver
   ```

## Usage

- **Creating Posts**: Users can create, edit, and delete posts with text and images.
- **Following Users**: Users can follow and unfollow others to customize their feed.
- **Commenting**: Users can leave comments on posts.
- **User Profiles**: Each user has a profile displaying their posts and follower statistics.
- **Group Pages**: Users can view posts related to specific topics or groups.
- **Authentication**: Secure user authentication system with login/logout functionality.

## YaTube
Социальная сеть для блогеров

Это учебный проект, созданный в целях практики работы с Python.
