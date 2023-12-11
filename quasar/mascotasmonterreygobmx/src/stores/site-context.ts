import {defineStore} from 'pinia';

const useSiteContextStore = () => {
  return defineStore('site-context', {

    state: () => ({
      animal_seleccionado: null,
      loading_job: false,
      current_page: null,
      drawerLeft: false,
      drawerRight: true,
      animales: [],
      animales_filtrados: [],
    }),
    actions: {},
    getters: {},
  })()
}

export {useSiteContextStore}
