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
        <p style="font-size: 30px; margin: 0 0 2px 0">Editar perfil</p>
        <p class="text-grey-8" style="font-size: 0.875rem; font-weight: 400">
          Datos generales de información personal.
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
              <q-card-section class="q-gutter-md">
                <q-item-label class="q-pt-sm text-h7 text-grey-9"
                  >Información general</q-item-label
                >

                <mty-form-field-input
                  :for="formData.nombres"
                  label="nombres(s)"
                  required
                  v-model="formData.nombres"
                />

                <mty-form-field-input
                  :for="formData.apellidos"
                  label="Apellidos"
                  required
                  v-model="formData.apellidos"
                />

                <q-input
                  dense
                  outlined
                  label="Biografía o semblanza personal"
                  v-model="formData.biografia"
                  type="textarea"
                  :rules="[(val) => !!val || 'Biografía requerida']"
                />

                <q-select
                  dense
                  outlined
                  label="Genero"
                  v-model="formData.genero"
                  :options="pageContext.generosOptions"
                  type="text"
                />

                <mty-form-field-input
                      :for="formData.telefono"
                      label="Teléfono"
                      type="tel"
                      required
                      mask="##########"
                      v-model="formData.telefono"
                    />

                <q-item-label class="q-pt-sm text-h7 text-grey-9"
                  >Información de residencia</q-item-label
                >

                <q-select
                  dense
                  outlined
                  label="Estado"
                  v-model="formData.estado"
                  map-options
                  :options="pageContext.filteredEstadoOptions"
                  @filter="filterEstadoOptions"
                  @update:model-value="preventMunicipiosMismatch()"
                  use-input
                  :rules="[(val) => !!val || 'Campo requerido']"
                />

                <q-select
                  dense
                  outlined
                  label="Situación Familiar"
                  v-model="formData.situacion_familiar"
                  map-options
                  :options="pageContext.situacionOptions"
                  use-input
                  :rules="[(val) => !!val || 'Campo requerido']"
                />

                <q-select
                  dense
                  outlined
                  label="Municipio"
                  v-model="formData.ciudad"
                  map-options
                  :options="pageContext.filteredMunicipioOptions"
                  @filter="filterMunicipioOptions"
                  use-input
                  :rules="[(val) => !!val || 'Campo requerido']"
                />

                <mty-form-field-input
                  :for="formData.domicilio"
                  label="Domicilio"
                  required
                  v-model="formData.domicilio"
                />

                <q-item-label class="q-pt-sm q-pb-sm text-h6 text-grey-9"
                  >Información para fines estadísticos</q-item-label
                >
                <q-item-label caption>
                  Esta información es opcional y se utilizará para fines estadísticos y programas especiales.
                </q-item-label>
                <q-item-label caption>
                  Ningúna empresa tendrá acceso a este tipo de información.
                </q-item-label>

                <q-item-label class="q-pt-lg">
                  Fecha de nacimiento.
                </q-item-label>
                <q-item-label caption>
                  Deberás ser mayor de edad para poder registrarte.
                </q-item-label>
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


                <q-item-label class="q-pt-lg">
                  Capacidades diferentes
                </q-item-label>

                <q-item-label caption class="q-pt-sm">
                  <q-checkbox
                    dense
                    outlined
                    v-model="formData.capacidad_diferente"
                    color="accent"
                    class="q-pr-sm"
                  />
                  Me percibo como una persona con capacidades diferentes.
                </q-item-label>

                <div class="flex justify-end">
                  <q-btn
                    no-caps
                    type="submit"
                    color="primary"
                    label="Guardar"
                    class="bg-accent"
                  />
                </div>
              </q-card-section>
            </q-form>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onBeforeMount, reactive } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'
import { apiAdopta } from '../boot/axios'
import { getEstados, getGeneros, getMunicipios } from '../boot/utils'
import MtyFormFieldInput from 'src/components/forms/fields/MtyFormFieldInput.vue'

const authStore = useAuthStore()

