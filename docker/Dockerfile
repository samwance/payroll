# Use the official Python image as the builder
FROM python:3.11.8-alpine3.19 as builder

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install psycopg2 dependencies and other required packages
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev g++ libffi-dev cairo-dev

# Copy dependency files
COPY poetry.lock pyproject.toml ./

# Install Poetry
RUN pip install --no-cache-dir poetry==1.4.2

# Export dependencies to requirements.txt
RUN poetry export --without-hashes --without dev,test -f requirements.txt -o requirements.txt

# Install dependencies as wheels
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

#########
# FINAL #
#########

# Pull official base image
FROM python:3.11.8-alpine3.19

# Create app user and group
RUN addgroup -S app && adduser -S app -G app

# Set environment variable for app home
ENV APP_HOME=/app

# Create app directory
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Install runtime dependencies
RUN apk update && apk add --no-cache libpq libffi-dev build-base libffi

# Copy wheels and requirements from the builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install the application dependencies
RUN pip install --no-cache-dir /wheels/*

# Copy the application code
COPY . $APP_HOME

# Set permissions for the app user
RUN chown -R app:app $APP_HOME

# Change to the app user
USER app

# Set the working directory
WORKDIR $APP_HOME

# Specify the command to run your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
