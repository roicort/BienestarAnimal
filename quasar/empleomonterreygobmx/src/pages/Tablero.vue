<template>
  <q-page class="row items-center justify-evenly" style="max-width: 1100px; margin: 0 auto">
    <div class="col-12 col-md-10 col-lg-10" v-bind:class="$q.screen.lt.sm ? 'q-py-md' : 'q-pa-xl'">
      <div class="text-center">
        <p style="font-size: 30px; margin: 0 0 2px 0">Tablero de analíticas</p>
        <p class="text-grey-8" style="font-size: 0.875rem; font-weight: 400">
          Aquí podrás encontrar estadístcas sobre las solicitudes de empleo.
        </p>
      </div>

      <div class="row justify-center align-center">
        <div class="col-xs-12">
          <div class="q-py-sm">
            <div class="texto-marcado-contenedor max-width-content q-mx-auto">
              <div class="q-px-lg">
                <template v-for="id in pageContext.targets" :key="id"> 
                  <div ref="TableroView" :id="id" style="height: 500px"><q-resize-observer @resize="onResize" /></div>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
        <JobLoader v-if="pageContext.empty == true"></JobLoader>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, reactive, onMounted } from 'vue'
import Plotly from 'plotly.js-dist'
import { useAuthStore } from 'stores/auth'
import { getPostulados } from 'boot/utils'
import JobLoader from 'src/components/common/JobLoader.vue'

export default defineComponent({
  name: 'TableroView',
  components: {
    JobLoader,
  },
  setup() {

    const authStore = useAuthStore()
    const pageContext = reactive({
      raw_data: [],
      targets: [
      '#oatrnroernb',
      ],
      empty: true,
    })

    const createChart = (target, data) => {
      pageContext.targets.push(target)
      const ctx = document.getElementById(target)
      Plotly.newPlot(ctx, data)
    }

    onMounted(() => {
      setTimeout(() => {

        getPostulados(authStore.firebaseUserData.accessToken).then(
          (vacantes) => {
            vacantes.forEach((obj) => {
              pageContext.raw_data.push(obj.estatus_aceptacion_postulacion)
            })
          }
        ).finally(() => {

          var data = [
            {
              values: [pageContext.raw_data.filter(element => element == true).length, pageContext.raw_data.filter(element => element == false).length, pageContext.raw_data.filter(element => element == null).length],
              labels: ['Colocados', 'En seguimiento', 'En revisión'],
              type: 'pie'
            }
          ]

          var layout = { 
            title: 'Responsive to window\'s size!',
            font: {size: 18}
          };

          createChart(pageContext.targets[0], data, layout)
          pageContext.empty = false

        })

      }, 1000)
    })
    return {
      pageContext,
    }
  },
  methods: {
    onResize() {
      for (let i = 0; i < this.pageContext.targets.length; i++) {
        const ctx = document.getElementById(this.pageContext.targets[i])
        Plotly.Plots.resize(ctx)
      }
    },
  },
})
</script>
