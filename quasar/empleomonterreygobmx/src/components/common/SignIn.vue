<template>
<!--  <q-page class="row items-center justify-evenly">-->
    <div class="col-12 col-md-5 col-lg-4 col-xl-3" v-bind:class="$q.screen.lt.sm ? 'q-pa-sm' : 'q-pa-xl'">
      <q-card class="my-card q-pa-lg" v-bind:style="$q.screen.lt.sm ? 'border: none;' : 'border: solid #ddd 1px;'">
        <q-card-section>
          <div class="row justify-center align-center">
            <div class="col-xs-12">
              <div class="text-center">
                <p style="font-size: 24px; margin: 0 0 2px 0;">Acceder con ID Monterrey</p>
                <p style="font-size: 16px;" v-if="authStore.continueToURL !== '/'">Continuar a {{ authStore.continueToURL.split('://')[1].split('/')[0] }}</p>

              </div>

              <div class="q-py-lg">
                <q-form class="q-gutter-md">
                  <q-input dense outlined label="Email" v-model="authStore.userData.email" type="email" :rules="[isValidEmail]"
                           hint="Dirección de email de tu cuenta de ID Monterrey"/>
                  <q-input dense outlined label="Contraseña" v-model="password"
                           :rules="[val => !!val || 'Escribe tu contraseña']"
                           :type="showPassword ? 'text' : 'password'"
                           hint="Contraseña de tu cuenta"/>
                  <q-checkbox class="q-pt-sm" v-model="showPassword" label="Mostrar contraseña"/>
                </q-form>
              </div>

            </div>

          </div>
          <div v-if="authStore.showResetPasswordBtn" class="column fit q-pb-lg">
            <q-btn @click="resetPassword" no-caps color="red" class="fullwidth"
                   :disabled="!emailPattern.test(authStore.userData.email) || !password === ''">Recuperar contraseña
            </q-btn>
          </div>
          <div class="row q-gutter-sm justify-between">
            <q-btn :to="authStore.signUpURL" flat no-caps color="primary">Crear cuenta</q-btn>
            <q-btn @click="authStore.loginUserWithEmailAndPassword(authStore.userData.email, password, $q, router)" no-caps color="primary"
                   :disabled="!emailPattern.test(authStore.userData.email) || !password">Acceder
            </q-btn>

            {{ authStore.userData.uid }}

          </div>
        </q-card-section>
      </q-card>
    </div>
<!--  </q-page>-->
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue'
import {useQuasar} from 'quasar'
import {useRouter, useRoute} from 'vue-router'
import {useAuthStore} from 'stores/auth';

const $q = useQuasar()
const router = useRouter()
const route = useRoute()

const authStore = useAuthStore()
const emailPattern = /^(?=[a-zA-Z0-9@.%+-]{6,254}$)[a-zA-Z0-9.%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/
const showPassword = ref<boolean>(false);
const password = ref<any>('')
const showResetPasswordBtn = ref<boolean>(false)

const isValidEmail = (val: string) => {
  if (!!val) {
    return emailPattern.test(val) || 'La dirección email no tiene formato correcto';
  } else {
    return 'Escribe tu email asociado a tu cuenta de ID Monterrey';
  }
}

const signIn = async () => {
  $q.loading.show({
    message: 'Estamos generando tu cuenta, por favor espera...'
  })
  try {
    // await signInWithEmailAndPassword(firebaseAuth, email.value, password.value)
    await router.push('/')
  } catch (error) {
    console.log(error.message)
    $q.dialog({
      title: 'Error',
      message: 'Error en la autenticación, verifica que tu email y contraseña sean correctos',
      ok: 'Entendido'
    }).onOk(() => {
      showResetPasswordBtn.value = true
    })
  } finally {
    $q.loading.hide()
  }
}

onMounted(() => {
  authStore.continueToURL = route.query.continue || '/'
})

</script>
