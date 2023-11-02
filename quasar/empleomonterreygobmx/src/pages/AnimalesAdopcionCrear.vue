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
        <p style="font-size: 30px; margin: 0 0 2px 0">
          Crear adopción animal
        </p>
        <p class="text-grey-8" style="font-size: 0.875rem; font-weight: 400">
          Asegúrate que los datos sean correctos
        </p>
      </div>
      <div class="row justify-center align-center">
        <div class="col-xs-12">
          <div class="q-py-sm">
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
              <q-step
                :name="0"
                title="Empresa y Sucursal"
                icon="note_add"
                :done="step > 0"
              >
                <q-item-label
                  class="q-pb-lg text-h6 text-weight-regular text-grey-9"
                  >Información general</q-item-label
                >

                <q-card-section class="q-gutter-md">

                  <q-select
                    dense
                    outlined
                    label="Asociacion que resguarda al animal"
                    v-model="formData.asociacion"
                    :options="pageContext.opcionesAsociaciones"
                    emit-value
                    map-options
                    :disable="pageContext.opcionesAsociaciones.length == 0"
                    :rules="[
                      (val) => (val && val.value !== 0) || 'Campo requerido',
                    ]"
                    use-input
                    :hint="
                      pageContext.opcionesAsociaciones.length == 0
                        ? 'Es necesario registrar una empresa para continuar'
                        : ''
                    "
                    @update:model-value="onSelectedCompany"
                  >
                  </q-select>

                  <q-select
                    dense
                    outlined
                    label="Centro de la asociación"
                    v-model="formData.centro"
                    v-if="formData.asociacion"
                    :options="pageContext.opcionesCentros"
                    emit-value
                    map-options
                    use-input
                    :readonly="pageContext.opcionesCentros.length == 0"
                    :hint="
                      pageContext.opcionesCentros.length == 0
                        ? 'Es necesario registrar una centro para continuar'
                        : ''
                    "
                  >
                    <template v-slot:no-option>
                      <q-item>
                        <q-item-section class="text-grey">
                          No se encontró el centro
                        </q-item-section>
                      </q-item>
                    </template>
                  </q-select>

                  <q-select
                    dense
                    outlined
                    label="Animal en adopción"
                    v-model="formData.animal"
                    v-if="formData.centro"
                    :options="pageContext.opcionesAnimales"
                    emit-value
                    map-options
                    use-input
                    :readonly="pageContext.opcionesAnimales.length == 0"
                    :hint="
                      pageContext.opcionesAnimales.length == 0
                        ? 'Es necesario registrar un animal para continuar'
                        : ''
                    "
                  >
                    <template v-slot:no-option>
                      <q-item>
                        <q-item-section class="text-grey">
                          No se encontró el animal
                        </q-item-section>
                      </q-item>
                    </template>
                  </q-select>

                  <q-stepper-navigation
                    class="row q-gutter-sm q-pt-sm justify-end"
                  >
                    <q-btn
                      no-caps
                      :disable="!step1Validation()"
                      @click="step = 1"
                      color="primary"
                      label="Continuar"
                      class="bg-accent"
                    />
                  </q-stepper-navigation>
                </q-card-section>
              </q-step>

              <q-step
                :name="1"
                title="Acuerdo"
                icon="alert"
                @submit.prevent="submitFormulario"
              >
                <q-card-section class="q-gutter-md">
                  <q-item-label
                    class="q-pb-lg text-h6 text-weight-regular text-grey-9"
                    >Resumen</q-item-label
                  >

                  <q-list bordered class="rounded-borders">
                    <q-expansion-item
                      expand-separator
                      icon="info"
                      caption="RAW JSON del formulario"
                    >
                      <q-card>
                        <q-card-section>
                          {{ formData }}
                        </q-card-section>
                      </q-card>
                    </q-expansion-item>
                  </q-list>

                  <q-item-label
                    caption
                    class="row justify-between"
                    style="text-align: right"
                  >
                    Declaro que todo la información aquí vertida es verídica.
                    <q-checkbox
                      dense
                      outlined
                      v-model="pageContext.acepto"
                      color="accent"
                    />
                  </q-item-label>

                  <q-separator />

                  <q-stepper-navigation
                    class="row q-gutter-sm q-pt-sm justify-between"
                  >
                    <q-btn
                      flat
                      no-caps
                      @click="step = 3"
                      label="Atrás"
                      class="text-accent"
                      style="background: rgba(13, 169, 184, 0.13)"
                    />
                    <q-btn
                      no-caps
                      @click="submitFormulario"
                      color="primary"
                      label="Enviar registro"
                      :disable="!pageContext.acepto"
                      class="bg-accent"
                    />
                  </q-stepper-navigation>
                </q-card-section>
              </q-step>

            </q-stepper>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, reactive, onBeforeMount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from 'stores/auth'
