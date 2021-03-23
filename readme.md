# Flask App accessed by Vue App OAuth Demo
In practice these will be two separate repositories.
They are presented together here for convenience.

## Flask App (API)
The flask app has resources that require auth.

- Authenticates user via oauth2
- Tracks logged in user via session

## Vue App (UI)
The Vue client has visualizations for the protected resources.

- Has callback route that handles talking to api callback endpoint.
- Displays logged in status

## Run
1. Start flask app
2. Start serving Vue app
3. Open Vue app in browser  

