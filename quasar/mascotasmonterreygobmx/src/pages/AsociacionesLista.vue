<template>
  <q-page
    class="row items-start justify-evenly"
    style="max-width: 100%; margin: 0 auto"
  >
    <div class="col-12" v-bind:class="$q.screen.lt.sm ? 'q-py-md' : 'q-pa-xl'">
      <div class="">
        <p style="font-size: 30px">Asociaciones animales</p>
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
          <p>Aún no has registrado una asociacion animal o no tienes permisos para editar.</p>
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
        {{ pageContext }}

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
            <q-td colspan="100%">
              <div class="col-4">{{ props.row.sucursales }}</div>
              <div class="col-4">{{ props.row.vinculaciones }}</div>
              <q-btn
                @click="router.push({ path: `/asociaciones/${props.row.value}` })"
                outlined
                flat
                no-caps
                label="Detalle empresa"
                class="text-accent"
              />
              <q-btn
                @click="
                  router.push({
                    path: `/asociaciones/centros/${props.row.value}`,
                  })
                "
                outlined
                flat
                no-caps
                label="Detalle sucursales"
                class="text-accent"
              />
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from 'stores/auth'
import JobLoader from 'src/components/common/JobLoader.vue'
import { getAsociaciones } from 'boot/utils'

const authStore = useAuthStore()
export default defineComponent({
  name: 'EmpresaLista',
  components: { JobLoader },
  // Watch for changes on siteContext.current_page
  watch: {
    siteContext: {
      handler: function (val) {
        console.log('siteContext changed', val)
      },
      deep: true,
    },
  },
  setup() {
    const router = useRouter()
    const pageContext = reactive({
      companies: [],
      rows: [],
      columns: [],
      emptyPet: false,
    })

    pageContext.columns = [
      {
        name: 'value',
        label: 'ID',
        field: 'value',
        sortable: true,
      },
      {
        name: 'label',
        label: 'Nombre',
        field: 'label',
        sortable: true,
      },
      {
        name: 'verificada',
        label: 'Verificada',
        field: 'esta_verificada',
        sortable: true,
      },
      {
        name: 'razon_social',
        label: 'Razon Social',
        field: 'razon_social',
        sortable: true,
      },
    ]

    onMounted(() => {
      setTimeout(() => {
        if (authStore.localUserData.is_staff) {
          getAsociaciones(authStore.firebaseUserData.accessToken).then(
            (companies) => {
              companies.forEach((obj) => {
                pageContext.rows.push(obj)
              })
              if (pageContext.rows == 0) {
                pageContext.emptyPet = true
              }
            }
          )
        } else {
          
          var permisos = authStore.perfilUsuario.vinculaciones_asociaciones.filter(
              (permiso) => permiso.user_rol == 'coordinador'
            )
            permisos.forEach((obj) => {
              obj.asociacion_info.label = obj.asociacion_info.nombre_comercial
              obj.asociacion_info.value = obj.asociacion_info.id
              pageContext.rows.push(obj.asociacion_info)
            })
          if (pageContext.rows == 0) {
            pageContext.emptyPet = true
          }
        }
      }, 2000)
    })
    const onDetail = (props) => {
      props.expand = !props.expand
    }
    return {
      alert,
      expanded: ref(),
      router,
      authStore,
      pageContext,
      onDetail,
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
