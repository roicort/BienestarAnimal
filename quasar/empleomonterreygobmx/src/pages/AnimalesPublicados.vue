<template>
  <q-page
    class="row items-start justify-evenly"
    style="max-width: 100%; margin: 0 auto"
  >
    <div class="col-12" v-bind:class="$q.screen.lt.sm ? 'q-py-md' : 'q-pa-xl'">
      <div class="">
        <p style="font-size: 30px">Mis animales en adopción</p>
      </div>

      <div class="row justify-end q-my-md">
        <q-btn
          color="no-shadow"
          class="bg-accent"
          unelevated
          no-caps
          :disable="loading"
          label="Publicar animal en adopción"
          to="/animales/publicar/"
        />
      </div>

      <JobLoader v-if="rows.length == 0 && pageContext.emptyPet == false"></JobLoader>

      <div v-if="pageContext.emptyPet == true" style="height:50vh;" class="flex full-width justify-center items-center">
        <div>
          <p>Aún no has publicado animales en adopción.</p>
        </div>
      </div>

      <q-table
        v-if="rows.length > 0"
        class="box-shadow-soft"
        style="max-width: 100%; min-height: 50%"
        :rows="rows"
        :columns="columns"
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
            <q-td colspan="100%">
              <q-btn
                @click="
                  router.push({ path: `/animales/detalle/${props.row.id}` })
                "
                outlined
                flat
                no-caps
                label="Detalle de animal"
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
import { defineComponent, onMounted, ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import { useAuthStore } from 'stores/auth'
import { useSiteContextStore } from 'stores/site-context'

import { getMisVacantes } from 'boot/utils'

import JobLoader from 'src/components/common/JobLoader.vue'

const authStore = useAuthStore()

export default defineComponent({
  name: 'ListadoEmpresa',
  components: {
    JobLoader,
  },
  setup() {
    const siteContext = useSiteContextStore()
    const router = useRouter()
    const route = useRoute()
    siteContext.current_page = route.path

    const pageContext = reactive({emptyPet:false})

    const rows = ref([])
    const columns = ref()

    onMounted(() => {
      setTimeout(() => {
        getMisVacantes(
          authStore.firebaseUserData.accessToken,
          authStore.perfilUsuario.vinculaciones_asociaciones
        ).then((vacantes) => {
          console.log(vacantes)
          if(vacantes.length == 0){
            pageContext.emptyPet = true
          }
          columns.value = [
            {
              name: 'id',
              label: 'ID',
              field: 'id',
              sortable: true,
            },
            {
              name: 'nombre',
              label: 'Animal',
              field: 'label',
              sortable: true,
            },
            {
              name: 'label',
              label: 'Nombre de asociacion animal',
              field: 'nombre_empresa',
              sortable: true,
            },
            {
              name: 'inicio',
              label: 'Inicio',
              field: 'fecha_publicacion_inicio',
              sortable: true,
            },
            {
              name: 'fin',
              label: 'Fin',
              field: 'fecha_publicacion_fin',
              sortable: true,
            },
          ]

          /*
          let fields = columns.value.map((item) => {
            return item.field
          })
          */

          vacantes.forEach((obj) => {
            obj.nombre_empresa = obj.asociacion_info.nombre
            rows.value.push(obj)
          })
        })
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
      rows,
      columns,
      onDetail,
      getMisVacantes,
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
