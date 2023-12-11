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
        listaApps.value = [
    {
        "id": 9,
        "titulo": "Ciudad de la niñez",
        "icono": null,
        "url": "https://ciudadninez.monterrey.gob.mx/",
        "hits": -2,
        "destacada": false,
        "color": "deep-purple-4",
        "icono_mdi": "emoji_people"
    },
    {
        "id": 14,
        "titulo": "Archivo histórico",
        "icono": null,
        "url": "https://www.monterrey.gob.mx/archivohistorico",
        "hits": 0,
        "destacada": true,
        "color": "indigo-5",
        "icono_mdi": "description"
    },
    {
        "id": 28,
        "titulo": "Bolsa de Empleo",
        "icono": null,
        "url": "https://empleo.monterrey.gob.mx",
        "hits": 0,
        "destacada": true,
        "color": "blue-6",
        "icono_mdi": "business"
    },
    {
        "id": 10,
        "titulo": "Decidimos Monterrey",
        "icono": null,
        "url": "https://decidimos.monterrey.gob.mx/",
        "hits": 0,
        "destacada": true,
        "color": "deep-orange-8",
        "icono_mdi": "extension"
    },
    {
        "id": 19,
        "titulo": "Emprendemos",
        "icono": "https://storage.googleapis.com/mty-webspa-cms-media/base/aplicacion_sistema_sitio_web/icono/mty_cem_logo.png",
        "url": "https://emprendemos.monterrey.gob.mx",
        "hits": 0,
        "destacada": true,
        "color": "primary",
        "icono_mdi": "business"
    },
    {
        "id": 2,
        "titulo": "Gacetas municipales",
        "icono": null,
        "url": "https://www.monterrey.gob.mx/transparencia/Oficial/Index_Gaceta.asp",
        "hits": 0,
        "destacada": true,
        "color": "amber",
        "icono_mdi": "note"
    },
    {
        "id": 18,
        "titulo": "Injure",
        "icono": "https://storage.googleapis.com/mty-webspa-cms-media/base/aplicacion_sistema_sitio_web/icono/logo_injure_v1.webp",
        "url": "https://injure.monterrey.gob.mx",
        "hits": 0,
        "destacada": true,
        "color": "orange-4",
        "icono_mdi": "electric_bolt"
    },
    {
        "id": 27,
        "titulo": "Módulo Digital",
        "icono": "https://storage.googleapis.com/mty-webspa-cms-media/base/aplicacion_sistema_sitio_web/icono/modulo_icono.png",
        "url": "https://modulodigital.monterrey.gob.mx/",
        "hits": 0,
        "destacada": true,
        "color": "green-12",
        "icono_mdi": "mdi-cellphone-text"
    },
    {
        "id": 5,
        "titulo": "Transparencia",
        "icono": null,
        "url": "https://www.monterrey.gob.mx/transparencia",
        "hits": 0,
        "destacada": true,
        "color": "deep-purple-6",
        "icono_mdi": "policy"
    },
    {
        "id": 21,
        "titulo": "#Turismo EsCultura",
        "icono": null,
        "url": "https://turismoescultura.monterrey.gob.mx/",
        "hits": 0,
        "destacada": null,
        "color": "pink-8",
        "icono_mdi": "museum"
    },
    {
        "id": 25,
        "titulo": "Facturación",
        "icono": null,
        "url": "https://servicios.adon.mx/site/portal/sfe/index.html",
        "hits": 0,
        "destacada": null,
        "color": "deep-orange-10",
        "icono_mdi": "mdi-cash-register"
    },
    {
        "id": 20,
        "titulo": "Jueces Auxiliares",
        "icono": null,
        "url": "https://juecesauxiliares.monterrey.gob.mx/",
        "hits": 0,
        "destacada": null,
        "color": "red-12",
        "icono_mdi": "groups"
    },
    {
        "id": 6,
        "titulo": "Monterrey ciudad digital",
        "icono": null,
        "url": "http://mtydigital.monterrey.gob.mx",
        "hits": 0,
        "destacada": null,
        "color": "indigo-14",
        "icono_mdi": "location_city"
    },
    {
        "id": 11,
        "titulo": "Monterrey construye",
        "icono": null,
        "url": "https://construye.monterrey.gob.mx",
        "hits": 0,
        "destacada": null,
        "color": "blue-grey-8",
        "icono_mdi": "engineering"
    },
    {
        "id": 26,
        "titulo": "Pago Predial",
        "icono": null,
        "url": "https://modulodigital.monterrey.gob.mx/modules/ventanillaDigital/procedures/pagoDeImpuestoPredial",
        "hits": 0,
        "destacada": null,
        "color": "teal-5",
        "icono_mdi": "inventory_2"
    },
    {
        "id": 8,
        "titulo": "Portal de datos abiertos",
        "icono": null,
        "url": "https://datos.monterrey.gob.mx/",
        "hits": 0,
        "destacada": null,
        "color": "green-14",
        "icono_mdi": "assessment"
    },
    {
        "id": 23,
        "titulo": "Premio SIGA",
        "icono": "https://storage.googleapis.com/mty-webspa-cms-media/base/aplicacion_sistema_sitio_web/icono/indigo.png",
        "url": "https://premiosiga.monterrey.gob.mx/",
        "hits": 0,
        "destacada": null,
        "color": "indigo-10",
        "icono_mdi": "auto_awesome"
    },
    {
        "id": 16,
        "titulo": "Covid-19",
        "icono": null,
        "url": "https://covid19.monterrey.gob.mx/",
        "hits": 1,
        "destacada": false,
        "color": "green-8",
        "icono_mdi": "coronavirus"
    },
    {
        "id": 3,
        "titulo": "Desarrollo verde",
        "icono": null,
        "url": "https://desarrolloverde.monterrey.gob.mx/",
        "hits": 1,
        "destacada": false,
        "color": "green-5",
        "icono_mdi": "eco"
    }
]
        //router.push('/error404')
      }
      //listaApps.value = []
    })


    return {
      listaApps,
    }
  },
}
</script>

<style scoped></style>
