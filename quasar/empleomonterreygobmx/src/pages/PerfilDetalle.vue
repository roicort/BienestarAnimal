<template>
  <q-page
    class="row items-start justify-evenly"
    style="max-width: 1000px; margin: 0 auto"
  >
    <div
      class="col-12 col-md-10 col-lg-10"
      v-bind:class="$q.screen.lt.sm ? 'q-pa-sm' : 'q-pa-xl'"
    >
      <div class="q-pa-sm text-center">
        <div class="q-pt-sm">
          <div class="text-center">
            <p style="font-size: 30px; margin: 0 0 2px 0">Mi perfil</p>
            <p
              class="text-grey-8"
              style="font-size: 0.875rem; font-weight: 400"
            >
              Datos generales del perfil personal.
            </p>
          </div>
        </div>
      </div>
      <q-card class="my-card col-12">
        <q-item-label
          header
          class="text-black text-weight-regular"
          style="font-weight: 500; font-size: 1rem; margin: 2px"
          >Datos personales
        </q-item-label>

        <q-btn
          to="/cuenta/perfil/editar"
          no-caps
          label="Editar perfil"
          color="primary"
          class="absolute-top-right"
          style="top: 0; right: 15px; transform: translateY(15px)"
        ></q-btn>

        <q-item>
          <q-item-section class="col-3">
            <q-item-label caption class="q-mt-sm" style="font-weight: 500">
              Nombre completo
            </q-item-label>
          </q-item-section>

          <q-item-section>
            <q-item-label class="q-mt-sm q-ml-lg text-grey-10">
              {{ authStore.perfilUsuario.nombre }}
              {{ authStore.perfilUsuario.apellidos }}
            </q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="q-ml-md"></q-separator>

        <q-item>
          <q-item-section class="col-3">
            <q-item-label caption class="q-mt-sm" style="font-weight: 500">
              Lugar de residencia
            </q-item-label>
          </q-item-section>

          <q-item-section>
            <q-item-label
              class="q-mt-sm q-ml-lg text-grey-10"
              v-show="
                authStore.perfilUsuario.ciudad && authStore.perfilUsuario.estado
              "
            >
              {{
                authStore.perfilUsuario.ciudad +
                ' ' +
                authStore.perfilUsuario.estado
              }}
            </q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="q-ml-md"></q-separator>

        <q-item>
          <q-item-section class="col-3">
            <q-item-label caption class="q-mt-sm" style="font-weight: 500"
              >Biografía</q-item-label
            >
          </q-item-section>

          <q-item-section>
            <q-item-label class="q-mt-sm q-ml-lg text-grey-10">{{
              authStore.perfilUsuario.biografia
            }}</q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="q-ml-md"></q-separator> 

        <q-item>
          <q-item-section class="col-3">
            <q-item-label caption class="q-mt-sm" style="font-weight: 500"
              >Género</q-item-label
            >
          </q-item-section>

          <q-item-section>
            <q-item-label class="q-mt-sm q-ml-lg text-grey-10">{{
              authStore.perfilUsuario.genero
            }}</q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="q-ml-md"></q-separator>

        <q-item>
          <q-item-section class="col-3">
            <q-item-label caption class="q-mt-sm" style="font-weight: 500"
              >Empleo actual</q-item-label
            >
          </q-item-section>

          <q-item-section>
            <q-item-label class="q-mt-sm q-ml-lg text-grey-10"
              >{{ authStore.perfilUsuario.empleo_actual }}
            </q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="q-ml-md"></q-separator> 

        <q-item>
          <q-item-section class="col-3">
            <q-item-label caption class="q-mt-sm" style="font-weight: 500"
              >Fecha de nacimiento</q-item-label
            >
          </q-item-section>
          <q-item-section>
            <q-item-label class="q-mt-sm q-ml-lg text-grey-10">{{
              authStore.perfilUsuario.fecha_nacimiento
            }}</q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="q-ml-md"></q-separator> 
          <q-item>
            <q-item-section class="col-3">
              <q-item-label caption class="q-mt-sm" style="font-weight: 500"
                >Teléfono</q-item-label
              >
            </q-item-section>
            <q-item-section>
              <q-item-label class="q-mt-sm q-ml-lg text-grey-10">{{
                authStore.perfilUsuario.telefono
              }}</q-item-label>
            </q-item-section>
          </q-item>

        <q-separator class="q-ml-md"></q-separator>

        <q-item>
          <q-item-section class="col-3">
            <q-item-label caption class="q-mt-sm" style="font-weight: 500"
              >Habilidades</q-item-label
            >
          </q-item-section>

          <q-item-section>
            <q-item-label
              v-for="habilidad in authStore.perfilUsuario.habilidades_nombre"
              :key="habilidad"
              class="q-mt-sm q-ml-lg text-grey-10"
            >
              {{ habilidad }}
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'

import { apiAdopta } from 'boot/axios'

import { useAuthStore } from 'stores/auth'
import { useSiteContextStore } from 'stores/site-context'

export default defineComponent({
  name: 'PerfilDetalle',
  setup() {
    const siteContext = useSiteContextStore()
    const route = useRoute()
    siteContext.current_page = route.path

    const authStore = useAuthStore()

    const direccion = ref([
      authStore.perfilUsuario.estado,
      authStore.perfilUsuario.ciudad,
    ])

    const is_loading = ref(true)

    is_loading.value = false

    onBeforeMount(() => {
      setTimeout(() => {
        authStore.perfilUsuario.habilidades_nombre = []

        apiAdopta
          .get('/base/habilidad/')
          .then((response) => {
            authStore.perfilUsuario.habilidades.map((id) => {
              response.data.map((habilidad) => {
                if (id == habilidad.id) {
                  authStore.perfilUsuario.habilidades_nombre.push(
                    habilidad.nombre
                  )
                }
              })
            })
          })
          .then(() => {
            is_loading.value = false
          })
          .catch((error) => {
            console.log(error)
          })
      }, 1000)
    })

    return {
      authStore,
      is_loading,
      direccion,
    }
  },
})
</script>
