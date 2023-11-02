<template>
  <q-page>

    <q-dialog v-if="false" v-model="pageContext.filterpop" persistent>
      <q-card class="q-pa-lg" style="width: 700px; max-width: 80vw">
        <q-item-label header class="text-h6 q-pt-lg">Filtros</q-item-label>

        <q-card-section class="column full-height">
          <q-select filled v-model="pageContext.orden" label="Categorías"
            :options="pageContext.opcionesOrden" @filter="filterCategoria">
            <template v-slot:no-option>
              <q-item>
                <q-item-section class="text-grey">
                  Sin resultados
                </q-item-section>
              </q-item>
            </template>
          </q-select>
        </q-card-section>

        <q-card-section class="column full-height">
          <q-select filled multiple v-model="pageContext.categorias_seleccionadas" use-chips label="Categorías"
            :options="pageContext.categorias" @filter="filterCategoria">
            <template v-slot:no-option>
              <q-item>
                <q-item-section class="text-grey">
                  Sin resultados
                </q-item-section>
              </q-item>
            </template>
          </q-select>
        </q-card-section>

        <q-card-section v-if="false">
          <q-select filled multiple v-model="pageContext.inclusiones_seleccionadas" use-chips label="Inclusiones"
            :options="pageContext.inclusiones" @filter="filterInclusion">
            <template v-slot:no-option>
              <q-item>
                <q-item-section class="text-grey">
                  Sin resultados
                </q-item-section>
              </q-item>
            </template>
          </q-select>
        </q-card-section>

        <q-card-actions class="q-pt-lg" align="right">
          <q-btn flat label="Cancelar" @click="removeFilter" v-close-popup />
          <q-btn flat label="Aplicar" color="primary" @click="filterData" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <JobLoader v-if="siteContext.animales_filtrados.length === 0 &&
      pageContext.emptyPet === false &&
      pageContext.emptyFilter == false
      "></JobLoader>

    <div class="row" v-if="pageContext.emptyPet === true">
      <div class="col self-center" style="padding-top: 15vh">
        <div class="q-mx-auto" :style="$q.screen.lt.sm ? 'max-width: 40%' : 'max-width: 20%'">
          <img src="/img/logos/logo_empleo.png" alt="Bolsa de empleo - Gobierno de Monterrey" />
        </div>
        <div class="flex full-width justify-center items-center q-pt-xl">
          <p style="font-size: 30px">{{ '¡Enhorabuena!' }}</p>
        </div>
        <div class="flex justify-center items-center q-pl-xl q-pr-xl q-pt-md">
          <span style="max-width: 75%; text-align: center">
          {{'Si estas viendo esto es porque esta es una instalación nueva de la Bolsa de Empleo y aún no se ha publicado una vacante.'}}
            </span>
        </div>
      </div>
    </div>


    <q-slide-transition v-if="false" > 
    <q-input class="q-ma-md" v-model="pageContext.search" dense debounce="1000" :borderless="!pageContext.activesearch" :rounded="pageContext.activesearch" :outlined="pageContext.activesearch" :loading="pageContext.searching" type="search"
      @update:model-value="filterData" @focus="pageContext.activesearch = true">
      <template v-slot:append v-if="!pageContext.searching">
        <q-icon name="search" />
        <q-btn v-if="pageContext.search == ''" flat
          class="text-weight-light text-grey-10 q-pt-sm q-px-sm q-my-sm q-mx-sm relative-position flat cursor-pointer"
          @click="pageContext.filterpop = !pageContext.filterpop">
          <q-icon name="tune" />
          <span class="q-ml-sm">Filtro</span>
        </q-btn>
      </template>
    </q-input>
  </q-slide-transition>

    <div v-if="siteContext.animales_filtrados.length > 0 &&
      pageContext.emptyPet === false &&
      pageContext.emptyFilter === false
      " :style="authStore.firebaseUserData.uid
      ? $q.screen.lt.md
        ? 'height: 86.8vh;'
        : 'height: 85.35vh;'
      : 'height: 89.8vh;'
    ">
      <q-pull-to-refresh @refresh="refresh">
        <q-infinite-scroll @load="onLoad" :offset="250" class="fit">
          <div v-if="siteContext.animales_filtrados" :class="siteContext.drawerRight ? '': 'row q-pa-md'">
            <ListaRenderer :animales="siteContext.animales_filtrados" :key="siteContext.categorias_seleccionadas" />
          </div>

          <template v-slot:loading>
            <div class="row justify-center q-my-md">
              <q-spinner-dots color="primary" size="40px" />
            </div>
          </template>
        </q-infinite-scroll>
      </q-pull-to-refresh>
    </div>

    <div class="row" v-if="pageContext.emptyFilter === true">
      <div class="col self-center" style="padding-top: 15vh">
        <div class="q-mx-auto" :style="$q.screen.lt.sm ? 'max-width: 40%' : 'max-width: 20%'">
          <img src="/img/logos/logo_empleo.png" alt="Bolsa de empleo - Gobierno de Monterrey" />
        </div>
        <div class="flex full-width justify-center items-center q-pt-xl">
          <p style="font-size: 30px">{{ '¡Cielos!' }}</p>
        </div>
        <div class="flex justify-center items-center q-pl-xl q-pr-xl q-pt-md">
          <span style="max-width: 75%; text-align: center">{{
            'No hay resultados en tu filtro'
          }}</span>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import {
  getAdopciones,
  getCategorias,
  getInclusiones,
} from '../boot/utils'
import { apiAdopta } from '../boot/axios'

