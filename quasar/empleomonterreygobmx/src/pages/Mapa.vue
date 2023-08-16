<template>
  <q-page>
    <JobLoader v-if="siteContext.geojson == null && pageContext.emptyPet === false"></JobLoader>
    <div class="col-12" v-bind:class="!!!pageContext.emptyPet || ($q.screen.lt.sm ? 'q-py-md' : 'q-pa-xl')">
      <div v-if="pageContext.emptyPet === true">
        <div class="">
        <p style="font-size: 30px">Vacantes Guardadas</p>
        </div>
        <div>
          <p>Aún no has guardado ninguna vacante.</p>
          <router-link to="/">Ver vacantes</router-link>
        </div>
      </div>
    </div>



    <template v-if="siteContext.geojson">

    <div
      v-if="pageContext.mapview === true"
      :style="authStore.firebaseUserData.uid ? $q.screen.lt.md ? 'height: 86.8vh;' : 'height: 85.35vh;' : 'height: 89.8vh;'"
    >
    <MTYMapa 
        geojson="https://empleo.api.dev.appsmty.gob.mx//rest/v1/empleos/vacante-geojson/"
    ></MTYMapa>
    </div>

    <div
      v-if="pageContext.mapview === false"
      :style="authStore.firebaseUserData.uid ? $q.screen.lt.md ? 'height: 86.8vh;' : 'height: 85.35vh;' : 'height: 89.8vh;'"
    >
      <q-scroll-area class="fit">
        <div
          v-for="(vacante, index) in siteContext.animales_filtrados"
          :key="index"
          @click="setSelectedJob(vacante)"
        >
          <div
            class="text-weight-light bg-white text-grey-10 q-pt-sm q-px-sm q-my-sm q-mx-sm relative-position box-shadow-soft cursor-pointer"
          >
            <q-item class="items-start">
              <q-item-section v-if="vacante.empresa_info" side>
                <q-avatar
                  rounded
                  size="40px"
                  :color="vacante.empresa_info.logo ? 'white' : 'primary'"
                >
                  <q-img
                    v-if="vacante.empresa_info.logo"
                    :src="vacante.empresa_info.logo"
                    :alt="vacante.empresa_info.nombre_comercial"
                    fit="contain"
                  />
                  <span v-else class="text-white text-weight-regular">
                    {{ vacante.empresa_info.nombre_comercial.slice(0, 1) }}
                  </span>
                </q-avatar>
              </q-item-section>

              <q-item-section>
                <q-item-label
                  v-if="vacante.empresa_info"
                  class="text-weight-regular"
                >
                  <div>
                    <div v-if="vacante.label" class="text-weight-light text-grey-8 q-mb-xs">
                      {{ vacante.label }}
                    </div>

                    {{ vacante.empresa_info.nombre_comercial }}

                    <q-icon size="sm" name="verified" class="q-mb-xs"
                            :color="vacante.empresa_info.esta_verificada ? 'blue' : 'grey'">
                      <q-tooltip :delay="1000" class="bg-grey-4 text-black"
                                  anchor="center end" self="center start">
                        {{ vacante.empresa_info.esta_verificada ? 'Empresa verificada' : 'Empresa no verificada' }}
                      </q-tooltip>
                    </q-icon>
                  </div>
                </q-item-label>
              </q-item-section>

              <q-item-section side top class="self-start text-right">
                <q-item-label caption>
                  hace
                  {{
                    Math.floor(
                      (Date.now() -
                        new Date(vacante.fecha_publicacion_inicio)) /
                        1000 /
                        60 /
                        60 /
                        24
                    )
                  }}
                  {{
                    Math.floor(
                      (Date.now() - new Date(vacante.fecha_publicacion_fin)) /
                        1000 /
                        60 /
                        60 /
                        24
                    ) > 1
                      ? 'días'
                      : 'día'
                  }}
                </q-item-label>
              </q-item-section>
            </q-item>

            <div
              class="text-body text-weight-light q-py-md q-px-md overflow-hidden"
            >
              <span class="ellipsis-3-lines">
                {{ vacante.descripcion }}
              </span>
            </div>
          </div>
        </div>
      </q-scroll-area>
    </div>

  </template>

  </q-page>
