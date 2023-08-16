<template>
  <!-- Boton Flotante Acciones-->
  <div v-if="siteContext.fab.length > 0" class="boton-flotante-acciones fixed-bottom-right"
       v-bind:class="$q.screen.lt.sm ? 'q-ma-md' : 'q-ma-xl'">
    <q-fab
      ref="botonFlotanteAccion"
      v-model="botonFlotante"
      rounded
      label="Accesos rápidos"
      label-position="left"
      vertical-actions-align="right"
      color="primary"
      icon="mdi-plus"
      direction="up"
      class="shadow-15"
      @show="ocultarEtiquetaBotonFlotante = false"
      @hide="ocultarEtiquetaBotonFlotante = true"
      :hide-label="ocultarEtiquetaBotonFlotante"
      tabindex="0"
    >

    <template v-for="(item, index) in siteContext.fab" :key="index">

      <q-fab-action
        v-if="item.value.enlace.tipo == 'url' "
        class="q-px-md shadow-10"
        square
        label-position="left"
        :color="item.value.color"
        :icon="item.value.icono"
        :label="item.value.enlace.titulo"
        @click="enviarEnlace(item)"
        :href="item.value.enlace.url"
      />

      <q-fab-action
        v-if="item.value.enlace.tipo == 'pagina' "
        class="q-px-md shadow-10"
        square
        label-position="left"
        :color="item.value.color"
        :icon="item.value.icono"
        :label="item.value.enlace.titulo"
        @click="enviarEnlace(item)"
      />

    </template>
    </q-fab>
  </div>
  <!-- Boton flotante Acciones-->
</template>

<script>
import {defineComponent, ref} from 'vue'
import {useRouter} from 'vue-router'
import {apiEmpleo} from 'boot/axios'

export default defineComponent({
  name: 'BotonFlotanteAcciones',
  props: ['count', 'acciones'],
  setup(props) {
    const router = useRouter()
    const botonFlotanteAccion = ref(null)
    const botonFlotante = ref(null)
    const counter = ref(props.count)
    const listaAcciones = ref(props.acciones)
    const ocultarEtiquetaBotonFlotante = ref(true)

    const enviarEnlace = (item) => {
      if (item.value.enlace.tipo === 'pagina') {
        apiEmpleo.get(`/paginas/${item.value.enlace.pagina}/`).then(response => {
          window.location.assign(response.data.meta.html_url.replace('cms.', ''))
        })
      } else {
        window.open(item.value.enlace.url)
      }
    }

    return {
      router,
      botonFlotante,
      counter,
      ocultarEtiquetaBotonFlotante,
      listaAcciones,
      enviarEnlace,
      botonFlotanteAccion,
      siteContext,
    }
  },
})
</script>

<style lang="scss" scoped>

  .boton-flotante-acciones {
    z-index: 800;
  }

  // Alineacion de items boton flotante
  .q-fab--align-right > .q-fab__actions--up,
  .q-fab--align-right > .q-fab__actions--down {
    align-items: stretch;
    min-width: 125px;
  }

</style>
