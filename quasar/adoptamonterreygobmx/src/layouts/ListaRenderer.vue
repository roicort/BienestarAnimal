<template>
  <div v-for="(mascota, index) in componentContext.animales" :key="index" @click="setSelectedPath(mascota)" class="col-12 col-md-3">

    <q-card class="my-card q-ml-lg q-mr-lg q-mb-xl" flat bordered>

      <q-img v-if="$q.screen.gt.sm && !siteContext.drawerRight" :src="mascota.animal_info.foto" :ratio="1 / 1"/>

      <q-card-section :horizontal="($q.screen.lt.sm || siteContext.drawerRight ) ? true : false"> 

        <q-img v-if="($q.screen.lt.sm || siteContext.drawerRight )" :src="mascota.animal_info.foto" :ratio="1 / 1" :style="($q.screen.lt.sm || siteContext.drawerRight ) ? 'width: 50%' : '' "/>

        <q-card-section>
        <div class="text-h5 q-mt-sm q-mb-xs">{{ mascota.animal_info.nombre }}</div>
        <div class="text-overline text-orange-9">{{ mascota.animal_info.categoria_nombre }}</div>

        <div class="text-caption text-grey q-mb-xs">
          {{ mascota.animal_info.descripcion }}
        </div>

        <q-item-section side top class="self-start text-right q-mb-xs">
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

        <q-item-section >

          <div v-if="mascota.asociacion_info" class="text-caption text-grey">
            <q-avatar rounded size="32px">
              <q-img v-if="mascota.asociacion_info.logo" :src="mascota.asociacion_info.logo" fit="contain" />
            </q-avatar>
            {{ mascota.asociacion_info.nombre }}
            <q-icon size="14px" name="verified" class="q-mb-xs"
              :color="mascota.asociacion_info.esta_verificada ? 'blue' : 'grey'">
              <q-tooltip :delay="1000" class="bg-grey-4 text-black" anchor="center end" self="center start">
                {{ mascota.asociacion_info.esta_verificada ? 'Asociacion verificada' : 'Asociacion no verificada' }}
              </q-tooltip>
            </q-icon>

          </div>
        
        </q-item-section>

        </q-card-section>

      </q-card-section>
      
    </q-card>

  </div>
</template>

<script setup lang="ts">

import { reactive } from 'vue'

import { useSiteContextStore } from 'stores/site-context'
import { useRouter } from 'vue-router'
import { getDetalleAnimal } from 'boot/utils'

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
  getDetalleAnimal(authStore.firebaseUserData.accessToken, job.animal).then(
    (response) => {
      console.log(response)
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
    const newPath = `/adopcion/${job.id}/`;
    router.push({ path: newPath });
  }
}

</script>