import { useAuthStore } from 'stores/auth'
import { useSiteContextStore } from 'stores/site-context'
import { date } from 'quasar'

import JobLoader from 'src/components/common/JobLoader.vue'
import ListaRenderer from 'src/layouts/ListaRenderer.vue'

export default defineComponent({
  name: 'EmpleosLista',
  components: { JobLoader, ListaRenderer },
  setup() {
    const siteContext = useSiteContextStore()
    const router = useRouter()
    const authStore = useAuthStore()
    const route = useRoute()

    siteContext.current_page = route.path

    const pageContext = reactive({
      emptyPet: false,
      emptylist: false,
      case: '',
      filterpop: false,
      categorias: [],
      categorias_seleccionadas: [],
      modalidades: [],
      inclusiones: [],
      modalidades_seleccionadas: [],
      inclusiones_seleccionadas: [],
      emptyFilter: false,
      search: '',
      searching: false,
      activesearch: false,
      opcionesOrden: [
        { label: 'Fecha (Ascendente)', value: '-fecha_publicacion_inicio' },
        { label: 'Fecha (Descendente)', value: 'fecha_publicacion_inicio' },
      ],
      orden: null,
    })

    pageContext.orden = pageContext.opcionesOrden[0]

    const onLoad = (index, done) => {
      setTimeout(() => {
        done()
      }, 2000)
    }

    const refresh = (done) => {
      update().then(() => {
        done()
      })
    }

    const removeFilter = () => {
      pageContext.categorias_seleccionadas = []
      filterData()
    }

    const update = async () => {
      pageContext.search = null
      pageContext.searching = false

      await getAdopciones(authStore.firebaseUserData.accessToken).then(
        (response) => {
          siteContext.animales_filtrados = []
          siteContext.animales_filtrados = response
          pageContext.emptyFilter = siteContext.animales_filtrados.length === 0
        }
      )
    }

    const filterData = async () => {

      siteContext.animales_filtrados = []
      let orden = '&ordering='+pageContext.orden.value

      if (pageContext.search != null && pageContext.search != '') {
        console.log('case1')

        pageContext.searching = true

        pageContext.categorias_seleccionadas = []
        pageContext.modalidades_seleccionadas = []
        pageContext.inclusiones_seleccionadas = []

        let petition = '/animales/animal/?search=' + pageContext.search
        apiAdopta.get(petition+orden).then((response) => {
          siteContext.animales_filtrados = response.data
          pageContext.emptyFilter = siteContext.animales_filtrados.length === 0
          pageContext.searching = false
        })
      }
      else if (
        pageContext.categorias_seleccionadas.length > 0 ||
        pageContext.modalidades_seleccionadas.length > 0 ||
        pageContext.inclusiones_seleccionadas.length > 0
      ) {
        console.log('case2')
        let petition = '/animales/animal/?'

        if (pageContext.categorias_seleccionadas.length > 0) {
          pageContext.categorias_seleccionadas.forEach((cat, index) => {
            petition += '&categoria=' + cat.value
          })
        }
        if (pageContext.inclusiones_seleccionadas.length > 0) {
          pageContext.inclusiones_seleccionadas.forEach((inc, index) => {
            petition += '&inclusion=' + inc.value
          })
        }
          apiAdopta.get(petition+orden).then((response) => {
            pageContext.search = ''
            siteContext.animales_filtrados = response.data
            pageContext.emptyFilter = siteContext.animales_filtrados.length === 0
          })

      } else {
        console.log('case3')
        apiAdopta.get('animales/animal/?'+orden).then((response) => {
          siteContext.animales_filtrados = response.data
          pageContext.emptyFilter = siteContext.animales_filtrados.length === 0
        })
      }
    }

    const filterCategoria = (val, update, abort) => {
      if (pageContext.categorias.length === 0) {
        update()
      }

      update(() => {
        getCategorias(authStore.firebaseUserData.accessToken).then(
          (response) => {
            pageContext.categorias = response
          }
        )
      })
    }

    const filterInclusion = (val, update, abort) => {
      if (pageContext.inclusiones.length === 0) {
        update()
      }

      update(() => {
        getInclusiones(authStore.firebaseUserData.accessToken).then(
          (response) => {
            pageContext.inclusiones = response
          }
        )
      })
    }

    return {
      authStore,
      router,
      pageContext,
      date,
      siteContext,
      onLoad,
      refresh,
      filterData,
      removeFilter,
      filterCategoria,
      filterInclusion,
    }
  },
  computed: {
    filtered: function () {
      return (
        this.pageContext.categorias_seleccionadas.length > 0 ||
        this.pageContext.modalidades_seleccionadas.length > 0 ||
        this.pageContext.inclusiones_seleccionadas.length > 0
      )
    },
  },
})
</script>

<style scoped></style>
