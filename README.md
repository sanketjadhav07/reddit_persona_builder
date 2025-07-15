# Reddit User Persona Builder

## Overview

This project is a Python script that takes a Reddit user's profile URL as input, scrapes their comments and posts, and builds a detailed user persona based on the extracted information. The user persona is then saved to a text file, with citations for each characteristic derived from the user's posts and comments.

## Features

- Input a Reddit profile URL or username.
- Scrape recent posts and comments from the specified Reddit user.
- Perform simple NLP analysis to extract top keywords.
- Build a user persona using OpenAI's language model.
- Save the generated user persona to a text file, including citations for each characteristic.

## Technologies Used

- Python
- PRAW (Python Reddit API Wrapper)
- NLTK (Natural Language Toolkit)
- OpenAI API
- dotenv (for environment variable management)

## Prerequisites

- Python 3.12.
- A Reddit account to create an application and obtain API credentials.
- An OpenAI account to access the language model.
