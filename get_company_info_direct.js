require('dotenv').config();
const axios = require('axios');
const refreshToken = require('./refresh_token');

async function getCompanyInfo() {
  try {
    // First refresh the token
    const newToken = await refreshToken();
    const accessToken = newToken || process.env.QB_ACCESS_TOKEN;
    const companyId = process.env.QB_COMPANY_ID;
    
    if (!accessToken || !companyId) {
      console.error('Missing required environment variables');
      return;
    }
    
    // Base URL depends on environment (sandbox or production)
    const baseUrl = process.env.QB_ENVIRONMENT === 'sandbox' 
      ? 'https://sandbox-quickbooks.api.intuit.com'
      : 'https://quickbooks.api.intuit.com';
    
    console.log('Using access token:', accessToken.substring(0, 20) + '...');
    console.log('Using company ID:', companyId);
    console.log('Using base URL:', baseUrl);
    
    // Make the API request
    const url = `${baseUrl}/v3/company/${companyId}/companyinfo/${companyId}?minorversion=65`;
    
    console.log('Making request to:', url);
    
    const response = await axios.get(url, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Response status:', response.status);
    
    if (response.data && response.data.CompanyInfo) {
      console.log('\nCompany Information:');
      const info = response.data.CompanyInfo;
      
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
      console.log(JSON.stringify(response.data, null, 2));
      
      return response.data.CompanyInfo;
    } else {
      console.error('Failed to get company info or unexpected response format:', response.data);
    }
  } catch (error) {
    console.error('Error getting company info:');
    if (error.response) {
      console.error('Status:', error.response.status);
      console.error('Data:', JSON.stringify(error.response.data, null, 2));
    } else {
      console.error(error.message);
    }
  }
}

// Run the function if this file is executed directly
if (require.main === module) {
  getCompanyInfo();
} else {
  module.exports = getCompanyInfo;
} 