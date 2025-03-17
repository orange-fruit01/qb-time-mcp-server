require('dotenv').config();
const QuickBooks = require('node-quickbooks');
const refreshToken = require('./refresh_token');

async function getCompanyInfo() {
  try {
    // First refresh the token
    const newToken = await refreshToken();
    const accessToken = newToken || process.env.QB_ACCESS_TOKEN;
    const companyId = process.env.QB_COMPANY_ID;
    const clientId = process.env.QB_CLIENT_ID;
    const clientSecret = process.env.QB_CLIENT_SECRET;
    const refreshTokenStr = process.env.QB_REFRESH_TOKEN;
    const environment = process.env.QB_ENVIRONMENT || 'production';
    
    if (!accessToken || !companyId || !clientId || !clientSecret) {
      console.error('Missing required environment variables');
      return;
    }
    
    // Create QuickBooks instance
    const qbo = new QuickBooks(
      clientId,
      clientSecret,
      accessToken,
      refreshTokenStr,
      companyId,
      environment === 'sandbox', // true for sandbox, false for production
      false, // debug
      null, // minor version
      '2.0', // oauth version
      refreshTokenStr // refresh token
    );
    
    // Get company info
    qbo.getCompanyInfo(companyId, (err, companyInfo) => {
      if (err) {
        console.error('Error getting company info:', err);
        return;
      }
      
      console.log('Company Information:');
      console.log(JSON.stringify(companyInfo, null, 2));
    });
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Run the function if this file is executed directly
if (require.main === module) {
  getCompanyInfo();
} else {
  module.exports = getCompanyInfo;
} 