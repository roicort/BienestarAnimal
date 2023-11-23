<template>

  <q-dialog v-model="pageContext.dialog">
    <q-card>

      <q-card-section>
        <div class="text-h6">Solicitud de adopción</div>
      </q-card-section>

      <q-separator />

      <q-card-section style="max-height: 50vh" class="scroll">
        <q-form @submit.prevent="submitPostulacion" ref="formulario" greedy class="q-gutter-lg">

          <mty-form-field-input for="cuidados" label="Describa los cuidados" required v-model="formData.cuidados"
            type="textarea" hint="Describa a continuación sus cuidados" />

          <mty-form-field-input for="espacio" label="Descripción del espacio" required v-model="formData.espacio"
            type="textarea" hint="Describa a continuación su espacio" />

          <q-checkbox dense outlined label="¿Considera que el espacio es seguro?" v-model="formData.seguridad"
            color="accent" />

          <q-checkbox dense outlined label="¿Tiene techo?" v-model="formData.techo" color="accent" />

          <q-checkbox dense outlined label="¿Saldrá a la calle?" v-model="formData.salida_calle" color="accent" />

          <mty-form-field-input for="precauciones" label="Descripción de las precauciones" required
            v-model="formData.precauciones" type="textarea" hint="Describa a continuación las precauciones" />

          <q-checkbox dense outlined label="¿Toleraría destrozos?" v-model="formData.destrozos" color="accent" />

          <mty-form-field-input for="alimentacion" label="Descripción de la alimentación" required
            v-model="formData.alimentacion" type="textarea" hint="Describa a continuación la alimentación" />

          <q-checkbox dense outlined label="¿Podría economicamente afrontar enfermedades?" v-model="formData.enfermedades"
            color="accent" />

          <mty-form-field-input for="atencion_veterinaria" label="Descripción de la atención veterinaria" required
            v-model="formData.atencion_veterinaria" type="textarea"
            hint="Describa a continuación la atención veterinaria" />

          <mty-form-field-input for="conservacion" label="¿Hay algo que te impediria conservarlo?" required
            v-model="formData.conservacion" type="textarea"
            hint="Describa a continuación si hay algo que te impediria conservarlo" />

          <q-checkbox dense outlined label="¿Está de acuerdo con que sea esterilizado?" v-model="formData.esterilizacion"
            color="accent" />

          <q-checkbox dense outlined label="¿Está de acuerdo con llevarle a consultas veterinarias de seguimiento?"
            v-model="formData.consulta_seguimiento" color="accent" />

          <q-checkbox dense outlined label="¿Todos los habitantes de su hogar estan de acuerdo?"
            v-model="formData.acuerdo" color="accent" />

        </q-form>
      </q-card-section>

      <q-separator />

      <q-card-actions align="right">
        <q-btn flat label="Declinar" color="primary" v-close-popup />
        <q-btn flat label="Enviar" color="primary" @click="submitPostulacion" />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-card class="box-shadow-soft"
    :class="(!!!siteContext.drawerLeft || $q.screen.gt.sm ? '' : 'q-ml-xl') + ($q.screen.gt.md ? ' q-pa-xl' : ' q-pa-md')">

    <q-btn v-if="$q.screen.lt.md" @click="siteContext.drawerRight = false" no-caps flat round size="md"
      color="grey-3"><q-icon color="primary" name="close"></q-icon></q-btn>
    <q-btn v-else @click="siteContext.drawerRight = false" no-caps flat round size="md" color="grey-3"><q-icon
        color="primary" name="close"></q-icon></q-btn>

    <q-card-section class="q-px-lg q-pt-lg">
      <div class="row justify-between">
        <div class="text-h4 text-grey-8 q-mb-md">
          {{ siteContext.animal_seleccionado.nombre }}
        </div>
        <q-space></q-space>
        <div class="col-auto self-center text-right">
          <q-btn v-if="authStore.firebaseUserData.uid === null" @click="
            authStore.firebaseUserData.uid
              ? presubmitPostulacion()
              : (showAvisoNoAuth = true)
            " no-caps flat round size="md" color="grey-3">
            <q-icon name="mdi-bookmark-outline" color="primary"></q-icon>
          </q-btn>
          <q-btn v-else v-bind:class="{ active: esFavorito }" @click="toggleFavorite()" no-caps flat round size="md"
            color="grey-3">
            <q-icon :name="esFavorito ? 'mdi-bookmark' : 'mdi-bookmark-outline'" color="primary"></q-icon>
          </q-btn>
        </div>
      </div>

      <div class="text-weight-regular text-grey-8">
        {{ siteContext.animal_seleccionado.asociacion_info.nombre }}
        <q-icon size="sm" name="verified" class="q-mb-xs" :color="siteContext.animal_seleccionado.asociacion_info.esta_verificada
          ? 'blue'
          : 'grey'
          ">
          <q-tooltip :delay="1000" class="bg-grey-4 text-black" anchor="center end" self="center start">
            {{
              siteContext.animal_seleccionado.asociacion_info.esta_verificada
              ? 'Empresa verificada'
              : 'Empresa no verificada'
            }}
          </q-tooltip>
        </q-icon>
      </div>

      <div class="q-pt-md q-pb-lg">
        <q-chip style="max-width: unset; font-weight: unset" v-if="siteContext.animal_seleccionado.categoria">
          {{ siteContext.animal_seleccionado.categoria_info.nombre }}
        </q-chip>
      </div>

      <div class="row justify-center q-pt-md">
        <q-avatar size="10rem">
          <q-img v-if="siteContext.animal_seleccionado.foto" :src="siteContext.animal_seleccionado.foto" :ratio="1 / 1" />
          <span v-else class="text-white text-weight-regular">
            {{ siteContext.animal_seleccionado.nombre.slice(0, 1) }}
          </span>
        </q-avatar>
      </div>

      <div class="row justify-center q-pt-md">
        <div class="col-auto q-pa-md">
          <q-card flat style="height: 7.5em; width: 7.5em;">
            <q-list class="q-ma-sm">
              <q-item>
                <q-item-section class="items-center" style="text-align: center;">
                  <q-icon style="font-size: xx-large;" color="primary" name="pets" />
                </q-item-section>
              </q-item>
              <q-item-section style="text-align: center;">
                <q-item-label>Cumpleaños</q-item-label>
                <q-item-label caption>{{ siteContext.animal_seleccionado.fecha_nacimiento }}.</q-item-label>
              </q-item-section>
            </q-list>
          </q-card>
        </div>

        <div class="col-auto q-pa-md">
          <q-card flat style="height: 7.5em; width: 7.5em;">
            <q-list class="q-ma-sm justify-center">
              <q-item>
                <q-item-section class="items-center" style="text-align: center;">
                  <q-icon style="font-size: xx-large;" color="primary" :name="siteContext.animal_seleccionado.sexo == 'macho' ? 'male' : siteContext.animal_seleccionado.sexo == 'hembra' ? 'female': ''" />
                </q-item-section>
              </q-item>
              <q-item-section style="text-align: center;">
                <q-item-label>Sexo</q-item-label>
                <q-item-label caption>{{ siteContext.animal_seleccionado.sexo}}</q-item-label>
              </q-item-section>
            </q-list>
          </q-card>
        </div>

      </div>

      <q-separator class="q-ml-xl q-mr-xl q-mb-xl"></q-separator>

      <div class="row justify-center q-pb-xl text-grey-8" style="text-align: justify;">
        <span :style="$q.screen.gt.md ? 'max-width: 90%;' : 'max-width: 100%'">
          {{ siteContext.animal_seleccionado.descripcion }}
        </span>
      </div>

    </q-card-section>

    <q-separator class="q-ml-xl q-mr-xl q-mb-xl"></q-separator>

    <div class="row justify-center q-pb-lg">
      <q-avatar rounded size="4em" :color="siteContext.animal_seleccionado.asociacion_info.logo ? 'white' : 'primary'
        " class="box-shadow-soft q-mr-md">
        <q-img v-if="siteContext.animal_seleccionado.asociacion_info.logo"
          :src="siteContext.animal_seleccionado.asociacion_info.logo"
          :alt="siteContext.animal_seleccionado.asociacion_info.nombre" fit="contain" />
        <span v-else class="text-white text-weight-regular">{{
          siteContext.animal_seleccionado.asociacion_info.nombre.slice(0, 1)
        }}</span>
      </q-avatar>
    </div>

    <div class="row justify-center q-pb-sm">
      <span>{{ siteContext.animal_seleccionado.asociacion_info.razon_social }}</span>
    </div>

    <div class="row justify-center q-pb-xl q-pt-md text-grey-6 text" style="text-align: justify;">
      <span :style="$q.screen.gt.md ? 'max-width: 70%;' : 'max-width: 90%'">
        {{ siteContext.animal_seleccionado.asociacion_info.descripcion }}
      </span>
    </div>

    <template v-if="authStore.firebaseUserData.uid">

      <q-card-section class="q-px-lg bg-grey-2" style="position: sticky; top: 0; background-color: #ffffff; z-index: 2">
        <q-btn no-caps :label="siteContext.animal_seleccionado.postulado_info.length === 0
          ? 'Solicitar adopción'
          : 'Ya has aplicado'
          " :color="siteContext.animal_seleccionado.postulado_info.length === 0
    ? 'primary'
    : 'pink-3'
    " :disable="siteContext.animal_seleccionado.postulado_info.length !== 0" :text-color="siteContext.animal_seleccionado.postulado_info.length === 0
    ? 'white'
    : 'pink-1'
    " @click="
    authStore.firebaseUserData.uid
      ? presubmitPostulacion()
      : (showAvisoNoAuth = true)
    " />

        <!--        <q-separator></q-separator>-->
      </q-card-section>

      <q-card-section class="q-px-lg q-pt-md">
        <div class="max-width-text q-pb-lg">
          <span class="text-weight-regular">Nombre</span>
          {{ siteContext.animal_seleccionado.nombre }}
        </div>

        <div class="max-width-text q-pb-lg">
          <span class="text-weight-regular">Habilidades:</span>
          <template v-for="habilidad in siteContext.animal_seleccionado.habilidades_info" :key="habilidad.id">
            <q-chip style="max-width: unset; font-weight: unset">{{
              habilidad.nombre
            }}</q-chip>
          </template>
        </div>

      </q-card-section>

      <q-separator></q-separator>

      <q-card-section class="q-px-lg q-pt-md">

        <div class="max-width-text q-pb-lg">
          <span class="text-weight-regular q-pr-sm">Apto para niños:</span>
          <q-toggle v-model="siteContext.animal_seleccionado.apto_niños" color="primary" dense disable
            unchecked-icon="clear" checked-icon="check" />
        </div>
      </q-card-section>

      <q-separator></q-separator>

      <q-card-section class="q-px-lg q-pt-xl">
        <div class="row justify-left q-pb-md">

          <q-avatar rounded size="3.5em" :color="siteContext.animal_seleccionado.asociacion_info.logo ? 'white' : 'primary'
              " class="box-shadow-soft q-mr-md">
            <q-img v-if="siteContext.animal_seleccionado.asociacion_info.logo"
              :src="siteContext.animal_seleccionado.asociacion_info.logo"
              :alt="siteContext.animal_seleccionado.asociacion_info.nombre" fit="contain" />
            <span v-else class="text-white text-weight-regular">{{
              siteContext.animal_seleccionado.asociacion_info.nombre.slice(0, 1)
            }}</span>
          </q-avatar>
          <span class="self-center">{{ siteContext.animal_seleccionado.asociacion_info.razon_social }}</span>
        </div>

        <div class="row justify-left q-pb-md">

        </div>

        <div class="max-width-text">
          Registro patronal:
          {{ siteContext.animal_seleccionado.asociacion_info.registro_patronal }}
        </div>

        <div class="max-width-text">
          Tipo:
          {{
            siteContext.animal_seleccionado.asociacion_info.tipo === 'persona_fisica'
            ? 'Persona física'
            : 'Persona moral'
          }}
        </div>

        <div class="max-width-text">
          RFC: {{ siteContext.animal_seleccionado.asociacion_info.rfc }}
        </div>

        <div class="max-width-text">
          Domicilio: {{ siteContext.animal_seleccionado.asociacion_info.domicilio }},
          Colonia {{ siteContext.animal_seleccionado.asociacion_info.colonia }}. <br />
          {{ siteContext.animal_seleccionado.asociacion_info.municipio }},
          {{ siteContext.animal_seleccionado.asociacion_info.estado }}. C.P.
          {{ siteContext.animal_seleccionado.asociacion_info.codigo_postal }}
        </div>
      </q-card-section>

    </template>
    <template v-else>

      <q-separator class="q-ml-xl q-mr-xl q-mb-xl"></q-separator>

      <div class="row justify-center q-pt-lg">
        <q-card flat bordered>

          <q-card-section class="row justify-center q-pt-xl q-pb-lg">

            <q-icon>
              <q-icon style="font-size: 4em" color="primary" name="people" />
            </q-icon>
          </q-card-section>

          <q-card-section class="q-ml-xl q-mr-xl q-mb-md">

            <div class="row justify-center">
              <div class="text-grey">
                ¿Quieres más información sobre este animal?
              </div>
            </div>

            <div class="row justify-center">
              <div class="text-caption text-grey">
                ¡Crea tu cuenta o inicia sesión!
              </div>
            </div>
          </q-card-section>

          <q-separator />

          <q-card-actions class="row justify-center">
            <q-btn flat text-color="primary" @click="loginOIDC($q)">
              Inicia Sesión
            </q-btn>
            <q-btn flat text-color="primary" to="/acerca">
              Aviso de Privacidad
            </q-btn>
          </q-card-actions>
        </q-card>

      </div>

    </template>

    <q-card-section>
      <q-dialog v-model="showAvisoNoAuth">
        <q-card style="width: 400px">
          <q-card-section>
            <div class="text-h6">Sección para usuarios registrados</div>
          </q-card-section>
          <q-separator></q-separator>
          <q-card-section class="q-pb-none">
            <div class="text-h7">
              Para esta acción necesitas tener una cuenta y haber iniciado
              sesión
            </div>
          </q-card-section>
          <q-card-section class="q-pa-md">
            <div class="column q-pa-md q-gutter-sm">
              <q-btn color="primary" label="Iniciar sesión" dense outline v-close-popup no-caps style="padding: 0 18px"
                @click="loginOIDC($q)" />
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">

