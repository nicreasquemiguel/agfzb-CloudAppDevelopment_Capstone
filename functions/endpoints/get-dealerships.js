/**
 * Get all dealerships
 */
const API = '1kgBEwgA8T3D3zaJIRkQMO9-vXUEjbc9xOWWVHiF3rRO'
const URL = 'https://8696e352-53b8-4302-bd32-5ebf2fd03a8b-bluemix.cloudantnosqldb.appdomain.cloud'

const DBNAME = 'dealerships'

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: API })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(URL);
            
      try {
        let response = await cloudant.postFind({
            db: DBNAME,
            selector: params.state ? {
                'state' : params.state
            } : { }
          })
        
        return { "dealerships": response.result['docs'] }
      } catch (error) {
          return { error: error.description };
      }
}

