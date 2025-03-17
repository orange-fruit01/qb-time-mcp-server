import { WorkerEntrypoint } from 'cloudflare:workers';
import { ProxyToSelf } from 'workers-mcp';

// Define environment variables interface
export interface Env {
  QB_COMPANY_ID: string;
  QB_ENVIRONMENT: string;
  QB_TIME_ACCESS_TOKEN: string;
  QB_ACCESS_TOKEN: string;
  SHARED_SECRET: string; // Required by workers-mcp
}

// QuickBooks API base URLs
const PRODUCTION_BASE_URL = "https://quickbooks.api.intuit.com";
const SANDBOX_BASE_URL = "https://sandbox-quickbooks.api.intuit.com";

export default class QuickBooksMCP extends WorkerEntrypoint<Env> {
  /**
   * Get company information from QuickBooks API
   * 
   * @return {object} The company information
   */
  async getCompanyInfo() {
    const env = this.env;
    const companyId = env.QB_COMPANY_ID;
    const baseUrl = env.QB_ENVIRONMENT.toLowerCase() === 'sandbox' ? SANDBOX_BASE_URL : PRODUCTION_BASE_URL;
    const accessToken = env.QB_ACCESS_TOKEN;
    
    const url = `${baseUrl}/v3/company/${companyId}/companyinfo/${companyId}`;
    
    const response = await fetch(url, {
      headers: {
        "Accept": "application/json",
        "Authorization": `Bearer ${accessToken}`
      }
    });
    
    if (response.status === 200) {
      return await response.json();
    } else {
      const errorText = await response.text();
      return {
        error: `Error getting company info: ${response.status}`,
        details: errorText
      };
    }
  }
  
  /**
   * Get current user information from QuickBooks Time API
   * 
   * @return {object} The user information
   */
  async getCurrentUser() {
    const env = this.env;
    const accessToken = env.QB_TIME_ACCESS_TOKEN;
    
    const url = "https://rest.tsheets.com/api/v1/current_user";
    
    const response = await fetch(url, {
      headers: {
        "Accept": "application/json",
        "Authorization": `Bearer ${accessToken}`
      }
    });
    
    if (response.status === 200) {
      return await response.json();
    } else {
      const errorText = await response.text();
      return {
        error: `Error getting current user: ${response.status}`,
        details: errorText
      };
    }
  }
  
