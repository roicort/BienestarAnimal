<template>
<!--  <q-page class="row items-center justify-evenly" style="max-width: 1100px; margin: 0 auto;">-->
    <div class="col-12 col-xs-12 col-sm-12 col-md-9 col-lg-10" v-bind:class="$q.screen.lt.sm ? 'q-pa-sm' : 'q-pa-xl'">
      <q-card class="my-card q-pa-lg" v-bind:style="$q.screen.lt.sm ? 'border: none;' : 'border: solid #ddd 1px;'">
        <q-card-section>
          <div class="row justify-center align-center">
            <div class="col-xs-12 col-sm-6 ">
              <p style="font-size: 24px; margin: 0 0 2px 0;" v-bind:class="$q.screen.lt.sm ? 'text-center' : ''">Crea tu cuenta ID Monterrey</p>
              <p style="font-size: 16px;" v-if="authStore.continueToURL !== '/'">Continuar a
                {{ authStore.continueToURL.split('://')[1].split('/')[0] }}</p>

              <div class="q-py-lg">
                <q-form class="q-gutter-lg" @submit.prevent="submitFormulario" greedy>


                  <q-input dense outlined label="Email" v-model="authStore.userData.email" type="email"
                           :rules="[isValidEmail]"
                           hint="Dirección de email que usarás como identificador"/>
                  <q-input dense outlined label="Contraseña" v-model="password" :rules="[isValidPassword]"
                           :type="showPassword ? 'text' : 'password'"
                           hint="Utiliza 10 caracteres o más; al menos una letra minúscula, una letra mayúscula, un número y un símbolo"/>
                  <q-checkbox class="q-pt-md" v-model="showPassword" label="Mostrar contraseña"/>
                </q-form>
              </div>

              {{ authStore.userData.uid }}
              <div class="row q-gutter-sm q-pt-lg" v-bind:class="$q.screen.lt.sm ? 'justify-end' : 'justify-between'">
                <q-btn @click="authStore.registerUserWithEmailAndPassword(authStore.userData.email, password, $q, router)" no-caps
                       color="primary"
                       :disabled="!emailPattern.test(authStore.userData.email) ||
                       authStore.userData.email === '' || !passwordPattern.test(password)"
                       class="order-first"
                       >Crear cuenta
                </q-btn>
                <q-btn :to="authStore.signInURL" flat no-caps color="primary" >Accede a tu cuenta</q-btn>

              </div>
            </div>
            <div class="col-sm-6 col-xs-12 text-center q-py-sm gt-xs" v-bind:class="{'q-pl-xl q-pt-xl': $q.screen.gt.xs}">
              <q-img src="/img/id1.png" alt="Account" fit="scale-down" style="height: 300px; max-width: 300px"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>
<!--  </q-page>-->
</template>

<script setup lang="ts">
// import {Todo, Meta} from 'components/models';
import {ref, onMounted, computed} from 'vue'
import {useRouter, useRoute} from 'vue-router'
import {useAuthStore} from 'stores/auth';
import {useQuasar} from 'quasar';

const $q = useQuasar()
const router = useRouter()
const route = useRoute()

const authStore = useAuthStore()
const emailPattern = /^(?=[a-zA-Z0-9@.%+-]{6,254}$)[a-zA-Z0-9.%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
const passwordPattern = /(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{10,})/;
const showPassword = ref<boolean>(false);
const email = ref<string>('');
const password = ref<string>('');
const password2 = ref<string>('');
//@typescript-eslint/no-explicit-any
const firebase_error = ref<any>(null);

const isValidEmail = (val: string) => {
  if (firebase_error.value && firebase_error.value.code === 'auth/email-already-in-use') {
    return 'Ya existe una cuenta con el mismo email'
  } else {
    if (!!val && val !== '') {
      return emailPattern.test(val) || 'La dirección email no tiene formato correcto';
    } else {
      return 'Correo electrónico obligatorio'
    }
  }
}

const isValidPassword = (val: string) => {
  if (!!val) {
    return passwordPattern.test(val) || 'La contraseña no cumple con los requisitos';
  } else {
    return 'Contraseña obligatoria'
  }
}

onMounted(() => {
  authStore.continueToURL = route.query.continue || '/'
  console.log(route.path)
  console.log(route.query.continue)
})



/*
const todos = ref<Todo[]>([
  {
    id: 1,
    content: 'ct1'
  },
  {
    id: 2,
    content: 'ct2'
  },
  {
    id: 3,
    content: 'ct3'
  },
  {
    id: 4,
    content: 'ct4'
  },
  {
    id: 5,
    content: 'ct5'
  }
]);
const meta = ref<Meta>({
  totalCount: 1200
});
*/

</script>
