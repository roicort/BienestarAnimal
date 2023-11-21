<template>
  <q-layout view="hhh LPR fff" container style="height: calc(100vh)">
    <q-header
      elevated
      bordered
      sticky
      class="bg-white text-grey-9"
      v-bind:style="$q.screen.lt.md ? 'min-height: 65px;' : 'min-height: 79px;'"
    >
    <q-slide-transition> 
      <q-banner
        inline-actions
        dense
        class="text-black bg-grey-4 q-ma-none q-py-sm"
        style="text-align: center"
        v-show="pageContext.banner"
      >
        <span>Adopta Monterrey [Beta] </span> <span class="gt-sm"> - Si tienes comentarios, por favor contáctanos.</span>
      </q-banner>
    </q-slide-transition>

      <q-toolbar
        class="q-py-none justify-between"
        v-bind:style="$q.screen.lt.md ? 'height: 65px;' : 'height: 79px;'"
      >
        <q-toolbar-title class="col-auto flex justify-start items-center">
          <transition
            v-if="authStore.firebaseUserData.accessToken"
            v-show="!buscador"
            appear
            enter-active-class="animated fadeInLeft"
            leave-active-class="animated fadeOutLeft"
          >
            <q-btn
              class="q-mr-sm"
              dense
              flat
              round
              icon="menu"
              v-if="authStore.firebaseUserData.uid && ( (authStore.perfilUsuario.vinculaciones_asociaciones ? authStore.perfilUsuario.vinculaciones_asociaciones.length > 0 : false) || authStore.localUserData.is_staff)"
              @click="siteContext.drawerLeft = !siteContext.drawerLeft"
            />
          </transition>
          <transition
            appear
            enter-active-class="animated fadeInLeft"
            leave-active-class="animated fadeOutLeft"
          >
            <q-btn
              v-show="!buscador"
              type="a"
              href="https://www.monterrey.gob.mx"
              target="_blank"
              title="Gobierno de Monterrey"
              :ripple="false"
              class="q-px-none q-pr-md no-border no-border-radius no-box-shadow no-outline no-shadow no-hovereable"
            >
              <q-avatar square size="3.5rem" class="q-mr-sm">
                <img src="/img/logos/iso_mty.png" alt="isotipo monterrey" />
              </q-avatar>
              <q-avatar v-show="!buscador" square size="3.5rem">
                <img src="/img/logos/type_mty.png" alt="logotipo monterrey" />
              </q-avatar>
            </q-btn>
          </transition>

          <transition
            appear
            enter-active-class="animated fadeInLeft"
            leave-active-class="animated fadeOutLeft"
          >
            <q-btn
              v-show="!buscador"
              :to="'/'"
              title="Bolsa de empleo"
              :ripple="false"
              class="q-px-none q-pr-sm-sm no-border no-border-radius no-box-shadow no-outline no-shadow no-hovereable"
            >
              <!--LOGO SITIO-->
              <div v-bind:style="$q.screen.lt.sm ? 'q-pa-xs' : 'q-pa-sm'"
              >
                <q-img
                  v-show="!buscador"
                  src="https://mty-microwebapps.web.app/img/sdh/mty_sdh_logo_iso.svg"
                  spinner-color="white"
                  style="width: 5rem"
                  alt="Logo Sub Sitio"
                />
              </div>
            </q-btn>
          </transition>
        </q-toolbar-title>

        <!-- BARRA DE BUSQUEDA -->
        <transition
          appear
          enter-active-class="animated fadeInDown"
          leave-active-class="animated fadeOutUp"
        >
          <div
            v-show="buscador"
            v-bind:class="{ active: buscador }"
            class="barra-buscador-contenedor absolute-top q-pt-md q-pb-lg q-gutter-sm row items-center no-wrap"
          >
            <q-input
              ref="inputBusqueda"
              v-model="pageContext.textoBusqueda"
              outlined
              color="grey-6"
              dense
              class="q-px-sm col"
              label="Búsqueda dentro del sitio"
              @keyup.enter="submitBusqueda()"
              @keyup.esc="limpiarBusqueda()"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
            <q-btn
              dense
              :disable="!pageContext.textoBusqueda"
              flat
              no-caps
              class="q-px-md bg-grey-3 text-grey-10"
              label="Buscar"
              @click.stop="submitBusqueda()"
            />
            <q-btn
              icon="close"
              clickable
              round
              flat
              class="cursor-pointer q-pa-xs q-ml-xs"
              v-ripple
              size="sm"
              font-size="lg"
              text-color="grey-8"
              color="transparent"
              @click="limpiarBusqueda()"
            />
          </div>
        </transition>
        <!-- BARRA DE BUSQUEDA -->

        <transition
          appear
          enter-active-class="animated fadeInRight"
          leave-active-class="animated fadeOutRight"
        >
          <div v-show="!buscador" class="flex column">
            <q-tabs
              v-model="pageContext.selectedTab"
              outside-arrows
              mobile-arrows
              indicator-color="primary"
              dense
              shrink
              no-caps
              class="self-end order-last gt-sm justify-end"
            >
              <template>
                <q-route-tab
                  v-if="navegacion"
                  icon="home"
                  :to="'/'"
                  class="text-grey-9 q-px-sm"
                  style="min-width: 24px; max-width: 44px"
                />
                <span v-else-if="!navegacion || !navegacion.length > 0"
                  ><q-icon name="home" color="transparent"
                /></span>

                <template v-for="item in navegacion">
                  <q-route-tab
                    v-if="!item.children"
                    :key="item.id"
                    :to="item.path"
                    :label="item.title"
                    class="text-grey-9 q-px-sm"
                  />
                  <q-btn-dropdown
                    v-if="item.children"
                    :key="item.id"
                    auto-close
                    flat
                    stretch
                    no-border-radius
                    no-caps
                    menu-anchor="bottom right"
                    no-scroll
                    :label="item.title"
                    class="text-grey-8 q-px-sm"
                  >
                    <q-list no-scroll no-border-radius max-height="auto">
                      <q-item
                        v-for="item in item.children"
                        :key="item.id"
                        v-bind="item.id"
                        :to="item.path"
                        clickable
                      >
                        <q-item-section>{{ item.title }}</q-item-section>
                      </q-item>
                    </q-list>
                  </q-btn-dropdown>
                  <!--                <q-separator :key="'sep' + id"  v-if="menuItem.separator" />-->
                </template>
              </template>
            </q-tabs>

            <div class="text-right q-pt-sm order-first row justify-end">
              <div class="q-gutter-md row items-center no-wrap">
                <div v-if="authStore.localUserData.is_staff">
                  <q-btn
                    radius
                    flat
                    no-caps
                    class="bg-primary gt-xs"
                    color="white"
                    to="/admin"
                  >
                    <span>Panel de administración</span> <span class="gt-sm"> </span>
                  </q-btn>
                </div>

                <div v-if="authStore.firebaseUserData.accessToken && (authStore.perfilUsuario.vinculaciones_asociaciones ? authStore.perfilUsuario.vinculaciones_asociaciones.length > 0 : false)">
                  <q-btn
                    radius
                    flat
                    no-caps
                    class="bg-primary gt-xs"
                    color="white"
                    to="/animales/adopcion/crear"
                  >
                    <span>Publicar adopción</span> <span class="gt-sm"> </span>
                  </q-btn>
                </div>

                <div v-if="authStore.firebaseUserData.accessToken && (authStore.perfilUsuario.vinculaciones_asociaciones ? authStore.perfilUsuario.vinculaciones_asociaciones.length > 0 : false)">
                  <q-btn 
                    round 
                    flat 
                    dense 
                    to="/ayuda"
                    icon="info"
                    >
                  <q-tooltip :delay="2000">Ayuda y preguntas frecuentes</q-tooltip>
                </q-btn>
                </div>

                <div v-if="!authStore.firebaseUserData.uid">
                  <!--inicio de sesion IDMty-->
                  <q-btn
                    radius
                    flat
                    no-caps
                    class="bg-primary"
                    color="white"
                    @click="loginOIDC($q)"
                  >
                    Entrar
                  </q-btn>
                  <!--                <q-btn radius flat-->
                  <!--                       no-caps-->
                  <!--                       class="bg-accent gt-xs"-->
                  <!--                       color="white"-->
                  <!--                       @click="authStore.showDialogCrearCuenta = true"-->
                  <!--                >-->
                  <!--                  <span>Crear cuenta</span> <span class="gt-sm"> </span>-->
                  <!--                </q-btn>-->
                </div>

                <BotonApps/>

                <BotonCuenta v-if="authStore.firebaseUserData.uid" />
                <!--
                <q-btn round dense flat
                       color="text-grey-7"
                       icon="search"
                       disable
                       @click="pageContext.abrirInputBusqueda()"
                >
                  <q-tooltip :delay="3000">Buscar</q-tooltip>
                </q-btn> -->
              </div>
            </div>
          </div>
        </transition>
      </q-toolbar>

      <q-tabs
        v-model="siteContext.current_page"
        align="left"
        class="bg-primary text-white"
      >
        <q-route-tab
          no-caps
          icon="pets"
          to="/"
          name="all"
          label="Adoptamos"
        />
        <q-route-tab
          no-caps
          icon="search"
          to="/perdidos"
          name="perdidos"
          label="Buscamos"
        >
        <q-tooltip> Próximamente </q-tooltip>
        </q-route-tab>
        <q-route-tab
          no-caps
          icon="mdi-bookmark-multiple"
          to="/adopcion/favoritos"
          name="saved"
          label="Guardados"
          v-show="authStore.firebaseUserData.uid"
        >
        </q-route-tab>
        <q-route-tab
          no-caps
          icon="mdi-file-send"
          to="/adopcion/aplicaciones"
          name="applied"
          label="Aplicados"
          v-show="authStore.firebaseUserData.uid"
        >
        <q-badge v-if="authStore.perfilUsuario.aceptaciones" color="red" floating>{{ authStore.perfilUsuario.aceptaciones }}</q-badge>
        </q-route-tab>
        <q-route-tab
          v-if="authStore.localUserData.is_staff"
          v-show="authStore.firebaseUserData.uid"
          no-caps
          icon="mdi-account"
          to="/tablero"
          name="tablero"
          label="Tablero"
        >
        </q-route-tab>
      </q-tabs>
    </q-header>

    <q-drawer
      v-model="siteContext.drawerLeft"
      v-if="authStore.firebaseUserData.uid && (authStore.perfilUsuario.vinculaciones_asociaciones ? authStore.perfilUsuario.vinculaciones_asociaciones.length > 0 : false)"
      :mini="pageContext.miniState"
      @mouseover="pageContext.miniState = false"
      @mouseout="pageContext.miniState = true"
      mini-to-overlay
      show-if-above
      :width="200"
      :breakpoint="700"
      bordered
    >
      <q-list class="q-mb-xl q-mt-sm">
        <template v-for="item in navegacionAuthData">
          <q-item
            clickable
            v-ripple
            v-if="!item.children"
            :key="item.id"
            :to="item.path"
          >
            <q-item-section avatar>
              <q-icon :name="item.icon" />
              <q-tooltip
                v-if="item.title"
                class="bg-primary"
                :delay="500"
                anchor="center right"
                self="center left"
                :offset="[20, 10]"
                transition-show="scale"
                transition-hide="scale"
              >
                {{ item.title }}
              </q-tooltip>
            </q-item-section>
            <q-item-section>
              {{ item.title }}
            </q-item-section>
          </q-item>

          <q-expansion-item
            switch-toggle-side
            v-if="item.children"
            :key="item.id"
            :label="item.title"
            default-opened
          >
            <q-item
              v-for="item in item.children"
              :key="item.id"
              :to="item.path"
              class="q-pl-xl"
              clickable
              v-ripple
            >
              <q-item-section avatar>
                <q-icon :name="item.icon" />
              </q-item-section>
              <q-item-section>
                {{ item.title }}
              </q-item-section>
            </q-item>
          </q-expansion-item>
        </template>
      </q-list>
    </q-drawer>

    <q-drawer
      side="right"
      v-model="siteContext.drawerRight"
      show-if-above
      bordered
      :width="!$q.screen.lt.md ? $q.screen.width / 1.5 : $q.screen.width"
      :breakpoint="500"
      class="bg-grey-3"
    >
      <q-scroll-area class="fit">
        <div
          class="q-pa-md"
          v-if="siteContext.loading_job == false && siteContext.animal_seleccionado != null"
          :key="siteContext.animal_seleccionado.id"
        >
          <DetalleAnimal></DetalleAnimal>

        </div>

    <div class="row" v-if="siteContext.loading_job === false && siteContext.animal_seleccionado === null">
      <div class="col self-center" style="padding-top: 25vh;">
        <div class="q-mx-auto" :style="$q.screen.lt.sm  ? 'max-width: 75%' : 'max-width: 50%'">
          <img
              src="/img/logos/logo_bolsa_empleo_v1.png"
              alt="Bolsa de Empleo Monterrey"
            />
        </div>
        <div class="flex justify-center items-center q-pl-xl q-pr-xl q-pt-xl">
          <span style="max-width: 75%; text-align: center; font-size: 30px" >¡El <strong>Gobierno de Monterrey</strong> te da la bienvenida!</span>
        </div>
      </div>
    </div>

        <JobLoader v-if="siteContext.loading_job === true"></JobLoader>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <q-page>
        <router-view />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { useQuasar } from 'quasar'

