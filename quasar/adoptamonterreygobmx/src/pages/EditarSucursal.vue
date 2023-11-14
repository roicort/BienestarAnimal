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
        <p style="font-size: 30px; margin: 0 0 2px 0">Editar sucursal</p>
        <p class="text-grey-8" style="font-size: 0.875rem; font-weight: 400">
          Asegúrate que tus datos sean correctos
        </p>
        <q-btn
          v-if="!pageContext.edit"
          flat
          no-caps
          @click="pageContext.edit = !pageContext.edit"
          label="Editar"
          class="text-accent"
          style="background: rgba(13, 169, 184, 0.13)"
        />
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
                    v-model="formData.nombre"
                    :readonly="!pageContext.edit"
                  />

                  <mty-form-field-input
                    for="domicilio"
                    label="Domicilio"
                    v-model="formData.domicilio"
                    :readonly="!pageContext.edit"
                  />

                  <mty-form-field-input
                    for="codigo_postal"
                    label="Código postal"
                    v-model="formData.codigo_postal"
                    mask="#####"
                    :readonly="!pageContext.edit"
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
                    :disable="!pageContext.edit"
                  />

                  <q-select
                    dense
                    outlined
                    label="Municipio"
                    v-model="pageContext.municipio"
                    :options="pageContext.opcionesMunicipio"
                    type="text"
                    map-options
                    @update:model-value="preventLocalidadesMismatch()"
                    :rules="[(val) => val || 'Campo requerido']"
                    :disable="!pageContext.edit"
                  />

                  <mty-form-field-input
                    for="colonia"
                    label="Colonia"
                    required
                    v-model="formData.colonia"
                    :readonly="!pageContext.edit"
                  />

                  <q-stepper-navigation
                    v-if="pageContext.edit"
                    class="row q-gutter-sm q-pt-sm justify-end"
                  >
                    <q-btn
                      no-caps
                      @click="submitFormulario"
                      color="primary"
                      label="Enviar"
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

import {
  getEstados,
  getMunicipios,
  getLocalidades,
  getSubsectorSCIAN,
  getDetalleSucursal,
} from '../boot/utils'
import MtyFormFieldInput from 'components/forms/fields/MtyFormFieldInput.vue'

export default defineComponent({
  name: 'EditarSucursal',
  components: { MtyFormFieldInput },
  setup() {
    const siteContext = useSiteContextStore()
    siteContext.selected_job = null
    const router = useRouter()
    const route = useRoute()
    siteContext.current_page = route.path

    const pageContext = ref({})

    const formData = ref({
      nombre_comercial: '',
      estado: '',
      municipio: '',
      codigo_postal: '',
      colonia: '',
      domicilio: '',
      localidad: '',
      empresa: route.params.id,
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
        getDetalleSucursal(
          authStore.firebaseUserData.accessToken,
          route.params.id
        ).then((result) => {
          formData.value = result
          pageContext.value.giro = result.giro
          pageContext.value.estado = result.estado
          pageContext.value.municipio = result.municipio
          pageContext.value.localidad = result.localidad
        })

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

    const preventLocalidadesMismatch = () => {
      pageContext.value.localidad = null
      getLocalidades(pageContext.value.municipio.value).then((result) => {
        pageContext.value.opcionesLocalidad = result
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
      // TODO: Verificar en quasar label y value de los selects

      formData.value.estado = pageContext.value.estado
        ? formData.value.estado
        : pageContext.value.estado.value
      formData.value.municipio = pageContext.value.municipio
        ? formData.value.municipio
        : pageContext.value.municipio.value
      formData.value.localidad = pageContext.value.localidad
        ? formData.value.localidad
        : pageContext.value.localidad.value

      $q.loading.show({
        message:
          'Estamos enviando la información. Espere un momento por favor...',
      })
      apiAdopta
        .put(`/empresas/sucursal/${route.params.id}/`, formData.value, {
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
            response.status === 200
              ? 'Perfil actualizado exitosamente'
              : 'Ocurrió un error: ' + response.status,
            response.status === 200 ? 'green' : 'red'
          )
          //setTimeout(() => {router.push(response.status === 201 || response.status === 200 ? '/cuenta/perfil/' : '/')},1000)
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
      preventLocalidadesMismatch,
      submitFormulario,

      step1Validation: () =>
        formData.value.tipo == 'persona_fisica' ||
        formData.value.tipo == 'persona_moral',
      step2Validation: () =>
        (formData.value.tipo == 'persona_moral'
          ? formData.value.nombre_comercial != '' &&
            formData.value.registro_patronal != '' &&
            formData.value.rfc != ''
          : formData.value.rfc != '') &&
        formData.value.descripcion != '' &&
        formData.value.rfc != '' &&
        formData.value.razon_social != '' &&
        pageContext.value.giro != '',
      step3Validation: () => (
        formData.value.domicilio != '' &&
          formData.value.codigo_postal != '' &&
          formData.value.colonia != '' &&
          pageContext.value.estado != null &&
          pageContext.value.municipio != null,
        pageContext.value.localidad != null
      ),
    }
  },
})
</script>
