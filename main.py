
import os
from website.app import create_app

# Must go outside of the main function so the docker
# image can detect and use it.
app = create_app()

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

