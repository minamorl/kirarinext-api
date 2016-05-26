import dotenv
import os
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


from kirarinext.server import app


def main():
    app.run(port=9010, debug=True)

if __name__ == '__main__':
    main()
