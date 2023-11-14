<template>
  <q-page class="row items-center justify-evenly" style="max-width: 1100px; margin: 0 auto">
    <div class="col-12 col-md-10 col-lg-10" v-bind:class="$q.screen.lt.sm ? 'q-py-md' : 'q-pa-xl'">
      <div class="text-center">
        <p style="font-size: 30px; margin: 0 0 2px 0">Ayuda</p>
        <p class="text-grey-8" style="font-size: 0.875rem; font-weight: 400">
          Aquí podrás resolver las dudas más frecuentes.
        </p>
      </div>

      <div class="flex full-width justify-left items-center q-pt-xl">
          <p style="font-size: 25px">Empresas</p>
        </div>

      <q-list bordered>
        <q-expansion-item
        group="somegroup"
        icon="fingerprint"
        label="Regístrate e inicia sesión"
        header-class="text-primary"
      >
        <q-card>
          <q-card-section>
            Para comenzar a utilizar la Bolsa de Empleo, inicia sesión con tu cuenta de IDMonterrey+ o crea una nueva cuenta.
            Haz clic en el botón "Entrar" en la esquina superior derecha de la pantalla.
          </q-card-section>
        </q-card>
      </q-expansion-item>

      <q-separator />

      <q-expansion-item
        group="somegroup"
        icon="business"
        label="Registra una empresa"
        header-class="text-primary"
      >
        <q-card>
          <q-card-section>
            Despues de iniciar sesión, haz clic en el botón "Gestión de Cuenta" en la esquina superior derecha de la pantalla.
            En el menú de tu cuenta, selecciona la opción "Registrar Empresa" y llena el formulario.
          </q-card-section>
        </q-card>
      </q-expansion-item>

      <q-separator />

      <q-expansion-item
        group="somegroup"
        icon="add_business"
        label="Añade una sucursal"
        header-class="text-primary"
      >
        <q-card>
          <q-card-section>
            Después de registrar una empresa, dirigete a la administración de empresas y selecciona la empresa a la que deseas agregar una sucursal en el menú.
          </q-card-section>
        </q-card>
      </q-expansion-item>

      <q-separator />

      <q-expansion-item
        group="somegroup"
        icon="work_outline"
        label="Publica una vacante"
        header-class="text-primary"
      >
        <q-card>
          <q-card-section>
            Publicar una vacante requiere que hayas registrado una empresa y una sucursal. Una vez que hayas hecho esto, dirigete al botón superior "Publicar Vacante" y llena el formulario.
          </q-card-section>
        </q-card>
      </q-expansion-item>
    </q-list>

    <div class="flex full-width justify-left items-center q-pt-xl">
          <p style="font-size: 25px">Usuarios</p>
        </div>

        <q-list bordered> 
        <q-expansion-item
        group="somegroup"
        icon="fingerprint"
        label="Regístrate e inicia sesión"
        header-class="text-primary"
      >
        <q-card>
          <q-card-section>
            Para comenzar a utilizar la Bolsa de Empleo, inicia sesión con tu cuenta de IDMonterrey+ o crea una nueva cuenta.
            Haz clic en el botón "Entrar" en la esquina superior derecha de la pantalla.
          </q-card-section>
        </q-card>
      </q-expansion-item>

      <q-separator />

      <q-expansion-item
        group="somegroup"
        icon="person"
        label="Completa tu perfil"
        header-class="text-primary"
      >
        <q-card>
          <q-card-section>
            Antes de aplicar a una vacante es necesario que completes tu perfil. Para hacerlo, haz clic en el botón "Gestión de Cuenta" en la esquina superior derecha de la pantalla una vez iniciada la sesión.
          </q-card-section>
        </q-card>
      </q-expansion-item>

      <q-separator />

      <q-expansion-item
        group="somegroup"
        icon="work_outline"
        label="Dirígete al listado de vacantes"
        header-class="text-primary"
      >
        <q-card>
          <q-card-section>
            Una vez que te encuentres en la lista de vacantes, podrás comenzar a explorar las vacantes disponibles.
          </q-card-section>
        </q-card>
      </q-expansion-item>

    </q-list>

    <div class="flex full-width justify-center items-center q-pt-xl">
      <q-btn href="/acerca" color="primary" flat label="Acerca" />
    </div>
        <JobLoader v-if="pageContext.empty == true"></JobLoader>
    </div>
  </q-page>
</template>

<script>

import { defineComponent, reactive } from 'vue'
import JobLoader from 'src/components/common/JobLoader.vue'

export default defineComponent({
  name: 'AyudaView',
  components: {
    JobLoader,
  },
  setup() {

    //const authStore = useAuthStore()
    const pageContext = reactive({
      empty: false,
    })

    return {
      pageContext,
    }
  }
})
</script>
