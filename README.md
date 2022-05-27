# BlogAPI Documentation

## Overview

This is a simple blog API that can be used to create, read, update and delete blog posts. I used the [`fastapi`](https://fastapi.tiangolo.com/) library to create this API, and [`Deta`](https://deta.sh/) to store the blog posts and user information. I am also using `DetaDrive` for the static files storage.


I wanted to create a personal blog website for myself, so I decided to create the blog API part using FastAPI and Deta over the weekend, am really excited to see how this project turns out.

---


## To Do

* [x] Create a blog post
* [x] Update a blog post
* [x] Delete a blog post
* [x] Show related post
* [x] User authentication
* [x] File upload
* [ ] Update post views when a blog post is viewed
* [ ] Live feed updates when a blog post is created
* [ ] Add comments to blog posts
* [ ] Search categories and tags
* [ ] Add a markdown editor

---


## Installation

    
    ```
    git clone https://github.com/jsaretin/blog-api.git
    cd blogapi
    pip install -r requirements.txt
    ```

## Running the API
    
    ```
    uvicorn main:app --reload
    ```

---

## Contributing

Contribution are highly welcome!

To contribute, please fork the repository and create a pull request.


## License

[`This project is licensed under the MIT License`](https://github.com/JSaretin/blog-api/blob/main/LICENSE)
