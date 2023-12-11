<template>
  <q-page
    class="row items-start justify-evenly"
    style="max-width: 100%; margin: 0 auto"
  >
    <div class="col-12" v-bind:class="$q.screen.lt.sm ? 'q-py-md' : 'q-pa-xl'">
      <div class="">
        <p style="font-size: 30px">Solicitudes de adopción</p>
      </div>

      <JobLoader
        v-if="pageContext.rows.length == 0 && pageContext.emptyPet == false"
      ></JobLoader>

      <div
        v-if="pageContext.emptyPet == true"
        style="height: 50vh"
        class="flex full-width justify-center items-center"
      >
        <div>
          <p>No hay solicitudes por ahora.</p>
        </div>
      </div>

      <q-table
        v-if="pageContext.rows.length > 0"
        class="box-shadow-soft"
        style="max-width: 100%; min-height: 50%"
        :rows="pageContext.rows"
        :columns="pageContext.columns"
        row-key="value"
        virtual-scroll
        :virtual-scroll-item-size="48"
        :pagination="pagination"
        :rows-per-page-options="[0]"
        v-model:expanded="expanded"
        no-data-label="Aún no se encuentra nada aquí"
        no-results-label="La búsqueda no arrojó ningún resultado"
      >
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
              <q-btn
                size="sm"
                color="accent"
                round
                dense
                @click="onDetail(props)"
                :icon="props.expand ? 'remove' : 'add'"
              />
            </q-td>

            <q-td v-for="col in props.cols" :key="col.name" :props="props">
              {{ col.value }}
            </q-td>
          </q-tr>

          <q-tr
            v-show="props.expand"
            :props="props"
            :key="`e_${props.row.index}`"
            class="q-virtual-scroll--with-prev"
          >
            <q-td colspan="100%" >
              <div class="row" v-if="props.row.perfil">
                <div class="col-4 self-center">
                  <div>
                    <q-chip>{{ 'Fecha: '+props.row['fecha_postulacion'] }}</q-chip>
                    <q-chip v-if="props.row['estatus_aceptacion_postulacion'] != null">{{ props.row['estatus_aceptacion_postulacion'] ? 'Aceptado' : 'Rechazado' }}</q-chip>
                    <q-chip v-if="props.row['fecha_evaluacion_postulacion']" > {{ props.row['fecha_evaluacion_postulacion'] }}</q-chip>
                  </div>
                  <div v-if="props.row.estatus_aceptacion_postulacion === null">
                    <q-btn
                      color="primary"
                      label="Contactar"
                      class="q-ma-md"
                      @click="setAceptacion(props, true)"
                    />
                    <q-btn
                      color="primary"
                      label="Rechazar"
                      class="q-ma-md"
                      @click="setAceptacion(props, false)"
                    />
                  </div>
                </div>
                <div class="col-8 q-pa-xl" >
                  <q-card bordered >
                    <q-card-section>
                      <div class="text-h6">{{ props.row.perfil.nombre + ' ' + props.row.perfil.apellidos}}</div>
                      <div class="text-subtitle2">{{ props.row.perfil.empleo_actual}}</div>
                      <div class="text-subtitle3">{{ props.row.perfil.ciudad + ', '+props.row.perfil.estado }}</div>
                    </q-card-section>
                    <q-separator inset />
                    <q-card-section>
                      <span style="white-space: pre-wrap;">{{ props.row.perfil.biografia }}</span>
                    </q-card-section>
                  </q-card>
                </div>
              </div>
              <div v-else>
                <div class="col-4 self-center">
                <JobLoader/>
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
import {apiAdopta} from 'boot/axios'

import { getPostulados, getPerfil } from 'boot/utils'
import JobLoader from 'src/components/common/JobLoader.vue'
import { useQuasar } from 'quasar'

const authStore = useAuthStore()

export default defineComponent({
  name: 'ReclutadoresPostulaciones',
  components: {JobLoader},
  setup() {
    const siteContext = useSiteContextStore()
    const router = useRouter()
    const route = useRoute()
    siteContext.current_page = route.path

    const $q = useQuasar()

    const pageContext = reactive({
      rows: [],
      columns: [],
      emptyPet: false,
    })

    onMounted(() => {
      siteContext.drawerRight = false
      setTimeout(() => {
        getPostulados(authStore.firebaseUserData.accessToken).then(
          (solicitudes) => {
            pageContext.columns = [
              {
                name: 'value',
                label: 'ID',
                field: 'value',
                sortable: true,
              },
              {
                name: 'vacante',
                label: 'ID Vacante',
                field: 'vacante',
                sortable: true,
              },
              {
                name: 'vacante_nombre',
                label: 'Nombre Vacante',
                field: 'vacante_nombre',
                sortable: true,
              },
              {
              name: 'empresa',
                label: 'Empresa',
                field: 'empresa',
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
                name: 'estatus_aceptacion_postulacion',
                label: 'Estatus',
                field: 'estatus_aceptacion_postulacion_text',
              },
            ]

            /*
          let fields = columns.value.map((item) => {
            return item.field
          })
          */

          solicitudes.forEach((obj) => {
              console.log(obj)
              pageContext.rows.push(obj)
            })
            if (pageContext.rows == 0) {
              pageContext.emptyPet = true
            }
          }
        )
      }, 1000)
    })

    const onDetail = (props) => {
      if(!props.expand){
      getPerfil(authStore.firebaseUserData.accessToken, props.row.user).then(
        (perfil) => {
          props.row.perfil = perfil
        }
      )
      }
      props.expand = !props.expand
    }

    const setAceptacion = (props, estado) => {
      $q.dialog({
          title: estado ? 'Contactar' : 'Rechazar',
          message: 'Esta acción es irreversible, ¿Desea continuar?',
          persistent: false,
          ok: {
            label: 'Aceptar',
            color: 'primary',
            class: 'no-caps'
          },
        }).onOk(() => {
          apiAdopta
            .patch('/empleos/postulacion-vacante/' + props.row.value + '/', { 'estatus_aceptacion_postulacion': estado },
                { headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authStore.firebaseUserData.accessToken }, }
            ).then((response) => {
                $q.loading.hide()
                showNotificacion(
                  response.status === 200
                    ? 'Actualizado exitosamente'
                    : 'Ocurrió un error: ' + response.status,
                  response.status === 200 ? 'green' : 'red'
                )})
            .catch((error) => {
              console.log(error)
            })
        }).onDismiss(() => {
          console.log('Solo ando viendo...')
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
      alert,
      expanded: ref(),
      router,
      authStore,
      pageContext,
      onDetail,
      showNotificacion,
      setAceptacion,
      JobLoader,
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
