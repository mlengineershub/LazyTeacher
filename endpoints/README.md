# FastAPI Endpoints for Automatic Essay Grading

Welcome to the endpoints section of our Automatic Essay Grading project. This directory contains the FastAPI code to deploy our machine learning models as RESTful APIs, enabling real-time essay grading.

![FastAPI Logo](./logo.png)

## Overview

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. The key features of FastAPI are:

- **Fast to run:** High performance, on par with NodeJS and Go (thanks to Starlette and Pydantic).
- **Fast to code:** Great editor support. Completion everywhere. Less time debugging.
- **Easy to deploy:** With no need to worry about a specific way of doing things; you get automatic interactive API documentation (with Swagger UI).

## Setting Up

To set up and run FastAPI for our project, you will need to install the necessary packages:

```bash
pip install fastapi[all]
```

For more information and installation guides, visit the [FastAPI official documentation](https://fastapi.tiangolo.com/).

## API Documentation

Once the API is running, you can access the auto-generated interactive API documentation (provided by Swagger UI) at:

```bash
http://localhost:8000/docs
```

This will allow you to see all the operational endpoints and interact with them directly from your browser.

## Running the API

To start the FastAPI server, navigate to the endpoints directory and run:

```bash
uvicorn endpoint:app --reload
```

This command starts the server with live reloading enabled, which is useful during development.

## Contributing

We encourage contributions to enhance the API functionality or improve the deployment methods. If you have ideas or improvements, please open an issue or submit a pull request.