import { reactive, ref } from 'vue'
import { useAuthStore } from 'stores/auth'
import { date, useQuasar } from 'quasar'
import { useSiteContextStore } from 'stores/site-context'
import { useRoute, useRouter } from 'vue-router/dist/vue-router'
import { apiAdopta } from 'boot/axios'
import { loginOIDC } from 'boot/utils'
import MtyFormFieldInput from 'components/forms/fields/MtyFormFieldInput.vue'

const $q = useQuasar()
const siteContext = useSiteContextStore()
const router = useRouter()
const route = useRoute()

const authStore = useAuthStore()
const showAvisoNoAuth = ref(false)

const userHasProfile = ref(false)
const esFavorito = ref(false)
const favoritoId = ref(null)

const formulario = ref(null)

const formData = reactive({
  animal: route.params.id,
  user: authStore.firebaseUserData.uid,
  cuidados: '',
  espacio: '',
  seguridad: false,
  techo: false,
  salida_calle: false,
  precauciones: '',
  destrozos: false,
  alimentacion: '',
  enfermedades: false,
  atencion_veterinaria: '',
  conservacion: '',
  esterilizacion: false,
  consulta_seguimiento: false,
  acuerdo: false,
})

const pageContext = reactive(
  {
    dialog: false,
  }
)

