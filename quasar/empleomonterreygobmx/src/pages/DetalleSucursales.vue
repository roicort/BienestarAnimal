<template>
  <q-page
    class="row items-start justify-evenly"
    style="max-width: 100%; margin: 0 auto"
  >
    <div class="col-12" v-bind:class="$q.screen.lt.sm ? 'q-py-md' : 'q-pa-xl'">
      <div class="">
        <p style="font-size: 30px">Listado Sucursales</p>
      </div>

      <div class="row justify-end q-my-md">
        <q-btn
          color="no-shadow"
          class="bg-accent"
          unelevated
          no-caps
          :disable="loading"
          label="Agregar sucursal"
          :to="`/empresas/sucursales/registrar/${empresaID}`"
        />
      </div>

      <q-table
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
            <q-td colspan="100%">
              <template v-for="field in Object.keys(props.row)" :key="field">
                <div class="col-4">{{ field }}: {{ props.row[field] }}</div>
              </template>
              <div class="col-4">{{ props.row.sucursales }}</div>
              <div class="col-4">{{ props.row.vinculaciones }}</div>
              <q-btn
                @click="
                  router.push({
                    path: `/empresas/sucursales/detalle/${props.row.value}`,
                  })
                "
                outlined
                flat
                no-caps
                label="Detalle"
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
import { defineComponent, ref, onBeforeMount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from 'stores/auth'
import { useQuasar } from 'quasar'

import { useSiteContextStore } from 'stores/site-context'

import { apiEmpleo } from '../boot/axios'

import { getSucursales } from '../boot/utils'

export default defineComponent({
  name: 'DetalleSucursales',
  props: ['id'],
  setup() {
    const siteContext = useSiteContextStore()
    siteContext.selected_job = null
    const router = useRouter()
    const route = useRoute()
    siteContext.current_page = route.path

    const pageContext = ref({
      rows: [],
      columns: [],
    })

    const empresaID = route.params.id

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
        getSucursales(authStore.firebaseUserData.accessToken, empresaID).then(
          (sucursales) => {
            pageContext.value.columns = [
              {
                name: 'value',
                label: 'ID',
                field: 'value',
                sortable: true,
              },
              {
                name: 'label',
                label: 'Nombre comercial',
                field: 'label',
                sortable: true,
              },
              {
                name: 'domicilio',
                label: 'Domilicio',
                field: 'domicilio',
                sortable: true,
              },
            ]

            /*
          let fields = columns.value.map((item) => {
            return item.field
          })
          */

            sucursales.forEach((obj) => {
              /*
            for (let key in obj) {
              if (!fields.includes(key)) {
                delete obj[key]
              }
              if (obj[key] === 'null') {
                obj[key] = ''
              }
            }*/
              pageContext.value.rows.push(obj)
            })
          }
        )
      }, 1000)
    })

    const showNotificacion = (message, color, actions) => {
      $q.notify({
        message: message,
        color: color,
        actions: actions,
      })
    }

    const submitFormulario = () => {
      // TODO: Verificar en quasar label y value de los selects

      formData.value.estado = pageContext.value.estado.value
      formData.value.municipio = pageContext.value.municipio.value
      formData.value.localidad = pageContext.value.localidad.value
      formData.value.giro = pageContext.value.giro.value

      $q.loading.show({
        message:
          'Estamos enviando la información. Espere un momento por favor...',
      })
      apiEmpleo
        .put('/empresas/empresa/', formData.value, {
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

    const onDetail = (props) => {
      props.expand = !props.expand
      /*
        getSucursales(authStore.firebaseUserData.accessToken, props.row.value).then(sucursales => {
          //console.log('sucursales', sucursales)
          props.row.sucursales = sucursales
        })
        */
      /*
        getVinculaciones(authStore.firebaseUserData.accessToken, props.row.value).then(vinculaciones => {
          //console.log('vinculaciones', vinculaciones)
          props.row.vinculaciones = vinculaciones
        })
        */
    }

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
      empresaID,
      onDetail,

      isValidDomain,
      alert,
      submitFormulario,
    }
  },
})
</script>
