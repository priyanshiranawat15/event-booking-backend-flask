from app import create_app


# Keep this name for current App Engine gunicorn entrypoint: main:ticketdemo
# defined in app.yaml.
ticketdemo = create_app()


if __name__ == "__main__":
    ticketdemo.run()