</template>

<script>
import { defineComponent, onMounted, reactive, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'


import { getVacantesGeoJSON, getFavoritos, getDetalleVacante } from '../boot/utils'

import { useAuthStore } from 'stores/auth'
import { useSiteContextStore } from 'stores/site-context'
import { date } from 'quasar'

import JobLoader from 'src/components/common/JobLoader.vue'
import MTYMapa from 'src/components/jobs/MTYMapa.vue'

export default defineComponent({
  name: 'EmpleosLista',
  components: { JobLoader, MTYMapa},
  setup() {
    const siteContext = useSiteContextStore()
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    const emptylist = ref(false)

    onMounted(() => {
      setTimeout(() => {
        getVacantesGeoJSON(authStore.firebaseUserData.accessToken).then((response) => {
          if(response.length !== 0){

            siteContext.geojson = response
          }else{
            pageContext.emptyPet = true
          }
          setCase(router.currentRoute.value.path)
        })
      }, 1000)
    })

    const setSelectedJob = (job) => {
      siteContext.drawerRight = true
      siteContext.loading_job = true
      getDetalleVacante(authStore.firebaseUserData.accessToken, job.id).then(
        (response) => {
          siteContext.selected_job = response
          siteContext.loading_job = false
        }
      )
      .finally(() => {
      const currentRoute = router.currentRoute.value.path;
      const newPath = currentRoute.includes('/empleos/favoritos')
        ? `/empleos/favoritos/${job.id}`
        : `/empleos/${job.id}`;

      router.push({ path: newPath });
    });
  }


    const setCase = (path) => {
      // Si el path es '' o sea es home -> Caso 1

      if (path === '/') {
        siteContext.drawerRight = false
        siteContext.animales_filtrados = siteContext.empleos
        pageContext.emptyPet = siteContext.animales_filtrados.length === 0
      }

      // Si el path es '/empleos/:id' -> Caso 2
      let regexempleo = new RegExp(/(\/empleos\/)\d+/)
      let favoritosRegex = new RegExp(/\/empleos\/favoritos/)
      let favoritosIdRegex = new RegExp(/\/empleos\/favoritos\/\d+/)

      if (regexempleo.test(path)) {
        siteContext.animales_filtrados = siteContext.empleos
        if (route.params.id) {
          for (let i = 0; i < siteContext.animales_filtrados.length; i++) {
            if (siteContext.animales_filtrados[i].id.toString() === route.params.id) {
              setSelectedJob(siteContext.animales_filtrados[i])
              break
            }
          }
          siteContext.drawerRight = true
        }
          } else if (favoritosRegex.test(path) || favoritosIdRegex.test(path)){
            if (route.params.id) {
              for (let i = 0; i < siteContext.animales_filtrados.length; i++) {
                if (siteContext.animales_filtrados[i].id.toString() === route.params.id) {
                  setSelectedJob(siteContext.animales_filtrados[i]);
                  break;
                }
              }
            siteContext.drawerRight = true
          }
      }

      // Si el path es /empleos/favoritos/ -> Caso 3
      if (path === '/empleos/favoritos') {
        getFavoritos(authStore.firebaseUserData.accessToken).then((favs) => {
          if(favs.length === 0){
            pageContext.emptyPet = true
          }
          siteContext.animales_filtrados = []
          favs = favs.map((fav) => fav.vacante)
          siteContext.empleos.forEach((job) => {
            if (favs.includes(job.id)) {
              siteContext.animales_filtrados.push(job)
            }
          })
        })
      }
      emptylist.value = siteContext.animales_filtrados.length === 0 ||
        siteContext.empleos.length === null
    }

    // Switch de casos

    watch(
      () => router.currentRoute.value.path,
      (path) => {
        setCase(path)
      }
    )

    const pageContext = reactive({
      emptyPet: false,
      mapview: true,
    })

    return {
      authStore,
      router,
      emptylist,
      pageContext,
      date,
      siteContext,
      setSelectedJob,
    }
  },
})
</script>

<style scoped></style>