import { onBeforeMount, onMounted, watch, reactive } from 'vue'
import { useAuthStore } from 'stores/auth'

import { useSiteContextStore } from 'stores/site-context'
import { useRoute, useRouter } from 'vue-router'

import { getAdopciones, getFavoritos, getDetalleAnimal } from '../boot/utils'

import DetalleAnimal from 'src/layouts/DetalleAnimal.vue'
import BotonCuenta from 'components/common/BotonCuenta.vue'
import JobLoader from 'src/components/common/JobLoader.vue'

import BotonApps from 'components/common/BotonApps.vue'

import { setCssVar } from 'quasar'
import { loginOIDC } from 'boot/utils'

export default {
  name: 'MainLayout',
  components: {
    DetalleAnimal,
    BotonCuenta,
    JobLoader,
    BotonApps,
  },
  setup() {

    const router = useRouter()
    const route = useRoute()

    const authStore = useAuthStore()
    const siteContext = useSiteContextStore()

    const pageContext = reactive({
      banner: true,
      selectedTab: 0,
      miniState: true,
    })

    const $q = useQuasar()

    onBeforeMount(() => {
      
      setCssVar('primary', '#FE4362')
      setCssVar('accent', '#FE4362')
      $q.loadingBar.setDefaults({ color: 'primary' })

    setTimeout(() => {
      if (authStore.localUserData.is_staff) {
        setCssVar('primary', '#0074BF')
        setCssVar('accent', '#0074BF')
      } else {
        setCssVar('primary', '#FE4362')
        setCssVar('accent', '#FE4362')
      }
    }, 1000)

    setTimeout(() => {
      pageContext.banner = false
    }, 10000)

    })

    const navegacionAuthData = [
      {
        title: 'Solicitudes',
        icon: 'people',
        path: '/adopciones',
      },
      {
        title: 'Asociaciones',
        icon: 'cottage',
        path: '/asociaciones',
      },
      {
        title: 'Animales',
        icon: 'cruelty_free',
        path: '/animales',
      },
      {
        title: 'Adopciones',
        icon: 'pets',
        path: '/animales/adopcion',
      },
      {
        title: 'Reportes',
        icon: 'travel_explore',
        path: '/animales/reportes',
      },
    ]

    onMounted(() => {

      // Splash drawer logic

      setTimeout(() => {
        siteContext.drawerLeft = false
      }, 500)

      if (route.path === '/') {
        if ($q.screen.lt.md) {
          setTimeout(() => {
            siteContext.drawerRight = false
          }, 2000)
        }
      } else {
        setTimeout(() => {
          siteContext.drawerRight = false
        }, 1)
      }

      watch($q.screen.lt.md, (to, from) => {
        console.log('watch $q.screen.lt.md', to, from)
        if (from === false && to === true) {
          siteContext.drawerRight = false
        }
      })

      // Data

      getAdopciones(authStore.firebaseUserData.accessToken).then((response) => {
          if(response.length !== 0){
            console.log('aqui',response)
            siteContext.animales = response
            siteContext.animales_filtrados = response
          }else{
            pageContext.emptyPet = true
          }
        }).then(() => {
          setCase(router.currentRoute.value.path)
        })

    })

    const setSelectedJob = (job) => {
      siteContext.drawerRight = true
      siteContext.loading_job = true
      console.log(job)
      getDetalleAnimal(authStore.firebaseUserData.accessToken, job.animal).then(
        (response) => {
          siteContext.animal_seleccionado = response
          siteContext.loading_job = false
        }
      )
  }

    const setCase = (path) => {

      let regexempleo = new RegExp(/(\/adopcion\/)\d+/)
      //let regexempleofav = new RegExp(/(\/empleos\/favoritos\/)\d+/)

      siteContext.animales_filtrados = []

      // Case 1: Home
      if (path === '/') {
        console.log('Case1')
        siteContext.drawerRight = false
        siteContext.animales_filtrados = siteContext.animales
      }

       // Case 2: Empleos

      else if (regexempleo.test(path)) {
        console.log('Case2')
        siteContext.animales_filtrados = siteContext.animales
        if (route.params.id) {
          const job = siteContext.animales_filtrados.find(
            (job) => job.id.toString() === route.params.id
          )
          setSelectedJob(job)
        }
      } 

      // Case 3: Empleos Favoritos

      else if (path === '/adopcion/favoritos') {
        console.log('Case3')
        siteContext.drawerRight = false
        getFavoritos(authStore.firebaseUserData.accessToken).then((favs) => {
              const favsIDs = favs.map((fav) => fav.animal)
              console.log(siteContext.animales)
              console.log(favsIDs)
              siteContext.animales.forEach((job) => {
                if(favsIDs.includes(job.id)){
                  siteContext.animales_filtrados.push(job)
                }
              });


          })

        }

    else{
      siteContext.drawerRight = false
    }
    
    pageContext.emptyPet = siteContext.animales_filtrados.length === 0 
  }

    watch(
      () => router.currentRoute.value.path,
      (path) => {
        setCase(path)
      }
    )
    

    return {

      navegacionAuthData,
      authStore,
      loginOIDC,
      siteContext,
      pageContext,

    }
  },
}
</script>
