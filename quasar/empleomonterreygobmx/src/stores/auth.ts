import { defineStore } from 'pinia';
import { firebaseAuth } from 'boot/firebase.js'
//import { createUserWithEmailAndPassword, sendEmailVerification } from 'firebase/auth';
//import router from 'src/router';


const useAuthStore = () => {
  return defineStore('auth', {

    state: () => ({
      continueToURL: '/',
      localUserData: {
        date_joined: '',
        email: '',
        groups: [],
        is_staff: false,
        last_login: '',
        username: '',
        access: '',
      },
      perfilUsuario: {
        user: '',
        nombre: '',
        apellidos: '',
        biografia: '',
        estado: '',
        ciudad: '',
        localidad: '',
        habilidades: [],
      },

      firebaseUserData: { accessToken: null, email: null, emailVerified: false, uid: null },
      loadingUser: false,
      loading: false,
      showResetPasswordBtn: false,
      showDialogCrearCuenta: false,
      showDialogIniciarSesion: false,
    }),
    getters: {
      signUpURL: (state) => state.continueToURL === '/' ? '/signup' : '/signup' + '?continue=' + state.continueToURL,
      signInURL: (state) => state.continueToURL === '/' ? '/signin' : '/signin' + '?continue=' + state.continueToURL,
      authorizationHeaders: (state) => ({ headers: { Authorization: `Bearer ${state.firebaseUserData.accessToken}` } }),

    },
    actions: {

      async logOutOIDC($q: any, router: any) {
        $q.loading.show({
          message: 'Cerrando sesión, por favor espera...'
        })
        try {
          await firebaseAuth.signOut()
          this.firebaseUserData = { accessToken: null, email: null, emailVerified: false, uid: null }
          router.push('/')
        } catch (error) {
          console.error('error', error);
        } finally {
          $q.loading.hide()
        }
      }
    },
  })()
}

export { useAuthStore };
