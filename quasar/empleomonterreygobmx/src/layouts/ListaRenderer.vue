<template>
  <div v-for="(mascota, index) in componentContext.animales" :key="index" @click="setSelectedPath(mascota)" class="col-12 col-md-3">

    <q-card class="my-card q-ml-lg q-mr-lg q-mb-xl" flat bordered>

      <q-card-section horizontal>
        <q-img :src="mascota.foto" :ratio="1 / 1" />
      </q-card-section>

      <q-card-section>
        <div class="text-overline text-orange-9">{{ mascota.categoria_info.nombre }}</div>
        <div class="text-h5 q-mt-sm q-mb-xs">{{ mascota.label }}</div>
        <div class="text-caption text-grey">
          {{ mascota.descripcion }}
        </div>

        <q-item-section side top class="self-start text-right">
          <q-item-label caption>
            hace
            {{
              Math.floor(
                (Date.now() -
                  new Date(mascota.fecha_publicacion_inicio)) /
                1000 /
                60 /
                60 /
                24
              )
            }}
            {{
              Math.floor(
                (Date.now() - new Date(mascota.fecha_publicacion_fin)) /
                1000 /
                60 /
                60 /
                24
              ) > 1
              ? 'días'
              : 'día'
            }}
          </q-item-label>
        </q-item-section>

      </q-card-section>

      <q-card-section>
        <q-avatar rounded size="20px">
          <q-img v-if="mascota.asociacion_info.logo" :src="mascota.asociacion_info.logo" fit="contain" />
          <span v-else class="text-white text-weight-regular">
            {{ mascota.nombre.slice(0, 1) }}
          </span>
        </q-avatar>
        <div v-if="mascota.label" class="text-caption text-grey">
          {{ mascota.asociacion_info.nombre }}
          <q-icon size="xs" name="verified" class="q-mb-xs"
            :color="mascota.asociacion_info.esta_verificada ? 'blue' : 'grey'">
            <q-tooltip :delay="1000" class="bg-grey-4 text-black" anchor="center end" self="center start">
              {{ mascota.asociacion_info.esta_verificada ? 'Empresa verificada' : 'Empresa no verificada' }}
            </q-tooltip>
          </q-icon>
        </div>
      </q-card-section>
      
    </q-card>
  </div>
</template>

<script setup lang="ts">

import { reactive } from 'vue'

import { useSiteContextStore } from 'stores/site-context'
import { useRouter } from 'vue-router'
import { getDetalleVacante } from 'boot/utils'

import { useAuthStore } from 'stores/auth'
const authStore = useAuthStore()


const siteContext = useSiteContextStore()
const router = useRouter()

const props = defineProps({
  animales: { type: ArrayBuffer },
});

const componentContext = reactive({
  animales: props.animales
});

const diasdesdepublicacion = (fecha_publicacion_inicio: any) => {
  return Math.floor(
    (Date.now() - new Date(fecha_publicacion_inicio)) /
    1000 /
    60 /
    60 /
    24
  )
}

const setSelectedJob = (job) => {
  siteContext.drawerRight = true
  siteContext.loading_job = true
  getDetalleVacante(authStore.firebaseUserData.accessToken, job.id).then(
    (response) => {
      siteContext.animal_seleccionado = response
      siteContext.loading_job = false
    }
  )
}

const setSelectedPath = (job: any) => {

  siteContext.drawerRight = true

  const currentRoute = router.currentRoute.value.path;
  if (currentRoute.includes('favoritos')) {
    setSelectedJob(job)
  } else {
    const newPath = `/animales/${job.id}/`;
    router.push({ path: newPath });
  }
}

</script>