  /**
   * Execute a query against the QuickBooks API
   * 
   * @param {string} queryString - The SQL-like query string
   * @return {object} The query results
   */
  async executeQuery(queryString: string) {
    const env = this.env;
    const companyId = env.QB_COMPANY_ID;
    const baseUrl = env.QB_ENVIRONMENT.toLowerCase() === 'sandbox' ? SANDBOX_BASE_URL : PRODUCTION_BASE_URL;
    const accessToken = env.QB_ACCESS_TOKEN;
    
    const url = `${baseUrl}/v3/company/${companyId}/query`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": `Bearer ${accessToken}`
      },
      body: JSON.stringify({
        query: queryString
      })
    });
    
    if (response.status === 200) {
      return await response.json();
    } else {
      const errorText = await response.text();
      return {
        error: `Error executing query: ${response.status}`,
        details: errorText
      };
    }
  }
  
  /**
   * Get employees from QuickBooks API
   * 
   * @return {object} The employees information
   */
  async getEmployees() {
    return this.executeQuery("SELECT * FROM Employee");
  }
  
  /**
   * Get customers from QuickBooks API
   * 
   * @return {object} The customers information
   */
  async getCustomers() {
    return this.executeQuery("SELECT * FROM Customer");
  }
  
  /**
   * Get invoices from QuickBooks API
   * 
   * @return {object} The invoices information
   */
  async getInvoices() {
    return this.executeQuery("SELECT * FROM Invoice");
  }
  
  /**
   * Get accounts from QuickBooks API
   * 
   * @return {object} The accounts information
   */
  async getAccounts() {
    return this.executeQuery("SELECT * FROM Account");
  }
  
  /**
   * Get items from QuickBooks API
   * 
   * @return {object} The items information
   */
  async getItems() {
    return this.executeQuery("SELECT * FROM Item");
  }
  
  /**
   * Get payments from QuickBooks API
   * 
   * @return {object} The payments information
   */
  async getPayments() {
    return this.executeQuery("SELECT * FROM Payment");
  }
  
  /**
   * Get bills from QuickBooks API
   * 
   * @return {object} The bills information
   */
  async getBills() {
    return this.executeQuery("SELECT * FROM Bill");
  }
  
  /**
   * Get vendors from QuickBooks API
   * 
   * @return {object} The vendors information
   */
  async getVendors() {
    return this.executeQuery("SELECT * FROM Vendor");
  }
  
  /**
   * Get purchase orders from QuickBooks API
   * 
   * @return {object} The purchase orders information
   */
  async getPurchaseOrders() {
    return this.executeQuery("SELECT * FROM PurchaseOrder");
  }
  
  /**
   * Get journal entries from QuickBooks API
   * 
   * @return {object} The journal entries information
   */
  async getJournalEntries() {
    return this.executeQuery("SELECT * FROM JournalEntry");
  }
  
  /**
   * Get reports from QuickBooks API
   * 
   * @param {string} reportType - The type of report to retrieve (e.g., "ProfitAndLoss", "BalanceSheet")
   * @return {object} The report information
   */
  async getReport(reportType: string) {
    const env = this.env;
    const companyId = env.QB_COMPANY_ID;
    const baseUrl = env.QB_ENVIRONMENT.toLowerCase() === 'sandbox' ? SANDBOX_BASE_URL : PRODUCTION_BASE_URL;
    const accessToken = env.QB_ACCESS_TOKEN;
    
    const url = `${baseUrl}/v3/company/${companyId}/reports/${reportType}`;
    
    const response = await fetch(url, {
      headers: {
        "Accept": "application/json",
        "Authorization": `Bearer ${accessToken}`
      }
    });
    
    if (response.status === 200) {
      return await response.json();
    } else {
      const errorText = await response.text();
      return {
        error: `Error getting report: ${response.status}`,
        details: errorText
      };
    }
  }
  
  /**
   * Get profit and loss report from QuickBooks API
   * 
   * @return {object} The profit and loss report
   */
  async getProfitAndLossReport() {
    return this.getReport("ProfitAndLoss");
  }
  
  /**
   * Get balance sheet report from QuickBooks API
   * 
   * @return {object} The balance sheet report
   */
  async getBalanceSheetReport() {
    return this.getReport("BalanceSheet");
  }
  
  /**
   * Get cash flow report from QuickBooks API
   * 
   * @return {object} The cash flow report
   */
  async getCashFlowReport() {
    return this.getReport("CashFlow");
  }
  
  /**
   * Get trial balance report from QuickBooks API
   * 
   * @return {object} The trial balance report
   */
  async getTrialBalanceReport() {
    return this.getReport("TrialBalance");
  }
  
  /**
   * Get accounts receivable aging report from QuickBooks API
   * 
   * @return {object} The accounts receivable aging report
   */
  async getAccountsReceivableReport() {
    return this.getReport("AgedReceivables");
  }
  
  /**
   * Get accounts payable aging report from QuickBooks API
   * 
   * @return {object} The accounts payable aging report
   */
  async getAccountsPayableReport() {
    return this.getReport("AgedPayables");
  }
  
  /**
   * Get customer income report from QuickBooks API
   * 
   * @return {object} The customer income report
   */
  async getCustomerIncomeReport() {
    return this.getReport("CustomerIncome");
  }
  
  /**
   * Get vendor expenses report from QuickBooks API
   * 
   * @return {object} The vendor expenses report
   */
  async getVendorExpensesReport() {
    return this.getReport("VendorExpenses");
  }
  
  /**
   * @ignore
   */
  async fetch(request: Request): Promise<Response> {
    // ProxyToSelf handles MCP protocol compliance
    return new ProxyToSelf(this).fetch(request);
  }
} 