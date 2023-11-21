<template>
  <q-btn v-if="listaApps.length > 0" round dense flat
         color="text-grey-7"
         icon="apps"
         class="relative-position"
  >
    <q-tooltip :delay="3000">Aplicaciones</q-tooltip>

    <q-menu anchor="top middle" self="bottom middle" class="z-top"
            transition-show="jump-down"
            transition-hide="jump-up">
      <div
        class="row wrap justify-start q-pa-xs"
        style="width: auto; max-width: 380px"
      >
        <div
          class="col-4 q-pa-xs text-center"
          v-for="(item, index) of listaApps"
          :key="index"
        >
          <q-btn
            square
            flat
            color="grey-8"
            stack
            no-caps
            size="xl"
            class="full-width"
            style="min-height: 90px"
            type="a"
            :href="item.url"
          >
            <q-img v-if="item.icono"
                   :src="item.icono"
                   :alt="item.titulo"
                   ratio="1"
                   width="40px"
                   fit="contain"/>
            <q-icon v-else-if="item.icono_mdi"
                    size="40px"
                    :name="item.icono_mdi"
                    :color="item.color"/>
            <span
              style="font-size: 15px; line-height: 1.2"
              class="text-weight-regular q-mt-sm"
            >
              {{ item.titulo }}
            </span>
          </q-btn>
        </div>
      </div>
    </q-menu>
  </q-btn>
</template>

<script>
import {ref} from 'vue'
import {apiCms} from 'boot/axios'
import {mostrarLoadingError429} from 'boot/utils'
import {useRouter, useRoute} from 'vue-router'
import {useQuasar} from 'quasar'


let listaApps = ref([])

listaApps.value = []

export default {
  name: 'BotonApps',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const $q = useQuasar()

    apiCms.get('/base/aplicacion-sistema-sitio-web/').then(response => {
      response.data.forEach(item => {
        listaApps.value.push({
          id: item.id,
          url: item.url,
          icono: item.icono,
          titulo: item.titulo,
          hits: item.hits,
          icono_mdi: item.icono_mdi,
          color: item.color,
        })
      })
    })
    .catch((error) => {
      if (error.response && error.response.status && error.response.status === 429) {
        mostrarLoadingError429(error, route.path, $q)
      } else {
        router.push('/error404')
      }
      listaApps.value = []
    })


    return {
      listaApps,
    }
  },
}
</script>

<style scoped></style>
