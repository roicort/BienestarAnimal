import { boot } from 'quasar/wrappers'
import { firebaseAuth } from 'boot/firebase'
import { apiAdopta } from 'boot/axios'
import { useAuthStore } from 'stores/auth'
//import { getRedirectResult, OAuthProvider } from 'firebase/auth'

const authStore = useAuthStore()

// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
export default boot(async ({ router }) => {
  // something to do
  firebaseAuth.onAuthStateChanged(async (user) => {
    if (user) {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      authStore.firebaseUserData = user
      await apiAdopta
        .get(`/users/user/${user.uid}/`, {
          headers: {
            Authorization: 'Bearer ' + authStore.firebaseUserData.accessToken,
          },
        })
        .then((response) => {
          authStore.localUserData = response.data
        })
      await apiAdopta
        .get(`/perfiles/perfil-general/${authStore.firebaseUserData.uid}/`, {
          headers: {
            Authorization: `Bearer ${authStore.firebaseUserData.accessToken}`,
          },
        })
        .then((response) => {
          authStore.perfilUsuario = response.data
          console.log(authStore.perfilUsuario)
          if (
            !authStore.perfilUsuario.nombre ||
            !authStore.perfilUsuario.apellidos
          ) {
            router.push('/cuenta')
          }
        })
    } else {
      authStore.firebaseUserData = {
        accessToken: null,
        email: null,
        emailVerified: false,
        uid: null,
      }
    }
  })
})
