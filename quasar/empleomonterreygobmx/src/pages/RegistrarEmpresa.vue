

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
        <p style="font-size: 30px; margin: 0 0 2px 0">Registrar asociacion animal</p>
        <p class="text-grey-8" style="font-size: 0.875rem; font-weight: 400">
          Asegúrate que tus datos sean correctos
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
              <!-- PASO 1 -->

              <q-step
                :name="1"
                title="Datos importantes de la empresa"
                icon="note_add"
                :done="step > 1"
              >
                <q-card-section class="q-gutter-md">
                  <q-form
                    @submit.prevent="submitFormulario1"
                    ref="formulario1"
                    greedy
                    class="q-gutter-lg"
                  >
                    <q-item-label
                      class="q-pt-md text-h7 text-weight-regular text-grey-9"
                    >
                      Información general
                    </q-item-label>

                    <mty-form-field-input
                      :for="formData.nombre"
                      label="Nombre comercial"
                      required
                      v-model="formData.nombre"
                    />

                    <mty-form-field-input
                        :for="formData.rfc"
                        label="RFC de empresa"
                        required
                        v-model="formData.rfc"
                        mask="XXXXXXXXXXXXX"
                        :min="0"
                        :max="13"
                      />

                      <mty-form-field-input
                      :for="formData.telefono"
                      label="Teléfono"
                      type="tel"
                      required
                      mask="##########"
                      v-model="formData.telefono"
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
                      >
                        <template v-slot:prepend>
                          <q-icon name="attach_file" />
                        </template>

                        <template v-if="pageContext.logo" v-slot:append>
                          <q-avatar square>
                            <q-img :src="pageContext.logo" />
                          </q-avatar>
                        </template>

                        <template v-slot:hint>
                          Restringido a imágenes
                        </template>
                      </q-file>

                    <mty-form-field-input
                      :for="formData.descripcion"
                      label="Información general"
                      hint="De las actividades del refugio"
                      required
                      v-model="formData.descripcion"
                    />

                    <div class="text-body2 text-grey-8 q-mx-lg q-mt-xl">
                      Los campos marcados con * son requeridos
                    </div>

                    <q-stepper-navigation
                      class="row q-gutter-sm q-pt-sm justify-between"
                    >
                      <q-btn
                        flat
                        no-caps
                        @click="step = 1"
                        label="Atrás"
                        class="text-accent"
                        style="background: rgba(13, 169, 184, 0.13)"
                      />
                      <!-- :disable="!step2Validation()" -->
                      <q-btn
                        no-caps
                        @click="submitFormulario1"
                        color="primary"
                        label="Continuar"
                        type="submit"
                        class="bg-accent"
                      />
                    </q-stepper-navigation>
                  </q-form>
                </q-card-section>
              </q-step>

              <!-- PASO 2  -->

              <q-step
                :name="3"
                title="Dirección de empresa"
                icon="note_add"
                :done="step > 2"
              >
                <q-card-section class="q-gutter-md">
                  <q-form
                    @submit.prevent="submitFormulario2"
                    ref="formulario2"
                    greedy
                    class="q-gutter-lg"
                  >
                    <q-item-label
                      class="q-pb-lg text-h6 text-weight-regular text-grey-9"
                      >Domicilio fiscal</q-item-label
                    >

                    <q-select
                      dense
                      outlined
                      label="* Estado"
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
                      label="* Municipio"
                      v-model="pageContext.municipio"
                      :options="pageContext.opcionesMunicipio"
                      type="text"
                      map-options
                      :rules="[(val) => val || 'Campo requerido']"
                    />

                    <mty-form-field-input
                      :for="formData.codigo_postal"
                      label="Código postal"
                      required
                      v-model="formData.codigo_postal"
                      type="cp"
                      mask="#####"
                      maxlength="5"
                      @update:model-value="formData.codigo_postal = $event"
                    />

                    <q-input
                      dense
                      outlined
                      label="* Colonia"
                      v-model="formData.colonia"
                      type="text"
                      :rules="[
                        (val) => (val && val.length > 0) || 'Campo requerido',
                      ]"
                    />

                    <mty-form-field-input
                      :for="formData.domicilio"
                      label="Calle (domicilio)"
                      required
                      v-model="formData.domicilio"
                      @update:model-value="formData.domicilio = $event"
                    />

                    <q-stepper-navigation
                      class="row q-gutter-sm q-pt-sm justify-between"
                    >
                      <q-btn
                        flat
                        no-caps
                        @click="step = 2"
                        label="Atrás"
                        class="text-accent"
                        style="background: rgba(13, 169, 184, 0.13)"
                      />

                      <q-btn
                        no-caps
                        @click="submitFormulario2"
                        color="primary"
                        label="Continuar"
                        type="submit"
                        class="bg-accent"
                      />
                    </q-stepper-navigation>
                  </q-form>
                </q-card-section>
              </q-step>

              <!-- PASO 4  -->

              <q-step
                :name="4"
                title="Verifica tus datos"
                icon="alert"
                @submit.prevent="submitFormulario"
              >
                <q-card-section class="q-gutter-md">
                  <q-item-label
                    class="q-pb-lg text-h6 text-weight-regular text-grey-9"
                    >Resumen</q-item-label
                  >

                  <q-list bordered class="rounded-borders">
                    <q-item v-if="pageContext.logo" align-center>
                      <q-avatar square size="100px">
                        <q-img :src="pageContext.logo" />
                      </q-avatar>
                    </q-item>
                    <q-item> Nombre: {{ formData.nombre }} </q-item>
                    <q-item> RFC: {{ formData.rfc }} </q-item>
                    <q-item>
                      Estado:
                      {{
                        pageContext.opcionesEstado.filter(
                          (item) => item.value === formData.estado
                        )[0].label
                      }}
                    </q-item>
                    <q-item>
                      Municipio:
                      {{
                        pageContext.opcionesMunicipio.filter(
                          (item) => item.value === formData.municipio
                        )[0].label
                      }}
                    </q-item>
                    <q-item>
                      Código postal: {{ formData.codigo_postal }}
                    </q-item>
                    <q-item> Colonia: {{ formData.colonia }} </q-item>
                    <q-item> Domicilio: {{ formData.domicilio }} </q-item>
                    <q-item>
                      Tipo de persona: {{ formData.tipo_persona }}
                    </q-item>
                    <q-item> Descripcion: {{ formData.descripcion }} </q-item>

                    <q-item v-if="formData.representante_legal">
                      Representante legal: {{ formData.representante_legal }}
                    </q-item>
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
                      :disabled="!pageContext.acepto"
                      @click="submitFormulario"
                      color="primary"
                      label="Enviar registro"
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
import MtyFormFieldInput from 'src/components/forms/fields/MtyFormFieldInput.vue'
//import MtyFormFieldSelect from 'src/components/forms/fields/MtyFormFieldSelect.vue'
import { useSiteContextStore } from 'stores/site-context'
import { apiEmpleo } from '../boot/axios'
import { getEstados, getMunicipios, getSubsectorSCIAN } from '../boot/utils'
export default defineComponent({
  name: 'RegistrarEmpresa',
  components: {
    MtyFormFieldInput,
    //MtyFormFieldSelect,
  },
  setup() {
    const siteContext = useSiteContextStore()
    siteContext.selected_job = null
    const router = useRouter()
    const route = useRoute()
    const step = ref(1)
    const formulario1 = ref(null)
    const formulario2 = ref(null)
    siteContext.current_page = route.path
    const pageContext = reactive({
      opcionesSubsector: [],
      acepto: false,
      logo_path: null,
    })
    const formData = reactive({
      nombre: '',
      tipo: '',
      rfc: '',
      descripcion: '',
      estado: '',
      municipio: '',
      codigo_postal: '',
      colonia: '',
      domicilio: '',
    })
    const $q = useQuasar()
    const authStore = useAuthStore()
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
    const submitFormulario1 = () => {
      formulario1.value.validate().then((ok) => {
        if (ok) {
          step.value = 3
        }
      })
    }
    const submitFormulario2 = () => {
      formulario2.value.validate().then((ok) => {
        if (ok) {
          step.value = 4
          formData.estado = pageContext.estado.value
          formData.municipio = pageContext.municipio.value
        }
      })
    }
    const submitFormulario = () => {
      for (const key in formData) {
        NativeformData.append(key, formData[key])
      }
      if (pageContext.logo_file) {
        NativeformData.append('logo', pageContext.logo_file)
      }
      // Print all values in NativeformData
      for (var value of NativeformData.values()) {
        console.log(value)
      }
      $q.loading.show({
        message:
          'Estamos enviando la información. Espere un momento por favor...',
      })
      apiEmpleo
        .post('/asociaciones/asociacion/', NativeformData, {
          headers: {
            Authorization: 'Bearer ' + authStore.firebaseUserData.accessToken,
            'Content-Type': pageContext.logo_file
              ? 'multipart/form-data'
              : 'application/json',
          },
        })
        .then((response) => {
          router.push('/empresas')
          if (response.status === 201) {
            responseMessage.value = 'Respuesta enviada exitosamente!'
            $q.loading.hide()
          } else {
            responseMessage.value = responseMessage.value + response.status
          }
          showNotificacion(
            response.status === 201
              ? 'Empresa registrada exitosamente'
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
    pageContext.opcionesPersonas = [
      { label: 'Persona física', value: 'persona_fisica', color: 'primary' },
      { label: 'Persona moral', value: 'persona_moral', color: 'primary' },
    ]
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
    const NativeformData = new FormData()
    return {
      step,
      pageContext,
      onRejected(rejectedEntries) {
        $q.notify({
          type: 'negative',
          message: `${rejectedEntries.length} archivo inválido`,
        })
      },
      authStore,
      router,
      responseMessage,
      formulario1,
      formulario2,
      NativeformData,
      isValidDomain,
      alert,
      formData,
      preventMunicipiosMismatch,
      submitFormulario,
      submitFormulario1,
      submitFormulario2,
      onLogoChange,
      step1Validation: () =>
        formData.tipo == 'persona_fisica' || formData.tipo == 'persona_moral',
    }
  },
})
</script>
