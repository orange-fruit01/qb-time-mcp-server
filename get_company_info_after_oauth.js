require('dotenv').config();
const QuickBooks = require('node-quickbooks');

async function getCompanyInfo() {
  try {
    // Load environment variables
    const accessToken = process.env.QB_ACCESS_TOKEN;
    const refreshToken = process.env.QB_REFRESH_TOKEN;
    const companyId = process.env.QB_COMPANY_ID;
    const clientId = process.env.QB_CLIENT_ID;
    const clientSecret = process.env.QB_CLIENT_SECRET;
    const environment = process.env.QB_ENVIRONMENT || 'production';
    
    if (!accessToken || !companyId || !clientId || !clientSecret) {
      console.error('Missing required environment variables');
      return;
    }
    
    console.log('Using access token:', accessToken.substring(0, 20) + '...');
    console.log('Using company ID:', companyId);
    
    // Create QuickBooks instance
    const qbo = new QuickBooks(
      clientId,
      clientSecret,
      accessToken,
      refreshToken,
      companyId,
      environment === 'sandbox', // true for sandbox, false for production
      false, // debug
      null, // minor version
      '2.0', // oauth version
      refreshToken // refresh token
    );
    
    // Wrap the callback-based method in a promise
    return new Promise((resolve, reject) => {
      qbo.getCompanyInfo(companyId, (err, companyInfo) => {
        if (err) {
          console.error('Error getting company info:', err);
          reject(err);
          return;
        }
        
        console.log('\nCompany Information:');
        const info = companyInfo;
        
        console.log(`\nCompany Name: ${info.CompanyName}`);
        if (info.LegalName) console.log(`Legal Name: ${info.LegalName}`);
        if (info.CompanyAddr) {
          const addr = info.CompanyAddr;
          console.log('\nAddress:');
          if (addr.Line1) console.log(`  ${addr.Line1}`);
          if (addr.Line2) console.log(`  ${addr.Line2}`);
          if (addr.City) console.log(`  ${addr.City}, ${addr.CountrySubDivisionCode || ''} ${addr.PostalCode || ''}`);
          if (addr.Country) console.log(`  ${addr.Country}`);
        }
        
        if (info.PrimaryPhone) console.log(`\nPhone: ${info.PrimaryPhone.FreeFormNumber}`);
        if (info.PrimaryEmailAddr) console.log(`Email: ${info.PrimaryEmailAddr.Address}`);
        if (info.WebAddr) console.log(`Website: ${info.WebAddr.URI}`);
        
        console.log('\nFull Response:');
        console.log(JSON.stringify(companyInfo, null, 2));
        
        resolve(companyInfo);
      });
    });
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Run the function if this file is executed directly
if (require.main === module) {
  getCompanyInfo().catch(console.error);
} else {
  module.exports = getCompanyInfo;
} 