# Social Networking API

## Problem Statement

This project aims to create a scalable, secure, and efficient API for a social networking application using Django Rest Framework. The API provides functionalities for user management, friend requests, notifications, and more.

## Table of Contents

-   [Installation](#installation)
-   [API Documentation](#api-documentation)
-   [Design Choices](#design-choices)
-   [Additional Features](#additional-features)
-   [Deployment](#deployment)
-   [Submission Requirements](#submission-requirements)
-   [Notes](#notes)

## Installation

### Prerequisites

-   Python 3.8+
-   PostgreSQL
-   Redis
-   Docker and Docker Compose (for deployment)

### Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Kayiro24/social-network.git
    cd social-networking-api
    ```

## API Documentation

Everything is setup you just have to call the APIs in postman and keys will be setup automatically. Easy Peasy.

## Authentication

The API uses Bearer token authentication. You must include the `access_token` in the Authorization header for requests that require authentication.

## API Endpoints

### User Endpoints

#### 1. Get User Details

-   **Endpoint:** `GET {{base_url}}/user/{{user_id}}/`
-   **Auth Required:** Yes (Bearer Token)
-   **Description:** Fetches the details of a specific user.

#### 2. Create User

-   **Endpoint:** `POST {{base_url}}/user/`
-   **Auth Required:** No
-   **Request Body:**
    ```json
    {
        "email": "example@gmail.com", // example
        "password": "@example123" // example
    }
    ```

#### 3. User Login

-   **Endpoint:** `POST {{base_url}}/user/login/`
-   **Auth Required:** No
-   **Request Body:**
    ```json
    {
        "email": "example@gmail.com", // example
        "password": "@example123" // example
    }
    ```

#### 4. Refresh Token

-   **Endpoint:** `POST {{base_url}}/user/token/refresh/?refresh_token={{refresh_token}}`
-   **Auth Required:** No
-   **Description:** Refreshes the access token using the provided refresh token.

### Friend Record Endpoints

#### 1. List Friends

-   **Endpoint:** `GET {{base_url}}/friend-record/?status=pending`
-   **Auth Required:** Yes (Bearer Token)
-   **Query Parameters:**
    -   `status`: Filter for the friend request status. (options: requested, pending, accepted, rejected, removed, blocked, un_block)

#### 2. Search Friend

-   **Endpoint:** `GET {{base_url}}/friend-record/search-friend/?query=lmao`
-   **Auth Required:** Yes (Bearer Token)
-   **Query Parameters:**
    -   `query`: The search term for finding friends.

#### 3. Add Friend

-   **Endpoint:** `POST {{base_url}}/friend-record/add-friend/`
-   **Auth Required:** Yes (Bearer Token)
-   **Request Body:**
    ```json
    {
        "friend_id": "{{friend_id}}"
    }
    ```

#### 4. Get Friend Details

-   **Endpoint:** `GET {{base_url}}/friend-record/{{friend_id}}`
-   **Auth Required:** Yes (Bearer Token)
-   **Description:** Fetches the details of a specific friend.

#### 5. Update Friend Request Status

-   **Endpoint:** `PATCH {{base_url}}/friend-record/{{friend_id}}/`
-   **Auth Required:** Yes (Bearer Token)
-   **Request Body:**
    ```json
    {
        "status": "accepted" // Choose from ['requested', 'pending', 'accepted', 'rejected', 'removed', 'blocked', 'un_block']
    }
    ```

## Variables

-   `base_url`: The base URL for the API.
-   `user_id`: The ID of the user.
-   `access_token`: The access token for authenticated requests.
-   `refresh_token`: The refresh token for token renewal.
-   `friend_id`: The ID of the friend.

## Testing

Ensure to run tests using your API client, like Postman, to validate the endpoints.

Now you can start interacting with the API!
