from app.app import app
import uvicorn
import os


if __name__ == "__main__":
    # get port from environment variable
    port = int(os.environ.get("PORT", 1234))
    uvicorn.run(app, host="127.0.0.1", port=port)