import {boot} from 'quasar/wrappers'
import OpenLayersMap, {
  type Vue3OpenlayersGlobalOptions,
} from 'vue3-openlayers';
import 'vue3-openlayers/dist/vue3-openlayers.css';

export default boot(({app}) => {
  const options: Vue3OpenlayersGlobalOptions = {
    debug: true,
  };
  app.use(OpenLayersMap, options)
})