export default defineComponent({
  name: 'CrearPerfil',
  components: {
    MtyFormFieldInput,
  },
  setup() {
    const $q = useQuasar()
    //const siteContext = useSiteContextStore()
    const router = useRouter()

    const submitResult = ref([])
    const responseStatus = ref(false)
    const responseMessage = ref('Error: ')

    const pageContext = reactive({
      categoryOptions: [],
      skillOptions: [],
      estadoOptions: [],
      municipioOptions: [],
      generosOptions: [],
      filteredCategoryOptions: [],
      filteredSkillOptions: [],
      filteredEstadoOptions: [],
      filteredMunicipioOptions: [],
    })

    const formData = ref(authStore.perfilUsuario)

    const tipo_perfil = ref(null)

    onBeforeMount(() => {
      setTimeout(() => {
        apiAdopta.get('/base/habilidad/').then((response) => {
          response.data.forEach(function (obj) {
            obj.label = obj.nombre
            delete obj.nombre
            obj.value = obj.id
            delete obj.id
          })
          pageContext.skillOptions = response.data
          pageContext.filteredSkillOptions = response.data
        })

        getGeneros().then((result) => {
          pageContext.generosOptions = result
          console.log(pageContext.generosOptions)
        })

        getEstados().then((result) => {
          pageContext.estadoOptions = result
          pageContext.filteredEstadoOptions = result
        })
      }, 1000)
    })

    const agregarNuevaHabilidad = (event) => {
      apiAdopta
        .post(
          '/base/habilidad/',
          { nombre: event },
          {
            headers: {
              Authorization: 'Bearer ' + authStore.firebaseUserData.accessToken,
            },
          }
        )
        .then((respose) => {
          pageContext.skillOptions.push({
            value: respose.data.id,
            label: respose.data.nombre,
          })
          pageContext.filteredSkillOptions.push({
            value: respose.data.id,
            label: respose.data.nombre,
          })
          formData.value.habilidades.push(respose.data.id)
        })
    }

    const preventMunicipiosMismatch = () => {
      formData.value.ciudad = null
      pageContext.filteredMunicipioOptions = []
      if (!!formData.value.estado) {
        getMunicipios(formData.value.estado.value).then((result) => {
          pageContext.municipioOptions = result
          pageContext.filteredMunicipioOptions = result
        })
      }
    }

    const showNotificacion = (message, color, actions) => {
      $q.notify({
        message: message,
        color: color,
        actions: actions,
      })
    }

    const submitFormulario = () => {

      formData.value.user = authStore.firebaseUserData.uid
      formData.value.estado = formData.value.estado.label
      formData.value.ciudad = formData.value.ciudad.label

      $q.loading.show({
        message:
          'Estamos actualizando tu perfil. Espera un momento por favor...',
      })
      if (formData.value.genero){
        formData.value.genero = formData.value.genero.label
      }
      apiAdopta
        .put(
          `/perfiles/perfil-general/${authStore.firebaseUserData.uid}/`,
          formData.value,
          {
            headers: {
              Authorization: 'Bearer ' + authStore.firebaseUserData.accessToken,
            },
          }
        )
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
          setTimeout(() => {
            router.push(
              response.status === 201 || response.status === 200
                ? '/cuenta/perfil/'
                : '/'
            )
          }, 1000)
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

    const filterCategory = (val, update) => {
      if (val === '') {
        update(() => {
          pageContext.filteredCategoryOptions = categoryOptions.value
        })
        return
      }
      update(() => {
        const needle = val.toLowerCase()
        pageContext.filteredCategoryOptions =
          pageContext.categoryOptions.filter(
            (v) => v.label.toLowerCase().indexOf(needle) > -1
          )
      })
    }

    const filterSkill = (val, update) => {
      if (val === '') {
        update(() => {
          pageContext.filteredSkillOptions = pageContext.skillOptions
        })
        return
      }
      update(() => {
        const needle = val.toLowerCase()
        pageContext.filteredSkillOptions = pageContext.skillOptions.filter(
          (v) => v.label.toLowerCase().indexOf(needle) > -1
        )
      })
    }

    const filterEstadoOptions = (val, update) => {
      if (val === '') {
        update(() => {
          pageContext.filteredEstadoOptions = pageContext.estadoOptions
        })
        return
      }
      update(() => {
        const needle = val.toLowerCase()
        pageContext.filteredEstadoOptions = pageContext.estadoOptions.filter(
          (v) => v.label.toLowerCase().indexOf(needle) > -1
        )
      })
    }

    const filterMunicipioOptions = (val, update) => {
      if (val === '') {
        update(() => {
          pageContext.filteredMunicipioOptions = pageContext.municipioOptions
        })
        return
      }
      update(() => {
        const needle = val.toLowerCase()
        pageContext.filteredMunicipioOptions =
          pageContext.municipioOptions.filter(
            (v) => v.label.toLowerCase().indexOf(needle) > -1
          )
      })
    }

    return {
      tipo_perfil,
      tipos_perfil: [
        {
          label: 'Quiero publicar vacantes',
          value: 'Reclutador',
          color: 'primary',
        },
        {
          label: 'Quiero aplicar a vacantes',
          value: 'Aspirante',
          color: 'primary',
        },
      ],

      formData,
      submitResult,
      responseStatus,
      responseMessage,
      submitFormulario,
      alert,
      filterEstadoOptions,
      filterMunicipioOptions,
      filterCategory,
      filterSkill,
      preventMunicipiosMismatch,
      agregarNuevaHabilidad,
      pageContext,
    }
  },
  computed: {
    MaxDate() {
      let fecha = new Date()
      fecha.setFullYear(fecha.getFullYear() - 18)
      let min = fecha.toISOString().split('T')[0].split('-')
      min = `${min[0]}/${min[1]}`
      console.log(min)
      return min
    },
  },
})
</script>
