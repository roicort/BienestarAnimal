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
        <p style="font-size: 30px; margin: 0 0 2px 0">Detalle oferta</p>
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
                <q-card-section class="q-gutter-md">
                  <q-item-label
                    class="q-pb-lg text-h6 text-weight-regular text-grey-9"
                    >Información general</q-item-label
                  >
                 
                  <q-select
                    v-if="formData.empresa_info"
                    dense
                    outlined
                    label="* Empresa donde se oferta la vacante"
                    v-model="formData.empresa_info.nombre_comercial"
                    :options="pageContext.opcionesEmpresas"
                    emit-value
                    map-options
                    :disable="true"
                    :rules="[
                      (val) => (val && val.value !== 0) || 'Campo requerido',
                    ]"
                    use-input
                    @update:model-value="onSelectedCompany"
                  >
                  </q-select>

                  <q-select
                    dense
                    outlined
                    label="* Sucursal de la empresa"
                    v-model="formData.sucursal"
                    :options="pageContext.sucursales"
                    emit-value
                    map-options
                    use-input
                    hint=""
                    :disable="!pageContext.edit"
                  >
                    <template v-slot:no-option>
                      <q-item>
                        <q-item-section class="text-grey">
                          No se encontró la sucursal
                        </q-item-section>
                      </q-item>
                    </template>
                  </q-select>

                  <mty-form-field-input
                    for="nombre_vacante"
                    label="Nombre o puesto de la vacante"
                    required
                    :readonly="!pageContext.edit"
                    v-model="formData.nombre"
                  />

                  <mty-form-field-input
                    for="descripción"
                    label="Descripción de la vacante"
                    required
                    v-model="formData.descripcion"
                    type="textarea"
                    hint="Describa a continuación las actividades y funciones a realizar"
                    :readonly="!pageContext.edit"
                  />

                  <mty-form-field-input
                    for="perfil_profesional"
                    label="Perfil profesional"
                    required
                    v-model="formData.perfil_profesional"
                    hint="Describa el perfil esperado"
                    :readonly="!pageContext.edit"
                  />

                  <mty-form-field-input
                    for="experiencia_previa"
                    label="Experiencia previa"
                    v-model="formData.experiencia_previa"
                    hint="Opcional"
                    :readonly="!pageContext.edit"
                  />

                  <mty-form-field-input
                    for="escolaridad"
                    label="Escolaridad deseada"
                    required
                    :readonly="!pageContext.edit"
                    v-model="formData.escolaridad_deseada"
                  />

                  <p>Rango de edad</p>
                  <q-range
                    class="q-pb-lg"
                    v-model="pageContext.rango_edad"
                    :min="18"
                    :max="80"
                    label-always
                    color="accent"
                    :marker-labels="{ 18: '18', 25: '25', 60: '60', 80: '80+' }"
                    :disable="!pageContext.edit"
                  />
                  <q-space />

                  <q-select
                    dense
                    outlined
                    label="* Categoría"
                    v-model="formData.categoria"
                    emit-value
                    map-options
                    use-input
                    :options="pageContext.opcionesCategorias"
                    @filter="filterCategory"
                    :rules="[
                      (val) => (val && val.length !== 0) || 'Campo requerido',
                    ]"
                    hint=""
                    :disable="!pageContext.edit"
                  />

                  <q-select
                    dense
                    outlined
                    label="* Habilidades requeridas"
                    v-model="formData.habilidades"
                    use-chips
                    multiple
                    emit-value
                    map-options
                    :options="pageContext.opcionesHabilidades"
                    @filter="filterSkill"
                    max-values="10"
                    use-input
                    hint=""
                    :rules="[
                      (val) => (val && val.length > 0) || 'Campo requerido',
                    ]"
                    :disable="!pageContext.edit"
                  />
                </q-card-section>

                <q-card-section class="q-gutter-md">
                  <q-item-label
                    class="q-pb-lg text-h6 text-weight-regular text-grey-9"
                    >Detalles adicionales</q-item-label
                  >

                  <q-select
                    dense
                    outlined
                    label="Unidad Temporal"
                    v-model="formData.unidad_temporal"
                    :options="pageContext.unidades_temporales"
                    type="text"
                    hint="Establece si el pago es por mes, día u hora"
                    :disable="!pageContext.edit"
                  />

                  <p>Salario</p>

                  <q-range
                    :key="formData.unidad_temporal"
                    class="q-pb-lg"
                    v-model="pageContext.rango_salario"
                    :min="0"
                    :max="50"
                    step="0.5"
                    label
                    color="accent"
                    :left-label-value="
                      'Pago mínimo: ' +
                      pageContext.rango_salario.min +
                      ' mil pesos'
                    "
                    :right-label-value="
                      'Pago máximio: ' +
                      pageContext.rango_salario.max +
                      ' mil pesos'
                    "
                    :marker-labels="
                      formData.unidad_temporal == 'hora' ||
                      formData.unidad_temporal == 'dia'
                        ? { 0: 'Mínimo', 1000: ' Max' }
                        : { 0: 'Mínimo', 50: 'Máximo' }
                    "
                    :disable="!pageContext.edit"
                  />

                  <q-space />

                  <mty-form-field-input
                    for="prestaciones_adicionales"
                    label="Prestaciones adicionales"
                    v-model="formData.prestaciones_adicionales"
                    :readonly="!pageContext.edit"
                    hint="(Opcional) Prestaciones adicionales a las de ley, si aplica"
                  />

                  <mty-form-field-input
                    for="horario"
                    label="Horario de trabajo"
                    required
                    v-model="formData.horario"
                    hint="Horario de trabajo"
                    :readonly="!pageContext.edit"
                  />

                  <mty-form-field-input
                    for="numero_vacantes_disponibles"
                    label="Número de vacantes disponibles"
                    v-model="formData.numero_vacantes_disponibles"
                    unmasked-value
                    mask="###"
                    hint="Opcional"
                    :readonly="!pageContext.edit"
                  />

                  <q-item tag="label" :disable="!pageContext.edit">
                    <q-item-section avatar top>
                      <q-checkbox
                        dense
                        outlined
                        v-model="formData.apto_estudiantes"
                        color="accent"
                        :disable="!pageContext.edit"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-item-label>Turno para estudiantes</q-item-label>
                      <q-item-label caption>
                        Esta vacante se puede ofrecer con horario flexible a
                        convenir por parte de la empresa y disponibilidad del
                        aspirante que está inscrito en una insitución académica
                        durante el periodo laboral y tiene un horario que cubre
                        el horario laboral común.
                      </q-item-label>
                    </q-item-section>
                  </q-item>

                  <q-item tag="label" :disable="!pageContext.edit">
                    <q-item-section avatar top>
                      <q-checkbox
                        dense
                        outlined
                        v-model="formData.requiere_licencia_conducir"
                        color="accent"
                        :disable="!pageContext.edit"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-item-label>Requiere licencia de conducir</q-item-label>
                      <q-item-label caption>
                        Esta vacante requiere licencia de conducir vigente para
                        la realización de actividades.
                      </q-item-label>
                    </q-item-section>
                  </q-item>

                  <q-item-label
                    class="q-pt-lg text-h7 text-weight-regular text-grey-9"
                    >Modalidad de trabajo
                  </q-item-label>
                  <q-option-group
                    v-model="formData.modalidad"
                    :options="pageContext.opcionesModalidades"
                    type="radio"
                    :rules="[
                      (val) => (val && val.length > 0) || 'Campo requerido',
                    ]"
                    :disable="!pageContext.edit"
                  />
                </q-card-section>

                <q-card-section class="q-gutter-md">
                  <q-item-label
                    class="q-pb-lg text-h6 text-weight-regular text-grey-9"
                    >Sensibilidad a la inclusión
                  </q-item-label>

                  <q-item-label
                    >Esta vacante es apta para personas con</q-item-label
                  >
                  <q-item-label caption>
                    Acepto en el nombre de la empresa postulante para esta
                    vacante, que es apta y tiene las condiciones laborales
                    necesarias y óptimas para el desempeño laboral y
                    contratación de la persona aspirante.
                  </q-item-label>

                  <q-option-group
                    v-model="formData.inclusiones"
                    :options="pageContext.opcionesInclusion"
                    emit-value
                    map-options
                    color="accent"
                    type="checkbox"
                    :disable="!pageContext.edit"
                  />

                  <q-item-section class="q-pt-sm">
                    <!-- <q-item-label>Vigencia de  publicación</q-item-label> -->
                  </q-item-section>
                </q-card-section>

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

