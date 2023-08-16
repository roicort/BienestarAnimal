<template>
  <q-btn v-if="authStore.firebaseUserData" round dense flat
         color="text-grey-7"
         icon="mdi-account-circle"
         class="relative-position"
         :disable="authStore.firebaseUserData.uid === 0">
    <!-- <q-badge color="primary" text-color="white" floating> 0 </q-badge> -->
    <q-tooltip :delay="3000">Mi cuenta</q-tooltip>

    <q-menu anchor="top middle" self="bottom middle" class="z-top"
            transition-show="jump-down"
            transition-hide="jump-up"
            style="width: 350px; min-width: 350px; height: auto;">
      <q-card class="my-card">

        <q-card-section class="text-center" v-if="authStore.firebaseUserData.uid">
          <div class="q-pa-md">
            <div class="items-center">
              <q-avatar round size="100px" font-size="50px" color="grey" text-color="white" icon="account_circle"/>

              <div class="text-subtitle1 q-mt-md q-mb-xs text-center">
                <p style="font-weight: 500; margin: 0 ">{{ authStore.perfilUsuario.uid }}</p>
                <template v-if="!!authStore.perfilUsuario.nombre && !!authStore.perfilUsuario.apellidos">
                  <p style="font-weight: 500; margin: 0 ">{{ authStore.perfilUsuario.nombre }}
                    {{ authStore.perfilUsuario.apellidos }}</p>
                </template>
                <template v-else>
                  <p style="font-weight: 500; margin: 0 ">Perfil incompleto</p>
                </template>
                <p style="font-weight: 300;">{{ authStore.firebaseUserData.email }}</p>
              </div>

              <q-btn
                color="grey-8"
                text-color="grey-8"
                label="Gestiona tu cuenta"
                dense
                rounded
                outline
                v-close-popup
                no-caps
                style="padding: 0 18px;"
                to="/cuenta"
              />

            </div>
          </div>
        </q-card-section>

        <q-card-section class="text-center" v-else>
          <div class="q-pa-md">
            <div class="items-center">
              <q-avatar round size="100px" font-size="50px" color="grey" text-color="white" icon="account_circle"/>

              <div class="text-subtitle1 q-mt-md q-mb-xs text-center">
                <p style="font-weight: 500; margin: 0 ">{{ authStore.userData.uid }}</p>
                <p style="font-weight: 300;">{{ authStore.firebaseUserData.email }}</p>
              </div>

              <div class="column q-gutter-sm">
                <q-btn
                  color="primary"
                  label="Iniciar sesión"
                  dense
                  outline
                  v-close-popup
                  no-caps
                  style="padding: 0 18px;"
                  @click="authStore.showDialogIniciarSesion = true"
                />
                <q-btn
                  color="teal"
                  label="Crear cuenta"
                  dense
                  outline
                  v-close-popup
                  no-caps
                  style="padding: 0 18px;"
                  @click="authStore.showDialogCrearCuenta = true"
                />
              </div>

            </div>
          </div>
        </q-card-section>

        <q-separator v-if="authStore.firebaseUserData.uid"/>

        <q-card-section class="text-center" v-if="authStore.firebaseUserData.uid">
          <q-btn
            color="grey-9"
            label="Cerrar sesión"
            @click="authStore.logOutOIDC($q, router)"
            dense
            outline
            v-close-popup
            no-caps
            style="padding: 0 18px;"
          />
        </q-card-section>

      </q-card>
    </q-menu>
  </q-btn>

  <q-btn v-else :to="authStore.signInURL" round flat dense icon="mdi-account-circle">
    <q-tooltip :delay="2000">Cuenta de usuario</q-tooltip>
  </q-btn>

  <q-dialog v-model="authStore.showDialogIniciarSesion" persistent>
    <q-card style="width: 600px;">
      <q-card-section>
        <div class="text-h6">Iniciar sesión</div>
      </q-card-section>
      <q-separator></q-separator>
      <q-card-section>
        <div class="q-pt-md">
          <q-form class="q-gutter-md"
                  @submit.prevent="authStore.loginUserWithEmailAndPassword(authStore.userData.email, authStore.userData.password, $q)"
                  greedy>
            <q-input dense outlined label="Email" v-model="authStore.userData.email" type="email"
                     :rules="[isValidEmail]"
                     hint="Dirección de email asociada a tu cuenta"/>
            <q-input dense outlined label="Contraseña" v-model="authStore.userData.password" :rules="[val => !!val || 'Escribe tu contraseña']"
                     :type="showPassword ? 'text' : 'password'"
                     hint="Contraseña de tu cuenta"/>
            <q-checkbox v-model="showPassword" label="Mostrar contraseña"/>
            <q-card-actions align="right" class="text-primary">
              <q-btn no-caps flat label="Cancelar" v-close-popup/>
              <q-btn no-caps label="Acceder" color="primary" type="submit"/>
            </q-card-actions>
          </q-form>
        </div>
      </q-card-section>

    </q-card>
  </q-dialog>

  <q-dialog v-model="authStore.showDialogCrearCuenta" persistent>
    <q-card style="width: 600px;">
      <q-card-section>
        <div class="text-h6">Crear cuenta</div>
      </q-card-section>
      <q-separator></q-separator>
      <q-card-section>
        <div class="q-pt-md">
          <q-form class="q-gutter-md"
                  @submit.prevent="authStore.registerUserWithEmailAndPassword(authStore.userData.email, authStore.userData.password, $q)"
                  greedy>
            <q-input dense outlined label="Email" v-model="authStore.userData.email" type="email"
                     :rules="[isValidEmail]"
                     hint="Dirección de email que usarás como identificador"/>
            <q-input dense outlined label="Contraseña" v-model="authStore.userData.password" :rules="[isValidPassword]"
                     :type="showPassword ? 'text' : 'password'"
                     hint="Utiliza 10 caracteres o más; al menos una letra minúscula, una letra mayúscula, un número y un símbolo"/>
            <q-checkbox class="q-pt-md" v-model="showPassword" label="Mostrar contraseña"/>
            <q-card-actions align="right" class="text-primary">
              <q-btn no-caps flat label="Cancelar" v-close-popup/>
              <q-btn no-caps label="Crear cuenta" color="primary" type="submit"/>
            </q-card-actions>
          </q-form>
        </div>
      </q-card-section>

    </q-card>
  </q-dialog>
</template>

<script>
import {onMounted, ref} from 'vue'
import {useAuthStore} from 'stores/auth';
import {useRouter} from 'vue-router'


export default {
  name: 'BotonApps',
  props: ['value'],
  setup() {
    const router = useRouter()
    const showPassword = ref(false);

    const emailPattern = /^(?=[a-zA-Z0-9@.%+-]{6,254}$)[a-zA-Z0-9.%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
    const passwordPattern = /(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{10,})/;

    const authStore = useAuthStore()

        onMounted(() => {
      if (authStore.firebaseUserData.uid) {

      }
    })

    const isValidEmail = (val) => {
      if (!!val && val !== '') {
        return emailPattern.test(val) || 'La dirección email no tiene formato correcto';
      } else {
        return 'Correo electrónico obligatorio'
      }
    }

    const isValidPassword = (val) => {
      if (!!val) {
        return passwordPattern.test(val) || 'La contraseña no cumple con los requisitos';
      } else {
        return 'Contraseña obligatoria'
      }
    }

    return {
      authStore,
      router,
      showPassword,
      isValidEmail,
      isValidPassword,
    }
  },
}
</script>

<style scoped></style>
