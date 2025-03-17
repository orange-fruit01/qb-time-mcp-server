require('dotenv').config();
const express = require('express');
const OAuthClient = require('intuit-oauth');
const fs = require('fs');
const path = require('path');

// Create Express app
const app = express();
const port = 3001;

// Load environment variables
const clientId = process.env.QB_CLIENT_ID;
const clientSecret = process.env.QB_CLIENT_SECRET;
const redirectUri = `http://localhost:${port}/callback`;
const environment = process.env.QB_ENVIRONMENT || 'production';

// Create OAuth client
const oauthClient = new OAuthClient({
  clientId,
  clientSecret,
  environment: environment === 'sandbox' ? 'sandbox' : 'production',
  redirectUri,
});

// Routes
app.get('/', (req, res) => {
  // Generate authorization URL
  const authUri = oauthClient.authorizeUri({
    scope: [
      OAuthClient.scopes.Accounting,
      OAuthClient.scopes.OpenId,
      OAuthClient.scopes.Profile,
      OAuthClient.scopes.Email,
      OAuthClient.scopes.Phone,
      OAuthClient.scopes.Address
    ],
    state: 'testState',
  });
  
  res.send(`
    <h1>QuickBooks OAuth Setup</h1>
    <p>Click the button below to authorize this application with QuickBooks:</p>
    <a href="${authUri}" style="display: inline-block; background-color: #2CA01C; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
      Connect to QuickBooks
    </a>
  `);
});

app.get('/callback', async (req, res) => {
  try {
    // Exchange authorization code for tokens
    const authResponse = await oauthClient.createToken(req.url);
    const tokens = authResponse.getJson();
    
    // Update .env file with new tokens
    const envPath = path.resolve(process.cwd(), '.env');
    let envContent = fs.readFileSync(envPath, 'utf8');
    
    // Replace tokens in .env
    envContent = envContent.replace(/QB_ACCESS_TOKEN=.*/, `QB_ACCESS_TOKEN=${tokens.access_token}`);
    envContent = envContent.replace(/QB_REFRESH_TOKEN=.*/, `QB_REFRESH_TOKEN=${tokens.refresh_token}`);
    
    fs.writeFileSync(envPath, envContent);
    
    res.send(`
      <h1>Authorization Successful!</h1>
      <p>Your QuickBooks tokens have been updated in the .env file.</p>
      <p>You can now close this window and use the QuickBooks API.</p>
      <pre>${JSON.stringify(tokens, null, 2)}</pre>
    `);
  } catch (error) {
    console.error('Error during OAuth callback:', error);
    res.status(500).send(`
      <h1>Authorization Failed</h1>
      <p>Error: ${error.message}</p>
      <pre>${JSON.stringify(error, null, 2)}</pre>
    `);
  }
});

// Start server
app.listen(port, () => {
  console.log(`OAuth server running at http://localhost:${port}`);
  console.log('Open this URL in your browser to start the authorization process.');
});