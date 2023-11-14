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
          Registrar animal
        </p>
        <p class="text-grey-8" style="font-size: 0.875rem; font-weight: 400">
          Asegúrate que los datos del animal sean correctos
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
                title="Información general"
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
                      class="q-pb-lg text-h6 text-weight-regular text-grey-9"
                      >Información general</q-item-label
                    >

                    <mty-form-field-input
                      for="nombre_mascota"
                      label="Nombre del animal"
                      required
                      v-model="formData.nombre"
                    />

                    <mty-form-field-input
                      for="descripción"
                      label="Descripción del animal"
                      required
                      v-model="formData.descripcion"
                      type="textarea"
                      hint="¡Cuéntanos por qué es asombroso este animalito!"
                    />

                    <p>Fecha de nacimiento (Aproximada)</p>


                    <q-date
                    v-model="formData.fecha_nacimiento"
                    landscape
                    mask="YYYY-MM-DD"
                    class="center"
                    label="Fecha de nacimiento"
                    :rules="[(val) => !!val || 'Fecha de nacimiento requerida']"
                    :navigation-max-year-month="MaxDate"
                    :default-year-month="MaxDate"
                  />
                    <q-space />
                    <mty-form-field-select
                      for="categoria"
                      label="Categoría"
                      v-model="formData.categoria"
                      use-input
                      :options="pageContext.opcionesCategorias"
                      option-label="label"
                      option-value="value"
                      @filter="filterCategory"
                    />

                    <mty-form-field-select
                      for="sexo"
                      label="Sexo"
                      v-model="formData.sexo"
                      use-input
                      :options="pageContext.opcionesSexo"
                      option-label="label"
                      option-value="value"
                    />

                    <mty-form-field-select
                      for="habilidades_requeridas"
                      label="Habilidades requeridas"
                      v-model="formData.habilidades"
                      use-input
                      multiple
                      use-chips
                      :options="pageContext.opcionesHabilidades"
                      option-label="label"
                      option-value="value"
                      @filter="filterSkill"
                      max-values="10"
                    />
                  </q-form>

                  <q-stepper-navigation
                    class="row q-gutter-sm q-pt-sm justify-end"
                  >
                    <q-btn
                      no-caps
                      @click="submitFormulario1"
                      color="primary"
                      label="Continuar"
                      class="bg-accent"
                    />
                  </q-stepper-navigation>
                </q-card-section>
              </q-step>

              <q-step
                :name="2"
                title="Detalles adicionales"
                icon="note_add"
                :done="step > 2"
              >
                <q-card-section class="q-gutter-md">
                  <q-item-label
                    class="q-pb-lg text-h6 text-weight-regular text-grey-9"
                    >Detalles adicionales</q-item-label
                  >

                  <q-form
                    @submit.prevent="submitFormulario2"
                    ref="formulario2"
                    greedy
                    class="q-gutter-lg"
                  >

                  <q-file
                        dense
                        outlined
                        clearable
                        bottom-slots
                        counter
                        name="foto"
                        v-model="pageContext.photo_file"
                        label="Foto"
                        hint="(Opcional) Foto del animal. Tamaño máximo de archivo de 2 Mb"
                        @update:model-value="onPhotoChange"
                        accept=".png,.jpeg,.jpg"
                        max-file-size="20971520"
                        @rejected="onRejected"
                      >
                        <template v-slot:prepend>
                          <q-icon name="attach_file" />
                        </template>

                        <template v-if="pageContext.foto" v-slot:append>
                          <q-avatar square>
                            <q-img :src="pageContext.foto" />
                          </q-avatar>
                        </template>

                        <template v-slot:hint>
                          Restringido a imágenes
                        </template>
                      </q-file>

                    <q-item tag="label">
                      <q-item-section avatar top>
                        <q-checkbox
                          dense
                          outlined
                          v-model="formData.apto_niños"
                          color="accent"
                        />
                      </q-item-section>
                      <q-item-section>
                        <q-item-label>Apto para niños</q-item-label>
                        <q-item-label caption>
                          Esta animalito tiene un comportamiento adecuado para familia con niños.
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-form>

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
                    <q-btn
                      no-caps
                      @click="submitFormulario2"
                      color="primary"
                      label="Continuar"
                      class="bg-accent"
                    />
                  </q-stepper-navigation>
                </q-card-section>
              </q-step>

              <q-step
                :name="3"
                title="Sensibilidad a la inclusión"
                icon="note_add"
                :done="step > 3"
              >
                <q-card-section class="q-gutter-md">
                  <q-item-label
                    class="q-pb-lg text-h6 text-weight-regular text-grey-9"
                    >Sensibilidad a la inclusión
                  </q-item-label>

                  <q-form
                    @submit.prevent="submitFormulario3"
                    ref="formulario3"
                    greedy
                    class="q-gutter-lg"
                  >
                  <q-item-label
                      >¿Esta animalito necesita consideraciones especiales?</q-item-label
                    >
                    <q-option-group
                      v-model="formData.inclusiones"
                      :options="pageContext.opcionesInclusion"
                      emit-value
                      map-options
                      color="accent"
                      type="checkbox"
                    />

                    <q-item-label caption>
                      Es importante establecer si este animalito necesita consideraciones especiales para su adopción.
                    </q-item-label>
                  </q-form>

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
                      @click="submitFormulario3"
                      color="primary"
                      label="Continuar"
                      class="bg-accent"
                    />
                  </q-stepper-navigation>
                </q-card-section>
              </q-step>

              <!-- PASO 4  -->

              <q-step
                :name="4"
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
                    <q-item v-if="pageContext.foto" align-center>
                      <q-avatar square size="256px">
                        <q-img :src="pageContext.foto" />
                      </q-avatar>
                    </q-item>
                    <q-item>
                      Empresa:
                      {{
                        pageContext.opcionesAsociaciones.filter(
                          (item) => item.value === formData.asociacion
                        )[0].label
                      }}
                    </q-item>
                    <q-item>
                      Sucursal:
                      {{
                        pageContext.opcionesCentros.filter(
                          (item) => item.value === formData.centro
                        )[0].label
                      }}
                    </q-item>
                    <q-item> Nombre: {{ formData.nombre }} </q-item>
                    <q-item> Descripción: {{ formData.descripcion }} </q-item>
                    <q-item>
                      Apto para niños:
                      {{ formData.apto_niños ? 'Sí' : 'No' }}
                    </q-item>
                    <q-item>
                      Inclusiones:
                      {{
                        formData.inclusiones
                          .map(
                            (item) =>
                              pageContext.opcionesInclusion.filter(
                                (op) => op.value === item
                              )[0].label
                          )
                          .join(', ')
                      }}
                    </q-item>
                    <q-item>
                      Habilidades:
                      {{
                        formData.habilidades
                          .map(
                            (item) =>
                              pageContext.opcionesHabilidades.filter(
                                (op) => op.value === item
                              )[0].label
                          )
                          .join(', ')
                      }}
                    </q-item>
                    <q-item>
                      Categoría:
                      {{
                        pageContext.opcionesCategorias.filter(
                          (item) => item.value === formData.categoria
                        )[0].label
                      }}
                    </q-item>
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
  getInclusiones,
} from '../boot/utils'
import MtyFormFieldInput from 'components/forms/fields/MtyFormFieldInput.vue'
import MtyFormFieldSelect from 'components/forms/fields/MtyFormFieldSelect.vue'
//import { computed } from '@vue/reactivity'