import { useQuasar } from 'quasar'

import { useSiteContextStore } from 'stores/site-context'

import { apiAdopta } from '../boot/axios'

import {
  getAsociaciones,
  getSucursales,
  getHabilidades,
  getCategorias,
  getPadron,
  getInclusiones,
} from '../boot/utils'
//import MtyFormFieldInput from 'components/forms/fields/MtyFormFieldInput.vue'
//import MtyFormFieldSelect from 'components/forms/fields/MtyFormFieldSelect.vue'
//import { computed } from '@vue/reactivity'

export default defineComponent({
  name: 'PostularVacante',
  //components: { MtyFormFieldSelect, MtyFormFieldInput },
  setup() {
    const siteContext = useSiteContextStore()
    siteContext.animal_seleccionado = null
    const router = useRouter()
    const route = useRoute()
    siteContext.current_page = route.path

    const step = ref(0)

    const pageContext = reactive({
      opcionesAsociaciones: [],
      opcionesCentros: [],
      opcionesAnimales: [],
      acepto: false,
    })

    const $q = useQuasar()
    const authStore = useAuthStore()
    const responseStatus = ref(false)
    const responseMessage = ref('Error: ')

    const formData = ref({
      //asociacion: null,
      //centro: null,
      //animal: null,
      //user: null,
    })

    const perfilBasicoCompletado = ref(false)

    onBeforeMount(() => {
      setTimeout(() => {
        if (authStore.localUserData.is_staff) {
          getAsociaciones(authStore.firebaseUserData.accessToken).then(
            (companies) => {
              companies.forEach((obj) => {
                pageContext.opcionesAsociaciones.push(obj)
              })
            }
          )
        }else{
            var permisos = authStore.perfilUsuario.vinculaciones_asociaciones
            permisos.forEach((obj) => {
              obj.asociacion_info.label = obj.asociacion_info.nombre
              obj.asociacion_info.value = obj.asociacion_info.id
              pageContext.opcionesAsociaciones.push(obj.asociacion_info)
            })
        }

        if (pageContext.opcionesAsociaciones == 0) {
          pageContext.emptyPet = true
        }

        getHabilidades().then((result) => {
          pageContext.opcionesHabilidades = result
        })

        getCategorias().then((result) => {
          pageContext.opcionesCategorias = result
        })

        getInclusiones().then((result) => {
          pageContext.opcionesInclusion = result
        })
        getPadron().then((result) => {
          pageContext.opcionesAnimales = result
        })
      }, 1000)
    })

    function onSelectedCompany() {
      pageContext.centros = []
      formData.value.centro = null
      getSucursales(
        authStore.firebaseUserData.accessToken,
        formData.value.asociacion
      ).then((result) => {
        pageContext.opcionesCentros = result
      })
    }

    const submitFormulario = () => {

      formData.value.user = authStore.firebaseUserData.uid

      console.log(formData.value)

      $q.loading.show({
        message:
          'Estamos enviando la información. Espere un momento por favor...',
      })
      apiAdopta
        .post('/animales/adopciones/', formData.value, {
          headers: {
            Authorization: 'Bearer ' + authStore.firebaseUserData.accessToken,
            'Content-Type': 'application/json',
          },
        })
        .then((response) => {
          if (response.status === 201) {
            responseStatus.value = true
            responseMessage.value = 'Respuesta enviada exitosamente!'
            router.push('/animales/adopcion')
          } else {
            responseMessage.value = responseMessage.value + response.status
          }
          $q.loading.hide()
          showNotificacion(
            response.status === 201
              ? 'Adopción publicada exitosamente'
              : 'Ocurrió un error: ' + response.status,
            response.status === 201 ? 'green' : 'orange'
          )
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

    const showNotificacion = (message, color, actions) => {
      $q.notify({
        message: message,
        color: color,
        actions: actions,
      })
    }

    return {
      step,
      pageContext,
      formData,
      authStore,
      router,
      siteContext,

      onSelectedCompany,
      perfilBasicoCompletado,
      responseStatus,
      responseMessage,
      submitFormulario,
      showNotificacion,

      step1Validation: () => formData.value.asociacion && formData.value.centro,

      route,
    }
  },
})
</script>
