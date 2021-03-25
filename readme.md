# Flask App accessed by Vue App OAuth Demo
Server side code running an authenticated API and a browser based client.
In practice these will be two separate repositories.
They are presented together here for convenience.

## Flask App (API)
The flask app has resources that require auth.

- Authenticates user via oauth2
- Tracks logged in user via session
- Runs on localhost:5000

## Vue App (UI)
The Vue client has visualizations for the protected resources.

- Has callback route that handles talking to api callback endpoint.
- Displays logged in status
- Runs on localhost:8080

## Configure
1. Create project in Google Cloud Platform
2. Configure Web application credentials
    - Authorized JavaScript origins:
      - http://127.0.0.1:8080
      - http://localhost:8080
      - http://127.0.0.1:5000
    - Authorized redirect URIs:
      - http://127.0.0.1:5000/auth_callback
3. Download client\_secret json, move to `client_secret.json` in flaskapp dir.
4. Create `client_config.js` containing client\_id in vue\_ui/src dir.

## Run
1. Start flask app
2. Start serving Vue app
3. Open Vue app in browser  

## Notes
- Server side API has endpoints for both web server application flow and server-side flow.
- Browsing API uses web server application flow similar to existing work.
- Vue UI uses server-side flow by initiating auth and passing one-time code to API.