const checkEsFavorito = async () => {
  console.log(siteContext.animal_seleccionado.animal_favorito)
  if (siteContext.animal_seleccionado.animal_favorito && siteContext.animal_seleccionado.animal_favorito.length > 0) {
    if (siteContext.animal_seleccionado.animal_favorito[0].id)
      console.log(siteContext.animal_seleccionado.animal_favorito[0].id)
    favoritoId.value = siteContext.animal_seleccionado.animal_favorito[0].id
    esFavorito.value = true
  }
}

checkEsFavorito()

const verifyProfileCompleted = () => {
  if (authStore.firebaseUserData.uid) {
    if (authStore.localUserData) {
      userHasProfile.value = true
    }
  }
}
verifyProfileCompleted()

function presubmitPostulacion() {
  console.log('presubmitPostulacion')
  if (userHasProfile.value === false) {
    $q.dialog({
      title: 'Aplicar a vacante',
      message:
        'Para aplicar a una vacante es necesario tener completo el perfil',
      persistent: false,
      ok: {
        label: 'Completar perfil',
        color: 'primary',
        class: 'no-caps',
      },
    })
      .onOk(() => {
        setTimeout(() => {
          router.push('/cuenta/perfil')
        }, 500)
      })
      .onDismiss(() => {
        console.log('Solo ando viendo...')
      })
  } else {
    pageContext.dialog = true
    console.log('dialogo abierto')
  }
}

