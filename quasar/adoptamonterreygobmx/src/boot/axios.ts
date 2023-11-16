import { boot } from 'quasar/wrappers';
import axios, { AxiosInstance } from 'axios';

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
  }
}

// Be careful when using SSR for cross-request estado pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)

let baseAPIURL = ''
let apiAuthURL = ''
let apiCMSURL = ''
let apiIDEURL = ''
let apiMTYURL = ''

//window.location.origin === 'http://localhost:9000' || window.location.origin === 'http://127.0.0.1:9000' ? baseURL = 'https://cms.pruebas.mty.gob.mx/api/v1' : baseURL = window.location.origin.replace('://', '://cms.') + '/api/v1'
//window.location.origin === 'http://localhost:9000' || window.location.origin === 'http://127.0.0.1:9000' ? baseURL = 'https://api.adopta.testing.monterrey.gob.mx/rest/v1' : baseURL = window.location.origin.replace('://', '://cms.') + '/api/v1'

baseAPIURL = 'https://adopta.drf.dev.mun.apismty.gob.mx/' // Adopta
apiAuthURL = 'https://auth.monterrey.gob.mx/rest/v1'   // Autenticación
apiCMSURL = 'https://cms.www.monterrey.gob.mx/rest/v1'    // Contenidos del CMS
apiIDEURL = 'https://ide.api.monterrey.gob.mx/rest/v1'  // Catálogos de IDE
apiMTYURL = 'https://api.monterrey.gob.mx/rest/v1'     // Catálogos de MTY

const apiController = new AbortController();
const apiAdopta = axios.create({ baseURL: baseAPIURL });
const apiAuth = axios.create({ baseURL: apiAuthURL });
const apiCms = axios.create({ baseURL: apiCMSURL });
const apiIde = axios.create({ baseURL: apiIDEURL });
const apiMty = axios.create({ baseURL: apiMTYURL });

// const tiposPaginasValidos = 'type=paginas.Estandar&type=paginas.Principal&search_operator=or'

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = apiAdopta;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

export { apiAdopta, apiAuth, apiCms, apiIde, apiMty, axios, apiController, baseAPIURL }
