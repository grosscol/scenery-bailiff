# Flask App accessed by Vue App OAuth Demo
In practice these will be two separate repositories.
They are presented together here for convenience.

## Flask App (API)
The flask app has resources that require auth.

## Vue App (UI)
The Vue client has visualizations for the protected resources.

- Responsible for taking grant and getting authorization token
- Responsible for providing token during requests to flask api.

## Run
1. Start flask app
2. Start serving Vue app
3. Open Vue app in browser  