const submitPostulacion = () => {
  formulario.value.validate().then((ok) => {
    if (ok) {
      apiAdopta
        .post(
          '/animales/postulacion-adopcion/', formData,
          {
            headers: {
              Authorization:
                'Bearer ' + authStore.firebaseUserData.accessToken,
            },
          }
        )
        .then((response) => {
          if (response.status === 201) {
            pageContext.dialog = false
            $q.dialog({
              title: '¡Postulación exitosa!',
              message: 'Su postulación ha sido enviada exitosamente.',
              persistent: false,
            })
          }
        })
        .catch((error) => {
          alert(error)
        })
    }
  })
}

const saveJob = () => {
  apiAdopta
    .post(
      '/animales/animal-favorito/',
      {
        user: authStore.firebaseUserData.uid,
        animal: siteContext.animal_seleccionado.id,
      },
      {
        headers: {
          Authorization: 'Bearer ' + authStore.firebaseUserData.accessToken,
        },
      }
    )
    .then((response) => {
      if (response.status === 201) {
        favoritoId.value = response.data.id
        esFavorito.value = true
        $q.dialog({
          title: '¡Vacante guardada!',
          message: 'Su vacante se ha guardado correctamente.',
          persistent: false,
        })
      }
    })
    .catch((error) => {
      alert(error)
    })
}

const deleteJob = () => {
  apiAdopta
    .delete(`/animales/animal-favorito/${favoritoId.value}/`, {
      headers: {
        Authorization: 'Bearer ' + authStore.firebaseUserData.accessToken,
      },
    })
    .then((response) => {
      if (response.status === 204) {
        esFavorito.value = false
        favoritoId.value = null
        $q.dialog({
          title: '¡Vacante eliminada de favoritos!',
          message: 'Su vacante se ha eliminado correctamente.',
          persistent: false,
        }).onOk(() => {
          if (route.path === `/animales/favoritos/${route.params.id}`) {
            router.push('/animales/favoritos')
          }
        })
      }
    })
    .catch((error) => {
      alert(error)
    })
}

const toggleFavorite = () => {
  esFavorito.value = !esFavorito.value
  if (!!esFavorito.value) {
    saveJob()
  } else {
    deleteJob()
  }
}

</script>

<style scoped lang="scss">
::v-deep(.disabled) {
  cursor: default !important;
  opacity: 1 !important;
}

::v-deep(.disabled *) {
  cursor: default !important;
}
</style>
