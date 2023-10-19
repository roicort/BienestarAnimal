<template>
  <q-page class="row items-start justify-evenly" style="max-width: 100%; margin: 0 auto">
    <JobLoader v-if="rows.length == 0 && pageContext.emptyPet == false"></JobLoader>
    <div class="col-12" v-bind:class="$q.screen.lt.sm ? 'q-py-md' : 'q-pa-xl'">
      <div class="">
        <p style="font-size: 30px">Postulaciones</p>
      </div>
      <template v-if="rows.length == 0 && pageContext.emptyPet">
        <div class="">
          <p>Aún no te has postulado a una adopción.</p>
          <router-link to="/">Ver animales</router-link>
        </div>
      </template>
      <q-table v-if="rows.length > 0" class="box-shadow-soft" style="max-width: 100%; min-height: 50%" :rows="rows"
        :columns="columns" row-key="value" virtual-scroll :virtual-scroll-item-size="48" :pagination="pagination"
        :rows-per-page-options="[0]" v-model:expanded="expanded" no-data-label="Aún no se encuentra nada aquí"
        no-results-label="La búsqueda no arrojó ningún resultado">
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th auto-width />
            <q-th v-for="col in props.cols" :key="col.name" :props="props">
              {{ col.label }}
            </q-th>
          </q-tr>
        </template>

        <template v-slot:body="props">
          <q-tr :props="props" :key="`m_${props.row.index}`">
            <q-td auto-width>
              <q-btn size="sm" color="accent" round dense @click="onDetail(props)"
                :icon="props.expand ? 'remove' : 'add'" />
            </q-td>

            <q-td v-for="col in props.cols" :key="col.name" :props="props">
              {{ col.value }}
            </q-td>
          </q-tr>

          <q-tr v-show="props.expand" :props="props" :key="`e_${props.row.index}`" class="q-virtual-scroll--with-prev">
            <q-td colspan="100%">
              <div class="row" v-if="props.row">
                <div class="col q-pa-md" v-if="props.row.estatus_aceptacion_postulacion === 'Aceptado'">
                  <q-card flat bordered style="height: 100%; white-space: pre-wrap">
                    <q-card-section>
                      <div class="text-h6">{{ 'A esta asociacion le interesa tu perfil' }}</div>
                      <div class="text-subtitle2">
                        {{ '¡Contacta a la asociacion en cuanto antes!' }}
                      </div>
                    </q-card-section>
                    <q-separator inset />
                    <q-card-section>
                      <div>
                        {{ 'Sucursal: ' + props.row.centro_info.nombre }}
                      </div>
                      <div>
                        {{ props.row.centro_info.domicilio }}
                      </div>
                      <div>
                        {{ props.row.centro_info.colonia }}
                      </div>
                      <div>
                        {{ props.row.centro_info.codigo_postal }}
                      </div>
                      <div class="q-pt-lg" v-if="props.row.centro_info.geom">
                        <MTYMapa :center="props.row.point">
                        </MTYMapa>
                      </div>
                    </q-card-section>
                  </q-card>
                </div>
                <div class="col q-pa-md">
                  <q-card flat bordered style="height: 100%; white-space: pre-wrap">
                    <q-card-section>
                      <div class="text-h6">{{ props.row.vacante_nombre }}</div>
                      <div class="text-subtitle2">{{ props.row.asociacion }}</div>
                    </q-card-section>
                    <q-separator inset />
                    <q-card-section>
                      <div class="max-width-text">
                        <span><strong>Descripción del empleo:</strong></span>
                        <p style="white-space: pre-wrap">
                          {{ props.row.animal_info.descripcion }}
                        </p>
                      </div>

                      <div class="max-width-text q-pb-sm">
                        <span class="text-weight-regular">Salario:</span>
                        <div v-if="props.row.animal_info.salario_minimo &&
                          props.row.animal_info.salario_maximo
                          ">
                          {{
                            new Intl.NumberFormat('es-MX', {
                              style: 'currency',
                              currency: 'MXN',
                            }).format(
                              props.row.animal_info.salario_minimo * 1000
                            )
                          }}
                          -
                          {{
                            new Intl.NumberFormat('es-MX', {
                              style: 'currency',
                              currency: 'MXN',
                            }).format(
                              props.row.animal_info.salario_minimo * 1000
                            )
                          }}
                          MXN
                        </div>
                        <div v-else-if="props.row.animal_info.salario_minimo &&
                            !props.row.animal_info.salario_maximo
                            ">
                          {{
                            new Intl.NumberFormat('es-MX', {
                              style: 'currency',
                              currency: 'MXN',
                            }).format(
                              props.row.animal_info.salario_minimo * 1000
                            )
                          }}
                          MXN
                        </div>
                        <div v-else-if="!props.row.animal_info.salario_minimo &&
                            props.row.animal_info.salario_maximo
                            ">
                          {{
                            new Intl.NumberFormat('es-MX', {
                              style: 'currency',
                              currency: 'MXN',
                            }).format(
                              props.row.animal_info.salario_maximo * 1000
                            )
                          }}
                          MXN
                        </div>
                        <div v-else></div>
                      </div>

                      <div v-if="props.row.animal_info.prestaciones_adicionales" class="max-width-text">
                        <span class="text-weight-regular">Prestaciones:</span>
                        <p style="white-space: pre-wrap">{{ props.row.animal_info.prestaciones_adicionales }}</p>
                      </div>


                      <div v-if="props.row.animal_info.experiencia_previa" class="max-width-text">
                        <span class="text-weight-regular">Experiencia requerida:</span>
                        <p style="white-space: pre-wrap">{{ props.row.animal_info.experiencia_previa }}</p>
                      </div>
                      <div v-if="props.row.animal_info.escolaridad_deseada" class="max-width-text q-pb-sm">
                        <span class="text-weight-regular">Nivel escolar:</span>
                        {{ props.row.animal_info.escolaridad_deseada }}
                      </div>

                      <div class="max-width-text q-pb-sm flex">
                        <span class="text-weight-regular">Rango de edad:</span>
                        <q-range class="q-pt-xl rango" readonly :model-value="{
                          min: props.row.animal_info.edad_minima || 0,
                          max: props.row.animal_info.edad_maxima || 100,
                        }" :min="0" :max="100" :step="10" markers thumb-size="26px" :left-label-value="(props.row.animal_info.edad_minima || '1') +
  ' años'
  " :right-label-value="(props.row.animal_info.edad_maxima || '100') +
    ' años'
    " label-always color="primary" />
                      </div>

                      <div v-if="props.row.animal_info.horario" class="max-width-text q-pt-sm q-pb-md">
                        <span class="text-weight-regular">Horario laboral:</span>
                        {{ props.row.animal_info.horario }}
                      </div>

                      <q-separator inset class="q-mb-lg" />

                      <div v-if="props.row.animal_info.requiere_licencia_conducir" class="max-width-text q-pb-sm">
                        <span class="text-weight-regular">Licencia de conducir</span>
                      </div>

                      <div v-if="props.row.animal_info.apto_estudiantes" class="max-width-text q-pb-sm">
                        <span class="text-weight-regular">Es apto para estudiantes</span>
                      </div>

                      <div v-if="props.row.animal_info.numero_vacantes_disponibles
                        " class="max-width-text q-pb-sm">
                        <span class="text-weight-regular">Vacantes disponibles:
                          {{
                            props.row.animal_info.numero_vacantes_disponibles
                          }}</span>
                      </div>

                      <div class="max-width-text q-pb-lg">
                        <span class="text-weight-regular">Habilidades:</span>
                        <template v-for="habilidad in props.row.animal_info
                          .habilidades_info" :key="habilidad.id">
                          <q-chip style="max-width: unset; font-weight: unset">{{ habilidad.nombre }}</q-chip>
                        </template>
                      </div>

                      <q-separator inset class="q-mb-lg" />

                      <div class="max-width-text q-pb-sm">
                        <div>
                          <span class="text-weight-regular">Publicado el:</span>
                          {{
                            new Date(
                              props.row.animal_info.fecha_publicacion_inicio
                            ).toLocaleDateString()
                          }}
                        </div>
                        <div>
                          <span class="text-weight-regular">Disponible hasta:</span>
                          {{
                            new Date(
                              props.row.animal_info.fecha_publicacion_fin
                            ).toLocaleDateString()
                          }}
                        </div>
                      </div>
                    </q-card-section>
                  </q-card>
                </div>
                <div class="col q-pa-md">
                  <q-card flat bordered style="height: 100%; white-space: pre-wrap">
                    <q-card-section>
                      <div class="flex items-center">
                        <div class="text-h6">{{ props.row.asociacion }}</div>
                        <q-icon size="sm" name="verified" class="q-mb-xs q-ml-xs" :color="props.row.animal_info.asociacion_info.esta_verificada
                          ? 'blue'
                          : 'grey'
                          " />
                      </div>
                      <div class="text-subtitle2">
                        {{ props.row.animal_info.asociacion_info.razon_social }}
                      </div>
                      <div class="text-subtitle3">
                        {{
                          props.row.animal_info.asociacion_info.domicilio +
                          ', ' +
                          props.row.animal_info.asociacion_info.colonia
                        }}
                      </div>
                      <q-separator inset />
                    </q-card-section>
                    <q-card-section>
                      <div style="white-space: pre-wrap" class="text-body">
                        {{ props.row.animal_info.asociacion_info.descripcion }}
                      </div>
                    </q-card-section>
                  </q-card>
                </div>
              </div>
              <div v-if="!props.row">
                <div class="col-4 self-center">
                  <JobLoader />
                </div>
              </div>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, onMounted, ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import { useAuthStore } from 'stores/auth'
