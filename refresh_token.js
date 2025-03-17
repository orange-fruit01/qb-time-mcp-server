require('dotenv').config();
const axios = require('axios');
const fs = require('fs');
const path = require('path');

async function refreshToken() {
  try {
    const clientId = process.env.QB_CLIENT_ID;
    const clientSecret = process.env.QB_CLIENT_SECRET;
    const refreshToken = process.env.QB_REFRESH_TOKEN;
    
    if (!clientId || !clientSecret || !refreshToken) {
      console.error('Missing required environment variables');
      return;
    }
    
    const url = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer';
    const data = new URLSearchParams();
    data.append('grant_type', 'refresh_token');
    data.append('refresh_token', refreshToken);
    
    const config = {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString('base64')}`
      }
    };
    
    const response = await axios.post(url, data, config);
    
    if (response.data && response.data.access_token) {
      // Update .env file with new access token
      const envPath = path.resolve(process.cwd(), '.env');
      let envContent = fs.readFileSync(envPath, 'utf8');
      
      // Replace the access token
      envContent = envContent.replace(
        /QB_ACCESS_TOKEN=.*/,
        `QB_ACCESS_TOKEN=${response.data.access_token}`
      );
      
      // Replace the refresh token if a new one was provided
      if (response.data.refresh_token) {
        envContent = envContent.replace(
          /QB_REFRESH_TOKEN=.*/,
          `QB_REFRESH_TOKEN=${response.data.refresh_token}`
        );
      }
      
      fs.writeFileSync(envPath, envContent);
      
      console.log('Token refreshed successfully!');
      console.log('New access token:', response.data.access_token);
      
      return response.data.access_token;
    } else {
      console.error('Failed to refresh token:', response.data);
    }
  } catch (error) {
    console.error('Error refreshing token:', error.response ? error.response.data : error.message);
  }
}

// Run the function if this file is executed directly
if (require.main === module) {
  refreshToken();
} else {
  module.exports = refreshToken;
} 