// RegistrarEmpresa /* TODOs */

<template>
  <q-page
    class="row items-center justify-evenly"
    style="max-width: 1100px; margin: 0 auto"
  >
    <div
      class="col-12 col-md-10 col-lg-10"
      v-bind:class="$q.screen.lt.sm ? 'q-py-md' : 'q-pa-xl'"
    >
      <div class="text-center">
        <p style="font-size: 30px; margin: 0 0 2px 0">Registrar sucursal</p>
        <p class="text-grey-8" style="font-size: 0.875rem; font-weight: 400">
          Asegúrate que tus datos sean correctos
        </p>
      </div>

      <div class="row justify-center align-center">
        <div class="col-xs-12">
          <div class="q-py-sm">
            <q-form
              @submit.prevent="submitFormulario"
              ref="formulario"
              greedy
              class="q-gutter-lg"
            >
              <q-stepper
                v-model="step"
                vertical
                color="primary"
                active-color="accent"
                done-color="green"
                animated
                class="my-card"
                v-bind:class="$q.screen.lt.sm ? '' : 'q-pa-lg'"
                v-bind:style="
                  $q.screen.lt.sm ? 'border: none;' : 'border: solid #ddd 1px;'
                "
              >
                <!-- PASO 1 -->

                <q-card-section class="q-gutter-md">
                  <mty-form-field-input
                    for="nombre"
                    label="Nombre comercial"
                    required
                    v-model="formData.nombre"
                  />

                  <mty-form-field-input
                    for="domicilio"
                    label="Domicilio"
                    required
                    v-model="formData.domicilio"
                  />

                  <mty-form-field-input
                    for="colonia"
                    label="Colonia"
                    required
                    v-model="formData.colonia"
                  />

                  <mty-form-field-input
                    for="codigo_postal"
                    label="Código postal"
                    required
                    v-model="formData.codigo_postal"
                    maxlength="5"
                  />

                  <q-select
                    dense
                    outlined
                    label="Estado"
                    v-model="pageContext.estado"
                    :options="pageContext.opcionesEstado"
                    type="text"
                    map-options
                    @update:model-value="preventMunicipiosMismatch()"
                    :rules="[(val) => val || 'Campo requerido']"
                  />

                  <q-select
                    dense
                    outlined
                    label="Municipio"
                    v-model="pageContext.municipio"
                    :options="pageContext.opcionesMunicipio"
                    type="text"
                    map-options
                    :rules="[(val) => val || 'Campo requerido']"
                  />

                  <q-stepper-navigation
                    class="row q-gutter-sm q-pt-sm justify-end"
                  >
                    <q-btn
                      no-caps
                      @click="submitFormulario"
                      color="primary"
                      label="Continuar"
                      class="bg-accent"
                    />
                  </q-stepper-navigation>
                </q-card-section>
              </q-stepper>
            </q-form>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onBeforeMount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from 'stores/auth'
import { useQuasar } from 'quasar'

import { useSiteContextStore } from 'stores/site-context'

import { apiAdopta } from '../boot/axios'

import { getEstados, getMunicipios, getSubsectorSCIAN } from '../boot/utils'
import MtyFormFieldInput from 'components/forms/fields/MtyFormFieldInput.vue'
export default defineComponent({
  name: 'RegistrarEmpresa',
  components: { MtyFormFieldInput },
  setup() {
    const siteContext = useSiteContextStore()
    siteContext.selected_job = null
    const router = useRouter()
    const route = useRoute()
    siteContext.current_page = route.path

    const pageContext = ref({})

    const formData = ref({
      nombre: '',
      estado: '',
      municipio: '',
      codigo_postal: '',
      colonia: '',
      domicilio: '',
      asociacion: route.params.id,
    })

    const $q = useQuasar()
    const authStore = useAuthStore()
    const responseStatus = ref(false)
    const responseMessage = ref('Error: ')

    const isValidDomain = (val) => {
      if (!!val) {
        return domainPattern.test(val) || 'El dominio no tiene formato correcto'
      } else {
        return 'Dirección de dominio obligatorio'
      }
    }

    onBeforeMount(() => {
      setTimeout(() => {
        getEstados().then((result) => {
          pageContext.value.opcionesEstado = result
        })

        getSubsectorSCIAN().then((result) => {
          pageContext.value.opcionesSubsector = result
        })
      }, 1000)
    })

    const preventMunicipiosMismatch = () => {
      pageContext.value.municipio = null
      getMunicipios(pageContext.value.estado.value).then((result) => {
        pageContext.value.opcionesMunicipio = result
      })
    }

    const showNotificacion = (message, color, actions) => {
      $q.notify({
        message: message,
        color: color,
        actions: actions,
      })
    }

    const submitFormulario = () => {
      formData.value.estado = pageContext.value.estado.value
      formData.value.municipio = pageContext.value.municipio.value
      $q.loading.show({
        message:
          'Estamos enviando la información. Espere un momento por favor...',
      })
      apiAdopta
        .post('/asociaciones/centro/', formData.value, {
          headers: {
            Authorization: 'Bearer ' + authStore.firebaseUserData.accessToken,
          },
        })
        .then((response) => {
          if (response.status === 201) {
            responseStatus.value = true
            responseMessage.value = 'Respuesta enviada exitosamente!'
          } else {
            responseMessage.value = responseMessage.value + response.status
          }
          $q.loading.hide()
          showNotificacion(
            response.status === 200 || response.status === 201
              ? 'Se ha creado una sucursal exitosamente'
              : 'Ocurrió un error: ' + response.status,
            response.status === 200 || response.status === 201 ? 'green' : 'red'
          )
          router.push(`/asociaciones/centros/${route.params.id}`)
        })
        .catch((error) => {
          showNotificacion('Ocurrió un error' + error, 'red', [
            {
              label: 'Aceptar',
              color: 'white',
              handler: () => {
                /* ... */
              },
            },
          ])
          $q.loading.hide()
        })
    }

    pageContext.value.opcionesPersonas = [
      { label: 'Física', value: 'persona_fisica', color: 'primary' },
      { label: 'Moral', value: 'persona_moral', color: 'primary' },
    ]

    return {
      step: ref(1),
      pageContext,

      onRejected(rejectedEntries) {
        $q.notify({
          type: 'negative',
          message: `${rejectedEntries.length} archivo inválido`,
        })
      },

      authStore,
      router,
      responseStatus,
      responseMessage,

      isValidDomain,
      alert,
      formData,
      preventMunicipiosMismatch,
      submitFormulario,
    }
  },
})
</script>