import { useSiteContextStore } from 'stores/site-context'

import { getMisPostulaciones } from 'boot/utils'
import JobLoader from 'src/components/common/JobLoader.vue'
import MTYMapa from 'src/layouts/MTYMapa.vue'

const authStore = useAuthStore()

export default defineComponent({
  name: 'EmpleosPostulados',
  components: { JobLoader, MTYMapa },
  setup() {

    const siteContext = useSiteContextStore()
    const router = useRouter()
    const route = useRoute()
    siteContext.current_page = route.path

    const pageContext = reactive({ emptyPet: false })

    const rows = ref([])
    const columns = ref()

    onMounted(() => {
      siteContext.drawerRight = false
      setTimeout(() => {
        getMisPostulaciones(authStore.firebaseUserData.accessToken).then(
          (animales) => {
            console.log(animales)
            if (animales.length == 0) {
              pageContext.emptyPet = true
            }
            columns.value = [
              {
                name: 'value',
                label: 'ID',
                field: 'value',
                sortable: true,
              },
              {
                name: 'animal',
                label: 'ID Animal',
                field: 'animal',
                sortable: true,
              },
              {
                name: 'animal_nombre',
                label: 'Nombre Vacante',
                field: 'animal_nombre',
                sortable: true,
              },
              {
                name: 'asociacion',
                label: 'Asociacion Animal',
                field: 'asociacion',
                sortable: true,
              },
              {
                name: 'fecha_postulacion',
                label: 'Fecha Postulación',
                field: 'fecha_postulacion',
                sortable: true,
              },
              {
                name: 'fecha_evaluacion_postulacion',
                label: 'Fecha Evaluación',
                field: 'fecha_evaluacion_postulacion',
                sortable: true,
              },
              {
                name: 'estatus_aceptacion_postulacion_texto',
                label: 'Estatus',
                field: 'estatus_aceptacion_postulacion_texto',
              },
            ]

            /*
          let fields = columns.value.map((item) => {
            return item.field
          })
          */
            authStore.perfilUsuario.aceptaciones = 0
            animales.forEach((obj) => {
              if (obj.centro_info) { obj.centro_info = obj.centro_info[0] }
              if (obj.centro_info && obj.centro_info.geom) {
                let s = obj.centro_info.geom.split(';')[1]
                obj.point = s.substring(s.indexOf('(') + 1, s.indexOf(')')).replace('"', '').split(' ').map((item) => parseFloat(item))
                obj.projection = obj.centro_info.geom.split(';')[0]
              }
              obj.animal_nombre = obj.animal_info.nombre
              //obj.asociacion = obj.animal_info.asociacion_info.nombre
              obj.fecha_evaluacion_postulacion =
                obj.fecha_evaluacion_postulacion == null
                  ? 'Pendiente de evaluación'
                  : obj.fecha_evaluacion_postulacion
              if (obj.estatus_aceptacion_postulacion === true) {
                authStore.perfilUsuario.aceptaciones += 1
              }
              obj.estatus_aceptacion_postulacion_texto = obj.estatus_aceptacion_postulacion ? (obj.estaus_aceptacion_postulacion == true ? 'Aceptado' : 'No cubre el perfil') : 'Pendiente'
              rows.value.push(obj)
            })
          }
        )
      }, 1000)
    })

    const onDetail = (props) => {
      props.expand = !props.expand
    }

    const formatDate = (dateString) => {
      const fecha = new Date(dateString)
      const day = fecha.getDate().toString().padStart(2, '0')
      const month = (fecha.getMonth() + 1).toString().padStart(2, '0')
      const year = fecha.getFullYear()
      return `${day}/${month}/${year}`
    }

    return {
      alert,
      expanded: ref(),
      router,
      authStore,
      pageContext,
      rows,
      columns,
      onDetail,
      formatDate,
      pagination: {
        rowsPerPage: 0,
      },
    }
  },
})
</script>

<style scoped lang="scss">
.sticky-column-table {
  /* specifying max-width so the example can
    highlight the sticky column on any browser window */
  max-width: 600px;

  thead tr:last-child th:last-child {
    /* bg color is important for th; just specify one */
    background-color: #fff;
  }

  td:last-child {
    background-color: #cbeee6;
    text-align: center !important;
  }

  th:last-child,
  td:last-child {
    position: sticky;
    right: 0;
    z-index: 1;
    text-align: center !important;
  }
}
</style>
