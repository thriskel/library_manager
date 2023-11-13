# Base it on the official python image
FROM python:3.9

# Set library_manager as the working directory
WORKDIR /library_manager

# Copy the rest of the files into the working directory
COPY /library_manager .

# Install the requirements
RUN pip install -r requirements.txt

# Set the environment variables
ENV DJANGO_SETTINGS_MODULE=library_manager.settings
ENV DJANGO_SECRET_KEY=django-insecure-b0+lfl5bu&4!=3-a=hopg@^4$8iyq01$u98!@h83m4rwcw78bz
ENV DJANGO_ALLOWED_HOSTS=*
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=something@test.com
ENV PYTHONBUFFERED=1

# Expose port 8000
EXPOSE 8000

# Set up the entrypoint
ENTRYPOINT ["/library_manager/django-setup.sh"]