export default defineComponent({
  name: 'PostularVacante',
  components: { MtyFormFieldSelect, MtyFormFieldInput },
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
      opcionesHabilidades: [],
      opcionesCategorias: [],
      opcionesInclusion: [],
      opcionesSexo: [
        { label: 'Macho', value: 'macho' },
        { label: 'Hembra', value: 'hembra' },
      ],
      rango_edad: { min: 18, max: 80 },
      rango_salario: { min: 0, max: 50 },
      acepto: false,
    })

    const $q = useQuasar()
    const authStore = useAuthStore()
    const responseStatus = ref(false)
    const responseMessage = ref('Error: ')

    const formData = ref({
      inclusiones: [],
      habilidades: [],
      apto_niños: false,
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

      formData.value.edad = pageContext.rango_edad.min + '-' + pageContext.rango_edad.max + 'años'
      formData.value.user = authStore.firebaseUserData.uid

      const NativeformData = new FormData()

      NativeformData.append('nombre', formData.value.nombre)
      NativeformData.append('descripcion', formData.value.descripcion)
      NativeformData.append('edad', formData.value.edad)
      NativeformData.append('sexo', formData.value.sexo)
      NativeformData.append('apto_niños', formData.value.apto_niños)
      NativeformData.append('categoria', formData.value.categoria)
      NativeformData.append('asociacion', formData.value.asociacion)
      NativeformData.append('centro', formData.value.centro)
      NativeformData.append('user', formData.value.user)

      formData.value.inclusiones.forEach((value) => { 
        NativeformData.append('inclusiones[]', value); 
      });

      formData.value.habilidades.forEach((value) => { 
        NativeformData.append('habilidades[]', value); 
      });

      if (pageContext.photo_file) {
        NativeformData.append('foto', pageContext.photo_file)
      }

      $q.loading.show({
        message:
          'Estamos enviando la información. Espere un momento por favor...',
      })
      apiAdopta
        .post('/animales/padron/', NativeformData, {
          headers: {
            Authorization: 'Bearer ' + authStore.firebaseUserData.accessToken,
            'Content-Type': pageContext.photo_file
              ? 'multipart/form-data'
              : 'application/json',
          },
        })
        .then((response) => {
          if (response.status === 201) {
            responseStatus.value = true
            responseMessage.value = 'Respuesta enviada exitosamente!'
            router.push('/animales')
          } else {
            responseMessage.value = responseMessage.value + response.status
          }
          $q.loading.hide()
          showNotificacion(
            response.status === 201
              ? 'Empleo publicado exitosamente'
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

    const formulario1 = ref(null)
    const formulario2 = ref(null)
    const formulario3 = ref(null)

    const submitFormulario1 = () => {
      formulario1.value.validate().then((ok) => {
        if (ok) {
          step.value = 2
        }
      })
    }
    const submitFormulario2 = () => {
      formulario2.value.validate().then((ok) => {
        if (ok) {
          step.value = 3
        }
      })
    }
    const submitFormulario3 = () => {
      formulario3.value.validate().then((ok) => {
        if (ok) {
          step.value = 4
        }
      })
    }

    const onPhotoChange = () => {
      if (pageContext.photo_file) {
        const reader = new FileReader()
        reader.readAsDataURL(pageContext.photo_file)
        reader.onload = (e) => {
          pageContext.foto = e.target.result
          showNotificacion('Imagen cargada exitosamente', 'green')
        }
      } else {
        pageContext.foto = null
      }
    }

    return {
      step,
      onPhotoChange,
      pageContext,
      formData,
      authStore,
      router,
      siteContext,
      formulario1,
      formulario2,
      formulario3,

      submitFormulario1,
      submitFormulario2,
      submitFormulario3,

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
