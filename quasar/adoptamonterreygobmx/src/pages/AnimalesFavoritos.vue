<template>
  <q-page>

    <JobLoader v-if="pageContext.loading"></JobLoader>

    <div class="row" v-if="siteContext.animales_filtrados == 0 && pageContext.loading===false">
      <div class="col self-center" style="padding-top: 15vh;">
        <div class="q-mx-auto" :style="$q.screen.lt.sm  ? 'max-width: 40%' : 'max-width: 20%'">
            <img
              src="https://mty-microwebapps.web.app/img/sdh/mty_sdh_logo_iso.svg"
              alt="Adopta Monterrey - Gobierno de Monterrey"
            />
        </div>
        <div class="flex full-width justify-center items-center q-pt-xl">
          <p style="font-size: 30px"> {{ 'No por aquí... nada por allá...' }}</p>
        </div>
        <div class="flex justify-center items-center q-pl-xl q-pr-xl q-pt-md">
          <span style="max-width: 75%; text-align: center;" >{{ 'Aún no has guardado animales' }}</span>
        </div>
      </div>
    </div>

    <div
      v-if="siteContext.animales_filtrados.length > 0"
      :style="authStore.firebaseUserData.uid ? $q.screen.lt.md ? 'height: 86.8vh;' : 'height: 85.35vh;' : 'height: 89.8vh;'"
    >

    <q-pull-to-refresh @refresh="refresh"> 

      <div v-if="siteContext.animales_filtrados" :class="siteContext.drawerRight ? '': 'row q-pa-md'">
            <ListaRenderer :animales="siteContext.animales_filtrados"/>
      </div>

    </q-pull-to-refresh>
    </div>

  </q-page>
</template>

<script>

import { defineComponent, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import ListaRenderer from 'src/layouts/ListaRenderer.vue'

import { useAuthStore } from 'stores/auth'
import { useSiteContextStore } from 'stores/site-context'
import { date } from 'quasar'

import JobLoader from 'src/components/common/JobLoader.vue'

export default defineComponent({
  name: 'AdopcionesLista',
  components: { JobLoader, ListaRenderer},
  setup() {

    const siteContext = useSiteContextStore()
    const router = useRouter()
    const authStore = useAuthStore()
    const route = useRoute()

    const pageContext = reactive({
      loading: true,
    })

    console.log(siteContext.animales_filtrados)

    siteContext.current_page = route.path

    const diasdesdepublicacion = (fecha_publicacion_inicio) => {
      return Math.floor(
        (Date.now() - new Date(fecha_publicacion_inicio)) /
          1000 /
          60 /
          60 /
          24
      )
    }

    // Create timeout to simulate loading
    setTimeout(() => {
      pageContext.loading = false
    }, 2000)

    const onLoad = (index, done) => {
        setTimeout(() => {
          done()
        }, 2000)
      }

    const refresh = (done) => {
        setTimeout(() => {
          done()
        }, 1000)
      }

    return {
      authStore,
      router,
      date,
      siteContext,
      diasdesdepublicacion,
      onLoad,
      refresh,
      pageContext
    }
  }
})
</script>

<style scoped></style>
