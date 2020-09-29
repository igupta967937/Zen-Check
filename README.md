How to run the ZenCheck site using Django:

NOTE: Guide assumes using OSX or Linux. If Windows, replace `python manage.py runserver` with `py manage.py runserver` in Step 4.

Step 1. Extract .zip file, then cd into the path that the zip file has been extracted to- you should be within zenchck.

Step 2. Install Python 3.7.6 (anything above 3.1 will likely work, but 3.7.6 is recommended for best compatibility), and pip, if not done previously.

Step 3. To install the required libraries in Python, run `pip install requirements.txt`

Step 4. After installing required Python libraries, ensuring you are still in the path that the zip file has been extracted to (if not done already), run `python manage.py runserver`

Step 5. If you want to turn off debug notifications and instead receive 404 errors, set `Debug = FALSE` in the mysite/settings.py

Step 6. To access the admin portal of the site, append `/admin` to the server address in your browser (i.e. if you are running on the default `http://127.0.0.1:8000/`, go to `http://127.0.0.1:8000/admin`). Here, you can log-in using admin as username and NEMaUg8Y as password.

USEFUL INFORMATION:

It is recommended you use Google Chrome as your web-browser. Also ensure that your browser's window size is full-screen or at least 90% width. Much of the CSS is attributed from Bootstrap 4.3.1, so you may lose styling when shrinking your window size.
