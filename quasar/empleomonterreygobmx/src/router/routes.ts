import {RouteRecordRaw} from 'vue-router'
import { baseAPIURL } from '../boot/axios'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [

      {path: '', component: () => import('src/pages/AnimalesLista.vue')},
      {path: 'adopcion/:id', component: () => import('src/pages/AnimalesLista.vue')},
      {path: 'adopcion/favoritos', component: () => import('src/pages/AnimalesFavoritos.vue')},
      {path: 'adopcion/favoritos/:id', component: () => import('src/pages/AnimalesFavoritos.vue')},
      {path: 'adopcion/aplicaciones', component: () => import('src/pages/PostulacionAdopcion.vue')},

      {path: 'cuenta', component: () => import('src/pages/CuentaDetalle.vue')},
      {path: 'cuenta/perfil', component: () => import('src/pages/PerfilDetalle.vue')},
      {path: 'cuenta/perfil/editar', component: () => import('pages/EditarPerfil.vue')},

      {path: 'animales/registrar', component: () => import('src/pages/AnimalRegistrar.vue')},
      {path: 'animales/detalle/:id', component: () => import('src/pages/DetalleAnimal.vue')},

      {path: 'animales/', component: () => import('src/pages/AnimalesPadron.vue')},
      {path: 'animales/adopcion', component: () => import('src/pages/AnimalesAdopcion.vue')},
      {path: 'animales/adopcion/crear', component: () => import('src/pages/AnimalesAdopcionCrear.vue')},
      {path: 'animales/reportes', component: () => import('src/pages/AnimalesReportes.vue')},


      {path: 'asociaciones', component: () => import('src/pages/AsociacionesLista.vue')},
      {path: 'asociaciones/:id', component: () => import('src/pages/DetalleEmpresa.vue')},
      {path: 'asociaciones/centros/:id', component: () => import('src/pages/DetalleSucursales.vue')},
      {path: 'asociaciones/centros/detalle/:id', component: () => import('src/pages/EditarSucursal.vue')},
      
      {path: 'adopciones/', component: () => import('src/pages/ReclutadorPostulaciones.vue')},

      {path: 'unauthorized', component: () => import('pages/Unauthorized.vue')},
      {path: 'tablero', component: () => import('pages/Tablero.vue')},
      //{path: 'mapa', component: () => import('pages/Mapa.vue')},
      {path: 'acerca', component: () => import('pages/Acerca.vue')},
      {path: 'ayuda', component: () => import('pages/Ayuda.vue')},

      {path: 'admin', beforeEnter: () => {window.location.href = baseAPIURL.replace('/rest/v1','')+'/dadmin/'}},
      
      {
        path: '/:catchAll(.*)*',
        component: () => import('pages/Error404.vue'),
      },
    ],
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/error404',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '', component: () => import('pages/Error404.vue')},
    ],
  },
]

export default routes