import { apiAdopta } from '../boot/axios'
import MTYMapa from 'src/components/jobs/MTYMapa.vue'

import {
  getSucursales,
  getHabilidades,
  getCategorias,
  getInclusiones,
  //getModalidades,
  //getDetalleVacante,
} from '../boot/utils'
import MtyFormFieldInput from 'components/forms/fields/MtyFormFieldInput.vue'

export default defineComponent({
  name: 'DetalleEmpleo',
  components: { MtyFormFieldInput, MTYMapa},
  setup() {
    const siteContext = useSiteContextStore()
    siteContext.selected_job = null
    const router = useRouter()
    const route = useRoute()
    siteContext.current_page = route.path

    const vacanteID = route.params.id

    const formData = ref({
      inclusiones: [],
      apto_estudiantes: false,
      requiere_licencia_conducir: false,
    })

    const pageContext = reactive({
      opcionesEmpresas: [],
      opcionesSucursales: [],
      opcionesHabilidades: [],
      opcionesCategorias: [],
      opcionesInclusion: [],
      opcionesModalidades: [],
      rango_edad: { min: 18, max: 80 },
      rango_salario: { min: 0, max: 50 },
      edit: false,
      geom: null,
    })

    const $q = useQuasar()
    const authStore = useAuthStore()
    const responseStatus = ref(false)
    const responseMessage = ref('Error: ')
    const perfilBasicoCompletado = ref(false)

    onBeforeMount(() => {
      setTimeout(() => {
        /*getDetalleVacante(authStore.firebaseUserData.accessToken, vacanteID)
          .then((result) => {
            console.log('result', result.empresa_info)
            formData.value = result
            pageContext.rango_salario.min = formData.value.salario_minimo
            pageContext.rango_salario.max = formData.value.salario_maximo
            pageContext.rango_edad.min = formData.value.edad_minima
            pageContext.rango_edad.max = formData.value.edad_maxima
            pageContext.geom = formData.value.geom ? formData.value.geom.substring(formData.value.geom.indexOf('(') + 1, formData.value.geom.indexOf(')')).replace('"', '').split(' ').map((item) => parseFloat(item)) : null 
          })
          .then(() => {
            onSelectedCompany(formData.value.empresa)
          })*/

        getHabilidades().then((result) => {
          pageContext.opcionesHabilidades = result
        })

        getCategorias().then((result) => {
          pageContext.opcionesCategorias = result
        })

        getInclusiones().then((result) => {
          pageContext.opcionesInclusion = result
        })

        /*getModalidades().then((result) => {
          pageContext.opcionesModalidades = result
        })*/
      }, 1000)
    })

    pageContext.unidades_temporales = [
      { vale: 'hora', label: 'Por hora' },
      { value: 'dia', label: 'Por día' },
      { value: 'semana', label: 'Por semana' },
      { value: 'mes', label: 'Por mes' },
      { value: 'anuo', label: 'Por año' },
    ]

    function onSelectedCompany() {
      pageContext.sucursales = []
      getSucursales(
        authStore.firebaseUserData.accessToken,
        formData.value.empresa
      ).then((result) => {
        pageContext.sucursales = result
      })
    }

    const submitFormulario = () => {
      formData.value.salario_minimo = pageContext.rango_salario.min
      formData.value.salario_maximo = pageContext.rango_salario.max
      formData.value.edad_minima = pageContext.rango_edad.min
      formData.value.edad_maxima = pageContext.rango_edad.max

      $q.loading.show({
        message:
          'Estamos enviando la información. Espere un momento por favor...',
      })
      apiAdopta
        .put(`/empleos/vacante/${vacanteID}/`, formData.value, {
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

    const showNotificacion = (message, color, actions) => {
      $q.notify({
        message: message,
        color: color,
        actions: actions,
      })
    }

    return {
      step: ref(1),

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

      route,
    }
  },
})
</script>
