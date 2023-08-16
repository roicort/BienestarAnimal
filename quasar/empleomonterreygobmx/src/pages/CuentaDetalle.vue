<template>
  <q-page
    class="row items-center justify-evenly"
    style="max-width: 1600px; margin: 0 auto"
  >
    <div
      class="col-md-10 col-lg-8"
      v-bind:class="$q.screen.lt.sm ? 'q-pa-md' : 'q-pa-xl'"
    >
      <div class="q-pa-sm text-center">
        <div class="q-pt-sm items-center">
          <q-avatar
            round
            size="100px"
            font-size="50px"
            color="grey"
            text-color="white"
            icon="account_circle"
          />
          <div class="text-subtitle1 q-mt-md text-center">
            <p style="font-weight: 300">
              {{ authStore.firebaseUserData.email }}
            </p>
          </div>
        </div>
      </div>

      <div class="row q-col-gutter-lg q-pb-lg">
        <!-- Tarjetas -->
        <div class="col-12 col-md-12">
          <!-- Tarjeta 1 -->
          <q-card class="my-card full-height q-pb-xl">
            <q-card-section horizontal>
              <q-card-section>
                <div class="text-left">
                  <p
                    style="font-weight: 500; font-size: 1rem; margin: 0 0 2px 0"
                  >
                    Información Personal
                  </p>
                  <div>
                    <p
                      class="text-left text-grey-8 q-pt-sm"
                      style="
                        font-size: 0.875rem;
                        font-weight: 400;
                        margin: 0 0 2px 0;
                      "
                    >
                      La información de tu perfil en los servicios de la
                      <strong>Bolsa de Empleo</strong> es importante y necesaria
                      para que puedas acceder a los servicios de la misma. Sí
                      aun no has completado tu perfil, te invitamos a hacerlo.
                    </p>
                  </div>
                </div>
              </q-card-section>
            </q-card-section>
            <router-link to="/cuenta/perfil">
              <q-btn
                no-caps
                flat
                align="left"
                size="19px"
                class="absolute-bottom text-grey-7 text-weight-light"
                style="border-top: solid #ddd 1px"
                >Ver o completar mi perfil
              </q-btn>
            </router-link>
          </q-card>
        </div>

        <div class="col-12 col-md-12">
          <q-card class="my-card full-height">
            <q-card-section horizontal>
              <q-card-section>
                <div class="text-left q-pb-md">
                  <p
                    style="font-weight: 500; font-size: 1rem; margin: 0 0 2px 0"
                  >
                    Información adicional
                  </p>
                </div>
                <div v-if="authStore.localUserData.is_staff">
                  <q-chip>Staff</q-chip>
                </div>
                <p class="text-left text-grey-8 q-pt-xs">
                  Vinculaciones:
                  <template
                    v-for="(item, index) in authStore.perfilUsuario
                      .vinculaciones_asociaciones"
                    :key="index"
                  >
                    <q-btn
                      flat
                      rounded
                      :label="
                        item.asociacion_info.nombre +
                        ': ' +
                        item.user_rol
                      "
                      color="grey-4"
                      class="text-left text-grey-8 q-pt-xs"
                      @click="alert(item)"
                    />
                  </template>
                </p>
                <p class="text-left text-grey-8 q-pt-xs">
                  ID: {{ authStore.localUserData.username }}
                </p>
                <p class="text-left text-grey-8 q-pt-xs">
                  Miembro desde: {{ authStore.localUserData.date_joined }}
                </p>
                <p class="text-left text-grey-8 q-pt-xs">
                  Última conexión: {{ authStore.localUserData.last_login }}
                </p>
              </q-card-section>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from 'stores/auth'
import { useSiteContextStore } from 'stores/site-context'

import { useQuasar } from 'quasar'

export default defineComponent({
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'MiCuenta',
  setup() {
    const siteContext = useSiteContextStore()
    const router = useRouter()
    const route = useRoute()
    siteContext.current_page = route.path

    const authStore = useAuthStore()

    const $q = useQuasar()

    function alert(vinculacion) {
      let mensaje =
        'ID Empresa: ' + vinculacion.id + '\n' + 'Rol: ' + vinculacion.user_rol
      $q.dialog({
        title: vinculacion.empresa_info.nombre,
        message: mensaje,
      }).onOk(() => {
        console.log('OK')
      })
    }

    if (!authStore.firebaseUserData.uid) {
      router.push('/')
    }

    return {
      authStore,
      alert,
    }
  },
})
</script>
