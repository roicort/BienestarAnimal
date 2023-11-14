<template>
  <q-page class="row items-center justify-evenly" style="max-width: 1100px; margin: 0 auto">
    <div class="col-12 col-md-10 col-lg-10" v-bind:class="$q.screen.lt.sm ? 'q-py-md' : 'q-pa-xl'">
      
      <div class="text-center">
        <p style="font-size: 30px; margin: 0 0 2px 0">Acerca</p>
        <q-separator />
        <p class="text-grey-8 q-pt-sm" style="font-size: 0.875rem; font-weight: 400">
          Sobre Adopta Monterrey
        </p>
      </div>
      
      <div class="flex full-width justify-center items-center q-pt-md">
        {{ 'Este es in proyecto de la Secretaría de Innovación y Gobierno Abierto del Municipio de Monterrey en conjunto con la Secretaría de Desarrollo Económico.' }}
      </div>

      <div class="q-mx-auto q-pt-xl" :style="$q.screen.lt.sm  ? 'max-width: 30%' : 'max-width: 10%'">
        <img
          src="/img/logos/logo_siga.png"
          alt="Adopta Monterrey - Gobierno de Monterrey"
        />
      </div>

      <div class="flex full-width justify-center items-center q-pt-xl">
          <p style="font-size: 20px">Software Libre y de Código Abierto</p>
      </div>

      <div class="flex full-width justify-center items-center">
        <ul>
          <li>Django</li>
          <li>Vue3</li>
          <li>Quasar</li>
        </ul>
      </div>

      <div class="flex full-width justify-center items-center q-pt-lg">
          <p style="font-size: 20px">Licencia</p>
      </div>

      <div class="flex full-width justify-center items-center">
        {{ 'Este es un proyecto con licencia MIT' }}
      </div>

      
      <div class="flex full-width justify-center items-center q-pt-xl">
        <p style="font-size: 14px">{{ 'Hecho con ❤️ en Monterrey. Dirección de Gobierno Digital, 2023.' }}</p>
      </div>

      <div class="flex text-grey full-width justify-center items-center q-pt-sm">
        <p style="font-size: 2px">{{ 'Rodrigo Cortez Madrigal estuvo aquí.' }}</p>
      </div>
      
      <JobLoader v-if="pageContext.empty == true"></JobLoader>
    </div>
  </q-page>
</template>

<script>

import { defineComponent, reactive } from 'vue'
import JobLoader from 'src/components/common/JobLoader.vue'

export default defineComponent({
  name: 'AcercaView',
  components: {
    JobLoader,
  },
  setup() {

    //const authStore = useAuthStore()
    const pageContext = reactive({
      empty: false,
    })

    return {
      pageContext,
    }
  }
})
</script>
