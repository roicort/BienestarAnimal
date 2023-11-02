/* TODOs */

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
        <p style="font-size: 30px; margin: 0 0 2px 0">Detalle de empresa</p>
        <p class="text-grey-8" style="font-size: 0.875rem; font-weight: 400">
          Revisa o edita tus datos.
        </p>

        <q-btn
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
                  <q-item-label
                    class="q-pt-lg text-h6 text-weight-regular text-grey-9"
                    >Tipo de persona</q-item-label
                  >
                  <q-option-group
                    v-model="formData.tipo"
                    :options="pageContext.opcionesPersonas"
                    type="radio"
                    :disable="true"
                  />
                </q-card-section>

                <!-- PASO 2  -->

                <q-card-section class="q-gutter-md">
                  <q-item-label
                    class="q-pt-md text-h7 text-weight-regular text-grey-9"
                  >
                    Información general
                  </q-item-label>

                  <q-input
                    dense
                    outlined
                    label="* Nombre comercial"
                    v-model="formData.nombre_comercial"
                    type="text"
                    :rules="[
                      (val) => (val && val.length > 0) || 'Campo requerido',
                    ]"
                    :disable="!pageContext.edit"
                  />

                  <q-input
                    dense
                    outlined
                    label="* Registro patronal"
                    v-model="formData.registro_patronal"
                    unmasked-value
                    mask="XXXXXXXXXXX"
                    type="text"
                    :rules="[
                      (val) => (val && val.length === 11) || 'Campo requerido',
                    ]"
                    :disable="!pageContext.edit"
                  />

                  <template v-if="formData.tipo === 'persona_moral'">
                    <q-input
                      dense
                      outlined
                      label="* RFC de empresa"
                      v-model="formData.rfc"
                      unmasked-value
                      mask="XXXXXXXXXXXX"
                      type="text"
                      :rules="[
                        (val) =>
                          (val && val.length === 12) || 'Campo requerido',
                      ]"
                      :disable="!pageContext.edit"
                    />

                    <q-input
                      dense
                      outlined
                      label="Representante legal"
                      v-model="formData.representante_legal"
                      type="text"
                      hint="(Opcional) Nombre completo de representante legal"
                      :disable="!pageContext.edit"
                    />

                    <mty-form-field-input
                      :for="formData.telefono"
                      label="Teléfono"
                      type="tel"
                      required
                      mask="##########"
                      v-model="formData.telefono"
                      :disable="!pageContext.edit"
                    />

                    <q-file
                      dense
                      outlined
                      clearable
                      bottom-slots
                      counter
                      name="logo"
                      v-model="pageContext.logo_file"
                      label="Logo"
                      hint="(Opcional) Imagen con el logo de la empresa, si cuenta con él. Tamaño máximo de archivo de 2 Mb"
                      @update:model-value="onLogoChange"
                      accept=".png,.jpeg,.jpg"
                      max-file-size="20971520"
                      @rejected="onRejected"
                      :disable="!pageContext.edit"
                    >
                      <template v-slot:prepend>
                        <q-icon name="attach_file" />
                      </template>

                      <template v-if="pageContext.logo" v-slot:append>
                        <q-avatar square>
                          <q-img :src="pageContext.logo" />
                        </q-avatar>
                      </template>

                      <template v-slot:hint> Restringido a imágenes </template>
                    </q-file>
                  </template>

                  <template v-if="formData.tipo === 'persona_fisica'">
                    <q-input
                      dense
                      outlined
                      label="* RFC de persona"
                      v-model="formData.rfc"
                      unmasked-value
                      mask="XXXXXXXXXXXXX"
                      type="text"
                      :rules="[
                        (val) =>
                          (val && val.length === 13) || 'Campo requerido',
                      ]"
                      :disable="!pageContext.edit"
                    />
                  </template>

                  <q-input
                    dense
                    outlined
                    label="* Información general de la empresa o negocio, así como su giro o actividades principales"
                    v-model="formData.descripcion"
                    type="textarea"
                    :rules="[
                      (val) => (val && val.length > 0) || 'Campo requerido',
                    ]"
                    :disable="!pageContext.edit"
                  />

                  <q-input
                    dense
                    outlined
                    label="* Razón social"
                    v-model="formData.razon_social"
                    type="text"
                    :rules="[
                      (val) => (val && val.length > 0) || 'Campo requerido',
                    ]"
                    :disable="!pageContext.edit"
                  />

                  <q-select
                    dense
                    outlined
                    label="* Giro comercial"
                    v-model="pageContext.giro"
                    type="text"
                    :options="pageContext.opcionesSubsector"
                    :hint="
                      formData.giro.descripcion === undefined
                        ? 'Seleccione un giro comercial'
                        : formData.giro.descripcion
                    "
                    :disable="!pageContext.edit"
                  />
                </q-card-section>

                <!-- PASO 3  -->

                <q-card-section class="q-gutter-md">
                  <q-item-label
                    class="q-pb-lg text-h6 text-weight-regular text-grey-9"
                    >Domicilio fiscal
                  </q-item-label>

                  <q-input
                    dense
                    outlined
                    label="Domicilio"
                    v-model="formData.domicilio"
                    type="text"
                    :rules="[
                      (val) => (val && val.length > 0) || 'Campo requerido',
                    ]"
                    :disable="!pageContext.edit"
                  />

                  <q-input
                    dense
                    outlined
                    label="Código postal"
                    v-model="formData.codigo_postal"
                    type="text"
                    unmasked-value
                    mask="#####"
                    :rules="[
                      (val) => (val && val.length === 5) || 'Campo requerido',
                    ]"
                    :disable="!pageContext.edit"
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
                    :rules="[(val) => val || 'Campo requerido']"
                    :disable="!pageContext.edit"
                  />

                  <q-input
                    dense
                    outlined
                    label="Colonia"
                    v-model="formData.colonia"
                    type="text"
                    :rules="[
                      (val) => (val && val.length > 0) || 'Campo requerido',
                    ]"
                    :disable="!pageContext.edit"
                  />

                </q-card-section>

                <!-- PASO 4  -->

                <div class="q-pt-lg" v-if="pageContext.geom">
                  <MTYMapa
                    :center="pageContext.geom">
                  </MTYMapa>
                </div>

                <q-card-section class="q-gutter-md">
                  <q-stepper-navigation
                    class="row q-gutter-sm q-pt-sm justify-between"
                  >
                    <q-btn
                      v-if="pageContext.edit"
                      no-caps
                      @click="submitFormulario"
                      color="primary"
                      label="Enviar registro"
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
import { defineComponent, ref, onBeforeMount, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from 'stores/auth'
import { useQuasar } from 'quasar'
import { useSiteContextStore } from 'stores/site-context'
import { apiAdopta } from 'boot/axios'
import MtyFormFieldInput from 'src/components/forms/fields/MtyFormFieldInput.vue'
import MTYMapa from 'src/components/jobs/MTYMapa.vue'

import {
  getEstados,
  getMunicipios,
  getSubsectorSCIAN,
} from 'boot/utils'
export default defineComponent({
  name: 'RegistrarEmpresa',
  components: {
    MtyFormFieldInput,MTYMapa
  },
  setup() {
    const siteContext = useSiteContextStore()
    siteContext.selected_job = null
    const router = useRouter()
    const route = useRoute()
    siteContext.current_page = route.path

    const pageContext = reactive({ edit: false, logo_file: null })

    const empresaID = route.params.id
    const formData = ref({
      nombre_comercial: '',
      tipo: '',
      rfc: '',
      razon_social: '',
      giro: '',
      descripcion: '',
      estado: '',
      municipio: '',
      codigo_postal: '',
      colonia: '',
      domicilio: '',
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
        apiAdopta
          .get(`/empresas/empresa/${empresaID}/`, {
            headers: {
              Authorization: 'Bearer ' + authStore.firebaseUserData.accessToken,
            },
          })
          .then((response) => {
            formData.value = response.data
            pageContext.giro = formData.value.giro
            pageContext.estado = formData.value.estado
            pageContext.municipio = formData.value.municipio
            pageContext.geom = formData.value.geom ? formData.value.geom.substring(formData.value.geom.indexOf('(') + 1, formData.value.geom.indexOf(')')).replace('"', '').split(' ').map((item) => parseFloat(item)) : null 
          })
          .catch((error) => {
            if (error.response.status === 403) {
              showNotificacion('Acceso no autorizado', 'red', [
                {
                  label: 'Aceptar',
                  color: 'white',
                  handler: () => {
                    /* ... */
                  },
                },
              ])
            } else {
              showNotificacion('Ocurrió un error' + error, 'red', [
                {
                  label: 'Aceptar',
                  color: 'white',
                  handler: () => {
                    /* ... */
                  },
                },
              ])
            }
          })
        getEstados().then((result) => {
          pageContext.opcionesEstado = result
        })
        getSubsectorSCIAN().then((result) => {
          pageContext.opcionesSubsector = result
        })
      }, 1000)
    })
    const preventMunicipiosMismatch = () => {
      pageContext.municipio = null
      getMunicipios(pageContext.estado.value).then((result) => {
        pageContext.opcionesMunicipio = result
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

      formData.value.estado = pageContext.estado
        ? formData.value.estado
        : pageContext.estado.value
      formData.value.municipio = pageContext.municipio
        ? formData.value.municipio
        : pageContext.municipio.value
      formData.value.giro = pageContext.giro
        ? formData.value.giro
        : pageContext.giro.value

      for (const key in formData) {
        NativeformData.append(key, formData[key])
      }

      if (pageContext.logo_file != null) {
        NativeformData.append('logo', pageContext.logo_file)
      }

      $q.loading.show({
        message:
          'Estamos enviando la información. Espere un momento por favor...',
      })
      apiAdopta
        .patch(`/empresas/empresa/${empresaID}/`, NativeformData, {
          headers: {
            Authorization: 'Bearer ' + authStore.firebaseUserData.accessToken,
            'Content-Type': pageContext.logo_file
              ? `multipart/form-data; boundary=empresa_${empresaID}`
              : 'application/json',
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

    const onLogoChange = () => {
      if (pageContext.logo_file) {
        const reader = new FileReader()
        reader.readAsDataURL(pageContext.logo_file)
        reader.onload = (e) => {
          pageContext.logo = e.target.result
          showNotificacion('Imagen cargada exitosamente', 'green')
        }
      } else {
        pageContext.logo = null
      }
    }

    pageContext.opcionesPersonas = [
      { label: 'Física', value: 'persona_fisica', color: 'primary' },
      { label: 'Moral', value: 'persona_moral', color: 'primary' },
    ]

    const NativeformData = new FormData()

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
      NativeformData,

      isValidDomain,
      alert,
      formData,
      preventMunicipiosMismatch,
      submitFormulario,
      onLogoChange,

      step1Validation: () =>
        formData.value.tipo === 'persona_fisica' ||
        formData.value.tipo == 'persona_moral',
      step2Validation: () =>
        (formData.value.tipo === 'persona_moral'
          ? formData.value.nombre_comercial != '' &&
            formData.value.registro_patronal != '' &&
            formData.value.rfc != ''
          : formData.value.rfc != '') &&
        formData.value.descripcion != '' &&
        formData.value.rfc != '' &&
        formData.value.razon_social != '' &&
        pageContext.giro != '',
      step3Validation: () =>
        formData.value.domicilio !== '' &&
        formData.value.codigo_postal != '' &&
        formData.value.colonia != '' &&
        pageContext.estado != null &&
        pageContext.municipio != null,
    }
  },
})
</script>
